import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import AgentQuery, AgentRequest, PhoneNumber
from cuenca_validations.typing import DictStrAny
from pydantic import ConfigDict, Field

from ..http import Session, session as global_session
from .base import Creatable, Queryable


class Agent(Creatable, Queryable):
    _resource: ClassVar = 'agents'
    _query_params: ClassVar = AgentQuery

    created_at: dt.datetime
    user_id: str
    platform_id: str
    agent_verification_id: str
    session_id: str
    device_info: DictStrAny = Field(default_factory=dict)
    deactivated_at: Optional[dt.datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'AG1G6Bm0oGQOCRjTDaeFSsyA',
                'created_at': '2026-06-27T01:56:42.613781',
                'user_id': 'USMP3EPgI4T4CPFyVmXUPi8A',
                'platform_id': 'PTZbBlk__kQt-wfwzP5nwA9A',
                'agent_verification_id': 'AV7A1FLC7MSnqKcb7oAkiQxA',
                'session_id': 'SSH0M5yteyRHas-PmfT9pu9w',
                'device_info': {'client': 'cursor', 'os': 'macOS'},
            }
        }
    )

    @classmethod
    def create(
        cls,
        pairing_code: str,
        phone_number: PhoneNumber,
        device_info: Optional[DictStrAny] = None,
        *,
        session: Session = global_session,
    ) -> 'Agent':
        req = AgentRequest(
            pairing_code=pairing_code,
            phone_number=phone_number,
            device_info=device_info or {},
        )
        return cls._create(session=session, **req.model_dump())
