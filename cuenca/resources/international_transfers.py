import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types import (
    Country,
    Currency,
    InternationalTransferRequest,
    InternationalTransferUpdateRequest,
    TransactionQuery,
    TransactionStatus,
)
from pydantic.dataclasses import dataclass

from .base import Creatable, Queryable, Retrievable, Updateable


@dataclass
class InternationalTransfer(Creatable, Retrievable, Updateable, Queryable):
    _resource: ClassVar = 'international_transfers'
    _query_params: ClassVar = TransactionQuery

    user_id: str
    updated_at: dt.datetime
    idempotency_key: str
    bank_number: str
    account_number: str
    account_country: Country
    account_name: str
    received_amount: int
    received_currency: Currency
    sent_amount: int
    sent_currency: Currency
    status: TransactionStatus

    @classmethod
    def create(
        cls,
        user_id: str,
        idempotency_key: str,
        bank_number: str,
        account_number: str,
        account_country: Country,
        account_name: str,
        received_amount: int,
        received_currency: Currency,
        sent_amount: int,
        sent_currency: Currency,
    ) -> 'InternationalTransfer':
        req = InternationalTransferRequest(
            user_id=user_id,
            idempotency_key=idempotency_key,
            bank_number=bank_number,
            account_number=account_number,
            account_country=account_country,
            account_name=account_name,
            received_amount=received_amount,
            received_currency=received_currency,
            sent_amount=sent_amount,
            sent_currency=sent_currency,
        )
        return cast('InternationalTransfer', cls._create(**req.dict()))

    @classmethod
    def update(
        cls,
        transfer_id: str,
        status: TransactionStatus = None,
    ) -> 'InternationalTransfer':
        req = InternationalTransferUpdateRequest(status=status)
        resp = cls._update(transfer_id, **req.dict())
        return cast('InternationalTransfer', resp)
