from typing import Optional, cast

from cuenca_validations.types import (
    WalletTransactionRequest,
    WalletTransactionType,
)

from cuenca.resources.base import Creatable, Transaction
from cuenca.resources.resources import retrieve_uri

from .base import Wallet
from .commissions import Commission


class WalletTransaction(Transaction, Creatable):
    _resource = 'wallet_transactions'
    type: WalletTransactionType
    wallet_uri: str
    # amount: int  # From Transaction -> always in MXN
    amount_currency: int  # In wallet currency [mxn | usd ]
    commission_uri: Optional[str]

    @property
    def commission(self) -> Optional['Commission']:
        if not self.commission_uri:
            return None
        return cast('Commission', retrieve_uri(self.commission_uri))

    @property
    def wallet(self) -> Optional['Wallet']:
        return cast('Wallet', retrieve_uri(self.wallet_uri))

    @classmethod
    def create(
        cls,
        wallet_id: str,
        transaction_type: WalletTransactionType,
        amount: Optional[int] = None,
    ):
        request = WalletTransactionRequest(
            wallet_id=wallet_id,
            transaction_type=transaction_type,
            amount=amount,
        )
        return cast('WalletTransaction', cls._create(**request.dict()))
