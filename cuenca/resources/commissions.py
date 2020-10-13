from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    CommissionType,
    EntryType,
    RelatedTransaction,
)
from pydantic.dataclasses import dataclass

from cuenca import resources

from .base import Transaction
from .resources import retrieve_uri

mapper = {CommissionType.cash_deposit: EntryType.credit}


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    type: CommissionType
    related_transaction_uri: Optional[RelatedTransaction]

    @property  # type: ignore
    def related_transaction(self):
        rt = self.related_transaction_uri
        if not rt:
            return None
        resource = getattr(resources, rt.get_model())
        return cast(resource, retrieve_uri(rt)) if resource else None
