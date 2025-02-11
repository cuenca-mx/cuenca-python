from typing import ClassVar

from cuenca_validations.types import Signature, SignatureRequest
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class Signature(Creatable, Retrievable):
    _resource: ClassVar = 'signatures'
    signature_id: Signature

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'string',
                'signature_id': Signature.schema().get('example'),
                'created_at': '2020-05-24T14:15:22Z',
            }
        }
    )

    @classmethod
    def create(
        cls,
        signature: Signature,
        user_id: str,
        session: Session = global_session,
    ) -> 'Signature':
        req = SignatureRequest(signature=signature, user_id=user_id)
        return cls._create(**req.model_dump(), session=session)
