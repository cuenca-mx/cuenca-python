import datetime as dt
from dataclasses import dataclass
from typing import ClassVar

from ..types import Estado
from .base import Resource


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
        resp = cls._client.post(
            data=dict(
                clabe=clabe,
                monto=monto,
                concepto=concepto,
                idempotency_key=idempotency_key,
            )
        )
        return cls(**resp)

    @classmethod
    def get(cls, id: str) -> 'Transferencia':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)
