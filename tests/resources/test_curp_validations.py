import pytest

from cuenca.resources import CurpValidation


@pytest.mark.vcr
def test_create_curp_validations(curp_validation_request) -> None:
    curp_validation = CurpValidation.create(**curp_validation_request)
    assert curp_validation.id is not None
    assert curp_validation.renapo_curp_match


@pytest.mark.vcr
def test_retrieve_curp_validations():
    curp_validation_id = 'CVKTTRnlVtTVaAh7bMfV4P0Q'
    curp_validation = CurpValidation.retrieve(curp_validation_id)
    assert curp_validation.id == curp_validation_id
