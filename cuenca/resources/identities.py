import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    Address,
    Gender,
    KYCFile,
    States,
    TOSAgreement,
)
from pydantic.dataclasses import dataclass

from .base import Retrievable, Updateable


@dataclass
class Identity(Retrievable, Updateable):  # y/o Humans
    _resource: ClassVar = 'identities'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    nombres: str
    primer_apellido: str
    segundo_apellido: Optional[str]
    curp: Optional[str]
    rfc: Optional[str]
    gender: Optional[Gender]
    birth_date: Optional[dt.date]
    birth_place: Optional[States]
    birth_country: Optional[str]  # enum countries
    status: str  # enum UserStatus
    tos_agreement: TOSAgreement
    blacklist_validation_status: Optional[str]
    # estos van a ser campos que también están en cada user
    address: Optional[Address]
    govt_id: Optional[KYCFile]
    proof_of_address: Optional[KYCFile]
    proof_of_life: Optional[KYCFile]
