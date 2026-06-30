import datetime as dt
from typing import ClassVar

from cuenca_validations.types.identities import PhoneNumber
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class AgentVerification(Creatable):
    _resource: ClassVar = 'agent_verifications'

    created_at: dt.datetime
    user_id: str
    platform_id: str
    phone_number: PhoneNumber
    pairing_code: str
    deactivated_at: dt.datetime

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'AVjTtPH1mhT65GEgOeomJ4DQ',
                'created_at': '2026-06-25T22:50:08.495768',
                'user_id': 'USMP3EPgI4T4CPFyVmXUPi8A',
                'platform_id': 'PTZbBlk__kQt-wfwzP5nwA9A',
                'phone_number': '+525512345678',
                'pairing_code': 'OJC37W',
                'deactivated_at': '2026-06-25T22:55:08.495779',
            }
        }
    )

    @classmethod
    def create(cls, session: Session = global_session) -> 'AgentVerification':
        return cls._create(session=session)
