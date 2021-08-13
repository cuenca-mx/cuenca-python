from typing import Optional, cast

from cuenca_validations.types import (
    WalletTransactionRequest,
    WalletTransactionType,
)

from cuenca.resources.base import Creatable, Transaction
from cuenca.resources.resources import retrieve_uri

from .base import Wallet


class WalletTransaction(Transaction, Creatable):
    _resource = 'wallet_transactions'
    type: WalletTransactionType
    wallet_uri: str

    @property
    def wallet(self) -> Optional['Wallet']:
        return cast('Wallet', retrieve_uri(self.wallet_uri))

    @classmethod
    def create(
        cls,
        wallet_uri: str,
        transaction_type: WalletTransactionType,
        amount: Optional[int] = None,
    ):
        request = WalletTransactionRequest(
            wallet_uri=wallet_uri,
            transaction_type=transaction_type,
            amount=amount,
        )
        return cast('WalletTransaction', cls._create(**request.dict()))
