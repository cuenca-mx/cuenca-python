import datetime as dt
from typing import Annotated, ClassVar, Optional

from cuenca_validations.types import (
    CardFundingType,
    CardIssuer,
    CardStatus,
    CardType,
)
from cuenca_validations.types.general import LogConfig
from cuenca_validations.types.queries import CardQuery
from cuenca_validations.types.requests import CardRequest, CardUpdateRequest

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable

from ..http import Session, session as global_session

MAX_PIN_ATTEMPTS = 3


class Card(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'cards'
    _query_params: ClassVar = CardQuery

    user_id: Optional[str] = None
    number: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    exp_month: int
    exp_year: int
    cvv2: str
    pin: Optional[str] = None
    type: CardType
    status: CardStatus
    issuer: CardIssuer
    funding_type: CardFundingType
    dcvv: Optional[str] = None
    dcvv_expires_at: Optional[dt.datetime] = None
    pin_attempts_failed: Optional[int] = None
    platform_id: Optional[str] = None
    card_holder_user_id: Optional[str] = None
    is_dynamic_cvv: bool = False

    @property
    def last_4_digits(self):
        return self.number[-4:]

    @property
    def bin(self):
        return self.number[:6]

    @property
    def pin_attempts_exceeded(self) -> bool:
        return (
            self.pin_attempts_failed >= MAX_PIN_ATTEMPTS
            if self.pin_attempts_failed
            else False
        )

    @classmethod
    def create(
        cls,
        issuer: CardIssuer,
        funding_type: CardFundingType,
        user_id: str = 'me',
        card_holder_user_id: Optional[str] = None,
        is_dynamic_cvv: bool = False,
        *,
        session: Session = global_session,
    ) -> 'Card':
        """
        Assigns user_id and ledger_account_id to a existing virtual card

        :param user_id: associated user id (Owner of card)
        :param funding_type: debit or credit
        :param issuer:
        :param card_holder_user_id: Holder user of card, not is the owner
        :return: New assigned card
        """
        req = CardRequest(
            user_id=user_id,
            issuer=issuer,
            funding_type=funding_type,
            card_holder_user_id=card_holder_user_id,
            is_dynamic_cvv=is_dynamic_cvv,
        )
        return cls._create(session=session, **req.model_dump())

    @classmethod
    def update(
        cls,
        card_id: str,
        status: Optional[CardStatus] = None,
        pin_block: Optional[str] = None,
        is_dynamic_cvv: bool = False,
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
        req = CardUpdateRequest(
            status=status, pin_block=pin_block, is_dynamic_cvv=is_dynamic_cvv
        )
        return cls._update(card_id, session=session, **req.model_dump())

    @classmethod
    def deactivate(
        cls, card_id: str, *, session: Session = global_session
    ) -> 'Card':
        """
        Deactivates a card
        """
        url = f'{cls._resource}/{card_id}'
        resp = session.delete(url)
        return cls(**resp)
