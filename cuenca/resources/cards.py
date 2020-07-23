from typing import ClassVar

from cuenca_validations.types import CardType, CardStatus
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Updateable, Retrievable, Queryable, Creatable


@dataclass
class Card(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'cards'

    user_id: str
    ledger_account_id: str
    card_number: str
    cvv: int
    exp_month: int
    exp_year: int
    cvv2: str
    type: CardType
    status: CardStatus


class PhysicalCard(Card):
    batch: str
    manufacturer: str
    cvv: str
    pin_id: str
