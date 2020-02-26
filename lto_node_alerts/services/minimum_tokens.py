import os
import requests
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u
from lto_node_alerts.cli import tbot


def job():

    for node_id in s.NODES:

        url = u.get_node_url_balance(node_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise AssertionError("Request error: {}".format(url))
        json = response.json()

        if json["balance"] >= s.NODES[node_id]["min_tokens"]:
            continue

        tbot.send_message(
            chat_id=os.environ["GROUP_CHAT_ID"],
            text=s.MESSAGE_MINIMUM_TOKENS.format(
                s.NODES[node_id]["name"],
                u.get_number_formatted(json["balance"]),
            ),
            parse_mode="HTML",
        )
