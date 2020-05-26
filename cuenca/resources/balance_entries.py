from functools import lru_cache
from typing import ClassVar

from .base import Cacheable, Queryable
from .resources import retrieve_uri


class BalanceEntry(Cacheable, Queryable):
    _resource: ClassVar = 'balance_entries'

    amount: int  # negative in the case of a debit
    descriptor: str
    rolling_balance: int
    transaction_uri: str

    @property  # type: ignore
    @lru_cache()
    def transaction(self):
        return retrieve_uri(self.transaction_uri)
