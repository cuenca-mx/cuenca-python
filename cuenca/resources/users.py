import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    Address,
    Beneficiary,
    KYCFile,
    PhoneNumber,
    TOSAgreement,
    UserRequest,
)
from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable, Updateable
from .identities import Identity
from .resources import retrieve_uri

# TODO: checar si agregar modelo de plataforma o no


@dataclass
class User(Creatable, Retrievable, Updateable):
    # TODO: cambiar los tipos opcionales a cuenca-validations
    _resource: ClassVar = 'users'

    id: str
    identity_uri: str
    platform_id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    phone_number: PhoneNumber
    email_address: EmailStr
    profession: str  # mover a identity (?)
    # TOS de la plataforma
    terms_of_service: TOSAgreement
    # status dentro de la plataforma
    status: str  # enum UserStatus
    level: int
    # estos campos se van a pasar a Identity igual
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
    beneficiary: Optional[Beneficiary]

    @classmethod
    def create(
        cls,
        # este user request va a traer ya los otros campos
        user_request: UserRequest,
        *,
        session: Session = global_session,
    ) -> 'User':
        """
        Este método en Identify va a buscar si ya existe un Identity con ese
        curp, en caso de que sí exista, se hace fetch del Identity y se asigna.
        En caso de que no exista se crea el Identity desde cero. Se tienen que
        pasar todos los datos para poder hacer la creación en caso de que
        no exista.
        """
        return cast(
            'User', cls._create(session=session, **user_request.dict())
        )

    # TODO: checar si el identity se regresa en un mismo request

    @property
    def identity(self):
        return cast(Identity, retrieve_uri(self.identity_uri))
