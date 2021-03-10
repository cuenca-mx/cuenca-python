from typing import ClassVar, cast

from cuenca_validations.types import CommissionType, EntryType
from pydantic.dataclasses import dataclass

from .base import Transaction
from .resources import retrieve_uri

mapper = {CommissionType.cash_deposit: EntryType.credit}


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    type: CommissionType
    related_transaction_uri: str

    @property  # type: ignore
    def related_transaction(self) -> Transaction:
        return cast(Transaction, retrieve_uri(self.related_transaction_uri))
