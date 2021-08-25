import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    SavingCategory,
    SavingRequest,
    SavingUpdateRequest,
    StrictPositiveInt,
)

from .base import Updateable, Wallet


@dataclass
class Saving(Wallet, Updateable):
    _resource: ClassVar = 'savings'
    name: str
    category: SavingCategory
    goal_amount: StrictPositiveInt
    goal_date: dt.datetime

    @classmethod
    def create(
        cls,
        name: str,
        category: SavingCategory,
        goal_amount: int,
        goal_date: dt.datetime,
    ):
        request = SavingRequest(
            name=name,
            category=category,
            goal_amount=goal_amount,
            goal_date=goal_date,
        )
        return cast('Saving', cls._create(**request.dict()))

    @classmethod
    def update(
        cls,
        saving_id: str,
        name: Optional[str] = None,
        category: Optional[SavingCategory] = None,
        goal_amount: Optional[int] = None,
        goal_date: Optional[dt.datetime] = None,
    ) -> 'Saving':
        request = SavingUpdateRequest(
            name=name,
            category=category,
            goal_amount=goal_amount,
            goal_date=goal_date,
        )
        return cast('Saving', cls._update(id=saving_id, **request.dict()))
