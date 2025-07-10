import datetime as dt
from typing import ClassVar

from cuenca_validations.types import Country, PostalCodeQuery, State

from .base import Queryable, Retrievable


class PostalCodes(Retrievable, Queryable):
    _resource: ClassVar = 'postal_codes'
    _query_params: ClassVar = PostalCodeQuery

    id: str
    created_at: dt.datetime
    postal_code: str
    colonia: str
    city: str
    state: State
    state_name: str
    country: Country
    country_name: str
