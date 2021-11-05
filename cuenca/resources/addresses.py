import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Creatable, Retrievable, Updateable


@dataclass
class Address(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'addresses'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    calle: str
    numero_ext: str
    numero_int: str
    codigo_postal: str
    estado: str
    ciudad: str
    colonia: str
    identity_id: str  # property? foreign key?
    deactivated_at: dt.datetime
