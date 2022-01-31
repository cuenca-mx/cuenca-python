from typing import ClassVar

from cuenca_validations.types import EventQuery
from pydantic.dataclasses import dataclass

from .base import Event


@dataclass
class UserEvent(Event):
    _resource: ClassVar = 'user_events'
    _query_params: ClassVar = EventQuery

    user_id: str
    platform_id: str
