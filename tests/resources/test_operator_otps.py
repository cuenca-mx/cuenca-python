from unittest.mock import MagicMock, patch

import pytest

from cuenca import OperatorOtp
from cuenca.http.client import Session


@pytest.fixture
def session() -> Session:
    s = Session()
    s.configure('api_key', 'api_secret', sandbox=True)
    return s


@patch('cuenca.http.client.requests.Session.request')
def test_operator_otp_create(mock_request: MagicMock, session: Session):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OCWqY5cvkISJOxHyEKjAKf8w",'
        b'"expires_at":"2026-09-25T12:34:56"}'
    )

    otp = OperatorOtp.create(session=session)

    assert otp.id == 'OCWqY5cvkISJOxHyEKjAKf8w'
    assert otp.expires_at is not None

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://sandbox.cuenca.com/operator-otps'
    assert kwargs['json'] == {}


@patch('cuenca.http.client.requests.Session.request')
def test_operator_otp_create_with_active_session(
    mock_request: MagicMock, session: Session
):
    """Verify that create() works when called with an active session."""
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OCWqY5cvkISJOxHyEKjAKf8w",'
        b'"expires_at":"2026-09-25T12:34:56"}'
    )

    # Set session header (normally done by OperatorLogin.update/complete)
    session.headers['X-Cuenca-SessionId'] = 'SEWqY5cvkISJOxHyEKjAKf8w'

    otp = OperatorOtp.create(session=session)

    assert otp.id == 'OCWqY5cvkISJOxHyEKjAKf8w'
    # Verify session header is preserved
    assert session.headers['X-Cuenca-SessionId'] == 'SEWqY5cvkISJOxHyEKjAKf8w'
