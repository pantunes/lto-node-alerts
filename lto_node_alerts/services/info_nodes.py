import os
import requests
import redis
import telebot
import time
from requests.exceptions import ConnectionError
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u


REDIS_KEY = "LTO-Totals-Changed"

red = redis.Redis.from_url(s.BROKER_URL)


def _get_stats_from_lpos():
    url = s.LPOS_URL
    response = requests.get(url)
    if response.status_code != 200:
        raise AssertionError("Request error: {}".format(url))
    _json = response.json()
    return (
        {n["generator"]: (n, i) for i, n in enumerate(
            _json, start=1) if n["generator"] in s.NODES},
        len(_json),
        sum([n["fromLeases"] for n in _json]) / 10 ** 8,
        sum([n["balance"] for n in _json]) / 10 ** 8,
    )


def _get_node_balance(node_id):
    url = u.get_node_url_balance(node_id)
    response = requests.get(url)
    if response.status_code != 200:
        raise AssertionError("Request error: {}".format(url))
    return response.json()


def get_node_effective_balance(node_id):
    url = u.get_node_url_effective_balance(node_id)
    response = requests.get(url)
    if response.status_code != 200:
        raise AssertionError("Request error: {}".format(url))
    return response.json()


def job():
    lines = []
    (
        leases,
        num_total_lessors,
        total_leased,
        total_balance,
    ) = _get_stats_from_lpos()

    for node_id in s.NODES:

        json = _get_node_balance(node_id)
        json["effective_balance"] = get_node_effective_balance(node_id)[
            "balance"
        ]

        node_balance = json["balance"] / 10 ** 8
        node_effective_balance = json["effective_balance"] / 10 ** 8

        kwargs = dict(
            node_id=json["address"],
            node_name=s.NODES[node_id]["name"],
            node_balance=u.get_number_formatted(node_balance),
            node_leases=u.get_number_formatted(
                (node_effective_balance - node_balance)
            ),
            node_effective_balance=u.get_number_formatted(
                node_effective_balance
            ),
        )

        row = (
            '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
            "{node_name}</a>:\n"
            "  🔸 Ranking 👉 <b>{{ranking}}</b>\n"
            "  🔸 Balance 👉 <b>{node_balance} LTO</b>\n"
            "  🔸 Leases 👉 <b>{node_leases} LTO</b>\n"
            "  🔸 Effective Balance 👉 <b>{node_effective_balance} "
            "LTO</b>\n".format(**kwargs)
        )

        if node_id in leases:
            _leases = leases[node_id][0]["leases"]
            num_leases = len(_leases)
            unique_leasers = len(list(set([x["sender"] for x in _leases])))
            row = row.format(ranking=leases[node_id][1])
            row += (
                "  🔸 Number of Leases 👉 <b>{num_leases}</b>\n"
                "  🔸 Unique Leasers 👉 <b>{unique_leasers}</b>\n".format(
                    num_leases=u.get_number_formatted(num_leases),
                    unique_leasers=u.get_number_formatted(unique_leasers),
                )
            )

        lines.append(row)

    if lines:
        body = "\n".join(lines)
    else:
        body = "(no nodes)"

    num_total_lessors_change = 0
    total_leased_change = 0
    total_balance_change = 0

    in_redis = red.hgetall(REDIS_KEY)
    if in_redis:
        num_total_lessors_change = (
            (num_total_lessors - float(in_redis[b"num_total_lessors"]))
            / float(in_redis[b"num_total_lessors"])
        ) * 100
        total_leased_change = (
            (total_leased - float(in_redis[b"total_leased"]))
            / float(in_redis[b"total_leased"])
        ) * 100
        total_balance_change = (
            (total_balance - float(in_redis[b"total_balance"]))
            / float(in_redis[b"total_balance"])
        ) * 100

    red.hmset(
        REDIS_KEY,
        dict(
            num_total_lessors=num_total_lessors,
            total_leased=total_leased,
            total_balance=total_balance,
        ),
    )

    text = s.MESSAGE_INFO_NODES.format(
        body=body,
        num_total_lessors=u.get_number_formatted(num_total_lessors),
        num_total_lessors_change=u.get_number_formatted(
            num_total_lessors_change
        ),
        total_leased=u.get_number_formatted(total_leased),
        total_leased_change=u.get_number_formatted(total_leased_change),
        total_balance=u.get_number_formatted(total_balance),
        total_balance_change=u.get_number_formatted(total_balance_change),
    )

    if "DEBUG" in os.environ:
        print(text)
        return

    tbot = telebot.TeleBot(os.environ["BOT_TOKEN_ID"])

    kwargs = dict(
        chat_id=os.environ["GROUP_CHAT_ID"],
        text=text,
        parse_mode="HTML",
    )

    try:
        tbot.send_message(**kwargs)
    except (
        ConnectionError,
    ):
        time.sleep(2.0)
        tbot.send_message(**kwargs)
