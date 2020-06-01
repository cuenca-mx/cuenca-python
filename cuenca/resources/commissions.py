from typing import ClassVar, Optional

from pydantic.dataclasses import dataclass

from .base import Cacheable, Transaction


@dataclass
class Commission(Transaction, Cacheable):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: Optional[str]
