from typing import ClassVar

from .base import Queryable, Retrievable


class CashReference(Queryable, Retrievable):
    _resource: ClassVar = 'cash_references'

    number: str
    user_id: str
