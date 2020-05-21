import datetime as dt
from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseModel, Extra, validator
from pydantic.types import ConstrainedInt
from pydantic.validators import int_validator, number_size_validator

MAX_PAGE_LIMIT = 100


if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class Limit(ConstrainedInt):
    ge = 0
    le = MAX_PAGE_LIMIT

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield int_validator
        yield cls.bound_value
        yield number_size_validator

    @classmethod
    def bound_value(cls, limit: int) -> int:
        return min(cls.ge, max(cls.le, limit))


class QueryParams(BaseModel):
    count: bool = False
    limit: Optional[Limit] = None
    created_before: Optional[dt.datetime] = None

    class Config:
        extra = Extra.forbid

    @validator('count')
    def _validate_count(cls, count: Union[bool, int, str]) -> bool:
        if count == '1':
            count = True
        elif count == '0':
            count = False
        else:
            count = bool(count)
        return count

    def dict(self, *args, **kwargs):
        return super().dict(
            exclude_none=True, exclude_unset=True, exclude={'count'}
        )


class TransferQuery(QueryParams):
    account_number: Optional[str] = None
    idempotency_key: Optional[str] = None
    status: Optional[str] = None


class ApiKeyQuery(QueryParams):
    active: Optional[bool]
