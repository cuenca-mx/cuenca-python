import datetime as dt
from typing import Annotated, ClassVar, Optional, Union

from cuenca_validations.types import LogConfig, OperatorRole
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class OperatorToken(Creatable):
    """One-time invitation token to set an operator password.

    ``POST /operator_tokens`` creates the invite in Authed and returns the
    plaintext ``token`` once (for the magic-link email). Does not send email.
    """

    _resource: ClassVar = 'operator_tokens'

    id: str
    operator_id: str
    email: str
    legal_person_id: str
    role: Union[OperatorRole, str]
    token: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    created_at: Optional[dt.datetime] = None
    expires_at: Optional[dt.datetime] = None
    used_at: Optional[dt.datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'OTWqY5cvkISJOxHyEKjAKf8w',
                'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w',
                'email': 'maria.lopez@aceros.com',
                'legal_person_id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'role': 'operator',
                'token': 'plaintext-invite-secret',
                'expires_at': '2026-09-24T21:30:56Z',
            }
        }
    )

    @classmethod
    def create(
        cls,
        operator_id: str,
        email: str,
        legal_person_id: str,
        role: Union[OperatorRole, str],
        *,
        session: Session = global_session,
    ) -> 'OperatorToken':
        role_value = role.value if isinstance(role, OperatorRole) else role
        return cls._create(
            session=session,
            operator_id=operator_id,
            email=email,
            legal_person_id=legal_person_id,
            role=role_value,
        )
