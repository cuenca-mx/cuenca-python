__all__ = [
    'ApiKey',
    'Account',
    'BalanceEntry',
    'BillPayment',
    'CardTransaction',
    'Commission',
    'Deposit',
    'Transfer',
]

from .accounts import Account
from .api_keys import ApiKey
from .balance_entries import BalanceEntry
from .bill_payments import BillPayment
from .card_transactions import CardTransaction
from .commissions import Commission
from .deposits import Deposit
from .resources import RESOURCES
from .transfers import Transfer

resource_classes = [
    ApiKey,
    Account,
    BalanceEntry,
    BillPayment,
    CardTransaction,
    Commission,
    Deposit,
    Transfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls
