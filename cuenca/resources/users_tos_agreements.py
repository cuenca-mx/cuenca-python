import datetime as dt
from typing import ClassVar

from cuenca_validations.types import TermsOfService
from cuenca_validations.types.general import SerializableHttpUrl

from .base import Creatable, Queryable, Retrievable


class UserTOSAgreement(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'users_tos_agreements'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    user_id: str
    type: TermsOfService
    version: str
    ip: str
    location: str
    digital_signature: str
    signed_document_url: SerializableHttpUrl
    notification_id: str
