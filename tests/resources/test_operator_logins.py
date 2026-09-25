from unittest.mock import MagicMock, patch

import pytest
from cuenca_validations.types import OperatorRole

from cuenca import OperatorLogin
from cuenca.http.client import Session


@pytest.fixture
def session() -> Session:
    s = Session()
    s.configure('api_key', 'api_secret', sandbox=True)
    return s


@patch('cuenca.http.client.requests.Session.request')
def test_operator_login_create(mock_request: MagicMock, session: Session):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"OLWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"expires_at":"2026-09-21T20:15:22",'
        b'"email_hint":"ma****@aceros.com"}'
    )

    login = OperatorLogin.create(
        'Maria+Tag@Aceros.com',
        'supersecret',
        session=session,
    )

    assert login.id == 'OLWqY5cvkISJOxHyEKjAKf8w'
    assert login.operator_id == 'OPWqY5cvkISJOxHyEKjAKf8w'
    assert login.email_hint == 'ma****@aceros.com'
    assert login.expires_at is not None
    assert login.role is None
    assert login.legal_person_id is None
    assert 'X-Cuenca-SessionId' not in session.headers

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://sandbox.cuenca.com/operator-logins'
    assert kwargs['json'] == {
        'email': 'maria@aceros.com',
        'password': 'supersecret',
    }


@patch('cuenca.http.client.requests.Session.request')
def test_operator_login_update(mock_request: MagicMock, session: Session):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"SEWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"role":"operator",'
        b'"legal_person_id":"USWqY5cvkISJOxHyEKjAKf8w"}'
    )

    login = OperatorLogin.update(
        'OLWqY5cvkISJOxHyEKjAKf8w',
        '123456',
        session=session,
    )

    assert login.id == 'SEWqY5cvkISJOxHyEKjAKf8w'
    assert login.operator_id == 'OPWqY5cvkISJOxHyEKjAKf8w'
    assert login.role == OperatorRole.operator
    assert login.legal_person_id == 'USWqY5cvkISJOxHyEKjAKf8w'
    assert session.headers['X-Cuenca-SessionId'] == login.id
    assert 'X-Cuenca-LoginId' not in session.headers

    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'patch'
    assert kwargs['url'] == (
        'https://sandbox.cuenca.com/operator-logins/'
        'OLWqY5cvkISJOxHyEKjAKf8w'
    )
    assert kwargs['json'] == {'code': '123456'}


@patch('cuenca.http.client.requests.Session.request')
def test_operator_login_complete_alias(
    mock_request: MagicMock, session: Session
):
    mock_request.return_value.ok = True
    mock_request.return_value.content = (
        b'{"id":"SEWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"role":"authorizer",'
        b'"legal_person_id":"USWqY5cvkISJOxHyEKjAKf8w"}'
    )

    login = OperatorLogin.complete(
        'OLWqY5cvkISJOxHyEKjAKf8w',
        '654321',
        session=session,
    )

    assert login.role == OperatorRole.authorizer
    assert session.headers['X-Cuenca-SessionId'] == login.id
