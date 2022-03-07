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
    'CurpValidation',
    'Deposit',
    'File',
    'FileBatch',
    'Identity',
    'IdentityEvent',
    'LoginToken',
    'Saving',
    'ServiceProvider',
    'Session',
    'Statement',
    'Transfer',
    'User',
    'UserEvent',
    'UserLogin',
    'WalletTransaction',
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
from .curp_validations import CurpValidation
from .deposits import Deposit
from .file_batches import FileBatch
from .files import File
from .identities import Identity
from .identity_events import IdentityEvent
from .login_tokens import LoginToken
from .resources import RESOURCES
from .savings import Saving
from .service_providers import ServiceProvider
from .sessions import Session
from .statements import Statement
from .transfers import Transfer
from .user_credentials import UserCredential
from .user_events import UserEvent
from .user_logins import UserLogin
from .users import User
from .wallet_transactions import WalletTransaction
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
    CurpValidation,
    Commission,
    Deposit,
    File,
    FileBatch,
    Identity,
    IdentityEvent,
    LoginToken,
    Saving,
    Session,
    ServiceProvider,
    Statement,
    Transfer,
    User,
    UserCredential,
    UserEvent,
    UserLogin,
    WalletTransaction,
    WhatsappTransfer,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
