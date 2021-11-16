import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    Address,
    BlacklistValidation,
    KYCFile,
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
    curp: str
    rfc: Optional[str]
    gender: Optional[str]  # enum gender
    birth_date: Optional[dt.date]
    birth_place: Optional[str]  # enum states
    birth_country: Optional[str]  # enum countries
    status: str  # enum UserStatus
    tos_agreement: TOSAgreement
    blacklist_validation: BlacklistValidation
    # estos van a ser campos que también están en cada user
    address: Address
    govt_id: KYCFile
    proof_of_address: KYCFile
    proof_of_life: KYCFile
