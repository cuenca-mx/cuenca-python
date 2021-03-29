from typing import ClassVar, Optional, TypeVar, cast

from cuenca_validations.types import EntryType
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

    amount: int  # negative in the case of a debit
    descriptor: str
    name: str
    rolling_balance: int
    type: EntryType
    related_transaction_uri: str
    funding_instrument_uri: Optional[str]

    @property  # type: ignore
    def related_transaction(self) -> Transaction:
        return cast(Transaction, retrieve_uri(self.related_transaction_uri))

    @property  # type: ignore
    def funding_instrument(self) -> Optional[FundingInstrument]:
        if not self.funding_instrument_uri:
            return None
        return cast(
            FundingInstrument,
            retrieve_uri(self.funding_instrument_uri),
        )
