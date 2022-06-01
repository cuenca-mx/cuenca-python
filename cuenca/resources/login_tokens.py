from typing import ClassVar, cast

from ..http import Session, session as global_session
from .base import Creatable


class LoginToken(Creatable):
    _resource: ClassVar = 'login_tokens'

    class Config:
        schema_extra = {'example': {'id': 'LTNEUInh69SuKXXmK95sROwQ'}}

    @classmethod
    def create(cls, session: Session = global_session) -> 'LoginToken':
        """
        Use this method to create a token that will last for 7 days
        Make sure to store this token in a safe place
        :return: Token that you can use in cuenca.configure
        """
        return cast('LoginToken', cls._create(session=session))
