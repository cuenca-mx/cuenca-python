import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import EventType
from pydantic.dataclasses import dataclass

from .base import Creatable, Retrievable


@dataclass
class Session(Creatable, Retrievable):
    _resource: ClassVar = 'sessions'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    user_id: str
    platform_uri: str
    expires_at: dt.datetime
    policy_uri: str
    success_url: Optional[str]
    failure_url: Optional[str]
    event_type: Optional[EventType]
