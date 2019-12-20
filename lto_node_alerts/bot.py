import os
import telebot
import schedule
import time
from lto_node_alerts import settings as s


if "BOT_TOKEN_ID" not in os.environ:
    raise AssertionError(
        "Please configure BOT_TOKEN_ID as environment variable"
    )


bot = telebot.TeleBot(os.environ['BOT_TOKEN_ID'])


def _get_jobs() -> tuple:
    from lto_node_alerts.services.minimum_tokens import \
        job as job_minimum_tokens

    return (
        job_minimum_tokens,
    )


def scheduler():
    for job in _get_jobs():
        schedule.every().day.at(s.JOB_TIME).do(job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print('Aborting scheduler...')


def start():
    bot.polling()
