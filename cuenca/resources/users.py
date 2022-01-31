import datetime as dt
from typing import ClassVar, List, Optional, cast

from cuenca_validations.types import (
    Address,
    AddressUpdateRequest,
    Beneficiary,
    KYCFile,
    KYCFileUpdateRequest,
    PhoneNumber,
    TOSAgreement,
    TOSUpdateRequest,
    UserRequest,
    UserUpdateRequest,
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

    @classmethod
    def update(
        cls,
        user_id: str,
        phone_number: Optional[str] = None,
        email_address: Optional[EmailStr] = None,
        profession: Optional[str] = None,
        address: Optional[AddressUpdateRequest] = None,
        beneficiary: Optional[List[Beneficiary]] = None,
        govt_id: Optional[KYCFileUpdateRequest] = None,
        proof_of_address: Optional[KYCFileUpdateRequest] = None,
        proof_of_life: Optional[KYCFileUpdateRequest] = None,
        terms_of_service: Optional[TOSUpdateRequest] = None,
    ):
        request = UserUpdateRequest(
            phone_number=phone_number,
            email_address=email_address,
            profession=profession,
            address=address,
            beneficiary=beneficiary,
            govt_id=govt_id,
            proof_of_address=proof_of_address,
            proof_of_life=proof_of_life,
            terms_of_service=terms_of_service,
        )
        return cast(
            'User', cls._update(id=user_id, **request.dict(exclude_none=True))
        )

    @property
    def identity(self) -> Identity:
        return cast(Identity, retrieve_uri(self.identity_uri))
