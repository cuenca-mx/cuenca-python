import pytest
from cuenca_validations.types import VerificationStatus

from cuenca.exc import CuencaResponseException
from cuenca.resources import UserListsValidation


@pytest.mark.vcr
def test_create_user_validation_with_response():
    user_validation = UserListsValidation.create(
        curp='LOBR810330HTCPLM05',
        names='José Ramón',
        first_surname='López',
        second_surname='Beltrán',
    )
    assert user_validation.status == VerificationStatus.rejected
    assert len(user_validation.ppe_matches) == 1
    assert user_validation.ppe_matches[0]['parentesco'] == 'HIJO'


@pytest.mark.vcr
def test_create_user_validation(user_lists_request):
    user_validation = UserListsValidation.create(**user_lists_request)
    assert user_validation.status == VerificationStatus.succeeded
    assert len(user_validation.ppe_matches) == 0
    assert user_validation.id


@pytest.mark.vcr
def test_create_user_validation_invalid_inputs():
    with pytest.raises(CuencaResponseException) as exc:
        UserListsValidation.create(**dict(curp='MAVM112222HWIERN02'))
        assert exc.status_code == 403
        assert exc.json['error'] == 'There is an error with the inputs'
