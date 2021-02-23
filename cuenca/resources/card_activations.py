from typing import ClassVar, cast

from cuenca_validations.types import CardFundingType, CardIssuer
from cuenca_validations.types.requests import CardActivationRequest

from ..http import Session, session as global_session
from .cards import Card


class CardActivation:
    _resource: ClassVar = 'card_activations'

    @classmethod
    def create(
        cls,
        number: str,
        exp_month: int,
        exp_year: int,
        cvv2: str,
        issuer: CardIssuer,
        funding_type: CardFundingType,
        *,
        session: Session = global_session,
    ) -> Card:
        """
        Associates a physical card with the current user

        :param number: Card number
        :param exp_month:
        :param exp_year:
        :param cvv2:
        :param issuer:
        :param funding_type: debit or credit
        """
        req = CardActivationRequest(
            number=number,
            exp_month=exp_month,
            exp_year=exp_year,
            cvv2=cvv2,
            issuer=issuer,
            funding_type=funding_type,
        )
        resp = session.post(cls._resource, req.dict())
        return cast(Card, Card._from_dict(resp))
