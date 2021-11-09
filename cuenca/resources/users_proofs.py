import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    UserProofRequest,
    UserProofStatus,
    UserProofType,
)
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable


@dataclass
class UserProof(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'identities_proofs'

    id: str
    type: UserProofType
    created_at: dt.datetime
    feedme_uri: str
    deactivated_at: Optional[dt.datetime]
    status: UserProofStatus  # se va a acatualizar solito en identifier

    user_uri: str  # property? foreign key?

    @classmethod
    def create(
        cls,
        user_id: str,
        type: str,
        feedme_uri: str,
        *,
        session: Session = global_session,
    ):
        req = UserProofRequest(
            user_id=user_id,
            type=type,
            feedme_uri=feedme_uri,
        )
        return cast('UserProof', cls._create(session=session, **req.dict()))
