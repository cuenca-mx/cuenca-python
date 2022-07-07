import datetime as dt

import pytest
from cuenca_validations.types import VerificationType

from cuenca import Verification
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
    assert not user.clabe
    assert user.balance == 0


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
def test_user_fetch_balance(user_request, curp_validation_request):
    user_id = 'USlen-v7UQSqqZTGVe3vQmLQ'
    user = User.retrieve(user_id)
    assert user.clabe
    assert user.balance == 10000


@pytest.mark.vcr
def test_user_identity_retrieve():
    user_id = 'USCM-zlFcNQk6ue4gZ_mTGeQ'
    user = User.retrieve(user_id)
    assert user_id == user.id
    identity = user.identity
    assert identity.id is not None


@pytest.mark.vcr
def test_user_query_by_identity_id():
    identity_id = 'IDzqdGEBX_SMScteGcRDNtOg'
    user = User.first(identity_uri=identity_id)
    assert identity_id in user.identity_uri


@pytest.mark.vcr
def test_user_query_all_identity_id():
    identity_id = 'IDzqdGEBX_SMScteGcRDNtOg'
    users = [user for user in User.all(identity_uri=identity_id)]
    assert len(users) == 2
    assert users[0].id != users[1].id
    assert users[0].identity_uri == users[1].identity_uri


@pytest.mark.vcr
def test_user_update_user_email_from_verification():
    user_id = 'USV6ONckmjQNOM9p3_bRMyxg'
    ver = Verification.create(
        recipient='mail@cuenca.com',
        type=VerificationType.email,
        platform_id='PL01',
    )
    user = User.update(user_id, email_verification_id=ver.id)
    assert user.to_dict()['email_address'] == ver.recipient


@pytest.mark.vcr
def test_user_beneficiaries_update():
    user_id = 'USw182B9fVTxK3J1A2ElKV7g'
    request = dict(
        beneficiaries=[
            dict(
                name='Pedro Pérez',
                birth_date=dt.date(2020, 1, 1),
                phone_number='+525555555555',
                user_relationship='brother',
                percentage=50,
            ),
            dict(
                name='José Pérez',
                birth_date=dt.date(2020, 1, 2),
                phone_number='+525544444444',
                user_relationship='brother',
                percentage=50,
            ),
        ]
    )
    user = User.update(user_id, **request)
    assert all(item in user.to_dict().keys() for item in request.keys())
