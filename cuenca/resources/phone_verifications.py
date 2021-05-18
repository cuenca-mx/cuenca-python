import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import BaseRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable


class PhoneVerificationUpdateRequest(BaseRequest):
    token: str
    token_secret: str

@dataclass
class PhoneVerification(Creatable, Updateable):
    _resource: ClassVar = 'phone_verifications'

    token: str
    phone_number: Optional[str]

    @classmethod
    def create(cls, *, session: Session = global_session) -> 'PhoneVerification':
        return cast('PhoneVerification', cls._create(session=session))

    @classmethod
    def update(
        cls,
        pv_id: str,
        token: Optional[dict] = None,
        token_secret: Optional[dict] = None,
        *,
        session: Session = global_session,
    ) -> 'PhoneVerification':
        req = PhoneVerificationUpdateRequest(
        	token=token,
            token_secret=token_secret,
        )
        resp = cls._update(pv_id, **req.dict(), session=session)
        return cast('PhoneVerification', resp)
