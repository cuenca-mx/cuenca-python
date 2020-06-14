from functools import lru_cache
from typing import ClassVar, Optional, cast

from cuenca_validations.types import DepositNetwork

from .accounts import Account
from .base import Cacheable, Transaction
from .resources import retrieve_uri


class Deposit(Transaction, Cacheable):
    _resource: ClassVar = 'deposits'

    network: DepositNetwork
    source_uri: Optional[str]
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    @lru_cache()
    def source(self) -> Optional[Account]:
        if self.source_uri is None:  # cash deposit
            acct = None
        else:
            acct = cast(Account, retrieve_uri(self.source_uri))
        return acct
