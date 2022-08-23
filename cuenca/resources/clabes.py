from typing import ClassVar, cast

from cuenca_validations.types import QueryParams

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class Clabe(Creatable, Queryable, Retrievable):
    _resource: ClassVar = 'clabes'
    _query_params: ClassVar = QueryParams
    clabe: str
    user_id: str

    @classmethod
    def create(cls, session: Session = global_session):
        return cast('Clabe', cls._create(session=session))
