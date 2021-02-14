from typing import ClassVar, cast

from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable

from ..exc import CuencaException
from ..http import Session, session as global_session


@dataclass
class LoginToken(Creatable):
    _resource: ClassVar = 'login_tokens'

    login_token: str

    @classmethod
    def create(cls, session: Session = global_session) -> 'LoginToken':
        """
        Use this method to create a token that will last for 7 days
        Make sure to store this token in a safe place

        :return: Token that you can use in cuenca.configure
        """
        if not session.login:
            raise CuencaException('You have to login first')
        return cast('LoginToken', cls._create(session=session))
