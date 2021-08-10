from typing import Optional, TypeVar, cast

from cuenca_validations.types import WalletTransactionRequest

from cuenca.resources.base import Creatable, Transaction
from cuenca.resources.resources import retrieve_uri

from .accounts import Account
from .base import Wallet

FundingInstrumentWallet = TypeVar('FundingInstrumentWallet', Account, Wallet)


class WalletTransaction(Transaction):
    funding_instrument_uri: str

    @property  # type: ignore
    def funding_instrument(self) -> FundingInstrumentWallet:
        return cast(
            FundingInstrumentWallet,
            retrieve_uri(self.funding_instrument_uri),
        )


class WalletDeposit(WalletTransaction):
    _resource = 'wallet_deposits'


class WalletTransfer(WalletTransaction, Creatable):
    _resource = 'wallet_transfers'

    @classmethod
    def create(
        cls,
        source_id: str,
        destination_id: str,
        amount: Optional[int] = None,
    ):
        request = WalletTransactionRequest(
            source_id=source_id,
            destination_id=destination_id,
            amount=amount,
        )
        return cast('WalletTransfer', cls._create(**request.dict()))
