URL = 'https://lto.tools/generators/json'

MESSAGE_MINIMUM_TOKENS = '''The {} Node is running out of tokens.
The current balance is {} LTO.
Please cash in!'''

MESSAGE_INFO_TOKENS = '''Daily report with Nodes and their current balances:

{}

Contact @pjmlantunes to add or remove your Node from this list.
'''

JOB_MINIMUM_TOKENS_TIME = '10:00'
JOB_INFO_TOKENS_TIME = '10:30'


from lto_node_alerts.settings_nodes import (
    NODES,
)  # noqa

from lto_node_alerts.settings_bot import (
    MESSAGES,
)  # noqa

__all__ = ['NODES', 'MESSAGES']
