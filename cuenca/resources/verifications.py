import datetime as dt
from typing import ClassVar, Optional, Union

from cuenca_validations.types import (
    VerificationAttemptRequest,
    VerificationRequest,
    VerificationType,
)
from cuenca_validations.types.identities import PhoneNumber
from pydantic import ConfigDict, EmailStr, Field

from ..http import Session, session as global_session
from .base import Creatable, Updateable


class Verification(Creatable, Updateable):
    _resource: ClassVar = 'verifications'

    recipient: Union[EmailStr, PhoneNumber] = Field(
        description='Phone or email to validate'
    )
    type: VerificationType
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime] = None
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'VENEUInh69SuKXXmK95sROwQ',
                'recipient': 'user@example.com',
                'type': 'email',
                'created_at': '2022-05-24T14:15:22Z',
                'deactivated_at': None,
            }
        }
    )

    @classmethod
    def create(
        cls,
        recipient: str,
        type: VerificationType,
        platform_id: str,
        session: Session = global_session,
    ) -> 'Verification':
        req = VerificationRequest(
            recipient=recipient, type=type, platform_id=platform_id
        )
        return cls._create(**req.model_dump(), session=session)

    @classmethod
    def verify(
        cls,
        id: str,
        code: str,
        session: Session = global_session,
    ) -> 'Verification':
        req = VerificationAttemptRequest(code=code)
        return cls._update(id=id, **req.model_dump(), session=session)
