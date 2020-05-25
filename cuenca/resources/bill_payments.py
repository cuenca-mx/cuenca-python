from typing import ClassVar

from .base import Transaction


class BillPayment(Transaction):
    _resource: ClassVar = 'bill_payments'
