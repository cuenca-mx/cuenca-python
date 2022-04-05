__all__ = [
    '__version__',
    'ApiKey',
    'Account',
    'Arpc',
    'BalanceEntry',
    'BillPayment',
    'Card',
    'CardActivation',
    'CardTransaction',
    'CardValidation',
    'CurpValidation',
    'Commission',
    'Deposit',
    'Endpoint',
    'File',
    'FileBatch',
    'Identity',
    'IdentityEvent',
    'LimitedWallet',
    'LoginToken',
    'Saving',
    'ServiceProvider',
    'Session',
    'Statement',
    'Transfer',
    'User',
    'UserCredential',
    'UserEvent',
    'UserLogin',
    'Verification',
    'WalletTransaction',
    'Webhook',
    'WhatsappTransfer',
    'configure',
    'get_balance',
]

from typing import cast

from . import http
from .resources import (
    Account,
    ApiKey,
    Arpc,
    BalanceEntry,
    BillPayment,
    Card,
    CardActivation,
    CardTransaction,
    CardValidation,
    Commission,
    CurpValidation,
    Deposit,
    Endpoint,
    File,
    FileBatch,
    Identity,
    IdentityEvent,
    LimitedWallet,
    LoginToken,
    Saving,
    ServiceProvider,
    Session,
    Statement,
    Transfer,
    User,
    UserCredential,
    UserEvent,
    UserLogin,
    Verification,
    WalletTransaction,
    Webhook,
    WhatsappTransfer,
)
from .version import __version__

configure = http.session.configure
session = http.session


def get_balance(session: http.Session = session) -> int:
    balance_entry = cast('BalanceEntry', BalanceEntry.first(session=session))
    return balance_entry.rolling_balance if balance_entry else 0
