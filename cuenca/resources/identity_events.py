from typing import ClassVar

from cuenca_validations.types import EventQuery
from pydantic.dataclasses import dataclass

from .base import Event


@dataclass
class IdentityEvent(Event):
    _resource: ClassVar = 'identity_events'
    _query_params: ClassVar = EventQuery
