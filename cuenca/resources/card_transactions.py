import datetime as dt
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
    merchant: str
    metadata: dict
    error_type: str
    expired_at: dt.datetime

    @property  # type: ignore
    def related_card_transactions(self) -> List['CardTransaction']:
        return [
            cast('CardTransaction', retrieve_uri(uri))
            for uri in self.related_card_transaction_uris
        ]
