import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types.requests import UserPldRiskLevelRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Retrievable

from ..http import Session, session as global_session


@dataclass
class UserPldRiskLevel(Retrievable, Creatable):
    _resource: ClassVar = 'user_pld_risk_levels'

    created_at: dt.datetime
    updated_at: dt.datetime
    level: float
    is_user_defined: bool

    @classmethod
    def create(
        cls, user_id: str, level: float, *, session: Session = global_session
    ) -> 'UserPldRiskLevel':
        req = UserPldRiskLevelRequest(user_id=user_id, level=level)
        return cast(
            'UserPldRiskLevel', cls._create(session=session, **req.dict())
        )
