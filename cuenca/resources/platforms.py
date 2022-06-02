import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types import PlatformRequest

from ..http import Session, session as global_session
from .base import Creatable


class Platform(Creatable):
    _resource: ClassVar = 'platforms'

    created_at: dt.datetime
    name: str

    class Config:
        fields = {
            'name': {'description': 'name of the platform being created'}
        }
        schema_extra = {
            'example': {
                'id': 'PT0123456789',
                'name': 'Arteria',
                'created_at': '2021-08-24T14:15:22Z',
            }
        }

    @classmethod
    def create(cls, name, *, session: Session = global_session):
        req = PlatformRequest(name=name)
        return cast('Platform', cls._create(session=session, **req.dict()))
