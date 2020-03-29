from dataclasses import dataclass
from typing import ClassVar

from .base import Resource


@dataclass
class ApiKey(Resource):
    _endpoint: ClassVar[str] = '/api_keys'

    id: str
    secret: str

    @classmethod
    def create(cls) -> 'ApiKey':
        resp = cls._client.post()
