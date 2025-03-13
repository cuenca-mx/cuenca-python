import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import UserListsRequest, VerificationStatus
from cuenca_validations.types.identities import Curp

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class UserListsValidation(Creatable, Retrievable):
    _resource: ClassVar = 'user_lists_validations'
    created_at: dt.datetime
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    curp: Optional[Curp] = None
    account_number: Optional[str] = None
    status: Optional[VerificationStatus] = None
    response: Optional[dict] = None

    @property
    def ppe_matches(self) -> list[dict]:
        if not self.response or 'persons' not in self.response:
            return []

        return [
            person
            for person in self.response['persons']
            if person.get('lista') == 'PPE'
        ]

    @classmethod
    def create(
        cls,
        names: Optional[str] = None,
        first_surname: Optional[str] = None,
        second_surname: Optional[str] = None,
        curp: Optional[Curp] = None,
        account_number: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'UserListsValidation':
        req = UserListsRequest(
            names=names,
            first_surname=first_surname,
            second_surname=second_surname,
            curp=curp,
            account_number=account_number,
        )
        return cls._create(session=session, **req.model_dump())
