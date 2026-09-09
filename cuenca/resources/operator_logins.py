from typing import Annotated, Any, ClassVar

from cuenca_validations.types import LogConfig, OperatorRole
from cuenca_validations.types.requests import OperatorLoginRequest
from pydantic import ConfigDict, model_validator

from ..http import Session, session as global_session
from .base import Creatable


class OperatorLogin(Creatable):
    """Authenticate a company operator (portal personas morales).

    Authed endpoint: ``POST /operator-login``. Use ``session_token`` as
    ``X-Cuenca-SessionId`` on subsequent requests.
    """

    _resource: ClassVar = 'operator-login'

    # Resource requires ``id``; Authed returns ``session_token`` (Session.id).
    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    session_token: Annotated[
        str, LogConfig(masked=True, unmasked_chars_length=4)
    ]
    operator_id: str
    role: OperatorRole
    legal_person_id: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'SEWqY5cvkISJOxHyEKjAKf8w',
                'session_token': 'SEWqY5cvkISJOxHyEKjAKf8w',
                'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
                'role': 'authorizer',
                'legal_person_id': 'USWqY5cvkISJOxHyEKjAKf8w',
            }
        }
    )

    @model_validator(mode='before')
    @classmethod
    def populate_id_from_session_token(cls, values: Any) -> Any:
        if isinstance(values, dict):
            token = values.get('session_token') or values.get('id')
            if token:
                values['id'] = token
                values['session_token'] = token
        return values

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        *,
        session: Session = global_session,
    ) -> 'OperatorLogin':
        req = OperatorLoginRequest(email=email, password=password)
        login = cls._create(
            session=session,
            email=str(req.email),
            password=req.password.get_secret_value(),
        )
        session.headers['X-Cuenca-SessionId'] = login.session_token
        return login
