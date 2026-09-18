import datetime as dt
from unittest.mock import MagicMock, patch

import pytest

from cuenca import OperatorOtpChallenge
from cuenca.http.client import Session


@pytest.fixture
def session() -> Session:
    configured_session = Session()
    configured_session.configure('api_key', 'api_secret', sandbox=True)
    return configured_session


@patch('cuenca.http.client.requests.Session.request')
def test_operator_otp_challenge_create(
    mock_request: MagicMock,
    session: Session,
):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OCWqY5cvkISJOxHyEKjAKf8w",'
        b'"expires_at":"2026-09-18T22:10:00+00:00",'
        b'"email_hint":"l***@example.com"}'
    )

    challenge = OperatorOtpChallenge.create(session=session)

    assert challenge.id == 'OCWqY5cvkISJOxHyEKjAKf8w'
    assert challenge.expires_at == dt.datetime(
        2026,
        9,
        18,
        22,
        10,
        tzinfo=dt.timezone.utc,
    )
    assert challenge.email_hint == 'l***@example.com'

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == (
        'https://sandbox.cuenca.com/operator-otp-challenges'
    )
    assert kwargs['json'] == {}
