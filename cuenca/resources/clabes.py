import datetime as dt
from typing import ClassVar, cast

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class Clabe(Creatable, Retrievable):
    _resource: ClassVar = 'clabes'
    clabe: str
    created_at: dt.datetime
    user_id: str

    @classmethod
    def create(cls, user_id: str = 'me', session: Session = global_session):
        req = dict(user_id=user_id)
        return cast('Clabe', cls._create(session=session, **req))
