import datetime as dt
from unittest.mock import patch
from urllib.parse import quote

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
    id_key = 'AKe2V4KrZUQ7-GTmzvjexvrw'
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.id == id_key
    assert api_key.secret == '********'


@pytest.mark.vcr
def test_api_key_deactivate():
    id_key = 'AKSMPzsvVPROyLZhkwcOtHxA'
    api_key: ApiKey = ApiKey.retrieve(id_key)
    assert api_key.active

    disabled = ApiKey.deactivate(id_key, 0)
    assert disabled.id == api_key.id
    assert disabled.deactivated_at is not None
    assert not disabled.active

    api_key.refresh()
    assert not api_key.active


@pytest.mark.vcr
def test_update_api_key():
    fields_to_update = dict(
        metadata='ANYTHING', user_id='USiBeLDwEWT_inkyE4CrRsrQ'
    )
    api_key_id = 'AKkVaALThyQ3SSFeR-qBAKiw'

    updated = ApiKey.update(api_key_id, **fields_to_update)
    assert all(
        getattr(updated, key) == value
        for key, value in fields_to_update.items()
    )

    api_key = ApiKey.retrieve(api_key_id)
    assert all(
        getattr(api_key, key) == value
        for key, value in fields_to_update.items()
    )


def test_api_key_to_dict():
    created = dt.datetime.now()
    date = created.astimezone(dt.timezone.utc).isoformat()
    api_key: ApiKey = ApiKey(
        id='12345',
        secret='********',
        created_at=created,
        deactivated_at=None,
        updated_at=date,
        metadata=None,
        user_id=None,
    )
    api_key_dict = dict(
        id='12345',
        secret='********',
        created_at=date,
        deactivated_at=None,
        updated_at=date,
        metadata=None,
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


@pytest.mark.parametrize(
    'permissions, response, result',
    [
        (['cuenca://oaxaca/{user_id}/transfers.read]'], [], (None, [])),
        (
            ['cuenca://oaxaca/{user_id}/transfers.read'],
            ['cuenca://no_oaxaca/*/transfers.read'],
            (None, []),
        ),
        (
            [
                'cuenca://oaxaca/{user_id}/transfers.read',
                'cuenca://oaxaca/{user_id}/transfers.write',
            ],
            ['cuenca://oaxaca/US12345/transfers.read'],
            ('US12345', ['cuenca://oaxaca/{user_id}/transfers.read']),
        ),
        (
            [
                'cuenca://oaxaca/{user_id}/transfers.read',
                'cuenca://oaxaca/{user_id}/transfers.write',
            ],
            ['cuenca://oaxaca/*/transfers.read'],
            (None, ['cuenca://oaxaca/{user_id}/transfers.read']),
        ),
        (
            ['cuenca://oaxaca/transfers.read'],
            ['cuenca://oaxaca/transfers.read'],
            (None, ['cuenca://oaxaca/transfers.read']),
        ),
        (
            ['cuenca://oaxaca/transfers.read'],
            ['cuenca://oaxaca/transfers.write'],
            (None, []),
        ),
    ],
)
@patch('cuenca.http.session.get')
def test_validate_not_approved(mocked_get, permissions, response, result):
    mocked_get.return_value = dict(allow=response)
    assert result == ApiKey.validate(permissions)
    quoted = quote(','.join(permissions))
    mocked_get.assert_called_once_with('/authorizations', dict(actions=quoted))
