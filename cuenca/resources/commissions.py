from typing import ClassVar

from .base import Transaction


class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: str
