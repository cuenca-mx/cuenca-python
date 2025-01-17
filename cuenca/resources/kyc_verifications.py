import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    Address,
    Curp,
    KYCVerificationUpdateRequest,
    Rfc,
)
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable, Retrievable, Updateable


class KYCVerification(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'kyc_verifications'

    platform_id: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime] = None
    verification_id: Optional[str] = None
    curp: Optional[Curp] = None
    rfc: Optional[Rfc] = None
    address: Optional[Address] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'KVNEUInh69SuKXXmK95sROwQ',
                'updated_at': '2020-05-24T14:15:22Z',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
                'created_at': '2020-05-24T14:15:22Z',
                'verification_id': 'string',
                'curp': 'GOCG650418HVZNML08',
                'rfc': 'GOCG650418123',
                'address': Address.schema().get('example'),
            }
        }
    )

    @classmethod
    def create(cls, session: Session = global_session) -> 'KYCVerification':
        return cls._create(session=session)

    @classmethod
    def update(
        cls,
        kyc_id: str,
        curp: Optional[Curp] = None,
    ) -> 'KYCVerification':
        req = KYCVerificationUpdateRequest(curp=curp)
        return cls._update(id=kyc_id, **req.model_dump())
