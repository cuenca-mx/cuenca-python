from typing import ClassVar

from cuenca_validations.types import CardStatus, CardType
from cuenca_validations.types.requests import CardUpdateRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable


@dataclass
class Card(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'cards'
    _update_validator: ClassVar = CardUpdateRequest

    user_id: str
    ledger_account_id: str
    card_number: str
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
