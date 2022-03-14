import datetime as dt
from typing import ClassVar, Optional, Union, cast

from cuenca_validations.types import VerificationType
from cuenca_validations.types.identities import PhoneNumber
from cuenca_validations.types.requests import (
    VerificationAttemptRequest,
    VerificationRequest,
)
from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Updateable


@dataclass
class Verification(Creatable, Updateable):
    _resource: ClassVar = 'verifications'

    sender: Union[EmailStr, PhoneNumber]
    type: VerificationType
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime]

    @classmethod
    def create(
        cls,
        sender: str,
        type: VerificationType,
        *,
        session: Session = global_session,
    ) -> 'Verification':
        req = VerificationRequest(sender=sender, type=type)
        return cast('Verification', cls._create(**req.dict(), session=session))

    @classmethod
    def verify(
        cls,
        id: str,
        code: str,
        *,
        session: Session = global_session,
    ) -> 'Verification':
        req = VerificationAttemptRequest(code=code)
        return cast(
            'Verification',
            cls._update(id=id, **req.dict(), session=session),
        )
