import datetime as dt
from typing import ClassVar, Optional, cast

from clabe import Clabe
from cuenca_validations.types import (
    Address,
    Beneficiary,
    BeneficiaryRequest,
    KYCFile,
    PhoneNumber,
    SATRegimeCode,
    TOSAgreement,
    UserQuery,
    UserRequest,
    UserStatus,
    UserUpdateRequest,
    VerificationStatus,
)
from cuenca_validations.types.enums import (
    AccountUseType,
    Country,
    Gender,
    IncomeType,
    MonthlyMovementsType,
    MonthlySpendingType,
    State,
)
from cuenca_validations.types.general import SerializableHttpUrl
from cuenca_validations.types.identities import AddressRequest, Curp, Rfc
from pydantic import ConfigDict, EmailStr, Field

from ..http import Session, session as global_session
from .balance_entries import BalanceEntry
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable
from .identities import Identity
from .resources import retrieve_uri


class User(Creatable, Retrievable, Updateable, Queryable, Deactivable):
    _resource: ClassVar = 'users'
    _query_params: ClassVar = UserQuery

    identity_uri: str
    level: int = Field(
        description='Account level according to KYC information'
    )
    required_level: int = Field(
        description='Maximum level User can reach. Set by platform'
    )
    created_at: dt.datetime
    phone_number: Optional[PhoneNumber] = None
    email_address: Optional[EmailStr] = None
    profession: Optional[str] = None
    terms_of_service: Optional[TOSAgreement] = None
    status: Optional[UserStatus] = None
    address: Optional[Address] = None
    govt_id: Optional[KYCFile] = Field(
        None, description='Government ID document validation'
    )
    proof_of_address: Optional[KYCFile] = Field(
        None, description='Detail of proof of address document validation'
    )
    proof_of_life: Optional[KYCFile] = Field(
        None, description='Detail of selfie video validation'
    )
    beneficiaries: Optional[list[Beneficiary]] = Field(
        None, description='Beneficiaries of account in case of death'
    )
    platform_id: Optional[str] = None
    clabe: Optional[Clabe] = None
    fiscal_regime_code: Optional[SATRegimeCode] = None
    fiscal_address: Optional[Address] = None
    account_use_type: Optional[AccountUseType] = None
    monthly_spending_type: Optional[MonthlySpendingType] = None
    monthly_movements_type: Optional[MonthlyMovementsType] = None
    income_type: Optional[IncomeType] = None
    # These fields are added by identify when retrieving a User:
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    curp: Optional[str] = None
    rfc: Optional[str] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[dt.date] = None
    state_of_birth: Optional[State] = None
    nationality: Optional[Country] = None
    country_of_birth: Optional[Country] = None
    blacklist_validation_status: Optional[VerificationStatus] = None
    pronouns: Optional[str] = None
    deactivated_at: Optional[dt.datetime] = None
    user_tos_agreements_id: Optional[str] = None

    @property
    def balance(self) -> int:
        be = BalanceEntry.first(user_id=self.id)
        return be.rolling_balance if be else 0

    @property
    def full_name(self) -> str:
        parts = [self.names, self.first_surname, self.second_surname]
        return ' '.join(p for p in parts if p)

    model_config = ConfigDict(
        json_schema_extra={
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
                'terms_of_service': TOSAgreement.model_json_schema().get(
                    'example'
                ),
                'status': 'active',
                'address': Address.model_json_schema().get('example'),
                'govt_id': KYCFile.model_json_schema().get('example'),
                'proof_of_address': None,
                'proof_of_life': None,
                'beneficiaries': [
                    Beneficiary.model_json_schema().get('example'),
                ],
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
            }
        }
    )

    @classmethod
    def create(
        cls,
        curp: Curp,
        profession: Optional[str] = None,
        address: Optional[AddressRequest] = None,
        email_verification_id: Optional[str] = None,
        phone_verification_id: Optional[str] = None,
        account_use_type: Optional[AccountUseType] = None,
        monthly_spending_type: Optional[MonthlySpendingType] = None,
        monthly_movements_type: Optional[MonthlyMovementsType] = None,
        income_type: Optional[IncomeType] = None,
        *,
        session: Session = global_session,
    ) -> 'User':
        req = UserRequest(
            curp=curp,
            profession=profession,
            address=address,
            email_verification_id=email_verification_id,
            phone_verification_id=phone_verification_id,
            account_use_type=account_use_type,
            monthly_spending_type=monthly_spending_type,
            monthly_movements_type=monthly_movements_type,
            income_type=income_type,
        )
        return cls._create(session=session, **req.model_dump())

    @classmethod
    def update(
        cls,
        user_id: str,
        profession: Optional[str] = None,
        address: Optional[AddressRequest] = None,
        beneficiaries: Optional[list[BeneficiaryRequest]] = None,
        govt_id: Optional[KYCFile] = None,
        proof_of_address: Optional[KYCFile] = None,
        proof_of_life: Optional[KYCFile] = None,
        status: Optional[UserStatus] = None,
        email_verification_id: Optional[str] = None,
        phone_verification_id: Optional[str] = None,
        curp_document_uri: Optional[SerializableHttpUrl] = None,
        rfc: Optional[Rfc] = None,
        fiscal_regime_code: Optional[SATRegimeCode] = None,
        fiscal_address: Optional[AddressRequest] = None,
        account_use_type: Optional[AccountUseType] = None,
        monthly_spending_type: Optional[MonthlySpendingType] = None,
        monthly_movements_type: Optional[MonthlyMovementsType] = None,
        income_type: Optional[IncomeType] = None,
        pronouns: Optional[str] = None,
        blacklist_validation_status: Optional[VerificationStatus] = None,
        *,
        session: Session = global_session,
    ) -> 'User':
        request = UserUpdateRequest(
            profession=profession,
            address=address,
            beneficiaries=beneficiaries,
            govt_id=govt_id,
            proof_of_address=proof_of_address,
            proof_of_life=proof_of_life,
            status=status,
            email_verification_id=email_verification_id,
            phone_verification_id=phone_verification_id,
            curp_document_uri=curp_document_uri,
            rfc=rfc,
            fiscal_regime_code=fiscal_regime_code,
            fiscal_address=fiscal_address,
            account_use_type=account_use_type,
            monthly_spending_type=monthly_spending_type,
            monthly_movements_type=monthly_movements_type,
            income_type=income_type,
            pronouns=pronouns,
            blacklist_validation_status=blacklist_validation_status,
        )
        return cls._update(id=user_id, **request.model_dump(), session=session)

    @property
    def identity(self) -> Identity:
        return cast(Identity, retrieve_uri(self.identity_uri))
