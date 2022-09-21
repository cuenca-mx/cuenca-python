import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import KYCFile, KYCValidationRequest

from ..http import Session, session as global_session
from .base import Creatable, Retrievable, Updateable


class KYCValidation(Creatable, Retrievable):
    _resource: ClassVar = 'kyc_verifications'
    platform_id: str
    created_at: dt.datetime
    verification_id: Optional[str]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]

    class Config:
        schema_extra = {
            'example': {
                'id': 'KVNEUInh69SuKXXmK95sROwQ',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
                'created_at': '2020-05-24T14:15:22Z',
                'verification_id': 'string',
                'govt_id': KYCFile.schema().get('example'),
                'proof_of_address': None,
                'proof_of_life': None,
            }
        }

    @classmethod
    def create(
        cls, user_id: str, session: Session = global_session
    ) -> 'KYCValidation':
        req = KYCValidationRequest(user_id=user_id)
        return cast(
            'KYCValidation', cls._create(**req.dict(), session=session)
        )
