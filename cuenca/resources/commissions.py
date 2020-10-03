from typing import ClassVar, Optional, cast

from cuenca_validations.types import EntryModel, LedgerEntryType
from pydantic.dataclasses import dataclass

from cuenca import resources

from .base import Transaction
from .resources import retrieve_uri


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: Optional[str]

    @property  # type: ignore
    def related_transaction(self):
        if not self.related_transaction_uri:
            return None
        related_transaction = self.related_transaction_uri.split('/')[-1]
        entry = EntryModel(id=related_transaction, type=LedgerEntryType.credit)
        return cast(
            getattr(resources, entry.get_model()),
            retrieve_uri(self.related_transaction_uri),
        )
