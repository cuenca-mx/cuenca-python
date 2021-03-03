import pytest

from cuenca import UserLogin
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
def test_valid_login(session: Session):
    login = UserLogin.create('222222', session=session)
    assert login.success
    assert login.last_login_at is not None
    assert login.id is not None
    assert session.session.headers['X-Cuenca-LoginId'] == login.id


@pytest.mark.vcr
def test_invalid_login(session: Session):
    login = UserLogin.create('111111', session=session)
    assert not login.success
    assert login.last_login_at is None
    assert login.id is not None
    assert 'X-Cuenca-LoginId' not in session.session.headers


@pytest.mark.vcr
def test_logout(session: Session):
    UserLogin.create('222222', session=session)
    UserLogin.logout(session=session)
    assert 'X-Cuenca-LoginId' not in session.session.headers
