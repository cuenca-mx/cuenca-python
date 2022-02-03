import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import SessionRequest, SessionType
from pydantic.dataclasses import dataclass

from .. import Session as SessionModel, session as global_session
from .base import Creatable, Queryable, Retrievable


@dataclass
class Session(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'sessions'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    user_id: str
    platform_id: str
    expires_at: dt.datetime
    success_url: Optional[str]
    failure_url: Optional[str]
    type: Optional[SessionType]

    @classmethod
    def create(
        cls,
        user_id: str,
        type: SessionType,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        *,
        session: SessionModel = global_session,
    ) -> 'Session':
        req = SessionRequest(
            user_id=user_id,
            type=type,
            success_url=success_url,
            failure_url=failure_url,
        )
        return cast('Session', cls._create(session=session, **req.dict()))
