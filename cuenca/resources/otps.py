from typing import ClassVar, cast

from ..http import Session, session as global_session
from .base import Creatable


class Otp(Creatable):
    _resource: ClassVar = 'otps'
    secret: str

    class Config:
        schema_extra = {
            'example': {
                'id': 'OTNEUInh69SuKXXmK95sROwQ',
                'secret': 'somesecret',
            }
        }

    @classmethod
    def create(cls, session: Session = global_session) -> 'Otp':
        """
        Use this method to create a OTP seed
        """
        return cast('Otp', cls._create(session=session))
