from typing import ClassVar, TypeVar, cast

from cuenca_validations.types import BalanceEntryQuery, EntryType
from pydantic.dataclasses import dataclass

from .accounts import Account
from .base import Queryable, Retrievable, Transaction
from .cards import Card
from .resources import retrieve_uri
from .service_providers import ServiceProvider

FundingInstrument = TypeVar(
    'FundingInstrument', Account, ServiceProvider, Card
)


@dataclass
class BalanceEntry(Retrievable, Queryable):
    _resource: ClassVar = 'balance_entries'
    _query_params: ClassVar = BalanceEntryQuery

    amount: int  # negative in the case of a debit
    descriptor: str
    name: str
    rolling_balance: int
    type: EntryType
    related_transaction_uri: str
    funding_instrument_uri: str

    @property  # type: ignore
    def related_transaction(self) -> Transaction:
        return cast(Transaction, retrieve_uri(self.related_transaction_uri))

    @property  # type: ignore
    def funding_instrument(self) -> FundingInstrument:
        return cast(
            FundingInstrument,
            retrieve_uri(self.funding_instrument_uri),
        )
