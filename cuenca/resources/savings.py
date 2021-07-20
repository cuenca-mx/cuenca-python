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
        amount: int,
        end_date: datetime,
        category: SavingCategory,
    ):
        request = SavingRequest(
            amount=amount,
            name=name,
            category=category,
            end_date=end_date,
            currency=Currency.mxn,  # For now
        )
        return cast('Saving', cls._create(**request.dict()))
