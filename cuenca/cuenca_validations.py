import datetime as dt
from typing import List, Optional

from cuenca_validations.types import Address, CurpField, PhoneNumber, Rfc
from pydantic import BaseModel, EmailStr


class BusinessDetails(BaseModel):
    business_description: str
    account_usage_description: str


class TransactionalProfile(BaseModel):
    currency: str
    monthly_amount: str
    recipients_num: int
    payers_num: int
    internal_transfers_amount: int
    internal_transfers_num: int
    spei_transfers_amount: int
    spei_transfers_num: int


class LicenseDetails(BaseModel):
    license_required: bool
    supervisory_entity: Optional[str] = None
    license_type: Optional[str] = None
    license_date: Optional[dt.date] = None


class AuditDetails(BaseModel):
    has_audit: bool
    audit_provider: Optional[str] = None
    audit_date: Optional[dt.date] = None
    audit_comments: Optional[str] = None


class VulnerableActivityDetails(BaseModel):
    is_vulnerable_activity: bool
    has_sat_register: bool = None
    sat_registered_date: Optional[dt.date] = None
    is_in_compliance: Optional[bool] = None


class PhysicalPerson(BaseModel):
    # Usar curp_validation?
    names: str
    first_surname: str
    second_surname: Optional[str] = None
    curp: CurpField
    rfc: Rfc


class LegalRepresentative(PhysicalPerson):
    job: str
    phone_number: Optional[PhoneNumber]
    email_address: Optional[EmailStr]
    address: Optional[Address]


class ShareholderPhysical(PhysicalPerson):
    percentage: str


class ShareholderMoral(BaseModel):
    name: str
    percentage: str
    shareholders: List[ShareholderPhysical]
    legal_representatives: List[LegalRepresentative]
