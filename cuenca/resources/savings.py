import datetime as dt
from typing import ClassVar, Optional

from cuenca_validations.types import (
    SavingCategory,
    SavingRequest,
    SavingUpdateRequest,
    StrictPositiveInt,
    WalletQuery,
)

from .base import Updateable, Wallet


class Saving(Wallet, Updateable):
    _resource: ClassVar = 'savings'
    _query_params: ClassVar = WalletQuery
    name: str
    category: SavingCategory
    goal_amount: Optional[StrictPositiveInt] = None
    goal_date: Optional[dt.datetime] = None

    @classmethod
    def create(
        cls,
        name: str,
        category: SavingCategory,
        goal_amount: Optional[int] = None,
        goal_date: Optional[dt.datetime] = None,
    ) -> 'Saving':
        request = SavingRequest(
            name=name,
            category=category,
            goal_amount=goal_amount,
            goal_date=goal_date,
        )
        return cls._create(**request.model_dump())

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
        return cls._update(id=saving_id, **request.model_dump())
