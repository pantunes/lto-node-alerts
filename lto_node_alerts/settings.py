BROKER_URL = "redis://localhost:6379"

REDIS_KEY = "LTO-Totals-Changed"

NODES_ADDRESSES = (
    "172.104.227.247:6869",  # pauloantunes.com/lto
    "142.93.238.193:6869",  # LowSea Leasing
    "142.93.142.26:6869",  # Liquid Leasing Network
    "95.216.198.5:6869",  # ZAVODIL
    "167.86.76.73:6869",  # KruptosNomisma
    "63.34.255.13:6869",  # jasny
    "163.172.89.89:6869",  # lto.banteg.xyz
    "88.198.26.92:6869",  # WeSimplifyTech
    "23.106.254.106:6869",  # LTO Network Node Japan
    "104.248.80.65:6869",  # Joel_SMART_WORKFLOW_FUNDATION
    "23.19.61.195:6869",  # To The Moon
    "94.177.241.31:6869",  # iiccSuperNode
    "81.169.222.76:6869",  # NODEX06
    # add more reliable nodes below
)

LPOS_URL = "https://lto.tools/lpos/json"
GENERATORS_URL = "https://lto.tools/generators/json"
NODE_URL_BALANCE = "http://{}/addresses/balance/{}"
NODE_URL_EFFECTIVE_BALANCE = "http://{}/addresses/effectiveBalance/{}"

MESSAGE_MINIMUM_TOKENS = """The Node {} is running out of tokens.
Current balance 👉 {} LTO.
Please cash in!"""

MESSAGE_INFO_NODES = """Daily report with Nodes and their current stats:

{body}

<b>Totals from Nodes that lease in LTO Network:</b>

  💎 Number of Lessors:  👉 <b>{num_total_lessors}</b>   <i>({num_total_lessors_change}%)</i>
  💎 Leased:  👉 <b>{total_leased} LTO</b>   <i>({total_leased_change}%)</i>
  💎 Balance:  👉 <b>{total_balance} LTO</b>   <i>({total_balance_change}%)</i>


<i>(* - Percentages are related with yesterday's values)</i>

Contact @pjmlantunes to add or remove your Node from this list."""

JOB_MINIMUM_TOKENS_TIME = "10:00"
JOB_INFO_NODES_TIME = "10:30"

from lto_node_alerts.settings_nodes import NODES  # noqa
from lto_node_alerts.settings_bot import MESSAGES  # noqa

__all__ = ["NODES", "MESSAGES"]
