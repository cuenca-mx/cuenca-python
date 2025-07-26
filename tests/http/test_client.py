import datetime as dt

import pytest
from pytest_httpx import HTTPXMock
from cuenca_validations.errors import (
    NoPasswordFoundError,
    UserNotLoggedInError,
)
from freezegun import freeze_time

from cuenca.exc import CuencaResponseException
from cuenca.http.client import Session
from cuenca.resources import Card, Transfer, UserCredential, UserLogin


@pytest.mark.vcr
def test_invalid_auth():
    session = Session()
    session.configure(sandbox=False)
    with pytest.raises(CuencaResponseException) as e:
        session.post('/api_keys', dict())
    assert e.value.status_code == 401
    assert str(e.value)


@pytest.mark.usefixtures('cuenca_creds')
def test_basic_auth_configuration():
    session = Session()
    assert session.auth == session.basic_auth
    assert session.auth == ('api_key', 'secret')
    assert not session.jwt_token


@pytest.mark.vcr
@pytest.mark.usefixtures('cuenca_creds')
def test_configures_jwt():
    session = Session()
    session.configure(use_jwt=True)
    assert session.auth
    assert session.jwt_token


@pytest.mark.vcr
@pytest.mark.usefixtures('cuenca_creds')
def test_request_valid_token():
    session = Session()
    # Set date when the cassette was created otherwise will retrieve
    # an expired token
    with freeze_time(dt.date(2020, 10, 22)):
        session.configure(use_jwt=True)
        response = session.get('/api_keys')
    assert response['items']


@pytest.mark.vcr
@pytest.mark.usefixtures('cuenca_creds')
def test_request_expired_token():
    session = Session()
    session.configure(use_jwt=True)
    previous_jwt = session.jwt_token.token
    with freeze_time(dt.datetime.utcnow() + dt.timedelta(days=40)):
        response = session.get('/api_keys')
    assert response['items']
    assert session.jwt_token != previous_jwt


def test_overrides_session(httpx_mock: HTTPXMock):
    # Setup mock response
    httpx_mock.add_response(
        status_code=200,
        json={"items": []}
    )
    
    # Configure session with custom credentials
    session = Session()
    session.configure(
        api_key='USER_API_KEY', api_secret='USER_SECRET', sandbox=True
    )
    
    # Make the request
    Card.first(user_id='USER_ID', session=session)
    
    # Verify the request was made with the correct auth
    request = httpx_mock.get_request()
    assert request.headers.get("authorization", "").startswith("Basic ")
    assert request.url.params.get("user_id") == "USER_ID"


@pytest.mark.vcr
def test_no_password():
    UserLogin.create('111111')
    UserCredential.update(password=None)
    with pytest.raises(NoPasswordFoundError):
        Transfer.count()


@pytest.mark.vcr
def test_no_session():
    with pytest.raises(UserNotLoggedInError):
        Transfer.count()
