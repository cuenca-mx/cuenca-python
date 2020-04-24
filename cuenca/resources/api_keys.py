import datetime as dt
from typing import ClassVar, Optional

from pydantic.dataclasses import dataclass

from .base import Resource


@dataclass
class ApiKey(Resource):
    _endpoint: ClassVar = '/api_keys'
    _query_params: ClassVar = {}

    id: str
    secret: str
    created_at: dt.datetime
    deactivated_at: Optional[dt.datetime]

    @property
    def active(self) -> bool:
        return (
            self.deactivated_at is None
            or self.deactivated_at >= dt.datetime.utcnow()
        )

    @classmethod
    def create(cls) -> 'ApiKey':
        resp = cls._client.post()
        return cls(**resp)

    def deactivate(self, minutes: int = 0) -> None:
        """
        deactivate an ApiKey in a certain number of minutes. If minutes is
        negative, the API will treat it the same as 0
        """
        resp = self._client.delete(self._endpoint, dict(minutes=minutes))
        self.deactivated_at = resp['deactivated_at']

    def roll(self, minutes: int = 0) -> 'ApiKey':
        """
        1. create a new ApiKey
        2. deactivate prior ApiKey in a certain number of minutes
        3. configure client with new ApiKey
        4. return new ApiKey
        """
        new = self.create()
        self.deactivate(minutes)
        self._client._api_key = new.id
        self._client._secret_key = new.secret
        return new
