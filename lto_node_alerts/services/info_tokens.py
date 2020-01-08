import os
import requests
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u
from lto_node_alerts.cli import tbot


def job():
    lines = []

    for node in s.NODES:
        url = s.URL.format(node)
        response = requests.get(url)

        if response.status_code != 200:
            raise AssertionError("Request error: {}".format(url))

        json = response.json()

        lines.append(
            '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
            '{node_name}</a> 👉 <b>{node_balance} LTO</b>'.format(
                node_id=json['address'],
                node_name=s.NODES[node]['name'],
                node_balance=u.get_number_formatted(json['balance']/10**8)
            )
        )

    if lines:
        text = "\n".join(lines)
    else:
        text = "(no nodes)"

    tbot.send_message(
        chat_id=os.environ['GROUP_CHAT_ID'],
        text=s.MESSAGE_INFO_TOKENS.format(text),
        parse_mode='HTML'
    )
