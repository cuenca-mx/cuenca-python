import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types import UserDataRequest, UserDataType
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable


@dataclass
class UserData(Creatable, Retrievable, Updateable, Deactivable, Queryable):
    _resource: ClassVar = 'identities_datas'

    id: str
    type: UserDataType
    created_at: dt.datetime
    data: str  # phone number, email, profession

    user_uri: str  # property? foreign key?

    @classmethod
    def create(
        cls,
        user_id: str,
        type: str,
        data: str,
        *,
        session: Session = global_session,
    ):
        """
        - se crea una instancia de Data en la db y se le asigna el user id
        - se hace fetch del user usando el user_id
        - se setea el id en el campo correspondiente (teléfono email, etc)
        dependiendo del tipo, del recien creado data y se guarda el objeto
        """
        req = UserDataRequest(
            user_id=user_id,
            type=type,
            data=data,
        )
        return cast('UserData', cls._create(session=session, **req.dict()))
