import datetime as dt
from enum import Enum
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable


# pasar a cuenca-validations
class GovtIdType(Enum):
    ine_front = 'ine_front'
    ine_back = 'ine_back'
    passport = 'passport'
    residence = 'residence'
    matricula_consular = 'matricula_consular'
    matricula_back = 'matricula_back'
    residence_back = 'residence_back'
    proof_of_liveness = 'proof_of_liveness'


class GovtIDRequest(BaseModel):
    user_uri: Optional[str]
    type: GovtIdType
    is_mx: bool
    feedme_uri: str
    number: Optional[str] = None


@dataclass
class GovtID(Creatable, Retrievable, Updateable, Queryable, Deactivable):
    _resource: ClassVar = 'govt_ids'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    type: GovtIdType
    is_mx: bool
    feedme_uri: str
    dectivated_at: dt.datetime
    number: Optional[str]

    user_uri: str

    @classmethod
    def create(
        cls,
        type: GovtIdType,
        is_mx: bool,
        feedme_uri: str,
        number: Optional[str] = None,
        *,
        session: Session = global_session,
    ):
        req = GovtIDRequest(
            type=type,
            is_mx=is_mx,
            feedme_uri=feedme_uri,
            number=number,
        )
        return cast('GovtID', cls._create(session=session, **req.dict()))
