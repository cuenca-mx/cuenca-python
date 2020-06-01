__all__ = [
    'ApiKey',
    'Account',
    'BalanceEntry',
    'Deposit',
    'Transfer',
    'WhatsappTransfer',
]

from .accounts import Account
from .api_keys import ApiKey
from .balance_entries import BalanceEntry
from .deposits import Deposit
from .resources import RESOURCES
from .transfers import Transfer
from .whatsapp_transfers import WhatsappTransfer

# avoid circular imports
resource_classes = [
    ApiKey,
    Account,
    BalanceEntry,
    Deposit,
    Transfer,
    WhatsappTransfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
