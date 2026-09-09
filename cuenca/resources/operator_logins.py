from typing import Annotated, ClassVar

from cuenca_validations.types import LogConfig, OperatorRole
from cuenca_validations.types.requests import OperatorLoginRequest
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class OperatorLogin(Creatable):
    """Authenticate a company operator (portal personas morales).

    Authed endpoint: ``POST /operator-login``. Response ``id`` is the
    Session.id; use it as ``X-Cuenca-SessionId`` on subsequent requests.
    """

    _resource: ClassVar = 'operator-login'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    operator_id: str
    role: OperatorRole
    legal_person_id: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'SEWqY5cvkISJOxHyEKjAKf8w',
                'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
                'role': 'authorizer',
                'legal_person_id': 'USWqY5cvkISJOxHyEKjAKf8w',
            }
        }
    )

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
        session.headers['X-Cuenca-SessionId'] = login.id
        return login
