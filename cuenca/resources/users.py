import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types import UserRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .addresses import Address
from .base import Creatable, Retrievable, Updateable
from .identity import Identity
from .kyc_file import KYCFile
from .resources import retrieve_uri
from .tos_agreements import TOSAgreement

# TODO: checar si agregar modelo de plataforma o no


@dataclass
class User(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'users'

    id: str
    identity_uri: str
    platform_id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    phone_number: str
    email_address: str
    profession: str
    # TOS de la plataforma
    terms_of_service: TOSAgreement
    # status dentro de la plataforma
    status: str  # enum UserStatus
    level: int
    # estos campos se van a pasar a Identity igual
    address: Address
    govt_id: KYCFile
    proof_of_address: KYCFile
    proof_of_life: KYCFile

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

    # TODO: poner como una propiedad el Identity/Human
    # (checar si se regresa en un mismo request)

    @property
    def identity(self):
        return cast(Identity, retrieve_uri(self.identity_uri))
