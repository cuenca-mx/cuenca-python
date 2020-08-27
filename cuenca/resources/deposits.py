from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types import DepositNetwork

from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


@dataclass
class Deposit(Transaction):
    _resource: ClassVar = 'deposits'

    network: DepositNetwork
    source: Optional[str]
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    def source_data(self) -> Optional[Account]:
        if self.source is None:  # cash deposit
            acct = None
        else:
            source_uri = f'/accounts/{self.source}'
            acct = cast(Account, retrieve_uri(source_uri))
        return acct
