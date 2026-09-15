from typing import ClassVar, Union

from cuenca_validations.types import (
    ClabeQuery,
    Curp,
    ReferencedClabeRequest,
    Rfc,
)
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable, Queryable


class Clabe(Creatable, Queryable):
    _resource: ClassVar = 'clabes'
    _query_params: ClassVar = ClabeQuery

    clabe: str
    user_id: str
    allowed_curp_rfc: Union[Curp, Rfc]
    is_default: bool = False

    model_config = ConfigDict(
        extra='ignore',
        json_schema_extra={
            'example': {
                'id': '646180157020143365',
                'clabe': '646180157020143365',
                'user_id': 'USbIRH85qFQP5ggPKKQAu5PA',
                'allowed_curp_rfc': 'LOPJ900101XXX',
                'is_default': False,
                'created_at': '2026-09-09T18:00:00.000000',
            }
        },
    )

    @classmethod
    def create(
        cls,
        legal_person_id: str,
        allowed_curp_rfc: Union[Curp, Rfc],
        *,
        session: Session = global_session,
    ) -> 'Clabe':
        req = ReferencedClabeRequest(
            legal_person_id=legal_person_id,
            allowed_curp_rfc=allowed_curp_rfc,
        )
        return cls._create(session=session, **req.model_dump())
