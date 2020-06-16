from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class Account(Retrievable, Queryable):
    _resource: ClassVar = 'accounts'

    name: str  # legal name provided by institution
    account_number: str
    institution_name: str
