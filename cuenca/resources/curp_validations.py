import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import CurpValidationRequest, Gender, State
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


@dataclass
class CurpValidation(Creatable, Retrievable):
    _resource: ClassVar = 'curp_validations'

    id: str
    names: str
    first_surname: str
    second_surname: Optional[str]
    date_of_birth: dt.date
    country_of_birth: Optional[str]
    state_of_birth: State
    gender: Gender
    nationality: Optional[str]
    manual_curp: Optional[str]
    calculated_curp: str
    validated_curp: Optional[str]
    renapo_curp_match: Optional[str]
    renapo_full_match: Optional[str]

    @classmethod
    def create(
        cls,
        curp_validation_request: CurpValidationRequest,
        *,
        session: Session = global_session,
    ) -> 'CurpValidation':
        return cast(
            'CurpValidation',
            cls._create(session=session, **curp_validation_request.dict()),
        )
