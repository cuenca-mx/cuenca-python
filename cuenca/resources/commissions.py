import re
from typing import ClassVar, Optional, cast

from cuenca_validations.types import EntryModel, EntryType
from pydantic.dataclasses import dataclass

from cuenca import resources

from .base import Transaction
from .resources import retrieve_uri


class RelatedTransaction(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, rt_uri):
        rt_match = re.search(r'/[a-z]+/(\w+)', rt_uri)
        rt_id = rt_match.group(1)
        entry = EntryModel(id=rt_id, type=EntryType.commission)
        return rt_uri, entry.get_model()


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: Optional[RelatedTransaction]

    @property  # type: ignore
    def related_transaction(self):
        if not self.related_transaction_uri:
            return None
        rt_uri, entry_model = self.related_transaction_uri
        return cast(getattr(resources, entry_model), retrieve_uri(rt_uri))
