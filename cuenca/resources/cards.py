from typing import ClassVar

from pydantic.dataclasses import dataclass

from cuenca.resources.base import Updateable


@dataclass
class Card(Updateable):
    _resource: ClassVar = 'cards'
    number: str
    cvv: int
