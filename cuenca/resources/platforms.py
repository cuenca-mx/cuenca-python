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
    establishment_date: Optional[dt.date] = None
    country: Optional[Country] = None
    state: Optional[State] = None
    economic_activity: Optional[str] = None

    class Config:
        fields = {
            'name': {'description': 'name of the platform being created'},
            'rfc_curp': {'description': 'RFC or CURP of the platform'},
            'establishment_date': {
                'description': 'when the platform was established'
            },
            'country': {'description': 'country where the platform resides'},
            'state': {'description': 'state where the platform resides'},
            'economic_activity': {'description': 'what the platform does'},
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
    def create(
        cls,
        name: str,
        rfc_curp: Optional[str] = None,
        establishment_date: Optional[str] = None,
        country: Optional[Country] = None,
        state: Optional[State] = None,
        economic_activity: Optional[str] = None,
        *,
        session: Session = global_session,
    ):
        req = PlatformRequest(
            name=name,
            rfc_curp=rfc_curp,
            establishment_date=establishment_date,
            country=country,
            state=state,
            economic_activity=economic_activity,
        )
        return cast('Platform', cls._create(session=session, **req.dict()))
