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
    'CashReference',
    'Clabe',
    'Commission',
    'CurpValidation',
    'Deposit',
    'Endpoint',
    'File',
    'FileBatch',
    'Identity',
    'IdentityEvent',
    'KYCVerification',
    'LimitedWallet',
    'LoginToken',
    'Platform',
    'Saving',
    'ServiceProvider',
    'Session',
    'Statement',
    'Transfer',
    'User',
    'UserEvent',
    'UserLogin',
    'Verification',
    'WalletTransaction',
    'Webhook',
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
from .cash_references import CashReference
from .clabes import Clabe
from .commissions import Commission
from .curp_validations import CurpValidation
from .deposits import Deposit
from .endpoints import Endpoint
from .file_batches import FileBatch
from .files import File
from .identities import Identity
from .identity_events import IdentityEvent
from .kyc_verifications import KYCVerification
from .limited_wallets import LimitedWallet
from .login_tokens import LoginToken
from .platforms import Platform
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
from .verifications import Verification
from .wallet_transactions import WalletTransaction
from .webhooks import Webhook
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
    CashReference,
    Clabe,
    CurpValidation,
    Commission,
    Deposit,
    Endpoint,
    File,
    FileBatch,
    Identity,
    IdentityEvent,
    KYCVerification,
    LimitedWallet,
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
    Verification,
    WalletTransaction,
    WhatsappTransfer,
    Webhook,
    Platform,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
