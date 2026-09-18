import datetime as dt
from typing import ClassVar

from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class OperatorOtpChallenge(Creatable):
    """One-shot email OTP challenge for an operator session."""

    _resource: ClassVar = 'operator-otp-challenges'

    expires_at: dt.datetime
    email_hint: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'OCWqY5cvkISJOxHyEKjAKf8w',
                'expires_at': '2026-09-18T22:10:00+00:00',
                'email_hint': 'l***@example.com',
            }
        }
    )

    @classmethod
    def create(
        cls,
        *,
        session: Session = global_session,
    ) -> 'OperatorOtpChallenge':
        return cls._create(session=session)
