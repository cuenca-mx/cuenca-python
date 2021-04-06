from typing import ClassVar

from cuenca_validations.types import AccountQuery
from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class Account(Retrievable, Queryable):
    _resource: ClassVar = 'accounts'
    _query_params: ClassVar = AccountQuery

    name: str  # legal name provided by institution
    account_number: str
    institution_name: str
