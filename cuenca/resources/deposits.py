from functools import lru_cache
from typing import ClassVar

from ..types import DepositNetwork
from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


class Deposit(Transaction):
    _resource: ClassVar = 'deposits'

    network: DepositNetwork
    source_uri: str

    @property  # type: ignore
    @lru_cache()
    def source(self) -> Account:
        return retrieve_uri(self.source_uri)
