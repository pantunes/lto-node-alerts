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
    @bot.message_handler(commands=['start'])
    def on_start(message):
        bot.reply_to(message, s.MESSAGES['start'])

    @bot.message_handler(commands=['list'])
    def on_start(message):
        lines = list()
        for node_id, node_data in s.NODES.items():
            lines.append(
                '🔹 <a href="https://explorer.lto.network/addresses/{node_id}">'
                '{node_id}</a> 👉 {node_name}'.format(
                    node_id=node_id,
                    node_name=node_data['name']
                )
            )
        bot.reply_to(
            message,
            s.MESSAGES['list'].format("\n".join(lines)),
            parse_mode='HTML'
        )

    bot.polling()
