import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import Address, CurpField, Rfc
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


@dataclass
class KYCVerification(Creatable, Retrievable):
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
