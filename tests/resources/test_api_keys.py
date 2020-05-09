import pytest

from cuenca import ApiKey
from cuenca.http import Session


@pytest.mark.skip('oaxaca.sandbox is not ready')
@pytest.mark.usefixtures('test_client')
def test_api_keys_create():
    api_key = ApiKey.create()
    assert api_key.id is not None
    assert api_key.secret is not None
    assert api_key.active


@pytest.mark.skip('oaxaca.sandbox is not ready')
@pytest.mark.usefixtures('test_client')
def test_api_keys_retrieve():
    id_key = 'PKUvRwK7imQK2JcjJV91iEzg=='
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.id == id_key
    assert api_key.secret == '********'


@pytest.mark.skip('oaxaca.sandbox is not ready')
@pytest.mark.usefixtures('test_client')
def test_api_key_deactivate():
    id_key = 'PK7Xylj0o2S1mvWUie36NWSA=='
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.active

    disabled = ApiKey.deactivate(id_key, 0)
    assert disabled.id == api_key.id
    assert disabled.deactivated_at is not None
    assert not disabled.active

    assert api_key.active
    api_key.refresh()
    assert not api_key.active


@pytest.mark.skip('oaxaca.sandbox is not ready')
def test_api_key_roll_keys(test_client: Session):
    auth_key, auth_secret = test_client.auth
    old_keys, new_keys = ApiKey.roll(0)

    assert old_keys.id == auth_key
    assert not old_keys.active
    assert new_keys.active
    auth_key, auth_secret = test_client.auth
    assert new_keys.id == auth_key
