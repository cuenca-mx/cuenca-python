from unittest.mock import MagicMock, patch

import pytest
from cuenca_validations.types import OperatorRole

from cuenca import OperatorToken
from cuenca.http.client import Session


@pytest.fixture
def session() -> Session:
    s = Session()
    s.configure('api_key', 'api_secret', sandbox=True)
    return s


@patch('cuenca.http.client.requests.Session.request')
def test_operator_token_create(mock_request: MagicMock, session: Session):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OTWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"email":"maria.lopez@aceros.com",'
        b'"legal_person_id":"USWqY5cvkISJOxHyEKjAKf8w",'
        b'"role":"operator",'
        b'"token":"plaintext-invite-secret",'
        b'"expires_at":"2026-09-24T21:30:56"}'
    )

    token = OperatorToken.create(
        'OPWqY5cvkISJOxHyEKjAKf8w',
        'maria.lopez@aceros.com',
        'USWqY5cvkISJOxHyEKjAKf8w',
        OperatorRole.operator,
        session=session,
    )

    assert token.id == 'OTWqY5cvkISJOxHyEKjAKf8w'
    assert token.operator_id == 'OPWqY5cvkISJOxHyEKjAKf8w'
    assert token.email == 'maria.lopez@aceros.com'
    assert token.legal_person_id == 'USWqY5cvkISJOxHyEKjAKf8w'
    assert token.role == OperatorRole.operator
    assert token.token == 'plaintext-invite-secret'
    assert token.expires_at is not None

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://sandbox.cuenca.com/operator_tokens'
    assert kwargs['json'] == {
        'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
        'email': 'maria.lopez@aceros.com',
        'legal_person_id': 'USWqY5cvkISJOxHyEKjAKf8w',
        'role': 'operator',
    }


@patch('cuenca.http.client.requests.Session.request')
def test_operator_token_create_accepts_role_str(
    mock_request: MagicMock, session: Session
):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OTWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"email":"maria.lopez@aceros.com",'
        b'"legal_person_id":"USWqY5cvkISJOxHyEKjAKf8w",'
        b'"role":"authorizer",'
        b'"token":"plaintext-invite-secret"}'
    )

    token = OperatorToken.create(
        'OPWqY5cvkISJOxHyEKjAKf8w',
        'maria.lopez@aceros.com',
        'USWqY5cvkISJOxHyEKjAKf8w',
        'authorizer',
        session=session,
    )

    assert token.role == OperatorRole.authorizer
    _, kwargs = mock_request.call_args
    assert kwargs['json']['role'] == 'authorizer'
