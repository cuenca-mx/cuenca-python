import datetime as dt
from typing import Annotated, ClassVar, Optional

from cuenca_validations.types import LogConfig, OperatorRole
from cuenca_validations.types.requests import (
    OperatorLoginRequest,
    OperatorLoginUpdateRequest,
)
from pydantic import BaseModel, ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class OperatorLoginResponse(BaseModel):
    """POST /operator-logins response (OTP challenge pending).

    Requires cuenca-validations >= 2.1.48.
    """

    id: str
    operator_id: str
    expires_at: dt.datetime
    email_hint: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'OLWqY5cvkISJOxHyEKjAKf8w',
                'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
                'expires_at': '2026-09-21T20:15:22Z',
                'email_hint': 'ma****@aceros.com',
            }
        },
    )


class OperatorLoginSessionResponse(BaseModel):
    """PATCH /operator-logins/{id} response (session after OTP).

    Requires cuenca-validations >= 2.1.48.
    """

    id: str
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
        },
    )


class OperatorLogin(Creatable):
    """Two-step operator portal login (Cuenca Empresas).

    ``POST /operator-logins`` validates email/password and emails an OTP.
    ``PATCH /operator-logins/{id}`` verifies the OTP and returns a Session.

    Both routes are auth_exempt. Set ``X-Cuenca-SessionId`` only after
    ``update`` / ``complete`` (response ``id`` is ``SE*``).
    """

    _resource: ClassVar = 'operator-logins'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    operator_id: str
    # Present after create (OTP challenge)
    expires_at: Optional[dt.datetime] = None
    email_hint: Optional[str] = None
    # Present after update/complete (session)
    role: Optional[OperatorRole] = None
    legal_person_id: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'OLWqY5cvkISJOxHyEKjAKf8w',
                'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
                'expires_at': '2026-09-21T20:15:22Z',
                'email_hint': 'ma****@aceros.com',
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
        return cls._create(
            session=session,
            email=str(req.email),
            password=req.password.get_secret_value(),
        )

    @classmethod
    def update(
        cls,
        login_id: str,
        code: str,
        *,
        session: Session = global_session,
    ) -> 'OperatorLogin':
        req = OperatorLoginUpdateRequest(code=code)
        resp = session.patch(f'/{cls._resource}/{login_id}', req.model_dump())
        login = cls(**resp)
        session.headers['X-Cuenca-SessionId'] = login.id
        return login

    @classmethod
    def complete(
        cls,
        login_id: str,
        code: str,
        *,
        session: Session = global_session,
    ) -> 'OperatorLogin':
        """Alias of ``update`` — verify OTP and create the Session."""
        return cls.update(login_id, code, session=session)
