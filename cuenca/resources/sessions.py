import datetime as dt
from typing import Annotated, ClassVar, Optional

from cuenca_validations.types import LogConfig, SessionRequest, SessionType
from cuenca_validations.types.general import SerializableAnyUrl
from pydantic import ConfigDict

from .. import http
from .base import Creatable, Queryable, Retrievable


class Session(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'sessions'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    created_at: dt.datetime
    user_id: str
    platform_id: str
    expires_at: dt.datetime
    success_url: Optional[SerializableAnyUrl] = None
    failure_url: Optional[SerializableAnyUrl] = None
    type: Optional[SessionType] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'SENEUInh69SuKXXmK95sROwQ',
                'created_at': '2022-08-24T14:15:22Z',
                'user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
                'expires_at': '2022-08-24T14:30:22Z',
                'success_url': 'http://example_success.com',
                'failure_url': 'http://example_failure.com',
                'type': 'session.registration',
            }
        }
    )

    @classmethod
    def create(
        cls,
        user_id: str,
        type: SessionType,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        *,
        session: http.Session = http.session,
    ) -> 'Session':
        req = SessionRequest(
            user_id=user_id,
            type=type,
            success_url=success_url,
            failure_url=failure_url,
        )
        return cls._create(session=session, **req.model_dump())
