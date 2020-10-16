from dataclasses import dataclass
from typing import ClassVar, List, cast

from cuenca_validations.types import CardNetwork, CardTransactionType, CardType

from .base import Transaction
from .resources import retrieve_uri


@dataclass
class CardTransaction(Transaction):
    _resource: ClassVar = 'card_transactions'

    type: CardTransactionType
    network: CardNetwork
    related_card_transaction_uris: List[str]
    card_last4: str
    card_type: CardType

    @property  # type: ignore
    def related_card_transactions(self) -> List['CardTransaction']:
        card_transactions = []
        for uri in self.related_card_transaction_uris:
            card_transactions.append(
                cast('CardTransaction', retrieve_uri(uri))
            )
        return card_transactions
