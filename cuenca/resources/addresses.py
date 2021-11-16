import datetime as dt
from typing import Optional

from pydantic.dataclasses import dataclass


# va a cuenca-validations?
@dataclass
class Address:
    created_at: dt.datetime
    calle: str
    numero_ext: str
    numero_int: Optional[str]
    codigo_postal: str
    estado: str
    ciudad: Optional[str]
    colonia: str
