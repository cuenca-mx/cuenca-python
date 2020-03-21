import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, List, Optional

from clabe import Clabe
from pydantic import BaseModel, PositiveInt, StrictStr

from ..types import Estado
from .base import Resource


class TransferenciaRequest(BaseModel):
    clabe: Clabe
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
    def retrieve(cls, id: str) -> 'Transferencia':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        tr = self.retrieve(self.id)
        for attr, value in tr.__dict__.items():
            setattr(self, attr, value)

    @classmethod
    def list(cls, idempotency_key: Optional[str]) -> List['Transferencia']:
        url = cls._endpoint
        if idempotency_key:
            url += f'?idempotency_key={idempotency_key}'
        resp = cls._client.get(url)
        return [cls(**tr) for tr in resp]
