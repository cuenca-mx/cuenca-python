import pytest

from cuenca import LoginToken, Otp, UserLogin
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
def test_otps(session):
    UserLogin.create('111111', session=session)
    login_token = LoginToken.create(session=session)
    session.headers.pop(
        'X-Cuenca-LoginId',
    )
    session.configure(login_token=login_token.id)
    otp = Otp.create()
    assert otp
    assert isinstance(otp.secret, str)
