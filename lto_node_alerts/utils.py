import locale
import random
import requests
from tenacity import (
    retry,
    wait_fixed,
    stop_after_attempt,
)
from lto_node_alerts import settings as s


def get_number_formatted(number):
    try:
        locale.setlocale(locale.LC_ALL, "en_US.utf8")
    except locale.Error:
        locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")
    return locale.format_string("%d", number, grouping=True)


def get_node_url_balance(node_id):
    def wrapper():
        node_address = random.choice(s.NODES_ADDRESSES)
        return s.NODE_URL_BALANCE.format(node_address, node_id)

    return wrapper


def get_node_url_effective_balance(node_id):
    def wrapper():
        node_address = random.choice(s.NODES_ADDRESSES)
        return s.NODE_URL_EFFECTIVE_BALANCE.format(node_address, node_id)

    return wrapper


def get_lpos_url():
    def wrapper():
        return s.LPOS_URL

    return wrapper


def get_generators_url():
    def wrapper():
        return s.GENERATORS_URL

    return wrapper


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def get_(handler):
    url = handler()
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error when accessing {url}.")
    return response.json()
