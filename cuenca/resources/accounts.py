from typing import ClassVar

from .base import Cacheable, Queryable


class Account(Cacheable, Queryable):
    _resource: ClassVar = 'accounts'

    name: str
    account_number: str
    institution_name: str
