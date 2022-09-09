from typing import ClassVar, Optional, cast

from cuenca_validations.types import BillPaymentQuery, ServiceProviderFieldType, BillPaymentRequest

from .base import Creatable, Transaction
from .resources import retrieve_uri
from .service_providers import ServiceProvider


class BillPayment(Transaction, Creatable):
    _resource: ClassVar = 'bill_payments'
    _query_params: ClassVar = BillPaymentQuery

    account_number: str
    provider_uri: str

    @classmethod
    def create(
        cls,
        account_number: str,
        amount: int,
        provider_id: str,
        field_type: ServiceProviderFieldType,
        accountholder_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> 'BillPayment':
        """
        :param account_number: account id to be paid
        :param amount: needs to be in centavos (not pesos)
        :param provider_id: ServiceProvider.id
        :param field_type: payment type you choose
        :param accountholder_name: needed for some services
        :param user_id: Source user to take the funds
        :return: BillPayment object
        """
        req = BillPaymentRequest(
            account_number=account_number,
            amount=amount,
            provider_id=provider_id,
            field_type=field_type,
            accountholder_name=accountholder_name,
            user_id=user_id,
        )
        return cast('BillPayment', cls._create(**req.dict()))

    @property
    def provider(self) -> ServiceProvider:
        provider = cast(ServiceProvider, retrieve_uri(self.provider_uri))
        return provider
