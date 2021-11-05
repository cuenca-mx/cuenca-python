import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Creatable, Deactivable, Retrievable, Updateable


@dataclass
class IdentityData(Creatable, Retrievable, Updateable, Deactivable):
    _resource: ClassVar = 'identities_datas'

    id: str
    type: str  # enum (phone number, email_address, profession)
    created_at: dt.datetime
    data: str  # phone number, email, etc
    identity_id: str  # property? foreign key?
    deactivated_at: dt.datetime

    @classmethod
    def create(cls, identity_id, type):
        """
        - se crea una instancia de Data en la db y se le asigna el identity id
        - se hace fetch del identity usando el identity_id
        - se setea el id en el campo correspondiente (teléfono email, etc)
        dependiendo del tipo, del recien creado data y se guarda el objeto
        """
