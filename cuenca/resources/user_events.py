from typing import ClassVar

from .identity_events import IdentityEvent
from .users import User


class UserEvent(IdentityEvent):
    _resource: ClassVar = 'user_events'

    user_id: str
    platform_id: str

    class Config:
        schema_extra = {
            'example': {
                'id': 'UEYE4qnWs3Sm68tbgqkx_d5Q',
                'created_at': '2022-05-24T14:15:22Z',
                'identity_id': 'IDNEUInh69SuKXXmK95sROwQ',
                'type': 'created',
                'user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
                'new_model': User.schema().get('example'),
            }
        }
