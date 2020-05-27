from functools import lru_cache
from typing import ClassVar, cast

from ..types import DepositNetwork
from .accounts import Account
from .base import Cacheable, Transaction
from .resources import retrieve_uri


class Deposit(Transaction, Cacheable):
    _resource: ClassVar = 'deposits'

    source_uri: str
    network: DepositNetwork
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    @lru_cache()
    def source(self) -> Account:
        return cast(Account, retrieve_uri(self.source_uri))
