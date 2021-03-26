import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import CardActivationRequest

from ..http import Session, session as global_session
from .base import Creatable
from .cards import Card
from .resources import retrieve_uri


@dataclass
class CardActivation(Creatable):
    _resource: ClassVar = 'card_activations'

    created_at: dt.datetime
    user_id: str
    ip_address: str
    card_uri: Optional[str]
    success: bool

    @classmethod
    def create(
        cls,
        number: str,
        exp_month: int,
        exp_year: int,
        cvv2: str,
        *,
        session: Session = global_session,
    ) -> 'CardActivation':
        """
        Associates a physical card with the current user

        :param number: Card number
        :param exp_month:
        :param exp_year:
        :param cvv2:
        """
        req = CardActivationRequest(
            number=number,
            exp_month=exp_month,
            exp_year=exp_year,
            cvv2=cvv2,
        )
        return cast(
            'CardActivation', cls._create(session=session, **req.dict())
        )

    @property
    def card(self) -> Optional[Card]:
        result = None
        if self.card_uri:
            result = cast(Card, retrieve_uri(self.card_uri))
        return result
