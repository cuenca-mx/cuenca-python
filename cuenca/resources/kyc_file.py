import datetime as dt
from typing import Optional

from cuenca_validations.types import KYCFileType
from pydantic.dataclasses import dataclass


# va a cuenca-validations?
@dataclass
class KYCFile:
    created_at: dt.datetime
    updated_at: dt.datetime
    type: KYCFileType  # govt_id, proof_of_address, proof_of_life
    feedme_uri_front: str
    feedme_uri_back: str
    is_mx: bool
    data: Optional[str]
