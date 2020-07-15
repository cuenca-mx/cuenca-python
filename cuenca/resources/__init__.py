__all__ = [
    "ApiKey",
    "Account",
    "BalanceEntry",
    "Commission",
    "Deposit",
    "TerminalPayment",
    "Transfer",
    "WhatsappTransfer",
]

from .accounts import Account
from .api_keys import ApiKey
from .balance_entries import BalanceEntry
from .commissions import Commission
from .deposits import Deposit
from .resources import RESOURCES
from .terminal_payment import TerminalPayment
from .transfers import Transfer
from .whatsapp_transfers import WhatsappTransfer

# avoid circular imports
resource_classes = [
    ApiKey,
    Account,
    BalanceEntry,
    Commission,
    Deposit,
    TerminalPayment,
    Transfer,
    WhatsappTransfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
