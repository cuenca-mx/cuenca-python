from typing import ClassVar

from aio_bitso.types import QueryParams
from pydantic.dataclasses import dataclass

from .base import Retrievable, Queryable


@dataclass
class CashDepositReference(Retrievable, Queryable):
    _resource: ClassVar = 'cash_deposit_reference'
    _query_params: ClassVar = QueryParams

    number: str
    partner: str
