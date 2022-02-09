import pytest

from cuenca.resources import CurpValidation


@pytest.mark.vcr
def test_curp_validations_create(curp_validation_request) -> None:
    curp_validation = CurpValidation.create(**curp_validation_request)
    assert curp_validation.id is not None
    assert curp_validation.renapo_curp_match


@pytest.mark.vcr
def test_curp_validations_retrieve():
    curp_validation_id = 'CVhY5Pi6yBQJO22p1lg-_EPw'
    curp_validation = CurpValidation.retrieve(curp_validation_id)
    assert curp_validation.id == curp_validation_id
