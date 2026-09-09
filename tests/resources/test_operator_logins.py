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
        b'{"session_token":"SEWqY5cvkISJOxHyEKjAKf8w",'
        b'"operator_id":"OPWqY5cvkISJOxHyEKjAKf8w",'
        b'"role":"operator",'
        b'"legal_person_id":"USWqY5cvkISJOxHyEKjAKf8w"}'
    )

    login = OperatorLogin.create(
        'Maria+Tag@Aceros.com',
        'supersecret',
        session=session,
    )

    assert login.session_token == 'SEWqY5cvkISJOxHyEKjAKf8w'
    assert login.id == login.session_token
    assert login.operator_id == 'OPWqY5cvkISJOxHyEKjAKf8w'
    assert login.role == OperatorRole.operator
    assert login.legal_person_id == 'USWqY5cvkISJOxHyEKjAKf8w'
    assert session.headers['X-Cuenca-SessionId'] == login.session_token
    assert 'X-Cuenca-LoginId' not in session.headers

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs['method'] == 'post'
    assert kwargs['url'] == 'https://sandbox.cuenca.com/operator-login'
    assert kwargs['json'] == {
        'email': 'maria@aceros.com',
        'password': 'supersecret',
    }
