import locale
import random
from lto_node_alerts import settings as s


def get_number_formatted(number):
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    return locale.format_string("%d", number, grouping=True)


def get_node_url(node_id):
    node_address = random.choice(s.NODES)
    return s.URL.format(node_address, node_id)
