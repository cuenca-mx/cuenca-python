import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import Country, PlatformRequest, State
from pydantic import ConfigDict, Field

from ..http import Session, session as global_session
from .base import Creatable


class Platform(Creatable):
    _resource: ClassVar = 'platforms'

    created_at: dt.datetime
    name: str = Field(description='name of the platform being created')
    rfc: Optional[str] = Field(None, description='RFC or CURP of the platform')
    establishment_date: Optional[dt.date] = Field(
        None, description='when the platform was established'
    )
    country: Optional[Country] = Field(
        None, description='country where the platform resides'
    )
    state: Optional[State] = Field(
        None, description='state where the platform resides'
    )
    economic_activity: Optional[str] = Field(
        None, description='what the platform does'
    )
    email_address: Optional[str] = Field(
        None, description='email address to contact the platform'
    )
    phone_number: Optional[str] = Field(
        None, description='phone number to contact the platform'
    )
    model_config = ConfigDict(
        json_schema_extra={
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
    )

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
        return cls._create(session=session, **req.model_dump())
