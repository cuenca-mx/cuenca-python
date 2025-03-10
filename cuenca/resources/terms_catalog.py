import datetime as dt
from typing import ClassVar

from cuenca_validations.types import TermsOfService
from cuenca_validations.types.general import SerializableHttpUrl

from .base import Queryable, Retrievable


class TermsCatalog(Retrievable, Queryable):
    _resource: ClassVar = 'terms_catalog'

    id: str
    created_at: dt.datetime
    type: TermsOfService
    version: str
    uri: SerializableHttpUrl
