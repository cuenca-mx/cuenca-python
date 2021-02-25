from typing import ClassVar, Type, Union, cast

from cuenca_validations.types import EntryType
from pydantic.dataclasses import dataclass

from .accounts import Account
from .base import Queryable, Retrievable, Transaction
from .resources import retrieve_uri
from .service_providers import ServiceProvider


@dataclass
class BalanceEntry(Retrievable, Queryable):
    _resource: ClassVar = 'balance_entries'

    amount: int  # negative in the case of a debit
    descriptor: str
    name: str
    rolling_balance: int
    type: EntryType
    related_transaction_uri: str
    funding_instrument_uri: str

    @property  # type: ignore
    def related_transaction(self) -> Type[Transaction]:
        return cast(
            Type[Transaction], retrieve_uri(self.related_transaction_uri)
        )

    @property  # type: ignore
    def funding_instrument(self) -> Union[Account, ServiceProvider]:
        return cast(
            Union[Account, ServiceProvider],
            retrieve_uri(self.funding_instrument_uri),
        )
