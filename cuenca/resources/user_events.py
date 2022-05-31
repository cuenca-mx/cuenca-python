from typing import ClassVar

from .identity_events import IdentityEvent
from .users import User


class UserEvent(IdentityEvent):
    _resource: ClassVar = 'user_events'

    user_id: str
    platform_id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "UE-123",
                "created_at": "2022-05-24T14:15:22Z",
                "identity_id": "ID-123",
                "type": "created",
                "user_id": "US-123",
                "platform_id": "PT-123",
                "new_model": User.schema().get('example'),
            }
        }
