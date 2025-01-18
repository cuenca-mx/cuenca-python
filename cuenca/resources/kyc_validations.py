from typing import ClassVar, Optional

from cuenca_validations.types import KYCFile, KYCValidationRequest
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class KYCValidation(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'kyc_validations'
    platform_id: str
    attemps: Optional[int] = None
    verification_id: Optional[str] = None
    files_uri: Optional[list[str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'KVNEUInh69SuKXXmK95sROwQ',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
                'created_at': '2020-05-24T14:15:22Z',
                'verification_id': 'string',
                'files_uri': ['cuenca.com/files/id', 'cuenca.com/files/id2'],
                'attemps': '1',
            }
        }
    )

    @classmethod
    def create(
        cls,
        user_id: str,
        force: bool = False,
        documents: list[KYCFile] = [],
        session: Session = global_session,
    ) -> 'KYCValidation':
        req = KYCValidationRequest(
            user_id=user_id,
            force=force,
            documents=documents,
        )
        return cls._create(**req.model_dump(), session=session)
