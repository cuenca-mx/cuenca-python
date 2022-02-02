import datetime as dt
from typing import ClassVar

from cuenca_validations.types import EventQuery, EventType
from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class IdentityEvent(Retrievable, Queryable):
    _resource: ClassVar = 'identity_events'
    _query_params: ClassVar = EventQuery

    identity_id: str
    new_model: dict
    type: EventType
    created_at: dt.datetime
