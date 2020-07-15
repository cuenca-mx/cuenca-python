import datetime as dt
from typing import ClassVar, List, Optional, Union, cast

from clabe import Clabe
from cuenca_validations.types import (
    PaymentCardNumber,
    StrictPositiveInt,
    TransferNetwork,
    TransferQuery,
)
from cuenca_validations.typing import DictStrAny
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass
from requests import HTTPError

from ..exc import CuencaException
from .accounts import Account
from .base import Creatable, Transaction
from .resources import retrieve_uri


class TransferRequest(BaseModel):
    recipient_name: StrictStr
    account_number: Union[Clabe, PaymentCardNumber]
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer


@dataclass
class Transfer(Transaction, Creatable):
    _resource: ClassVar = "transfers"
    _query_params: ClassVar = TransferQuery

    updated_at: dt.datetime
    recipient_name: str
    account_number: str
    idempotency_key: str
    network: TransferNetwork
    tracking_key: Optional[str]  # clave rastreo if network is SPEI
    destination_uri: Optional[str]  # defined after confirmation of receipt

    @property  # type: ignore
    def destination(self) -> Optional[Account]:
        if self.destination_uri is None:
            acct = None
        else:
            acct = cast(Account, retrieve_uri(self.destination_uri))
        return acct

    @classmethod
    def create(
        cls,
        account_number: str,
        amount: int,
        descriptor: str,
        recipient_name: str,
        idempotency_key: Optional[str] = None,
    ) -> "Transfer":
        """
        :param account_number: CLABE
        :param amount: needs to be in centavos (not pesos)
        :param descriptor: how it'll appear for the recipient
        :param recipient_name: name of recipient
        :param idempotency_key: must be unique for each transfer to avoid
            duplicates
        :return: Transfer object
        """
        if not idempotency_key:
            idempotency_key = cls._gen_idempotency_key(account_number, amount)
        req = TransferRequest(
            account_number=account_number,
            amount=amount,
            descriptor=descriptor,
            recipient_name=recipient_name,
            idempotency_key=idempotency_key,
        )
        return cast("Transfer", cls._create(**req.dict()))

    @classmethod
    def create_many(cls, requests: List[TransferRequest]) -> DictStrAny:
        transfers: DictStrAny = dict(submitted=[], errors=[])
        for req in requests:
            try:
                transfer = cls._create(**req.dict())
            except (CuencaException, HTTPError) as e:
                transfers["errors"].append(dict(request=req, error=e))
            else:
                transfers["submitted"].append(cast("Transfer", transfer))
        return transfers
