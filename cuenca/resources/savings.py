from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, cast

from cuenca_validations.types import Currency, SavingCategory, SavingRequest

from .base import Creatable, Updateable, Wallet


@dataclass
class Saving(Wallet, Creatable, Updateable):
    _resource: ClassVar = 'Saving'

    amount: int
    category: SavingCategory
    end_date: datetime
    name: str

    @classmethod
    def create(
        cls,
        name: str,
        category: SavingCategory,
        goal_amount: int,
        goal_date: datetime,
        currency: Currency = Currency.mxn,
    ):
        request = SavingRequest(
            name=name,
            category=category,
            goal_amount=goal_amount,
            goal_date=goal_date,
            currency=currency,
        )
        return cast('Saving', cls._create(**request.dict()))
