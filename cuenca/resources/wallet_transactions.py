from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    WalletTransactionQuery,
    WalletTransactionRequest,
    WalletTransactionType,
)

from cuenca.resources.base import Creatable, Transaction
from cuenca.resources.resources import retrieve_uri

from .base import Wallet


@dataclass
class WalletTransaction(Transaction, Creatable):
    _resource: ClassVar = 'wallet_transactions'
    _query_params: ClassVar = WalletTransactionQuery

    transaction_type: WalletTransactionType
    wallet_uri: str

    @property
    def wallet(self) -> Optional['Wallet']:
        return cast('Wallet', retrieve_uri(self.wallet_uri))

    @classmethod
    def create(
        cls,
        wallet_uri: str,
        transaction_type: WalletTransactionType,
        amount: int,
    ):
        request = WalletTransactionRequest(
            wallet_uri=wallet_uri,
            transaction_type=transaction_type,
            amount=amount,
        )
        return cast('WalletTransaction', cls._create(**request.dict()))
