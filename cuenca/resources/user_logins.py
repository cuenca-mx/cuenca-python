import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, cast

from cuenca_validations.types.requests import (
    PasswordRequest,
    UserLoginUpdateRequest,
)

from ..http import Session, session as global_session
from .base import Creatable


@dataclass
class UserLogin(Creatable):
    _resource: ClassVar = 'user_logins'

    last_login_at: dt.datetime
    success: bool

    @classmethod
    def create(
        cls, password: str, *, session: Session = global_session
    ) -> 'UserLogin':
        req = PasswordRequest(password=password)
        login = cast('UserLogin', cls._create(session=session, **req.dict()))
        if login.success:
            session.session.headers['X-Cuenca-LoginId'] = login.id
        return login

    @classmethod
    def logout(
        cls, user_id: str = 'me', *, session: Session = global_session
    ) -> None:
        session.delete(f'{cls._resource}/{user_id}', dict())
        session.session.headers.pop('X-Cuenca-LoginId', None)

    @classmethod
    def update(
        cls,
        is_active: bool,
        user_id: str = 'me',
        *,
        session: Session = global_session,
    ) -> None:
        req = UserLoginUpdateRequest(is_active=is_active)
        session.patch(f'{cls._resource}/{user_id}', req.dict())
