import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import TermsOfService as TermsOfServiceEnum

from .base import Queryable, Retrievable


class TermsOfService(Retrievable, Queryable):
    _resource: ClassVar = 'terms_of_service'

    id: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime] = None
    type: TermsOfServiceEnum
    version: str
