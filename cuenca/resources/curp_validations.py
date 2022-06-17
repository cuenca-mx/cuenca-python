import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    Country,
    CurpValidationRequest,
    Gender,
    State,
)
from cuenca_validations.types.identities import CurpField

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class CurpValidation(Creatable, Retrievable):
    _resource: ClassVar = 'curp_validations'

    created_at: dt.datetime
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    date_of_birth: Optional[dt.date] = None
    country_of_birth: Optional[Country] = None
    state_of_birth: Optional[State] = None
    gender: Optional[Gender] = None
    nationality: Optional[Country] = None
    manual_curp: Optional[CurpField] = None
    calculated_curp: CurpField
    validated_curp: Optional[CurpField] = None
    renapo_curp_match: bool
    renapo_full_match: bool

    class Config:
        fields = {
            'names': {'description': 'Official name from Renapo'},
            'first_surname': {'description': 'Official surname from Renapo'},
            'second_surname': {'description': 'Official surname from Renapo'},
            'country_of_birth': {'description': 'In format ISO 3166 Alpha-2'},
            'state_of_birth': {'description': 'In format ISO 3166 Alpha-2'},
            'nationality': {'description': 'In format ISO 3166 Alpha-2'},
            'manual_curp': {'description': 'curp provided in request'},
            'calculated_curp': {
                'description': 'Calculated CURP based on request data'
            },
            'validated_curp': {
                'description': 'CURP validated in Renapo, null if not exists'
            },
            'renapo_curp_match': {
                'description': 'True if CURP exists and is valid'
            },
            'renapo_full_match': {
                'description': 'True if all fields provided match the response'
                ' from RENAPO. Accents in names are ignored'
            },
        }
        schema_extra = {
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
        }

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
        manual_curp: Optional[CurpField] = None,
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
        return cast(
            'CurpValidation',
            cls._create(session=session, **req.dict()),
        )
