import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    Country,
    CurpValidationRequest,
    Gender,
    State,
)
from cuenca_validations.types.identities import Curp
from pydantic import ConfigDict, Field

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class CurpValidation(Creatable, Retrievable):
    _resource: ClassVar = 'curp_validations'

    created_at: dt.datetime
    names: Optional[str] = Field(None, description='Official name from Renapo')
    first_surname: Optional[str] = Field(
        None, description='Official surname from Renapo'
    )
    second_surname: Optional[str] = Field(
        None, description='Official surname from Renapo'
    )
    date_of_birth: Optional[dt.date] = Field(
        None, description='In format ISO 3166 Alpha-2'
    )
    country_of_birth: Optional[Country] = Field(
        None, description='In format ISO 3166 Alpha-2'
    )
    state_of_birth: Optional[State] = Field(None, description='State of birth')
    gender: Optional[Gender] = Field(None, description='Gender')
    nationality: Optional[Country] = Field(
        None, description='In format ISO 3166 Alpha-2'
    )
    manual_curp: Optional[Curp] = Field(
        None, description='curp provided in request'
    )
    calculated_curp: Curp = Field(
        description='Calculated CURP based on request data'
    )
    validated_curp: Optional[Curp] = Field(
        None, description='CURP validated in Renapo, null if not exists'
    )
    renapo_curp_match: bool = Field(
        description='True if CURP exists and is valid'
    )
    renapo_full_match: bool = Field(
        description='True if all fields provided match the response from '
        'RENAPO. Accents in names are ignored',
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'CVNEUInh69SuKXXmK95sROwQ',
                'created_at': '2019-08-24T14:15:22Z',
                'names': 'Guillermo',
                'first_surname': 'Gonzales',
                'second_surname': 'Camarena',
                'date_of_birth': '1965-04-18',
                'country_of_birth': 'MX',
                'state_of_birth': 'VZ',
                'gender': 'male',
                'nationality': 'MX',
                'manual_curp': None,
                'calculated_curp': 'GOCG650418HVZNML08',
                'validated_curp': 'GOCG650418HVZNML08',
                'renapo_curp_match': True,
                'renapo_full_match': True,
            }
        },
    )

    @classmethod
    def create(
        cls,
        names: Optional[str] = None,
        first_surname: Optional[str] = None,
        date_of_birth: Optional[dt.date] = None,
        country_of_birth: Optional[str] = None,
        state_of_birth: Optional[State] = None,
        gender: Optional[Gender] = None,
        second_surname: Optional[str] = None,
        manual_curp: Optional[Curp] = None,
        *,
        session: Session = global_session,
    ) -> 'CurpValidation':
        req = CurpValidationRequest(
            names=names,
            first_surname=first_surname,
            second_surname=second_surname,
            date_of_birth=date_of_birth,
            state_of_birth=state_of_birth,
            country_of_birth=country_of_birth,
            gender=gender,
            manual_curp=manual_curp,
        )
        return cls._create(session=session, **req.model_dump())
