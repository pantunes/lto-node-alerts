import os
import requests
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u
from lto_node_alerts.cli import tbot


def _get_leases():
    url = "https://lto.tools/lpos/json"
    response = requests.get(url)
    if response.status_code != 200:
        raise AssertionError("Request error: {}".format(url))
    return {
        n["generator"]: n for n in response.json() if n["generator"] in s.NODES
    }


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

    leases = _get_leases()

    for node_id in s.NODES:

        json = _get_node_balance(node_id)
        json["effective_balance"] = get_node_effective_balance(node_id)[
            "balance"
        ]

        kwargs = dict(
            node_id=json["address"],
            node_name=s.NODES[node_id]["name"],
            node_balance=u.get_number_formatted(json["balance"] / 10 ** 8),
            node_effective_balance=u.get_number_formatted(
                json["effective_balance"] / 10 ** 8
            ),
        )

        row = (
            '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
            "{node_name}</a>:\n"
            "  🔸 Balance 👉 <b>{node_balance} LTO</b>\n"
            "  🔸 Effective Balance 👉 <b>{node_effective_balance} "
            "LTO</b>\n".format(**kwargs)
        )

        if node_id in leases:
            _leases = leases[node_id]["leases"]
            num_leases = len(_leases)
            unique_leasers = len(list(set([x["sender"] for x in _leases])))
            row += (
                "  🔸 Number of Leases 👉 <b>{num_leases}</b>\n"
                "  🔸 Unique Leasers 👉 <b>{unique_leasers}</b>\n".format(
                    num_leases=u.get_number_formatted(num_leases),
                    unique_leasers=u.get_number_formatted(unique_leasers),
                )
            )

        lines.append(row)

    if lines:
        text = "\n".join(lines)
    else:
        text = "(no nodes)"

    # print(s.MESSAGE_INFO_NODES.format(text))

    tbot.send_message(
        chat_id=os.environ["GROUP_CHAT_ID"],
        text=s.MESSAGE_INFO_NODES.format(text),
        parse_mode="HTML",
    )
