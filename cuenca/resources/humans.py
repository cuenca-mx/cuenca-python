import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Creatable, Retrievable, Updateable


@dataclass
class Human(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'humans'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    nombres: str
    primer_apellido: str
    segundo_apellido: str
    user_id: str  # propiedad? es foreign key
    rfc: str
    curp: str
    curp_url: str
    gender: str  # enum gender
    pronouns: str
    birth_place: str  # enum states
    birth_date: dt.date
    birth_country: str
    rating_requested_at: dt.datetime
    rated_at: dt.datetime
