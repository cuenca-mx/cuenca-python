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
from cuenca_validations.types.identities import Curp

from .base import Queryable, Retrievable


class Identity(Retrievable, Queryable):
    _resource: ClassVar = 'identities'
    _query_params: ClassVar = IdentityQuery

    created_at: dt.datetime
    names: str
    first_surname: str
    second_surname: Optional[str] = None
    curp: Optional[Curp] = None
    rfc: Optional[str] = None
    gender: Gender
    date_of_birth: Optional[dt.date] = None
    state_of_birth: Optional[State] = None
    country_of_birth: Optional[str] = None
    status: Optional[UserStatus] = None
    tos_agreement: Optional[TOSAgreement] = None
    blacklist_validation_status: Optional[VerificationStatus] = None
    address: Optional[Address] = None
    govt_id: Optional[KYCFile] = None
    proof_of_address: Optional[KYCFile] = None
    proof_of_life: Optional[KYCFile] = None
