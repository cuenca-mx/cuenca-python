from typing import ClassVar

from pydantic.dataclasses import dataclass

from .identity_events import IdentityEvent


@dataclass
class UserEvent(IdentityEvent):
    _resource: ClassVar = 'user_events'

    user_id: str
    platform_id: str
