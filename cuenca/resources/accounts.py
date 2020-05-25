from typing import ClassVar

from .base import Queryable, Retrievable


class Account(Retrievable, Queryable):
    _resource: ClassVar = 'accounts'

    name: str
    account_number: str
    institution_name: str
