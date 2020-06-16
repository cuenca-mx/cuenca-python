from typing import ClassVar, Optional

from pydantic.dataclasses import dataclass

from .base import Transaction


@dataclass
class Commission(Transaction):
    _resource: ClassVar = 'commissions'

    related_transaction_uri: Optional[str]
