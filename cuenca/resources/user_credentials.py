import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import (
    UserCredentialRequest,
    UserCredentialUpdateRequest,
)

from ..http import Session, session as global_session
from .base import Creatable, Updateable


class UserCredential(Creatable, Updateable):
    _resource: ClassVar = 'user_credentials'

    is_active: bool
    created_at: dt.datetime

    @classmethod
    def create(
        cls,
        password: str,
        user_id: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'UserCredential':
        req = UserCredentialRequest(password=password, user_id=user_id)
        return cast(
            'UserCredential', cls._create(**req.dict(), session=session)
        )

    @classmethod
    def update(
        cls,
        user_id: str = 'me',
        is_active: Optional[bool] = None,
        password: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'UserCredential':
        req = UserCredentialUpdateRequest(
            is_active=is_active,
            password=password,
        )
        return cast(
            'UserCredential',
            cls._update(id=user_id, **req.dict(), session=session),
        )
