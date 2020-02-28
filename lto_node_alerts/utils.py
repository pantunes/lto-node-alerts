import os
import locale
import random
from lto_node_alerts import settings as s


def get_number_formatted(number):
    locale.setlocale(
        locale.LC_ALL, "nl_NL.UTF-8" if "DEBUG" in os.environ else "en_US.utf8"
    )
    return locale.format_string("%d", number, grouping=True)


def get_node_url_balance(node_id):
    node_address = random.choice(s.NODES_ADDRESSES)
    return s.NODE_URL_BALANCE.format(node_address, node_id)


def get_node_url_effective_balance(node_id):
    node_address = random.choice(s.NODES_ADDRESSES)
    return s.NODE_URL_EFFECTIVE_BALANCE.format(node_address, node_id)
