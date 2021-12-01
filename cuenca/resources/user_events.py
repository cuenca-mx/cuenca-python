from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Event


@dataclass
class UserEvent(Event):
    _resource: ClassVar = 'user_events'
