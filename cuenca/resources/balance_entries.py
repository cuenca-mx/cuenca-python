from functools import lru_cache
from typing import ClassVar

from .base import Queryable, Retrievable
from .resources import retrieve_uri


class BalanceEntry(Retrievable, Queryable):
    _resource: ClassVar = 'balance_entries'

    amount: int
    rolling_balance: int  # negative in the case of a debit
    transaction_uri: str

    @property  # type: ignore
    @lru_cache()
    def transaction(self):
        return retrieve_uri(self.transaction_uri)
