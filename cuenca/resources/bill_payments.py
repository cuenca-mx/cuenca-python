from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from cuenca_validations.types import TransactionQuery

from .base import Transaction
from .resources import retrieve_uri
from .service_providers import ServiceProvider


@dataclass
class BillPayment(Transaction):
    _resource: ClassVar = 'bill_payment'
    _query_params: ClassVar = TransactionQuery

    account_number: str
    provider_uri: Optional[str]

    @property
    def provider(self) -> Optional[ServiceProvider]:
        if self.provider_uri is None:
            provider = None
        else:
            provider = cast(ServiceProvider, retrieve_uri(self.provider_uri))
        return provider
