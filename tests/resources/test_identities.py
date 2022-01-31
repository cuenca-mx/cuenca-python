import pytest

from cuenca.resources import CurpValidation, Identity


@pytest.mark.vcr
@pytest.mark.skip
def test_create_identity(curp_validation_request):
    # https://sentry.io/organizations/cuenca-mx/issues/2971297839/?project=6118571&query=is%3Aunresolved
    # creating a curp_validation automatically creates the identity
    curp_validation = CurpValidation.create(curp_validation_request)
    assert curp_validation.renapo_curp_match
    # querying the identity
    identity = Identity.one(curp=curp_validation.calculated_curp)
    assert identity.id is not None
