import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import BaseVerificationRequest, CurpField
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Updateable


@dataclass
class KYCVerification(Creatable, Updateable):
    _resource: ClassVar = 'kyc_verifications'

    platform_id: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime]
    curp: Optional[CurpField] = None

    @classmethod
    def create(
        cls,
        platform_id: str,
        session: Session = global_session,
    ) -> 'KYCVerification':
        req = BaseVerificationRequest(platform_id=platform_id)
        return cast(
            'KYCVerification', cls._create(**req.dict(), session=session)
        )
