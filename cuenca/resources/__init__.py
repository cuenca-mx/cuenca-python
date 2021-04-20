__all__ = [
    'ApiKey',
    'Account',
    'Arpc',
    'BalanceEntry',
    'BillPayment',
    'Card',
    'CardActivation',
    'CardTransaction',
    'CardValidation',
    'Commission',
    'Deposit',
    'LoginToken',
    'ServiceProvider',
    'Statement',
    'Transfer',
    'UserLogin',
    'WhatsappTransfer',
]

from .accounts import Account
from .api_keys import ApiKey
from .arpc import Arpc
from .balance_entries import BalanceEntry
from .bill_payments import BillPayment
from .card_activations import CardActivation
from .card_transactions import CardTransaction
from .card_validations import CardValidation
from .cards import Card
from .commissions import Commission
from .deposits import Deposit
from .login_tokens import LoginToken
from .resources import RESOURCES
from .service_providers import ServiceProvider
from .statements import Statement
from .transfers import Transfer
from .user_credentials import UserCredential
from .user_logins import UserLogin
from .whatsapp_transfers import WhatsappTransfer

# avoid circular imports
resource_classes = [
    ApiKey,
    Account,
    Arpc,
    BalanceEntry,
    BillPayment,
    Card,
    CardActivation,
    CardTransaction,
    CardValidation,
    Commission,
    Deposit,
    LoginToken,
    ServiceProvider,
    Statement,
    Transfer,
    UserCredential,
    UserLogin,
    WhatsappTransfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
