import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import UserCredentialRequest

from ..http import Session, session as global_session
from .base import Creatable


@dataclass
class UserLogin(Creatable):
    _resource: ClassVar = 'user_logins'

    last_login_at: Optional[dt.datetime]
    success: bool

    @classmethod
    def create(
        cls, password: str, *, session: Session = global_session
    ) -> 'UserLogin':
        req = UserCredentialRequest(password=password)
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
