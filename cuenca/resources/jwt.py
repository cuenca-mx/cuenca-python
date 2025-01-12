from typing import ClassVar

from pydantic import SecretStr

from .base import Creatable


class Jwt(Creatable):
    _resource: ClassVar = 'jwt'

    token: SecretStr
    api_key: str
