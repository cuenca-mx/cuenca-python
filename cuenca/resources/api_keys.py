import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional

from .base import Resource


@dataclass
class ApiKey(Resource):
    _endpoint: ClassVar[str] = '/api_keys'

    id: str
    secret: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime]

    @classmethod
    def create(cls) -> 'ApiKey':
        resp = cls._client.post()
        return cls(**resp)

    @property
    def active(self) -> bool:
        return (
            self.deactivated_at is None
            or self.deactivated_at >= dt.datetime.utcnow()
        )
