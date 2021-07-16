from dataclasses import dataclass
from typing import ClassVar, cast

from cuenca_validations.types import Currency, SavingRequest

from .base import Creatable, Updateable
from .resources import Wallet


@dataclass
class Saving(Wallet, Creatable, Updateable):
    _resource: ClassVar = 'Saving'

    category: str
    name: str
    goal: int
    end_goal: int

    @classmethod
    def create(cls, name: str, category: str, goal: int, end_goal: int):
        request = SavingRequest(
            name=name,
            category=category,
            goal=goal,
            end_goal=end_goal,
            currency=Currency.mxn,  # For now
        )
        return cast('Saving', cls._create(**request.dict()))
