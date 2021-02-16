from typing import ClassVar

from cuenca_validations.types.requests import PasswordRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable

from ..http import Session, session as global_session


@dataclass
class Password(Creatable):
    _resource: ClassVar = 'passwords'

    @classmethod
    def create(
        cls, password: str, *, session: Session = global_session
    ) -> None:
        """
        Creates a new password associated to the current api_key

        :param password:
        """
        req = PasswordRequest(password=password)
        cls._create(session=session, **req.dict())

    @classmethod
    def delete(
        cls, password: str, *, user_id: str = 'me', session: Session = global_session
    ) -> None:
        """
        Use this method to deactivate your current password

        :param password: Current password
        """
        req = PasswordRequest(password=password)
        url = f'{cls._resource}/{user_id}'
        session.delete(url, req.dict())
