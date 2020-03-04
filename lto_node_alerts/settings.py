BROKER_URL = "redis://localhost:6379"

NODES_ADDRESSES = (
    "172.104.227.247:6869",  # pauloantunes.com/lto
    "142.93.238.193:6869",  # LowSea Leasing
    "142.93.142.26:6869",  # Liquid Leasing Network
    "95.216.198.5:6869",  # ZAVODIL
    # add more reliable nodes below
)

LPOS_URL = "https://lto.tools/lpos/json"
NODE_URL_BALANCE = "http://{}/addresses/balance/{}"
NODE_URL_EFFECTIVE_BALANCE = "http://{}/addresses/effectiveBalance/{}"

MESSAGE_MINIMUM_TOKENS = """The Node {} is running out of tokens.
Current balance 👉 {} LTO.
Please cash in!"""

MESSAGE_INFO_NODES = """Daily report with Nodes and their current balances:

{body}

<b>Totals from Nodes that lease in LTO Network:</b>

  💎 Number of Lessors:  👉 <b>{num_total_lessors}</b>   <i>({num_total_lessors_change}%)</i>
  💎 Leased:  👉 <b>{total_leased} LTO</b>   <i>({total_leased_change}%)</i>
  💎 Balance:  👉 <b>{total_balance} LTO</b>   <i>({total_balance_change}%)</i>


(* - Percentages are related with yesterday's values)

Contact @pjmlantunes to add or remove your Node from this list."""

JOB_MINIMUM_TOKENS_TIME = "10:00"
JOB_INFO_NODES_TIME = "10:30"


from lto_node_alerts.settings_nodes import NODES  # noqa
from lto_node_alerts.settings_bot import MESSAGES  # noqa

__all__ = ["NODES", "MESSAGES"]
