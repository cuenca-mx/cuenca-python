from typing import Annotated, ClassVar

from cuenca_validations.types import LogConfig
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class LoginToken(Creatable):
    _resource: ClassVar = 'login_tokens'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]

    model_config = ConfigDict(
        json_schema_extra={'example': {'id': 'LTNEUInh69SuKXXmK95sROwQ'}}
    )

    @classmethod
    def create(cls, session: Session = global_session) -> 'LoginToken':
        """
        Use this method to create a token that will last for 7 days
        Make sure to store this token in a safe place
        :return: Token that you can use in cuenca.configure
        """
        return cls._create(session=session)
