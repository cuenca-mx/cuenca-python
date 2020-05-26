import datetime as dt
from typing import ClassVar, Optional

from clabe import Clabe
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass

from ..types import Network, Status
from ..validators import StrictPositiveInt, TransferQuery
from .base import Creatable, Queryable, Retrievable


class TransferRequest(BaseModel):
    recipient_name: StrictStr
    account_number: Clabe
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer


@dataclass
class Transfer(Creatable, Queryable, Retrievable):
    _endpoint: ClassVar = '/transfers'
    _query_params: ClassVar = TransferQuery

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    recipient_name: str
    account_number: str
    amount: int  # in centavos
    descriptor: str  # how it'll appear for the recipient
    idempotency_key: str
    status: Status
    network: Network
    tracking_key: Optional[str] = None  # clave rastreo

    @classmethod
    def create(
        cls,
        account_number: str,
        amount: int,
        descriptor: str,
        recipient_name: str,
        idempotency_key: Optional[str] = None,
    ) -> 'Transfer':
        """
        :param account_number: CLABE
        :param amount: needs to be in centavos (not pesos)
        :param descriptor: how it'll appear for the recipient
        :param recipient_name: name of recipient
        :param idempotency_key: must be unique for each transfer to avoid
            duplicates
        :return: Transfer object

        The recommended idempotency_key scheme:
        1. create a transfer entry in your own database with the status
            created
        2. call this method with the unique id from your database as the
            idempotency_key
        3. update your database with the status created or submitted after
            receiving a response from this method
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
        return cls._create(**req.dict())

    @staticmethod
    def _gen_idempotency_key(account_number: str, amount: int) -> str:
        """
        We *strongly* recommend using your own internal database id as the
        idempotency_key, but this provides some level of protection against
        submitting duplicate transfers
        """
        return f'{dt.datetime.utcnow().date()}:{account_number}:{amount}'
