from typing import ClassVar, cast

from cuenca_validations.types import EntryType, RelatedTransaction
from pydantic.dataclasses import dataclass

from cuenca import resources

from .base import Queryable, Retrievable
from .resources import retrieve_uri


@dataclass
class BalanceEntry(Retrievable, Queryable):
    _resource: ClassVar = 'balance_entries'

    amount: int  # negative in the case of a debit
    descriptor: str
    name: str
    rolling_balance: int
    type: EntryType
    related_transaction_uri: RelatedTransaction

    @property  # type: ignore
    def related_transaction(self):
        rt = self.related_transaction_uri
        resource = getattr(resources, rt.get_model())
        return cast(resource, retrieve_uri(rt)) if resource else None
