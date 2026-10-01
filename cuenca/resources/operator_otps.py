import datetime as dt
from typing import Annotated, ClassVar

from cuenca_validations.types import LogConfig
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class OperatorOtp(Creatable):
    """Email OTP challenge for authorized actions in operator portal.

    Requires an active operator Session (from completed OperatorLogin).
    ``POST /operator-otps`` creates an email OTP challenge and emails
    a 6-digit code to the operator. Use the code with the ``X-Cuenca-OTP``
    header in protected endpoints.

    Expires in 5 minutes.
    """

    _resource: ClassVar = 'operator-otps'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    expires_at: dt.datetime

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'OCWqY5cvkISJOxHyEKjAKf8w',
                'expires_at': '2026-09-25T12:34:56Z',
            }
        }
    )

    @classmethod
    def create(cls, *, session: Session = global_session) -> 'OperatorOtp':
        """Create an email OTP challenge for the current operator Session.

        Requires: X-Cuenca-SessionId header set (from OperatorLogin.update).
        A 6-digit code is sent via email to the operator's registered address.

        Returns: OperatorOtp with challenge id and expiration timestamp.
        """
        return cls._create(session=session)
