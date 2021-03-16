import pytest
from freezegun import freeze_time

from cuenca import UserCredential, UserLogin
from cuenca.http import Session


@pytest.mark.vcr
def test_update_password():
    UserCredential.create('222222')
    UserLogin.create('222222')
    UserCredential.update(password='111111')


@pytest.mark.vcr
@freeze_time('2020-03-19')
def test_block_user():
    session = Session()
    session.configure(
        'api_key',
        'api_secret',
        sandbox=True,
        use_jwt=True,
    )
    user_credential = UserCredential.update(
        'US46cuHpEJ5xFTOceMKVqSzF', is_active=False, session=session
    )
    assert not user_credential.is_active
    user_credential = UserCredential.update(
        'US46cuHpEJ5xFTOceMKVqSzF', is_active=True, session=session
    )
    assert user_credential.is_active
