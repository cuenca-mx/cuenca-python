import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class UserEvent(Retrievable, Queryable):
    _resource: ClassVar = 'user_events'

    id: str
    user_id: str
    previous_model: dict
    new_model: dict
    event_type: str  # crear enum
    created_at: dt.datetime
