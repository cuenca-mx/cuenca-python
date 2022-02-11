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
    UserQuery,
    UserRequest,
    UserStatus,
    UserUpdateRequest,
)
from cuenca_validations.types.identities import CurpField
from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable
from .identities import Identity
from .resources import retrieve_uri


@dataclass
class User(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'users'
    _query_params: ClassVar = UserQuery

    identity_uri: str
    level: int
    created_at: dt.datetime
    phone_number: PhoneNumber
    email_address: EmailStr
    profession: str
    terms_of_service: Optional[TOSAgreement]
    status: Optional[UserStatus]
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
    beneficiaries: Optional[List[Beneficiary]]
    platform_id: Optional[str] = None

    @classmethod
    def create(
        cls,
        curp: CurpField,
        phone_number: PhoneNumber,
        email_address: EmailStr,
        profession: str,
        address: Address,
        *,
        session: Session = global_session,
    ) -> 'User':
        req = UserRequest(
            curp=curp,
            phone_number=phone_number,
            email_address=email_address,
            profession=profession,
            address=address,
        )
        return cast('User', cls._create(session=session, **req.dict()))

    @classmethod
    def update(
        cls,
        user_id: str,
        phone_number: Optional[PhoneNumber] = None,
        email_address: Optional[str] = None,
        profession: Optional[str] = None,
        address: Optional[AddressUpdateRequest] = None,
        beneficiaries: Optional[List[Beneficiary]] = None,
        govt_id: Optional[KYCFileUpdateRequest] = None,
        proof_of_address: Optional[KYCFileUpdateRequest] = None,
        proof_of_life: Optional[KYCFileUpdateRequest] = None,
        terms_of_service: Optional[TOSUpdateRequest] = None,
        *,
        session: Session = global_session,
    ):
        request = UserUpdateRequest(
            phone_number=phone_number,
            email_address=email_address,
            profession=profession,
            address=address,
            beneficiaries=beneficiaries,
            govt_id=govt_id,
            proof_of_address=proof_of_address,
            proof_of_life=proof_of_life,
            terms_of_service=terms_of_service,
        )
        return cast(
            'User',
            cls._update(id=user_id, **request.dict(), session=session),
        )

    @property
    def identity(self) -> Identity:
        return cast(Identity, retrieve_uri(self.identity_uri))
