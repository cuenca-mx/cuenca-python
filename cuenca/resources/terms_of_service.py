import datetime as dt
from typing import ClassVar

from cuenca_validations.types import TermsOfService as TermsOfServiceEnum
from cuenca_validations.types.general import SerializableHttpUrl

from .base import Queryable, Retrievable


class TermsOfService(Retrievable, Queryable):
    _resource: ClassVar = 'terms_of_service'

    id: str
    is_active: bool
    created_at: dt.datetime
    type: TermsOfServiceEnum
    version: str
    uri: SerializableHttpUrl
