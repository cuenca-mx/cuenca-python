import datetime as dt
from dataclasses import asdict, dataclass, fields
from typing import ClassVar, Dict, Generator, Optional, Union
from urllib.parse import urlencode

from cuenca_validations.types import (
    QueryParams,
    SantizedDict,
    Status,
    TransactionQuery,
)

from ..exc import MultipleResultsFound, NoResultFound
from ..http import session


@dataclass
class Resource:
    _resource: ClassVar[str]

    id: str

    # purely for MyPy
    def __init__(self, **_):  # pragma: no cover
        ...

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Union[str, int]]) -> "Resource":
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)

    @classmethod
    def _filter_excess_fields(cls, obj_dict):
        """
        dataclasses don't allow __init__ to be called with excess fields. This
        method allows the API to add fields in the response body without
        breaking the client
        """
        excess = set(obj_dict.keys()) - {f.name for f in fields(cls)}
        for f in excess:
            del obj_dict[f]

    def to_dict(self):
        return asdict(self, dict_factory=SantizedDict)


class Retrievable(Resource):
    @classmethod
    def retrieve(cls, id: str) -> Resource:
        resp = session.get(f"/{cls._resource}/{id}")
        return cls._from_dict(resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def _create(cls, **data) -> Resource:
        resp = session.post(cls._resource, data)
        return cls._from_dict(resp)

    @staticmethod
    def _gen_idempotency_key(attr_1: Union[str, int], attr_2: Union[str, int]) -> str:
        """
        We *strongly* recommend using your own internal database id as the
        idempotency_key, but this provides some level of protection against
        submitting duplicate transfers.

        The recommended idempotency_key scheme:
        1. create a transfer entry in your own database with the status
            created
        2. call this method with the unique id from your database as the
            idempotency_key
        3. update your database with the status created or submitted after
            receiving a response from this method
        """
        return f"{dt.datetime.utcnow().date()}:{attr_1}:{attr_2}"


class Updateable(Resource):
    @classmethod
    def _update(cls, **data) -> Resource:
        resp = session.put(cls._resource, data)
        return cls._from_dict(resp)


@dataclass
class Queryable(Resource):
    _query_params: ClassVar = QueryParams

    created_at: dt.datetime

    @classmethod
    def one(cls, **query_params) -> Resource:
        q = cls._query_params(limit=2, **query_params)
        resp = session.get(cls._resource, q.dict())
        items = resp["items"]
        len_items = len(items)
        if not len_items:
            raise NoResultFound
        if len_items > 1:
            raise MultipleResultsFound
        return cls._from_dict(items[0])

    @classmethod
    def first(cls, **query_params) -> Optional[Resource]:
        q = cls._query_params(limit=1, **query_params)
        resp = session.get(cls._resource, q.dict())
        try:
            item = resp["items"][0]
        except IndexError:
            rv = None
        else:
            rv = cls._from_dict(item)
        return rv

    @classmethod
    def count(cls, **query_params) -> int:
        q = cls._query_params(count=True, **query_params)
        resp = session.get(cls._resource, q.dict())
        return resp["count"]

    @classmethod
    def all(cls, **query_params) -> Generator[Resource, None, None]:
        q = cls._query_params(**query_params)
        next_page_url = f"{cls._resource}?{urlencode(q.dict())}"
        while next_page_url:
            page = session.get(next_page_url)
            yield from (cls._from_dict(item) for item in page["items"])
            next_page_url = page["next_page_url"]


@dataclass
class Transaction(Retrievable, Queryable):
    _query_params: ClassVar = TransactionQuery

    amount: int  # in centavos
    status: Status
    descriptor: str  # how it appears for the customer
