import pytest

from cuenca.resources import CurpValidation, Identity


@pytest.mark.vcr
def test_identity_retrieve(curp_validation_request):
    # creating a curp_validation automatically creates the identity
    curp_validation = CurpValidation.create(**curp_validation_request)
    assert curp_validation.renapo_curp_match
    # querying the identity
    identity = Identity.one(curp=curp_validation.calculated_curp)
    assert identity.id is not None
