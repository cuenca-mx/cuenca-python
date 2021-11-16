import datetime as dt

from cuenca_validations.types import CardIssuerType
from pydantic.dataclasses import dataclass


# va a cuenca-validations?
@dataclass
class TOSAgreement:
    created_at: dt.datetime
    version: int
    ip: str
    location: str
    type: CardIssuerType
