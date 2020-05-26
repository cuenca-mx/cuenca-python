from typing import ClassVar

from .base import Cacheable, Transaction


class Commission(Transaction, Cacheable):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: str
