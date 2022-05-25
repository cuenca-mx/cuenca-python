from typing import ClassVar, List, Optional, cast

from cuenca_validations.types import (
    CardErrorType,
    CardNetwork,
    CardTransactionQuery,
    CardTransactionType,
    CardType,
)

from .base import Transaction
from .cards import Card
from .resources import retrieve_uri, retrieve_uris


class CardTransaction(Transaction):
    _resource: ClassVar = 'card_transactions'
    _query_params: ClassVar = CardTransactionQuery

    type: CardTransactionType
    network: CardNetwork
    related_card_transaction_uris: List[str]
    card_uri: str
    card_last4: str
    card_type: CardType
    metadata: dict
    error_type: Optional[CardErrorType]

    @property  # type: ignore
    def related_card_transactions(self) -> Optional[List['CardTransaction']]:
        if not self.related_card_transaction_uris:
            return []
        return cast(
            List['CardTransaction'],
            retrieve_uris(self.related_card_transaction_uris),
        )

    @property  # type: ignore
    def card(self) -> Card:
        return cast(Card, retrieve_uri(self.card_uri))
