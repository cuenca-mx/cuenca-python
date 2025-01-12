from typing import ClassVar, cast

from pydantic import ConfigDict, SecretStr

from ..http import Session, session as global_session
from .base import Creatable


# mypy: disable-error-code=override
class LoginToken(Creatable):
    _resource: ClassVar = 'login_tokens'

    # Override the `id` field to be a `SecretStr`
    # To ensure sensitive data is not exposed in logs.
    id: SecretStr  # type: ignore

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
        return cast('LoginToken', cls._create(session=session))
