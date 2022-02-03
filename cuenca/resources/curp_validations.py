import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    Country,
    CurpValidationRequest,
    Gender,
    State,
)
from cuenca_validations.types.identities import CurpField
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


@dataclass
class CurpValidation(Creatable, Retrievable):
    _resource: ClassVar = 'curp_validations'

    created_at: dt.datetime
    names: str
    first_surname: str
    second_surname: Optional[str]
    date_of_birth: dt.date
    country_of_birth: Country
    state_of_birth: State
    gender: Gender
    nationality: Optional[Country]
    manual_curp: Optional[CurpField]
    calculated_curp: CurpField
    validated_curp: Optional[CurpField]
    renapo_curp_match: bool
    renapo_full_match: bool

    @classmethod
    def create(
        cls,
        names: str,
        first_surname: str,
        date_of_birth: dt.date,
        country_of_birth: str,
        state_of_birth: State,
        gender: Gender,
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
