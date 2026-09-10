import datetime as dt
from unittest.mock import MagicMock, patch

import pytest

from cuenca import EmailOtp
from cuenca.http.client import Session


@pytest.fixture
def session() -> Session:
    s = Session()
    s.configure('api_key', 'api_secret', sandbox=True)
    return s


@patch('cuenca.http.client.requests.Session.request')
def test_email_otp_create(mock_request: MagicMock, session: Session):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"EOxxxxxxxxxxxxxxxxxxxxxx",'
        b'"owner_id":"SSxxxxxxxxxxxxxxxxxxxxxx",'
        b'"expires_at":"2026-09-09T18:00:00"}'
    )

    email_otp = EmailOtp.create(session=session)

    assert email_otp.id == 'EOxxxxxxxxxxxxxxxxxxxxxx'
    assert email_otp.owner_id == 'SSxxxxxxxxxxxxxxxxxxxxxx'
    assert email_otp.expires_at == dt.datetime(2026, 9, 9, 18, 0, 0)

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://sandbox.cuenca.com/email_otps'
    assert kwargs['json'] == {}
