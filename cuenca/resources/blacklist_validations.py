import datetime as dt
from typing import Optional

from cuenca_validations.types import UserProofStatus, UserProofType
from pydantic.dataclasses import dataclass


# va a cuenca-validations?
@dataclass
class BlacklistValidation:
    id: str
    type: UserProofType
    created_at: dt.datetime
    feedme_uri: Optional[str]
    value: Optional[str]
    deactivated_at: Optional[dt.datetime]
    status: UserProofStatus  # se va a acatualizar solito en identifier
