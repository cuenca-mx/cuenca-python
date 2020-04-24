import datetime as dt
from typing import ClassVar, List, Set
from urllib.parse import urlencode

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
    _endpoint: ClassVar[str] = '/transfers'
    _query_parameters: ClassVar[Set[str]] = {
        'account_number',
        'idempotency_key',
    }

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

    @classmethod
    def list(cls, **query) -> List['Transfer']:
        """
        Currently accepted query values:
        - account_number
        - idempotency_key
        """
        url = cls._endpoint
        if query:
            unaccepted = set(query.keys()) - cls._query_parameters
            if unaccepted:
                raise ValueError(
                    f'{unaccepted} are not accepted query parameters'
                )
            url += '?' + urlencode(query)
        resp = cls._client.get(url)
        return [cls(**tr) for tr in resp]
