import datetime as dt
from typing import Annotated, ClassVar, Optional

from cuenca_validations.types import LogConfig
from cuenca_validations.types.requests import UserLoginRequest
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class UserLogin(Creatable):
    _resource: ClassVar = 'user_logins'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]

    last_login_at: Optional[dt.datetime] = None
    success: bool

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'ULNEUInh69SuKXXmK95sROwQ',
                'last_login_at': '2022-01-01T14:15:22Z',
                'success': True,
            }
        }
    )

    @classmethod
    def create(
        cls,
        password: str,
        user_id: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'UserLogin':
        req = UserLoginRequest(password=password, user_id=user_id)
        login = cls._create(session=session, **req.model_dump())
        if login.success:
            session.headers['X-Cuenca-LoginId'] = login.id
        return login

    @classmethod
    def logout(
        cls, user_id: str = 'me', *, session: Session = global_session
    ) -> None:
        # Using user_id vs user_login_id to avoid needing to store
        # user_login_id or perform a query to fetch it
        session.delete(f'{cls._resource}/{user_id}', dict())
        session.headers.pop('X-Cuenca-LoginId', None)
