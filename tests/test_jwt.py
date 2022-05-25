import datetime as dt
from unittest.mock import MagicMock

import pytest

from cuenca.exc import MalformedJwtToken
from cuenca.jwt import Jwt

TEST_TOKEN = (
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6'
    'IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDYyNjI0MDB9.gbrIYP6Q0yf2'
    'V3GEgxnzO5fNHKgHPqaIzZ-cjvFlnik'
)


@pytest.mark.parametrize(
    'expires_at, should_be_expired',
    [
        (dt.datetime.utcnow() + dt.timedelta(days=-1), True),
        (dt.datetime.utcnow() + dt.timedelta(days=1), False),
    ],
)
def test_expired(expires_at: dt.datetime, should_be_expired: bool):
    jwt = Jwt(expires_at=expires_at, token='_')
    assert jwt.is_expired == should_be_expired


def test_get_expiration_date():
    assert Jwt.get_expiration_date(TEST_TOKEN) == dt.datetime(2020, 11, 25)


def test_invalid_token():
    test_token = 'INVALID'
    with pytest.raises(MalformedJwtToken):
        Jwt.get_expiration_date(test_token)


def test_create_token():
    session = MagicMock()
    session.post.return_value = dict(token=TEST_TOKEN)
    jwt = Jwt.create(session)
    assert jwt.expires_at == dt.datetime(2020, 11, 25)
    assert jwt.token == TEST_TOKEN
