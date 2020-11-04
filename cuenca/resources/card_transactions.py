from typing import ClassVar, List, Optional, cast

from cuenca_validations.types import (
    CardErrorType,
    CardNetwork,
    CardTransactionType,
    CardType,
)
from pydantic.dataclasses import dataclass

from .base import Transaction
from .resources import retrieve_uris


@dataclass
class CardTransaction(Transaction):
    _resource: ClassVar = 'card_transactions'

    type: CardTransactionType
    network: CardNetwork
    related_card_transaction_uris: List[str]
    card_id: str
    card_last4: str
    card_type: CardType
    metadata: dict
    error_type: Optional[CardErrorType]

    @property  # type: ignore
    def related_card_transactions(self) -> Optional[List['CardTransaction']]:
        if not self.related_card_transaction_uris:
            return None
        return cast(
            List['CardTransaction'],
            retrieve_uris(self.related_card_transaction_uris),
        )
