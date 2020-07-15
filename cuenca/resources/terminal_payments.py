import datetime as dt
from enum import Enum
from typing import ClassVar, Optional, cast

from cuenca_validations.types import StrictPositiveInt, TransactionQuery
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass

from .base import Creatable, Transaction


class TerminalNetwork(str, Enum):  # TO-DO: Move to cuenca_validations
    cash = 'cash'
    internal = 'internal'
    spei = 'spei'
    card = 'card'


class TerminalPaymentRequest(BaseModel):  # TO-DO: Move to cuenca_validations
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    terminal_uri: str
    network: TerminalNetwork
    sender_name: StrictStr
    phone_number: str
    idempotency_key: str  # must be unique for each transfer


class TerminalPaymentQuery(TransactionQuery):  # TO-DO: To cuenca_validations
    idempotency_key: Optional[str] = None
    network: Optional[str] = None


@dataclass
class TerminalPayment(Transaction, Creatable):

    _resource: ClassVar = 'terminal_payments'
    _query_params: ClassVar = TerminalPaymentQuery

    idempotency_key: str
    terminal_uri: str
    network: TerminalNetwork
    sender_name: StrictStr
    phone_number: str
    updated_at: dt.datetime  # read-only
    platform_fees: StrictPositiveInt  # read-only: Cuenca fees
    confirmation_code: str  # read-only
    external_processor_reference: str  # read-only

    @classmethod
    def create(
        cls,
        amount: int,
        descriptor: str,
        terminal_uri: str,
        network: TerminalNetwork,
        sender_name: str,
        phone_number: str,
        idempotency_key: str,
    ) -> 'TerminalPayment':
        """
        :param amount: principal amount (in centavos) excluding Cuenca fees,
            but including Stripe fees (card transactions only)
        :param descriptor: how it'll appear for the recipient
        :param terminal_uri: merchant that will receive the transaction
        :param network: network to complete the payment
        :param sender_name: name of the payer
        :param phone_number: whatsapp number of the payer
        :param idempotency_key: must be unique for each transfer to avoid
            duplicates
        :return: TerminalPayment object
        """

        req = TerminalPaymentRequest(
            amount=amount,
            descriptor=descriptor,
            terminal_uri=terminal_uri,
            network=network,
            sender_name=sender_name,
            phone_number=phone_number,
            idempotency_key=idempotency_key,
        )
        return cast('TerminalPayment', cls._create(**req.dict()))
