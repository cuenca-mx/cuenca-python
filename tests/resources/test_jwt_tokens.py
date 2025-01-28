import pytest

from cuenca import JwtToken, LoginToken, UserLogin
from cuenca.http.client import Session


@pytest.fixture(scope='function')
def session():
    session = Session()
    session.configure(
        'api_key',
        'api_secret',
        sandbox=True,
    )
    return session


@pytest.mark.vcr
def test_jwt_tokens(session):
    UserLogin.create('111111', session=session)
    login_token = LoginToken.create(session=session)
    session.headers.pop(
        'X-Cuenca-LoginId',
    )
    session.configure(login_token=login_token.id)
    jwt_token = JwtToken.create(session=session)
    assert jwt_token
    assert isinstance(jwt_token.token, str)
