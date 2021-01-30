import datetime as dt
from typing import ClassVar, List, Optional, Tuple, cast

from cuenca_validations.types import ApiKeyQuery, ApiKeyUpdateRequest
from pydantic.dataclasses import dataclass

from ..http import session
from .base import Creatable, Queryable, Retrievable, Updateable


@dataclass
class ApiKey(Creatable, Queryable, Retrievable, Updateable):
    _resource: ClassVar = 'api_keys'
    _query_params: ClassVar = ApiKeyQuery

    secret: str
    deactivated_at: Optional[dt.datetime]
    user_id: Optional[str]
    metadata: Optional[str]

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

    @classmethod
    def update(
        cls,
        api_key_id: str,
        metadata: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> 'ApiKey':
        """
        If the current user has enough permissions, it associates an ApiKey to
        the `user_id` or updates the correspoding metadata
        """
        req = ApiKeyUpdateRequest(metadata=metadata, user_id=user_id)
        resp = cls._update(api_key_id, **req.dict(exclude_none=True))
        return cast('ApiKey', resp)

    @classmethod
    def validate(cls, permissions: List[str]) -> Tuple[str, List[str]]:
        """
        User this method to validate if your credentials have access to a set
        of permissions.

        Parameters:
        permissions (List[str]): The cuenca URL's to be validated

        Returns:
        str: The user_id associated to the required permissions, None if it
              applies to everyone
        List[str]: The subset of `permissions` approved, an empty list if
        nothing was approved
        """
        resp = session.get('/authorizations', dict(actions=permissions))

        api_key = cast('ApiKey', resp['api_key'])

        # Most URL's will have the format cuenca://ENTITY/{user_id}/RESOURCE
        # We replace the {user_id} here for the current user_id or *, so we
        # canmake an exact match.
        authorized_permissions = []
        user_id = None
        for permission in permissions:
            if permission.replace('{user_id}', api_key.user_id) in resp['allow']:
                user_id = api_key.user_id
            elif permission.replace('{user_id}', '*') in resp['allow']:
                user_id = None
            else:
                continue
            authorized_permissions.append(permission)

        return user_id, authorized_permissions
