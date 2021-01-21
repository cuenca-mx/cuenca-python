import datetime as dt
from dataclasses import asdict, dataclass, fields
from io import BytesIO
from typing import ClassVar, Dict, Generator, Optional, Union
from urllib.parse import urlencode

from cuenca_validations.types import (
    FileFormat,
    QueryParams,
    SantizedDict,
    TransactionQuery,
    TransactionStatus,
)

from ..exc import MultipleResultsFound, NoResultFound
from ..http import Session, session as global_session


@dataclass
class Resource:
    _resource: ClassVar[str]

    id: str

    # purely for MyPy
    def __init__(self, **_):  # pragma: no cover
        ...

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Union[str, int]]) -> 'Resource':
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
    def retrieve(
        cls, id: str, *, session: Session = global_session
    ) -> Resource:
        resp = session.get(f'/{cls._resource}/{id}')
        return cls._from_dict(resp)

    def refresh(self, *, session: Session = global_session):
        new = self.retrieve(self.id, session=session)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def _create(cls, *, session: Session = global_session, **data) -> Resource:
        resp = session.post(cls._resource, data)
        return cls._from_dict(resp)


@dataclass
class Updateable(Resource):
    updated_at: dt.datetime

    @classmethod
    def _update(
        cls, id: str, *, session: Session = global_session, **data
    ) -> Resource:
        resp = session.patch(f'/{cls._resource}/{id}', data)
        return cls._from_dict(resp)


@dataclass
class Downloadable(Resource):
    @classmethod
    def download(
        cls,
        instance,
        file_format: FileFormat,
        *,
        session: Session = global_session,
    ) -> BytesIO:
        resp = session.request(
            'get',
            f'/{cls._resource}/{instance.id}',
            headers=dict(Accept=file_format.value),
        )
        return BytesIO(resp)

    @property
    def pdf(self) -> bytes:
        return self.download(self, file_format=FileFormat.pdf).read()

    @property
    def xml(self) -> bytes:
        return self.download(self, file_format=FileFormat.xml).read()


@dataclass
class Queryable(Resource):
    _query_params: ClassVar = QueryParams

    created_at: dt.datetime

    @classmethod
    def one(
        cls, *, session: Session = global_session, **query_params
    ) -> Resource:
        q = cls._query_params(limit=2, **query_params)
        resp = session.get(cls._resource, q.dict())
        items = resp['items']
        len_items = len(items)
        if not len_items:
            raise NoResultFound
        if len_items > 1:
            raise MultipleResultsFound
        return cls._from_dict(items[0])

    @classmethod
    def first(
        cls, *, session: Session = global_session, **query_params
    ) -> Optional[Resource]:
        q = cls._query_params(limit=1, **query_params)
        resp = session.get(cls._resource, q.dict())
        try:
            item = resp['items'][0]
        except IndexError:
            rv = None
        else:
            rv = cls._from_dict(item)
        return rv

    @classmethod
    def count(
        cls, *, session: Session = global_session, **query_params
    ) -> int:
        q = cls._query_params(count=True, **query_params)
        resp = session.get(cls._resource, q.dict())
        return resp['count']

    @classmethod
    def all(
        cls, *, session: Session = global_session, **query_params
    ) -> Generator[Resource, None, None]:
        session = session or global_session
        q = cls._query_params(**query_params)
        next_page_uri = f'{cls._resource}?{urlencode(q.dict())}'
        while next_page_uri:
            page = session.get(next_page_uri)
            yield from (cls._from_dict(item) for item in page['items'])
            next_page_uri = page['next_page_uri']


@dataclass
class Transaction(Retrievable, Queryable):
    _query_params: ClassVar = TransactionQuery

    user_id: str
    amount: int  # in centavos
    status: TransactionStatus
    descriptor: str  # how it appears for the customer
