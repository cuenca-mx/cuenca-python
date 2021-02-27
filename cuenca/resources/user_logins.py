import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, cast

from cuenca_validations.types.requests import PasswordRequest

from ..http import Session, session as global_session
from .base import Creatable


@dataclass
class UserLogin(Creatable):
    _resource: ClassVar = 'log_in'

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
    def logout(cls, *, session: Session = global_session) -> 'UserLogin':
        resp = session.post('/log_out', dict())
        login = cast('UserLogin', cls._from_dict(resp))
        session.session.headers.pop('X-Cuenca-LoginId', None)
        return login
