import datetime as dt
from typing import Annotated, ClassVar, Optional, cast

from cuenca_validations.types import SessionRequest, SessionType
from pydantic import AfterValidator, AnyUrl, ConfigDict

from .. import http
from .base import Creatable, Queryable, Retrievable

# In Pydantic v2, URL fields like `AnyUrl` are stored as internal objects
# instead of `str`, which can break compatibility with code expecting str.
# Using `AnyUrlString` ensures the field is validated as a URL but stored as
# a `str` for compatibility.
# https://github.com/pydantic/pydantic/discussions/6395

AnyUrlString = Annotated[AnyUrl, AfterValidator(str)]


class Session(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'sessions'

    id: str
    created_at: dt.datetime
    user_id: str
    platform_id: str
    expires_at: dt.datetime
    success_url: Optional[AnyUrlString] = None
    failure_url: Optional[AnyUrlString] = None
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
        success_url=cast(Optional[AnyUrl], success_url),
        failure_url=cast(Optional[AnyUrl], failure_url),
        *,
        session: http.Session = http.session,
    ) -> 'Session':
        req = SessionRequest(
            user_id=user_id,
            type=type,
            success_url=success_url,
            failure_url=failure_url,
        )
        return cast('Session', cls._create(session=session, **req.dict()))
