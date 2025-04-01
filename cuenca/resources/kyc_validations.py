from typing import ClassVar, Optional

from cuenca_validations.types import KYCValidationRequest, KYCValidationSource
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class KYCValidation(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'kyc_validations'
    platform_id: str
    user_id: str
    source_type: KYCValidationSource
    flow_id: str
    files_uri: Optional[list[str]] = None
    verification_id: Optional[str] = None
    identity_id: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'KVNEUInh69SuKXXmK95sROwQ',
                'created_at': '2020-05-24T14:15:22Z',
                'platform_id': 'PT-1234567890',
                'user_id': 'US-1234567890',
                'source_type': 'server',
                'flow_id': '123e4567-e89b-12d3-a456-426614174000',
                'files_uri': ['cuenca.com/files/id', 'cuenca.com/files/id2'],
                'verification_id': 'metamap-verification-id',
                'identity_id': 'metamap-identity-id',
            }
        }
    )

    @classmethod
    def create(
        cls,
        user_id: str,
        source_type: KYCValidationSource,
        force: bool = False,
        session: Session = global_session,
    ) -> 'KYCValidation':
        req = KYCValidationRequest(
            user_id=user_id,
            force=force,
            source_type=source_type,
        )
        return cls._create(**req.model_dump(), session=session)
