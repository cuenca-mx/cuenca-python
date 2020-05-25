from functools import lru_cache
from typing import ClassVar, List

from ..types import CardNetwork, CardTransactionType, CardType
from .base import Transaction
from .resources import retrieve_uri


class CardTransaction(Transaction):
    _resource: ClassVar = 'card_transactions'

    type: CardTransactionType
    network: CardNetwork
    related_card_transaction_uris: List[str]
    card_last4: str
    card_type: CardType

    @property  # type: ignore
    @lru_cache()
    def related_card_transactions(self) -> List['CardTransaction']:
        related = []
        for uri in self.related_card_transaction_uris:
            related.append(retrieve_uri(uri))
        return related

    def __hash__(self) -> int:
        """
        This ensures that the lru_cache doesn't use stale information
        """
        return hash((self.id, tuple(self.related_card_transaction_uris)))
