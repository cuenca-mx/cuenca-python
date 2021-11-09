import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import AddressRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable


@dataclass
class Address(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'addresses'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    calle: str
    numero_ext: str
    numero_int: Optional[str]
    codigo_postal: str
    estado: str
    ciudad: Optional[str]
    colonia: str
    deactivated_at: Optional[dt.datetime]

    user_id: str  # property? foreign key?

    @classmethod
    def create(
        cls,
        user_id: str,
        calle: str,
        numero_ext: str,
        codigo_postal: str,
        estado: str,
        colonia: str,
        ciudad: Optional[str] = None,
        numero_int: Optional[str] = None,
        *,
        session: Session = global_session,
    ):
        req = AddressRequest(
            user_id=user_id,
            calle=calle,
            numero_ext=numero_ext,
            numero_int=numero_int,
            codigo_postal=codigo_postal,
            estado=estado,
            colonia=colonia,
            ciudad=ciudad,
        )
        return cast('Address', cls._create(session=session, **req.dict()))
