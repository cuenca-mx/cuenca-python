from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    CardFundingType,
    CardIssuer,
    CardStatus,
    CardType,
)
from cuenca_validations.types.queries import CardQuery
from cuenca_validations.types.requests import CardRequest, CardUpdateRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable

from ..http import Session, session as global_session


@dataclass
class Card(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'cards'
    _query_params: ClassVar = CardQuery

    user_id: Optional[str]
    number: str
    exp_month: int
    exp_year: int
    cvv2: str
    pin: Optional[str]
    type: CardType
    status: CardStatus
    issuer: CardIssuer
    funding_type: CardFundingType

    @property
    def last_4_digits(self):
        return self.number[-4:]

    @property
    def bin(self):
        return self.number[:6]

    @classmethod
    def create(
        cls,
        issuer: CardIssuer,
        funding_type: CardFundingType,
        user_id: str = 'me',
        *,
        session: Session = global_session,
    ) -> 'Card':
        """
        Assigns user_id and ledger_account_id to a existing virtual card

        :param user_id: associated user id
        :param funding_type: debit or credit
        :param issuer:
        :return: New assigned card
        """
        req = CardRequest(
            user_id=user_id,
            issuer=issuer,
            funding_type=funding_type,
        )
        return cast('Card', cls._create(session=session, **req.dict()))

    @classmethod
    def update(
        cls,
        card_id: str,
        status: Optional[CardStatus] = None,
        pin_block: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'Card':
        """
        Updates card properties that are not sensitive or fixed data. It allows
        reconfigure properties like status, and manufacturer.

        :param card_id: existing card_id
        :param status:
        :param pin_block
        :param session:
        :return: Updated card object
        """
        req = CardUpdateRequest(status=status, pin_block=pin_block)
        resp = cls._update(card_id, session=session, **req.dict())
        return cast('Card', resp)

    @classmethod
    def deactivate(
        cls, card_id: str, *, session: Session = global_session
    ) -> 'Card':
        """
        Deactivates a card
        """
        url = f'{cls._resource}/{card_id}'
        resp = session.delete(url)
        return cast('Card', cls._from_dict(resp))
