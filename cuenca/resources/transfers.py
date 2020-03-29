import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, List, Optional

from clabe import Clabe
from pydantic import BaseModel, PositiveInt, StrictStr

from ..types import Status
from .base import Resource


class TransferRequest(BaseModel):
    clabe: Clabe
    amount: PositiveInt
    descriptor: StrictStr
    idempotency_key: str


@dataclass
class Transfer(Resource):
    _endpoint: ClassVar[str] = '/transfers'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    clabe: str
    amount: int
    descriptor: str
    idempotency_key: str
    status: Status

    @classmethod
    def create(
        cls, clabe: str, amount: int, descriptor: str, idempotency_key: str
    ) -> 'Transfer':
        req = TransferRequest(
            clabe=clabe,
            amount=amount,
            descriptor=descriptor,
            idempotency_key=idempotency_key,
        )
        resp = cls._client.post(cls._endpoint, data=req.dict())
        return cls(**resp)

    @classmethod
    def list(cls, idempotency_key: Optional[str]) -> List['Transfer']:
        url = cls._endpoint
        if idempotency_key:
            url += f'?idempotency_key={idempotency_key}'
        resp = cls._client.get(url)
        return [cls(**tr) for tr in resp]
