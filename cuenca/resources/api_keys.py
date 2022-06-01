import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import ApiKeyQuery, ApiKeyUpdateRequest

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable


class ApiKey(Creatable, Queryable, Retrievable, Updateable):
    _resource: ClassVar = 'api_keys'
    _query_params: ClassVar = ApiKeyQuery

    secret: str
    deactivated_at: Optional[dt.datetime]
    user_id: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'id': 'AKNEUInh69SuKXXmK95sROwQ',
                'updated_at': '2021-08-24T14:15:22Z',
                'created_at': '2021-08-24T14:15:22Z',
                'secret': 'super-secret-random-string',
                'deactivated_at': None,
                'user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
            }
        }

    @property
    def active(self) -> bool:
        return (
            self.deactivated_at is None
            or self.deactivated_at > dt.datetime.utcnow()
        )

    @classmethod
    def create(cls, *, session: Session = global_session) -> 'ApiKey':
        return cast('ApiKey', cls._create(session=session))

    @classmethod
    def deactivate(
        cls,
        api_key_id: str,
        minutes: int = 0,
        *,
        session: Session = global_session,
    ) -> 'ApiKey':
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

    @classmethod
    def update(
        cls,
        api_key_id: str,
        metadata: Optional[dict] = None,
        user_id: Optional[str] = None,
        platform_id: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'ApiKey':
        """
        If the current user has enough permissions, it associates an ApiKey to
        the `user_id` or updates the correspoding metadata
        """
        req = ApiKeyUpdateRequest(
            metadata=metadata, user_id=user_id, platform_id=platform_id
        )
        resp = cls._update(api_key_id, **req.dict(), session=session)
        return cast('ApiKey', resp)
