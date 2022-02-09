import pytest

from cuenca.resources import CurpValidation, User


@pytest.mark.vcr
def test_user_create(user_request, curp_validation_request):
    # we need to create the curp validation first
    curp_validation = CurpValidation.create(**curp_validation_request)
    assert curp_validation.renapo_curp_match
    # creating the user
    user = User.create(**user_request)
    assert user.id is not None
    assert user.level == 0


@pytest.mark.vcr
def test_user_query():
    user = User.one(email_address='jose@test.com')
    assert user.id is not None


@pytest.mark.vcr
def test_user_update():
    user_id = 'USCM-zlFcNQk6ue4gZ_mTGeQ'
    changes = dict(
        profession='programmer',
        phone_number='+525555555555',
        govt_id=dict(
            type='ine',
            uri_front='cuenca.com',
            uri_back='cuenca.com',
            is_mx=True,
        ),
    )
    user = User.update(user_id, **changes)
    assert all(item in user.to_dict().keys() for item in changes.keys())


@pytest.mark.vcr
def test_user_identity_retrieve():
    user_id = 'USCM-zlFcNQk6ue4gZ_mTGeQ'
    user = User.retrieve(user_id)
    assert user_id == user.id
    identity = user.identity
    assert identity.id is not None
