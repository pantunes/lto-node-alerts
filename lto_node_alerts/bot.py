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
    from lto_node_alerts.services.info_tokens import \
        job as job_info_tokens

    return (
        (job_minimum_tokens, s.JOB_MINIMUM_TOKENS_TIME),
        (job_info_tokens, s.JOB_INFO_TOKENS_TIME),
    )


def scheduler():
    for job_handler, job_time in _get_jobs():
        schedule.every().day.at(job_time).do(job_handler)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print('Aborting scheduler...')


def start():
    bot.polling()
