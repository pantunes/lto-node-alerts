import os
import telebot
from requests.exceptions import ConnectionError
from tenacity import (
    retry,
    wait_fixed,
    stop_after_attempt,
    retry_if_exception_type,
)
from lto_node_alerts import utils as u
from lto_node_alerts import settings as s


@retry(
    retry=retry_if_exception_type(ConnectionError),
    wait=wait_fixed(1),
    stop=stop_after_attempt(10),
)
def job():
    for node_id in s.NODES:
        json = u.get_(u.get_node_url_balance(node_id))

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

        tbot.send_message(**kwargs)
