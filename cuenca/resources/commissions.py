from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Cacheable, Transaction


@dataclass
class Commission(Transaction, Cacheable):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: str
