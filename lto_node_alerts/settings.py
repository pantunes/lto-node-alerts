URL = 'https://lto.tools/generators/json'

MESSAGE = '''The {} Node is running out of tokens.
The current balance is {} LTO.
Please cash in!'''

JOB_TIME = '10:00'


from lto_node_alerts.settings_nodes import (
    NODES,
)  # noqa

__all__ = ['NODES']
