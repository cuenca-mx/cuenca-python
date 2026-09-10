import datetime as dt
from typing import ClassVar, Optional

from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class EmailOtp(Creatable):
    _resource: ClassVar = 'email_otps'
    owner_id: Optional[str] = None
    expires_at: Optional[dt.datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'EOxxxxxxxxxxxxxxxxxxxxxx',
                'owner_id': 'SSxxxxxxxxxxxxxxxxxxxxxx',
                'expires_at': '2026-09-09T18:00:00',
            }
        }
    )

    @classmethod
    def create(cls, session: Session = global_session) -> 'EmailOtp':
        """Request a one-shot email OTP for the current Session."""
        return cls._create(session=session)
