import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    AddressRequest,
    GovtIDRequest,
    TOSAgreementRequest,
    UserDataRequest,
    UserProofRequest,
    UserRequest,
)
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .addresses import Address
from .base import Creatable, Retrievable, Updateable
from .govt_id import GovtID
from .resources import retrieve_uri
from .tos_agreements import TOSAgreement
from .users_datas import UserData
from .users_proofs import UserProof


@dataclass
class User(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'users'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    name: str
    type: str  # enum UserType
    status: str  # enum UserStatus
    # default_ledger_account_id: str  # foreign key
    available_invitations: Optional[int]
    beta_tester: bool
    login_attempts: bool
    pending_notifications: int
    last_login_at: Optional[dt.datetime]

    # este es el valor con el cual se va a hacer fetch de los recursos
    # todos estos valores se van a asignar al momento de crear el
    # recurso respectivo
    phone_uri: Optional[str]
    address_uri: Optional[str]
    email_address_uri: Optional[str]
    terms_uri: Optional[str]
    profession_uri: Optional[str]
    proof_of_address_uri: Optional[str]
    proof_of_life_uri: Optional[str]
    curp_uri: Optional[str]
    blacklist_check_uri: Optional[str]
    govt_id_uri: Optional[str]

    @classmethod
    def create(
        cls,
        nombres: str,
        primer_apellido: str,
        segundo_apellido: Optional[str] = None,
        gender: Optional[str] = None,
        birth_place: Optional[str] = None,
        birth_date: Optional[str] = None,
        birth_country: Optional[str] = None,
        pronouns: Optional[str] = None,
        curp: Optional[str] = None,
        # estos van en caso de que se cree con un solo request
        address: Optional[AddressRequest] = None,
        phone_number: Optional[UserDataRequest] = None,
        email_address: Optional[UserDataRequest] = None,
        terms: Optional[TOSAgreementRequest] = None,
        profession: Optional[UserDataRequest] = None,
        proof_of_address: Optional[UserProofRequest] = None,
        proof_of_life: Optional[UserProofRequest] = None,
        govt_id: Optional[GovtIDRequest] = None,
        *,
        session: Session = global_session,
    ) -> 'User':
        req = UserRequest(
            nombres=nombres,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            gender=gender,
            birth_place=birth_place,
            birth_date=birth_date,
            birth_country=birth_country,
            pronouns=pronouns,
            curp=curp,
            address=address,
            phone_number=phone_number,
            email_address=email_address,
            terms=terms,
            profession=profession,
            proof_of_address=proof_of_address,
            proof_of_life=proof_of_life,
            govt_id=govt_id,
        )
        return cast('User', cls._create(session=session, **req.dict()))

    @property
    def address(self):
        return cast(Address, retrieve_uri(self.address_uri))

    @property
    def phone_number(self):
        return cast(UserData, retrieve_uri(self.phone_uri))

    @property
    def email_address(self):
        return cast(UserData, retrieve_uri(self.email_address_uri))

    @property
    def profession(self):
        return cast(UserData, retrieve_uri(self.profession_uri))

    @property
    def proof_of_address(self):
        return cast(UserProof, retrieve_uri(self.proof_of_address_uri))

    @property
    def proof_of_life(self):
        return cast(UserProof, retrieve_uri(self.proof_of_life_uri))

    @property
    def curp(self):
        return cast(UserProof, retrieve_uri(self.curp_uri))

    @property
    def blacklist_check(self):
        return cast(UserProof, retrieve_uri(self.blacklist_check_uri))

    @property
    def govt_id(self):
        return cast(GovtID, retrieve_uri(self.govt_id_uri))

    @property
    def terms_of_service(self):
        return cast(TOSAgreement, retrieve_uri(self.terms_uri))
