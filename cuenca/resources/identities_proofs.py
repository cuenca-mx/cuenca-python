import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Creatable, Retrievable, Updateable


@dataclass
class IdentityProof(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'identities_proofs'

    id: str
    type: str  # enum (proof_of_address, proof_of_life)
    created_at: dt.datetime
    feedme_uri: str
    identity_id: str  # property? foreign key?
    deactivated_at: dt.datetime
