from typing import ClassVar, Optional, cast

from pydantic.dataclasses import dataclass

from .base import Transaction
from .deposits import Deposit
from .resources import retrieve_uri
from .transfers import Transfer


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: Optional[str]

    @property  # type: ignore
    def related_transaction(self):
        if self.related_transaction_uri is None:
            acct = None
        else:
            if 'deposits' in self.related_transaction_uri:
                acct = cast(
                    Deposit, retrieve_uri(self.related_transaction_uri)
                )
            else:
                acct = cast(
                    Transfer, retrieve_uri(self.related_transaction_uri)
                )
        return acct
