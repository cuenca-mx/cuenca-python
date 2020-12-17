__all__ = [
    'ApiKey',
    'Account',
    'BalanceEntry',
    'BillPayment',
    'Card',
    'CardTransaction',
    'Commission',
    'Deposit',
    'ServiceProvider',
    'Statement',
    'Transfer',
    'WhatsappTransfer',
]

from .accounts import Account
from .api_keys import ApiKey
from .balance_entries import BalanceEntry
from .bill_payments import BillPayment
from .card_transactions import CardTransaction
from .cards import Card
from .commissions import Commission
from .deposits import Deposit
from .resources import RESOURCES
from .service_providers import ServiceProvider
from .statements import Statement
from .transfers import Transfer
from .whatsapp_transfers import WhatsappTransfer

# avoid circular imports
resource_classes = [
    ApiKey,
    Account,
    BalanceEntry,
    BillPayment,
    Card,
    CardTransaction,
    Commission,
    Deposit,
    ServiceProvider,
    Statement,
    Transfer,
    WhatsappTransfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
