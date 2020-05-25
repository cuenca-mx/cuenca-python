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
from .base import Resource
from .bill_payments import BillPayment
from .card_transactions import CardTransaction
from .commissions import Commission
from .deposits import Deposit
from .resources import RESOURCES
from .transfers import Transfer

# this allows us to use retrieve_uri(uri)
resources = (local for local in locals() if isinstance(local, Resource))
for resource_cls in resources:
    RESOURCES[resource_cls._resource] = resource_cls
