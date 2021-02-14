from dataclasses import dataclass
import datetime as dt

from typing import TYPE_CHECKING
from .exc import InvalidPassword
if TYPE_CHECKING:
    from .http import Session
@dataclass
class Login:
    last_login_at: dt.datetime
    login_id: str

    @classmethod
    def log_in(cls, password: str, session: 'Session') -> 'Login':
        resp = session.post('/log_in', dict(password=password))
        if not resp['success']:
            raise InvalidPassword
        return cls(**resp)

    def log_out(self, session: 'Session') -> None:
        session.post('/log_out')
