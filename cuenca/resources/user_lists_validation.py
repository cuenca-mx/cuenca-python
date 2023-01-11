import datetime as dt
from typing import ClassVar, Optional, Union, cast

from clabe import Clabe
from cuenca_validations.types import UserListsRequest
from cuenca_validations.types.identities import CurpField

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class UserListsValidation(Creatable, Retrievable):
    _resource: ClassVar = 'user_lists_validations'
    created_at: dt.datetime
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    curp: Optional[CurpField] = None
    account_number: Optional[str] = None

    @classmethod
    def create(
        cls,
        names: Optional[str] = None,
        first_surname: Optional[str] = None,
        second_surname: Optional[str] = None,
        curp: Optional[CurpField] = None,
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
        return cast(
            'UserListsValidation',
            cls._create(session=session, **req.dict()),
        )
