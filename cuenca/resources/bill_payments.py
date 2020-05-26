from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Transaction


@dataclass
class BillPayment(Transaction):
    _resource: ClassVar = 'bill_payments'
