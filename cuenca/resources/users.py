import datetime as dt
from typing import ClassVar, List, Optional, cast

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


@dataclass
class User(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'users'

    id: str
    identity_uri: str
    platform_id: str
    level: int
    created_at: dt.datetime
    updated_at: dt.datetime
    phone_number: PhoneNumber
    email_address: EmailStr
    profession: str
    terms_of_service: Optional[TOSAgreement]
    status: Optional[str]
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
    beneficiary: Optional[List[Beneficiary]]

    @classmethod
    def create(
        cls,
        user_request: UserRequest,
        *,
        session: Session = global_session,
    ) -> 'User':
        return cast(
            'User', cls._create(session=session, **user_request.dict())
        )

    @property
    def identity(self):
        return cast(Identity, retrieve_uri(self.identity_uri))
