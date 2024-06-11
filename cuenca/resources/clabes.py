from typing import ClassVar

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class Clabe(Creatable, Queryable, Retrievable):
    _resource: ClassVar = 'clabes'
    clabe: str
    user_id: str

    @classmethod
    def create(cls, session: Session = global_session):
        return cls._create(session=session)
