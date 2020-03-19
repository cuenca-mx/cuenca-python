import datetime as dt
from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseModel, PositiveInt, StrictStr

from ..types import Estado
from .base import Resource


class TransferenciaRequest(BaseModel):
    clabe: str
    monto: PositiveInt
    concepto: StrictStr
    idempotency_key: str


@dataclass
class Transferencia(Resource):
    _endpoint: ClassVar[str] = '/transferencias'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    clabe: str
    monto: int
    concepto: str
    idempotency_key: str
    estado: Estado

    @classmethod
    def create(
        cls, clabe: str, monto: int, concepto: str, idempotency_key: str
    ) -> 'Transferencia':
        req = TransferenciaRequest(
            clabe=clabe,
            monto=monto,
            concepto=concepto,
            idempotency_key=idempotency_key,
        )
        resp = cls._client.post(cls._endpoint, data=req.dict())
        return cls(**resp)

    @classmethod
    def get(cls, id: str) -> 'Transferencia':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)
