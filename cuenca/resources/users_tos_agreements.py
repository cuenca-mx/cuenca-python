import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types.general import SerializableHttpUrl
from cuenca_validations.types.requests import (
    FileCuencaUrl,
    UserTOSAgreementRequest,
)

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class UserTOSAgreement(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'users_tos_agreements'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    terms_of_service_uri: str
    user_id: str
    ip: str
    location: str
    digital_signature: Optional[str] = None
    signature_image_url: Optional[FileCuencaUrl] = None
    signed_document_url: Optional[SerializableHttpUrl] = None
    notification_id: Optional[str] = None

    @classmethod
    def create(
        cls,
        location: str,
        tos_id: str,
        signature_image_url: Optional[FileCuencaUrl] = None,
        *,
        session: Session = global_session,
    ) -> 'UserTOSAgreement':
        req = UserTOSAgreementRequest(
            location=location,
            tos_id=tos_id,
            signature_image_url=signature_image_url,
        )
        return cls._create(session=session, **req.model_dump())
