import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import ApiKeyQuery
from pydantic.dataclasses import dataclass

from ..http import session
from .base import Creatable, Queryable, Retrievable


@dataclass
class ApiKey(Creatable, Queryable, Retrievable):
    _resource: ClassVar = 'api_keys'
    _query_params: ClassVar = ApiKeyQuery

    secret: str
    deactivated_at: Optional[dt.datetime]

    @property
    def active(self) -> bool:
        return (
            self.deactivated_at is None
            or self.deactivated_at > dt.datetime.utcnow()
        )

    @classmethod
    def create(cls) -> 'ApiKey':
        return cast('ApiKey', cls._create())

    @classmethod
    def deactivate(cls, api_key_id: str, minutes: int = 0) -> 'ApiKey':
        """
        deactivate an ApiKey in a certain number of minutes. If minutes is
        negative, the API will treat it the same as 0. You can't deactivate
        the same key with which the client is configured, since that'd risk
        locking you out. The deactivated key is returned so that you have the
        exact deactivated_at time.
        """
        url = cls._resource + f'/{api_key_id}'
        resp = session.delete(url, dict(minutes=minutes))
        return cast('ApiKey', cls._from_dict(resp))
