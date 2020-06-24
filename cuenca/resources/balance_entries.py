from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable
from .resources import retrieve_uri


@dataclass
class BalanceEntry(Retrievable, Queryable):
    _resource: ClassVar = 'balance_entries'

    amount: int  # negative in the case of a debit
    descriptor: str
    rolling_balance: int
    transaction_uri: str

    @property  # type: ignore
    def transaction(self):
        return retrieve_uri(self.transaction_uri)
