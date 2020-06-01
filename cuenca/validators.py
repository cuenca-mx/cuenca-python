import datetime as dt
from typing import ClassVar, Optional

from pydantic import BaseModel, Extra, PositiveInt, StrictInt
from pydantic.types import (
    ConstrainedInt,
    PaymentCardNumber as PydanticPaymentCardNumber,
)

from .types import sanitize_dict
from .typing import DictStrAny

MAX_PAGE_LIMIT = 100


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...


class Limit(ConstrainedInt):
    gt = 0
    le = MAX_PAGE_LIMIT


class QueryParams(BaseModel):
    count: bool = False
    limit: Optional[Limit] = None
    user: Optional[str] = None
    created_before: Optional[dt.datetime] = None
    created_after: Optional[dt.datetime] = None

    class Config:
        extra = Extra.forbid  # raise ValidationError if there are extra fields

    def dict(self, *args, **kwargs) -> DictStrAny:
        d = super().dict(exclude_none=True, exclude_unset=True)
        if self.count:
            d['count'] = 1
        sanitize_dict(d)
        return d


class TransactionQuery(QueryParams):
    status: Optional[str] = None


class TransferQuery(TransactionQuery):
    account_number: Optional[str] = None
    idempotency_key: Optional[str] = None


class ApiKeyQuery(QueryParams):
    active: Optional[bool] = None


class PaymentCardNumber(PydanticPaymentCardNumber):
    min_length: ClassVar[int] = 16
    max_length: ClassVar[int] = 16
