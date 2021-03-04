import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import (
    UserCredentialRequest,
    UserCredentialUpdateRequest,
)
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Updateable


@dataclass
class UserCredential(Creatable, Updateable):
    _resource: ClassVar = 'user_credentials'

    is_active: bool
    created_at: dt.datetime

    @classmethod
    def create(
        cls, password: str, *, session: Session = global_session
    ) -> 'UserCredential':
        req = UserCredentialRequest(password=password)
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
