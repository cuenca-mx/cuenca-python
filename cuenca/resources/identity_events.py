from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Event


@dataclass
class IdentityEvent(Event):
    _resource: ClassVar = 'identity_events'
