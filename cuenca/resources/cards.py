from typing import ClassVar, Optional, cast

from cuenca_validations.types import CardStatus, CardType
from cuenca_validations.types.queries import CardQuery
from cuenca_validations.types.requests import CardRequest, CardUpdateRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable

from ..http import Session, session as global_session


@dataclass
class Card(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'cards'
    _query_params: ClassVar = CardQuery

    user_id: str
    ledger_account_id: str
    number: str
    exp_month: int
    exp_year: int
    cvv2: str
    type: CardType
    status: CardStatus

    @classmethod
    def create(
        cls,
        ledger_account_id: str,
        user_id: str,
        *,
        session: Session = global_session,
    ) -> 'Card':
        """
        Assigns user_id and ledger_account_id to a existing card

        :param ledger_account_id: associated ledger account id
        :param user_id: associated user id
        :return: New assigned card
        """
        req = CardRequest(ledger_account_id=ledger_account_id, user_id=user_id)
        return cast('Card', cls._create(session=session, **req.dict()))

    @classmethod
    def update(
        cls,
        card_id: str,
        user_id: Optional[str] = None,
        ledger_account_id: Optional[str] = None,
        status: Optional[CardStatus] = None,
        *,
        session: Session = global_session,
    ):
        """
        Updates card properties that are not sensitive or fixed data. It allows
        reconfigure properties like status, and manufacturer.

        :param card_id: existing card_id
        :param user_id: owner user id
        :param ledger_account_id: owner ledger account
        :param status:
        :return: Updated card object
        """
        req = CardUpdateRequest(
            user_id=user_id, ledger_account_id=ledger_account_id, status=status
        )
        resp = cls._update(
            card_id, session=session, **req.dict(exclude_none=True)
        )
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
