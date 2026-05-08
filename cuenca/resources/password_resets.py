import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import VerificationStatus
from cuenca_validations.types.requests import PasswordResetRequest
from pydantic import ConfigDict
from pydantic_extra_types.coordinate import Coordinate

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class PasswordReset(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'password_resets'

    platform_id: str
    flow_id: str
    status: VerificationStatus = VerificationStatus.created
    mati_verification_id: Optional[str] = None
    identity_id: Optional[str] = None
    provider_url: Optional[str] = None
    created_at: dt.datetime
    updated_at: Optional[dt.datetime] = None
    deactivated_at: Optional[dt.datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'PRNEUInh69SuKXXmK95sROwQ',
                'platform_id': 'PT-1234567890',
                'flow_id': '123e4567-e89b-12d3-a456-426614174000',
                'status': 'created',
                'mati_verification_id': 'metamap-verification-id',
                'identity_id': 'metamap-identity-id',
                'created_at': '2026-05-06T14:15:22Z',
            }
        }
    )

    @classmethod
    def create(
        cls,
        location: Coordinate,
        *,
        session: Session = global_session,
    ) -> 'PasswordReset':
        req = PasswordResetRequest(location=location)
        return cls._create(session=session, **req.model_dump())
