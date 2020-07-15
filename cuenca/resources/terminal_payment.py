import datetime as dt
from enum import Enum
from typing import ClassVar, Optional, cast

from cuenca_validations.types import StrictPositiveInt
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass

from .base import Creatable, Transaction


class TerminalNetwork(str, Enum):  # TO-DO: Move to cuenca_validations
    cash = "cash"
    internal = "internal"
    spei = "spei"
    card = "card"


class TerminalPaymentRequest(BaseModel):  # TO-DO: Move to cuenca_validations
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    destination_uri: str
    network: TerminalNetwork
    sender_name: StrictStr
    phone_number: str
    idempotency_key: str  # must be unique for each transfer


@dataclass
class TerminalPayment(Transaction, Creatable):

    _resource: ClassVar = "terminal_payments"
    # _query_params: ClassVar = TransferQuery

    idempotency_key: str
    destination_uri: str
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
        amount: StrictPositiveInt,
        descriptor: StrictStr,
        destination_uri: str,
        network: TerminalNetwork,
        sender_name: StrictStr,
        phone_number: str,
        idempotency_key: Optional[str] = None,
    ) -> "TerminalPayment":
        """
        :param amount: principal amount (in centavos) excluding Cuenca fees,
            but including Stripe fees (card transactions only)
        :param descriptor: how it'll appear for the recipient
        :param destination_uri: merchant that will receive the transaction
        :param network: network to complete the payment
        :param sender_name: name of the payer
        :param phone_number: whatsapp number of the payer
        :param idempotency_key: must be unique for each transfer to avoid
            duplicates
        :return: TerminalPayment object
        """

        if not idempotency_key:
            idempotency_key = cls._gen_idempotency_key(destination_uri, amount)

        req = TerminalPaymentRequest(
            amount=amount,
            descriptor=descriptor,
            destination_uri=destination_uri,
            network=network,
            sender_name=sender_name,
            phone_number=phone_number,
            idempotency_key=idempotency_key,
        )
        return cast("TerminalPayment", cls._create(**req.dict()))
