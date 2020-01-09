NODES_ADDRESSES = (
    '172.104.227.247:6869',  # pauloantunes.com/lto
    '142.93.238.193:6869',   # LowSea Leasing
    '104.248.80.65:6869',    # Joel_SMART_WORKFLOW_FUNDATION
    '142.93.142.26:6869',    # Liquid Leasing Network
    '217.100.219.252.6869',  # ltonode.com
)

NODE_URL_BALANCE = 'http://{}/addresses/balance/{}'
NODE_URL_EFFECTIVE_BALANCE = 'http://{}/addresses/effectiveBalance/{}'

MESSAGE_MINIMUM_TOKENS = '''The Node {} is running out of tokens.
Current balance 👉 {} LTO.
Please cash in!'''

MESSAGE_INFO_TOKENS = '''Daily report with Nodes and their current balances:

{}

Contact @pjmlantunes to add or remove your Node from this list.'''

JOB_MINIMUM_TOKENS_TIME = '10:00'
JOB_INFO_TOKENS_TIME = '10:30'


from lto_node_alerts.settings_nodes import (
    NODES,
)  # noqa

from lto_node_alerts.settings_bot import (
    MESSAGES,
)  # noqa

__all__ = ['NODES', 'MESSAGES']
