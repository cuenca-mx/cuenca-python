import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import CardStatus, CardType
from cuenca_validations.types.requests import CardValidationRequest

from ..http import Session, session as global_session
from .base import Creatable
from .cards import Card
from .resources import retrieve_uri


class CardValidation(Creatable):
    _resource: ClassVar = 'card_validations'

    created_at: dt.datetime
    card_uri: str
    user_id: str
    card_status: CardStatus
    card_type: CardType
    is_valid_cvv: Optional[bool]
    is_valid_cvv2: Optional[bool]
    is_valid_icvv: Optional[bool]
    is_valid_pin_block: Optional[bool]
    is_valid_exp_date: Optional[bool]
    is_pin_attempts_exceeded: bool
    is_expired: bool
    platform_id: Optional[str] = None

    @classmethod
    def create(
        cls,
        number: str,
        cvv: Optional[str] = None,
        cvv2: Optional[str] = None,
        icvv: Optional[str] = None,
        exp_month: Optional[int] = None,
        exp_year: Optional[int] = None,
        pin_block: Optional[str] = None,
        pin_attempts_exceeded: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'CardValidation':
        req = CardValidationRequest(
            number=number,
            cvv=cvv,
            cvv2=cvv2,
            icvv=icvv,
            exp_month=exp_month,
            exp_year=exp_year,
            pin_block=pin_block,
            pin_attempts_exceeded=pin_attempts_exceeded,
        )
        return cast(
            'CardValidation', cls._create(session=session, **req.dict())
        )

    @property
    def card(self) -> Card:
        return cast(Card, retrieve_uri(self.card_uri))

    @property
    def card_id(self) -> str:
        return self.card_uri.split('/')[-1]

    @property
    def is_active(self):
        return self.card_status == CardStatus.active
