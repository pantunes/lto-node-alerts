import os
import telebot
import schedule
import time
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ConnectionError
from lto_node_alerts import settings as s


if "BOT_TOKEN_ID" not in os.environ:
    raise AssertionError(
        "Please configure BOT_TOKEN_ID as environment variable"
    )


tbot = telebot.TeleBot(os.environ["BOT_TOKEN_ID"])


def _get_jobs() -> tuple:
    from lto_node_alerts.services.minimum_tokens import (
        job as job_minimum_tokens,
    )
    from lto_node_alerts.services.info_nodes import job as job_info_nodes

    return (
        (job_minimum_tokens, s.JOB_MINIMUM_TOKENS_TIME),
        (job_info_nodes, s.JOB_INFO_NODES_TIME),
    )


def scheduler():
    if "GROUP_CHAT_ID" not in os.environ:
        raise AssertionError(
            "Please configure GROUP_CHAT_ID as environment variables"
        )

    for job_handler, job_time in _get_jobs():
        schedule.every().day.at(job_time).do(job_handler)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Aborting scheduler...")


def bot():
    @tbot.message_handler(commands=["start"])
    def on_start(message):
        tbot.reply_to(message, s.MESSAGES["start"])

    @tbot.message_handler(commands=["list"])
    def on_start(message):
        lines = []
        for node_id, node_data in s.NODES.items():
            lines.append(
                '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
                "{node_id}</a> 👉 {node_name}".format(
                    node_id=node_id, node_name=node_data["name"]
                )
            )

        kwargs = dict(
            message=message,
            text=s.MESSAGES["list"].format("\n".join(lines)),
            parse_mode="HTML",
        )

        try:
            tbot.reply_to(**kwargs)
        except (
            ConnectionError,
        ):
            time.sleep(5)
            tbot.reply_to(**kwargs)

    for x in range(s.MAX_RETRIES):
        try:
            tbot.polling(none_stop=True, timeout=60)
        except KeyboardInterrupt:
            print("Aborting bot...")
        except ReadTimeoutError:
            print("Socket timed out...")
