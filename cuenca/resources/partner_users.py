import datetime as dt
from typing import ClassVar, List, Optional

from clabe import Clabe
from cuenca_validations.types import Address, PhoneNumber, QueryParams
from cuenca_validations.types.enums import Country
from cuenca_validations.types.identities import Rfc
from pydantic import EmailStr

from ..cuenca_validations import (
    AuditDetails,
    BusinessDetails,
    LegalRepresentative,
    LicenseDetails,
    ShareholderMoral,
    TransactionalProfile,
    VulnerableActivityDetails,
)
from .base import Creatable, Queryable, Retrievable, Updateable


class PartnerUser(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'partner_users'
    _query_params: ClassVar = QueryParams

    created_at: dt.datetime
    updated_at: dt.datetime

    # 01 - General
    legal_name: str
    business_name: str
    nationality: Country
    incorporation_date: dt.date
    folio: str
    certificate_number: str
    rfc: Rfc
    documentation_url: str
    # 02 - Contacto
    web_site: str
    phone_number: PhoneNumber
    email_address: EmailStr
    address: Address
    # 03 - Detalles
    business_details: Optional[BusinessDetails] = None
    # 04 - Perfil transaccional
    transactional_profile: Optional[TransactionalProfile] = None
    # 05 Cuenta externa
    external_account: Optional[Clabe] = None

    # Estado regulatorio
    # 01 Licencia
    license: Optional[LicenseDetails] = None
    # 02 Auditoria
    audit: Optional[AuditDetails] = None
    # 03 Manuales y politicas: Son archivos, no pide info
    # 04 Actividades vulnearables
    vulnerable_activity: Optional[VulnerableActivityDetails] = None

    # Representantes y accionista
    legal_representatives: List[LegalRepresentative] = []
    shareholders: List[ShareholderMoral] = []
