import datetime as dt
from typing import ClassVar

from cuenca_validations.types.general import SerializableHttpUrl

from .base import Creatable, Queryable, Retrievable


class TermsOfService(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'terms_of_services'

    id: str
    created_at: dt.datetime
    user_id: str
    tos_id: str
    ip: str
    location: str
    hash: str
    url: SerializableHttpUrl
