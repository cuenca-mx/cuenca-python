from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import BaseRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Updateable


class PhoneVerificationUpdateRequest(BaseRequest):
    request_token: str
    access_token: str


@dataclass
class PhoneVerification(Creatable, Updateable):
    _resource: ClassVar = 'phone_verifications'

    request_token: str
    phone_number: Optional[str]

    @classmethod
    def create(
        cls, *, session: Session = global_session
    ) -> 'PhoneVerification':
        return cast('PhoneVerification', cls._create(session=session))

    @classmethod
    def update(
        cls,
        pv_id: str,
        request_token: Optional[dict] = None,
        access_token: Optional[dict] = None,
        *,
        session: Session = global_session,
    ) -> 'PhoneVerification':
        req = PhoneVerificationUpdateRequest(
            request_token=request_token,
            access_token=access_token,
        )
        resp = cls._update(pv_id, **req.dict(), session=session)
        return cast('PhoneVerification', resp)
