import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import HumanRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable, Updateable


@dataclass
class Human(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'humans'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    nombres: str
    primer_apellido: str
    segundo_apellido: Optional[str]
    rfc: Optional[str]
    curp: str
    curp_url: Optional[str]
    gender: Optional[str]  # enum gender
    pronouns: Optional[str]
    birth_place: Optional[str]  # enum states
    birth_date: Optional[dt.date]
    birth_country: Optional[str]
    rating_requested_at: Optional[dt.datetime]
    rated_at: Optional[dt.datetime]

    user_uri: str

    @classmethod
    def create(
        cls,
        user_id: str,
        nombres: str,
        primer_apellido: str,
        segundo_apellido: Optional[str],
        curp: Optional[str] = None,
        rfc: Optional[str] = None,
        gender: Optional[str] = None,
        pronouns: Optional[str] = None,
        birth_place: Optional[str] = None,
        birth_date: Optional[dt.datetime] = None,
        birth_country: Optional[str] = None,
        *,
        session: Session = global_session,
    ):
        req = HumanRequest(
            user_id=user_id,
            nombres=nombres,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            curp=curp,
            rfc=rfc,
            gender=gender,
            pronouns=pronouns,
            birth_place=birth_place,
            birth_date=birth_date,
            birth_country=birth_country,
        )
        return cast('Human', cls._create(session=session, **req.dict()))
