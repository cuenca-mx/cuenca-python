import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    Address,
    Gender,
    IdentityQuery,
    KYCFile,
    State,
    TOSAgreement,
    UserStatus,
    VerificationStatus,
)
from cuenca_validations.types.identities import CurpField
from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class Identity(Retrievable, Queryable):
    _resource: ClassVar = 'identities'
    _query_params: ClassVar = IdentityQuery

    created_at: dt.datetime
    names: str
    first_surname: str
    second_surname: Optional[str]
    curp: Optional[CurpField]
    rfc: Optional[str]
    gender: Gender
    date_of_birth: Optional[dt.date]
    state_of_birth: Optional[State]
    country_of_birth: Optional[str]
    status: Optional[UserStatus]
    tos_agreement: Optional[TOSAgreement]
    blacklist_validation_status: Optional[VerificationStatus]
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
