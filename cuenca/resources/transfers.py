import datetime as dt
from typing import ClassVar, Optional

from clabe import Clabe
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass

from ..http import session
from ..types import Network, Status, StrictPositiveInt
from .base import Resource


class TransferRequest(BaseModel):
    account_number: Clabe
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer


@dataclass
class Transfer(Resource):
    _endpoint: ClassVar = '/transfers'
    _query_params: ClassVar = {'account_number', 'idempotency_key', 'status'}

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
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
        idempotency_key: str,
    ) -> 'Transfer':
        """
        - amount: needs to be in centavos (not pesos)
        - descriptor: how it'll appear for the recipient
        - idempotency_key: must be unique for each transfer to avoid duplicates
        """
        req = TransferRequest(
            account_number=account_number,
            amount=amount,
            descriptor=descriptor,
            idempotency_key=idempotency_key,
        )
        resp = session.post(cls._endpoint, data=req.dict())
        return cls(**resp)
