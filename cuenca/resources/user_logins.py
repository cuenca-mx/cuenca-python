import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import UserLoginRequest

from ..http import Session, session as global_session
from .base import Creatable


class UserLogin(Creatable):
    _resource: ClassVar = 'user_logins'

    last_login_at: Optional[dt.datetime]
    success: bool

    class Config:
        schema_extra = {
            'example': {
                'id': 'ULNEUInh69SuKXXmK95sROwQ',
                'last_login_at': '2022-01-01T14:15:22Z',
                'success': True,
            }
        }

    @classmethod
    def create(
        cls,
        password: str,
        user_id: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'UserLogin':
        req = UserLoginRequest(password=password, user_id=user_id)
        login = cast('UserLogin', cls._create(session=session, **req.dict()))
        if login.success:
            session.session.headers['X-Cuenca-LoginId'] = login.id
        return login

    @classmethod
    def logout(
        cls, user_id: str = 'me', *, session: Session = global_session
    ) -> None:
        # Using user_id vs user_login_id to avoid needing to store
        # user_login_id or perform a query to fetch it
        session.delete(f'{cls._resource}/{user_id}', dict())
        session.session.headers.pop('X-Cuenca-LoginId', None)
