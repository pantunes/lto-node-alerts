import os
import requests
import telebot
import time
from requests.exceptions import ConnectionError
from lto_node_alerts import settings as s
from lto_node_alerts import utils as u


def job():
    for node_id in s.NODES:
        url = u.get_node_url_balance(node_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise AssertionError("Request error: {}".format(url))
        json = response.json()

        if json["balance"] >= s.NODES[node_id]["min_tokens"]:
            continue

        tbot = telebot.TeleBot(os.environ["BOT_TOKEN_ID"])

        kwargs = dict(
            chat_id=os.environ["GROUP_CHAT_ID"],
            text=s.MESSAGE_MINIMUM_TOKENS.format(
                s.NODES[node_id]["name"],
                u.get_number_formatted(json["balance"]),
            ),
            parse_mode="HTML",
        )

        for x in range(s.MAX_RETRIES):
            try:
                tbot.send_message(**kwargs)
                break
            except (ConnectionError,):
                time.sleep(5)
