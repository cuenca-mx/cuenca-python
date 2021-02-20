from typing import ClassVar, cast

from cuenca_validations.types import EntryType, RelatedResource
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
    related_transaction_uri: RelatedResource
    funding_instrument_uri: RelatedResource

    @property  # type: ignore
    def related_transaction(self):
        rt = self.related_transaction_uri
        resource = getattr(resources, rt.get_model())
        return cast(resource, retrieve_uri(rt)) if resource else None

    @property  # type: ignore
    def funding_instrument(self):
        fi = self.funding_instrument_uri
        resource = getattr(resources, fi.get_model())
        return cast(resource, retrieve_uri(fi)) if resource else None
