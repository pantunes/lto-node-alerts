import os
import requests
from lto_node_alerts import settings as s
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

        lines.append(' 🔹 {}: **{} LTO**'.format(_node['name'], node['balance']))

    if lines:
        text = "\n".join(lines)
    else:
        text = "(no nodes)"

    bot.send_message(os.environ['GROUP_CHAT_ID'], text)
