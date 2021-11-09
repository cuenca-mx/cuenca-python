import datetime as dt
from enum import Enum
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable


# pasar a cuenca-validations
class CardIssuerType(Enum):
    ifpe = 'ifpe'
    tarjetas_cuenca = 'tarjetas_cuenca'


class TOSAgreementRequest(BaseModel):
    user_id: Optional[str]
    version: int
    ip: str
    location: str
    type: CardIssuerType


@dataclass
class TOSAgreement(Creatable, Retrievable, Updateable, Queryable, Deactivable):
    _resource: ClassVar = 'tos_agreements'

    id: str
    created_at: dt.datetime
    version: int
    ip: str
    location: str
    type: CardIssuerType
    user_uri: str

    @classmethod
    def create(
        cls,
        user_id: str,
        version: int,
        ip: str,
        location: str,
        type: str,
        *,
        session: Session = global_session,
    ):
        req = TOSAgreementRequest(
            user_id=user_id,
            version=version,
            ip=ip,
            location=location,
            type=type,
        )
        return cast('TOSAgreement', cls._create(session=session, **req.dict()))
