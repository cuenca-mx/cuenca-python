import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import Country, PlatformRequest, State

from ..http import Session, session as global_session
from .base import Creatable


class Platform(Creatable):
    _resource: ClassVar = 'platforms'

    created_at: dt.datetime
    name: str
    rfc_curp: Optional[str] = None
    establishment_date: Optional[str] = None
    country: Optional[Country] = None
    state: Optional[State] = None
    economic_activity: Optional[str] = None

    class Config:
        fields = {
            'name': {'description': 'name of the platform being created'},
            'rfc_curp': {'description': 'name of the platform being created'},
            'establishment_date': {
                'description': 'name of the platform being created'
            },
            'country': {'description': 'name of the platform being created'},
            'state': {'description': 'name of the platform being created'},
            'economic_activity': {
                'description': 'name of the platform being created'
            },
        }
        schema_extra = {
            'example': {
                'id': 'PT0123456789',
                'name': 'Arteria',
                'created_at': '2021-08-24T14:15:22Z',
                'rfc_curp': 'ART123456FFF',
                'establishment_date': '2021-08-24T14:15:22Z',
                'country': 'MX',
                'state': 'DF',
                'economic_activity': 'fiinances and technologies',
            }
        }

    @classmethod
    def create(cls, name, *, session: Session = global_session):
        req = PlatformRequest(name=name)
        return cast('Platform', cls._create(session=session, **req.dict()))
