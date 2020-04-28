import datetime as dt
from typing import ClassVar, Optional, Tuple

from pydantic.dataclasses import dataclass

from ..http import session
from .base import Resource


@dataclass
class ApiKey(Resource):
    _endpoint: ClassVar = f'/api_keys'
    _query_params: ClassVar = set()

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

    @classmethod
    def roll(cls, minutes: int = 0) -> Tuple['ApiKey', 'ApiKey']:
        """
        1. create a new ApiKey
        2. configure client with new ApiKey
        3. deactivate prior ApiKey in a certain number of minutes
        4. return both ApiKeys
        """
        old_id = session.auth[0]
        new = cls.create()
        # have to use the new key to deactivate the old key
        session.configure(new.id, new.secret)
        old = cls.deactivate(old_id, minutes)
        return old, new

    @classmethod
    def deactivate(cls, api_key_id: str, minutes: int = 0) -> 'ApiKey':
        """
        deactivate an ApiKey in a certain number of minutes. If minutes is
        negative, the API will treat it the same as 0. You can't deactivate
        the same key with which the client is configured, since that'd risk
        locking you out. The deactivated key is returned so that you have the
        exact deactivated_at time.
        """
        url = cls._endpoint + f'/{api_key_id}'
        resp = session.delete(url, dict(minutes=minutes))
        return cls(**resp)
