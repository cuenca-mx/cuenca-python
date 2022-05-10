import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import Address, CurpField, KYCUpdateRequest, Rfc
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable, Updateable


@dataclass
class KYCVerification(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'kyc_verifications'

    platform_id: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime]
    verification_id: Optional[str]
    curp: Optional[CurpField] = None
    rfc: Optional[Rfc] = None
    address: Optional[Address] = None

    @classmethod
    def create(cls, session: Session = global_session) -> 'KYCVerification':
        return cast('KYCVerification', cls._create(session=session))

    @classmethod
    def update(
        cls,
        kyc_id: str,
        curp: Optional[CurpField] = None,
        rfc: Optional[Rfc] = None,
    ) -> 'KYCVerification':
        request = KYCUpdateRequest(
            curp=curp,
            rfc=rfc,
        )
        return cast(
            'KYCVerification', cls._update(id=kyc_id, **request.dict())
        )
