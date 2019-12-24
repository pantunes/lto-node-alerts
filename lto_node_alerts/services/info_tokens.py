import os
import requests
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u
from lto_node_alerts.bot import bot


if "GROUP_CHAT_ID" not in os.environ:
    raise AssertionError(
        "Please configure GROUP_CHAT_ID as environment variables"
    )


def job():
    response = requests.get(s.URL)

    if response.status_code != 200:
        raise AssertionError("Request error: {}".format(s.URL))

    lines = list()
    for node in response.json():
        if node['generator'] not in s.NODES:
            continue

        _node = s.NODES[node['generator']]

        lines.append(
            '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
            '{node_name}</a> 👉 <b>{node_balance} LTO</b>'.format(
                node_id=_node['node_id'],
                node_name=_node['name'],
                node_balance=u.get_number_formatted(node['balance'])
            )
        )

    if lines:
        text = "\n".join(lines)
    else:
        text = "(no nodes)"

    bot.send_message(
        chat_id=os.environ['GROUP_CHAT_ID'],
        text=s.MESSAGE_INFO_TOKENS.format(text),
        parse_mode='HTML'
    )
