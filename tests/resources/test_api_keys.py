import datetime as dt

import pytest

from cuenca import ApiKey


@pytest.mark.vcr
def test_api_keys_create():
    api_key = ApiKey.create()
    assert api_key.id is not None
    assert api_key.secret is not None
    assert api_key.active


@pytest.mark.vcr
def test_api_keys_retrieve():
    id_key = 'AKMPSxy2UeSKqU1J6spDNwqA'
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.id == id_key
    assert api_key.secret == '********'


@pytest.mark.vcr
def test_api_key_deactivate():
    api_key = ApiKey.create()
    assert api_key.active

    disabled = ApiKey.deactivate(api_key.id, 0)
    assert disabled.id == api_key.id
    assert disabled.deactivated_at is not None
    assert not disabled.active

    api_key.refresh()
    assert not api_key.active


@pytest.mark.vcr
def test_update_api_key():
    fields_to_update = dict(
        metadata=dict(info='v1.1.1'), user_id='USiBeLDwEWT_inkyE4CrRsrQ'
    )
    api_key_id = 'AKp-QELMN3Thih6AJG0Mgggg'

    updated = ApiKey.update(api_key_id, **fields_to_update)
    assert updated.user_id == fields_to_update['user_id']
    assert not hasattr(updated, 'metadata')


def test_api_key_to_dict():
    created = dt.datetime.now()
    date = created.astimezone(dt.timezone.utc).isoformat()
    api_key: ApiKey = ApiKey(
        id='12345',
        secret='********',
        created_at=created,
        deactivated_at=None,
        updated_at=date,
        user_id=None,
    )
    api_key_dict = dict(
        id='12345',
        secret='********',
        created_at=date,
        deactivated_at=None,
        updated_at=date,
        user_id=None,
    )
    assert api_key_dict == api_key.to_dict()


def test_api_key_from_dict():
    api_keys_dict = dict(
        id='123455',
        secret='*********',
        created_at=dt.datetime.utcnow(),
        deactivated_at=None,
        extra_field_1='not necessary',
        extra_field_2=12345,
        updated_at=dt.datetime.utcnow(),
        metadata=None,
        user_id=None,
    )
    api_key = ApiKey._from_dict(api_keys_dict)
    assert not hasattr(api_key, 'extra_field_1')
    assert not hasattr(api_key, 'extra_field_2')
    assert api_key.id is not None
