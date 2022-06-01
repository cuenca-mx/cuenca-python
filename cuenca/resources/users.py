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

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable
from .identities import Identity
from .resources import retrieve_uri


class User(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'users'
    _query_params: ClassVar = UserQuery

    identity_uri: str
    level: int
    created_at: dt.datetime
    phone_number: Optional[PhoneNumber]
    email_address: Optional[EmailStr]
    profession: Optional[str]
    terms_of_service: Optional[TOSAgreement]
    status: Optional[UserStatus]
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
    beneficiaries: Optional[List[Beneficiary]]
    platform_id: Optional[str] = None

    class Config:
        fields = {
            'level': {
                'description': 'Account level according to KYC information'
            },
            'govt_id': {
                'description': 'Detail of government id document validation'
            },
            'proof_of_address': {
                'description': 'Detail of proof of address document validation'
            },
            'proof_of_life': {
                'description': 'Detail of selfie video validation'
            },
            'beneficiaries': {
                'description': 'Beneficiaries of account in case of death'
            },
        }
        schema_extra = {
            'example': {
                'id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'created_at': '2019-08-24T14:15:22Z',
                'updated_at': '2019-08-24T14:15:22Z',
                'identity_uri': 'identities/IDNEUInh69SuKXXmK95sROwQ',
                'level': 2,
                'phone_number': '+525511223344',
                'email_address': 'user@example.com',
                'profession': 'engineer',
                'terms_of_service': TOSAgreement.schema().get('example'),
                'status': 'active',
                'address': Address.schema().get('example'),
                'govt_id': KYCFile.schema().get('example'),
                'proof_of_address': None,
                'proof_of_life': None,
                'beneficiaries': [
                    Beneficiary.schema().get('example'),
                ],
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
            }
        }

    @classmethod
    def create(
        cls,
        curp: CurpField,
        phone_number: Optional[PhoneNumber] = None,
        email_address: Optional[EmailStr] = None,
        profession: Optional[str] = None,
        address: Optional[Address] = None,
        email_verification_id: Optional[str] = None,
        phone_verification_id: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'User':
        req = UserRequest(
            curp=curp,
            phone_number=phone_number,
            email_address=email_address,
            profession=profession,
            address=address,
            email_verification_id=email_verification_id,
            phone_verification_id=phone_verification_id,
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
        verification_id: Optional[str] = None,
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
            verification_id=verification_id,
        )
        return cast(
            'User',
            cls._update(id=user_id, **request.dict(), session=session),
        )

    @property
    def identity(self) -> Identity:
        return cast(Identity, retrieve_uri(self.identity_uri))
