import datetime as dt
from typing import ClassVar, Optional

from pydantic.dataclasses import dataclass

from .addresses import Address
from .base import Retrievable, Updateable
from .blacklist_validations import BlacklistValidation
from .kyc_file import KYCFile
from .tos_agreements import TOSAgreement


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
    terms_of_service: TOSAgreement
    blacklist_check: BlacklistValidation
    # estos van a ser campos que también están en cada user
    address: Address
    govt_id: KYCFile
    proof_of_address: KYCFile
    proof_of_life: KYCFile
