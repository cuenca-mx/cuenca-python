import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import Country, PlatformRequest, State

from ..http import Session, session as global_session
from .base import Creatable


class Platform(Creatable):
    _resource: ClassVar = 'platforms'

    created_at: dt.datetime
    name: str
    rfc: Optional[str] = None
    establishment_date: Optional[dt.date] = None
    country: Optional[Country] = None
    state: Optional[State] = None
    economic_activity: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        fields = {
            'name': {'description': 'name of the platform being created'},
            'rfc': {'description': 'RFC or CURP of the platform'},
            'establishment_date': {
                'description': 'when the platform was established'
            },
            'country': {'description': 'country where the platform resides'},
            'state': {'description': 'state where the platform resides'},
            'economic_activity': {'description': 'what the platform does'},
            'phone_number': {
                'description': 'phone number to contact the platform'
            },
            'email_address': {
                'description': 'email address to contact the platform'
            },
        }
        schema_extra = {
            'example': {
                'id': 'PT0123456789',
                'name': 'Arteria',
                'created_at': '2021-08-24T14:15:22Z',
                'rfc': 'ART123456FFF',
                'establishment_date': '2021-08-24T14:15:22Z',
                'country': 'MX',
                'state': 'DF',
                'economic_activity': 'fiinances and technologies',
                'phone_number': '+525555555555',
                'email_address': 'art@eria.com',
            }
        }

    @classmethod
    def create(
        cls,
        name: str,
        rfc: Optional[str] = None,
        establishment_date: Optional[str] = None,
        country: Optional[Country] = None,
        state: Optional[State] = None,
        economic_activity: Optional[str] = None,
        phone_number: Optional[str] = None,
        email_address: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'Platform':
        req = PlatformRequest(
            name=name,
            rfc=rfc,
            establishment_date=establishment_date,
            country=country,
            state=state,
            economic_activity=economic_activity,
            phone_number=phone_number,
            email_address=email_address,
        )
        return cast('Platform', cls._create(session=session, **req.dict()))
