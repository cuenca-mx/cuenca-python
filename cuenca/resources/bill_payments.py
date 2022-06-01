from typing import ClassVar, cast

from cuenca_validations.types import BillPaymentQuery

from .base import Transaction
from .resources import retrieve_uri
from .service_providers import ServiceProvider


class BillPayment(Transaction):
    _resource: ClassVar = 'bill_payments'
    _query_params: ClassVar = BillPaymentQuery

    account_number: str
    provider_uri: str

    @property
    def provider(self) -> ServiceProvider:
        provider = cast(ServiceProvider, retrieve_uri(self.provider_uri))
        return provider
