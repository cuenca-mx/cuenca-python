import datetime as dt
from typing import ClassVar, List, Optional, cast

from clabe import Clabe
from cuenca_validations.types import (
    Address,
    Beneficiary,
    KYCFile,
    PhoneNumber,
    TOSAgreement,
    TOSRequest,
    UserQuery,
    UserRequest,
    UserStatus,
    UserUpdateRequest,
)
from cuenca_validations.types.enums import Country, Gender, State
from cuenca_validations.types.identities import CurpField
from pydantic import EmailStr, HttpUrl

from ..http import Session, session as global_session
from .balance_entries import BalanceEntry
from .base import Creatable, Queryable, Retrievable, Updateable
from .identities import Identity
from .resources import retrieve_uri


class User(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'users'
    _query_params: ClassVar = UserQuery

    identity_uri: str
    level: int
    required_level: int
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
    clabe: Optional[Clabe] = None
    # These fields are added by identify when retrieving a User:
    names: Optional[str]
    first_surname: Optional[str]
    second_surname: Optional[str]
    curp: Optional[str]
    rfc: Optional[str]
    gender: Optional[Gender]
    date_of_birth: Optional[dt.date]
    state_of_birth: Optional[State]
    nationality: Optional[Country]
    country_of_birth: Optional[Country]

    @property
    def balance(self) -> int:
        be = cast(BalanceEntry, BalanceEntry.first(user_id=self.id))
        return be.rolling_balance if be else 0

    class Config:
        fields = {
            'level': {
                'description': 'Account level according to KYC information'
            },
            'required_level': {
                'description': 'Maximum level User can reach. Set by platform'
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
                'required_level': 3,
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
        status: Optional[UserStatus] = None,
        required_level: Optional[int] = None,
        terms_of_service: Optional[TOSRequest] = None,
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
            required_level=required_level,
            status=status,
            terms_of_service=terms_of_service,
        )
        return cast('User', cls._create(session=session, **req.dict()))

    @classmethod
    def update(
        cls,
        user_id: str,
        phone_number: Optional[PhoneNumber] = None,
        email_address: Optional[str] = None,
        profession: Optional[str] = None,
        address: Optional[Address] = None,
        beneficiaries: Optional[List[Beneficiary]] = None,
        govt_id: Optional[KYCFile] = None,
        proof_of_address: Optional[KYCFile] = None,
        proof_of_life: Optional[KYCFile] = None,
        terms_of_service: Optional[TOSRequest] = None,
        verification_id: Optional[str] = None,
        status: Optional[UserStatus] = None,
        email_verification_id: Optional[str] = None,
        phone_verification_id: Optional[str] = None,
        curp_document: Optional[HttpUrl] = None,
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
            email_verification_id=email_verification_id,
            phone_verification_id=phone_verification_id,
            curp_document=curp_document,
            status=status,
        )
        return cast(
            'User',
            cls._update(id=user_id, **request.dict(), session=session),
        )

    @property
    def identity(self) -> Identity:
        return cast(Identity, retrieve_uri(self.identity_uri))
