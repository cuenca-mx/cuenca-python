from typing import ClassVar, Optional, cast

from cuenca_validations.types import DepositNetwork, DepositQuery
from pydantic.dataclasses import dataclass

from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


@dataclass
class Deposit(Transaction):
    _resource: ClassVar = 'deposits'
    _query_params: ClassVar = DepositQuery

    network: DepositNetwork
    source_uri: str
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    def source(self) -> Account:
        return cast(Account, retrieve_uri(self.source_uri))
