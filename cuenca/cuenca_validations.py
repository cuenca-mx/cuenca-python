# Todo: Move all content of this file to cuenca-validations
from enum import Enum

from cuenca_validations.types import Country, TransactionStatus
from cuenca_validations.types.requests import BaseRequest


class Currency(str, Enum):
    mxn = 'mxn'
    usd = 'usd'


class InternationalTransferRequest(BaseRequest):
    user_id: str
    idempotency_key: str
    bank_number: str
    account_number: str
    account_country: Country
    account_name: str
    received_amount: int
    received_currency: Currency
    sent_amount: int
    sent_currency: Currency


class InternationalTransferUpdateRequest(BaseRequest):
    status: TransactionStatus
