import datetime as dt
from typing import ClassVar

from clabe import Clabe
from pydantic import BaseModel, StrictStr
from pydantic.dataclasses import dataclass

from ..types import Status, StrictPositiveInt
from .base import Resource


class TransferRequest(BaseModel):
    account_number: Clabe
    amount: StrictPositiveInt
    descriptor: StrictStr
    idempotency_key: str


@dataclass
class Transfer(Resource):
    _endpoint: ClassVar = '/transfers'
    _query_params: ClassVar = {'account_number', 'idempotency_key'}

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    account_number: str
    amount: int
    descriptor: str
    idempotency_key: str
    status: Status

    @classmethod
    def create(
        cls,
        account_number: str,
        amount: int,
        descriptor: str,
        idempotency_key: str,
    ) -> 'Transfer':
        req = TransferRequest(
            account_number=account_number,
            amount=amount,
            descriptor=descriptor,
            idempotency_key=idempotency_key,
        )
        resp = cls._client.post(cls._endpoint, data=req.dict())
        return cls(**resp)
