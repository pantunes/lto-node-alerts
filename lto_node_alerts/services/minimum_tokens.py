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

    for node in response.json():
        if node['generator'] not in s.NODES:
            continue

        _node = s.NODES[node['generator']]

        if node['balance'] < _node['min_tokens']:
            bot.send_message(
                os.environ['GROUP_CHAT_ID'],
                s.MESSAGE.format(_node['name'], node['balance'])
            )
