import pytest

from cuenca import LoginToken, Transfer, UserLogin
from cuenca.http.client import Session


@pytest.fixture
def session():
    session = Session()
    session.configure(
        'api_key',
        'api_secret',
        sandbox=True,
    )
    return session


@pytest.mark.vcr
def test_login_token(session):
    UserLogin.create('222222', session=session)
    login_token = LoginToken.create(session=session)
    session.session.headers.pop('X-Cuenca-LoginId')
    session.configure(login_token=login_token.id)
    Transfer.count(session=session)
