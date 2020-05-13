import datetime as dt

import pytest

from cuenca import ApiKey
from cuenca.http import Session


@pytest.mark.vcr
def test_api_keys_create():
    api_key = ApiKey.create()
    assert api_key.id is not None
    assert api_key.secret is not None
    assert api_key.active


@pytest.mark.vcr
def test_api_keys_retrieve():
    id_key = 'PKUvRwK7imQK2JcjJV91iEzg=='
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.id == id_key
    assert api_key.secret == '********'


@pytest.mark.vcr
def test_api_key_deactivate():
    id_key = 'PKyyRnEL0XS6iHeSi2_8DDPA=='
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.active

    disabled = ApiKey.deactivate(id_key, 0)
    assert disabled.id == api_key.id
    assert disabled.deactivated_at is not None
    assert not disabled.active

    assert api_key.active
    api_key.refresh()
    assert not api_key.active


@pytest.mark.vcr
def test_api_key_roll_keys(test_client: Session):
    auth_key, auth_secret = test_client.auth
    old_keys, new_keys = ApiKey.roll(0)

    assert old_keys.id == auth_key
    assert not old_keys.active
    assert new_keys.active
    auth_key, auth_secret = test_client.auth
    assert new_keys.id == auth_key


def test_api_key_to_dict():
    created = dt.datetime.utcnow()
    api_key: ApiKey = ApiKey(
        id='12345', secret='********', created_at=created, deactivated_at=None,
    )
    api_key_dict = dict(
        id='12345',
        secret='********',
        created_at=created.isoformat(),
        deactivated_at=None,
    )

    assert api_key_dict == api_key.to_dict()
