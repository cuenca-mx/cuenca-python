import datetime as dt
from typing import ClassVar

from cuenca_validations.types.requests import (
    PhoneVerificationAssociationRequest,
)

from ..http import Session, session as global_session
from .base import Creatable


class PhoneVerificationAssociations(Creatable):
    _resource: ClassVar = 'phone_verification_associations'

    verification_id: str
    user_id: str
    created_at: dt.datetime

    @classmethod
    def create(
        cls, verification_id: str, session: Session = global_session
    ) -> 'PhoneVerificationAssociations':
        req = PhoneVerificationAssociationRequest(
            verification_id=verification_id
        )
        return cls._create(session=session, **req.model_dump())
