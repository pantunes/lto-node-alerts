import os
import requests
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u
from lto_node_alerts.cli import tbot


def job():
    lines = []

    for node_id in s.NODES:

        url = u.get_node_url_balance(node_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise AssertionError("Request error: {}".format(url))
        json = response.json()

        url = u.get_node_url_effective_balance(node_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise AssertionError("Request error: {}".format(url))
        json['effective_balance'] = response.json()['balance']

        lines.append(
            '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
            '{node_name}</a>:\n'
            '  🔸 Balance 👉 <b>{node_balance} LTO</b>\n'
            '  🔸 Effective Balance 👉 <b>{node_effective_balance} LTO</b>\n'.
            format(
                node_id=json['address'],
                node_name=s.NODES[node_id]['name'],
                node_balance=u.get_number_formatted(json['balance']/10**8),
                node_effective_balance=u.get_number_formatted(
                    json['effective_balance']/10**8
                )
            )
        )

    if lines:
        text = "\n".join(lines)
    else:
        text = "(no nodes)"

    tbot.send_message(
        chat_id=os.environ['GROUP_CHAT_ID'],
        text=s.MESSAGE_INFO_NODES.format(text),
        parse_mode='HTML'
    )
