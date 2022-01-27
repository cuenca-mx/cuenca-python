import datetime as dt
from typing import Dict

import pytest
from cuenca_validations.types import CurpValidationRequest, Gender, State

from cuenca.resources import CurpValidation


@pytest.fixture
def curp_validation_request() -> Dict:
    curp_validation = dict(
        names='José',
        first_surname='López',
        second_surname='Pérez',
        date_of_birth=dt.date(1992, 6, 4).isoformat(),
        state_of_birth=State.DF.value,
        country_of_birth='MX',
        gender=Gender.male,
    )
    return CurpValidationRequest(**curp_validation)


@pytest.fixture
def test_create_curp_validations(curp_validation_request) -> None:
    curp_validation = CurpValidation.create(curp_validation_request)
