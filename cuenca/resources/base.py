import base64
import datetime as dt
import json
from io import BytesIO
from typing import ClassVar, Dict, Generator, Optional, Type, TypeVar, Union
from urllib.parse import urlencode

from cuenca_validations.types import (
    FileFormat,
    QueryParams,
    SantizedDict,
    TransactionQuery,
    TransactionStatus,
)
from pydantic import BaseModel

from ..exc import MultipleResultsFound, NoResultFound
from ..http import Session, session as global_session

R = TypeVar('R', bound='Resource')
Q = TypeVar('Q', bound='Queryable')


class Resource(BaseModel):
    _resource: ClassVar[str]

    id: str

    @classmethod
    def _from_dict(cls: Type[R], obj_dict: Dict[str, Union[str, int]]) -> R:
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)

    @classmethod
    def _filter_excess_fields(cls, obj_dict) -> None:
        """
        dataclasses don't allow __init__ to be called with excess fields. This
        method allows the API to add fields in the response body without
        breaking the client
        """
        excess = set(obj_dict.keys()) - set(
            cls.schema().get("properties").keys()
        )
        for f in excess:
            del obj_dict[f]

    def to_dict(self):
        return SantizedDict(self.dict())


class Retrievable(Resource):
    @classmethod
    def retrieve(
        cls: Type[R], id: str, *, session: Session = global_session
    ) -> R:
        resp = session.get(f'/{cls._resource}/{id}')
        return cls._from_dict(resp)

    def refresh(self, *, session: Session = global_session) -> None:
        new = self.retrieve(self.id, session=session)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def _create(
        cls: Type[R], *, session: Session = global_session, **data
    ) -> R:
        resp = session.post(cls._resource, data)
        return cls._from_dict(resp)


class Updateable(Resource):

    updated_at: dt.datetime

    @classmethod
    def _update(
        cls: Type[R], id: str, *, session: Session = global_session, **data
    ) -> R:
        resp = session.patch(f'/{cls._resource}/{id}', data)
        return cls._from_dict(resp)


class Deactivable(Resource):
    deactivated_at: Optional[dt.datetime]

    @classmethod
    def deactivate(
        cls: Type[R], id: str, *, session: Session = global_session, **data
    ) -> R:
        resp = session.delete(f'/{cls._resource}/{id}', data)
        return cls._from_dict(resp)

    @property
    def is_active(self) -> bool:
        return not self.deactivated_at


class Downloadable(Resource):
    @classmethod
    def download(
        cls: Type[R],
        id: str,
        file_format: FileFormat = FileFormat.any,
        *,
        session: Session = global_session,
    ) -> BytesIO:
        resp = session.request(
            'get',
            f'/{cls._resource}/{id}',
            headers=dict(Accept=file_format.value),
        )
        return BytesIO(resp)

    @property
    def pdf(self) -> bytes:
        return self.download(self.id, file_format=FileFormat.pdf).read()

    @property
    def xml(self) -> bytes:
        return self.download(self.id, file_format=FileFormat.xml).read()


class Uploadable(Resource):
    @classmethod
    def _upload(
        cls: Type[R],
        file: bytes,
        user_id: str,
        *,
        session: Session = global_session,
        **data,
    ) -> R:
        encoded_file = base64.b64encode(file)
        resp = session.request(
            'post',
            cls._resource,
            files=dict(
                file=(None, encoded_file),
                user_id=(None, user_id),
                **{k: (None, v) for k, v in data.items()},
            ),
        )
        return cls._from_dict(json.loads(resp))


class Queryable(Resource):
    _query_params: ClassVar = QueryParams

    created_at: dt.datetime

    @classmethod
    def one(
        cls: Type[Q], *, session: Session = global_session, **query_params
    ) -> Q:
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
        cls: Type[Q], *, session: Session = global_session, **query_params
    ) -> Optional[Q]:
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
        cls: Type[Q], *, session: Session = global_session, **query_params
    ) -> int:
        q = cls._query_params(count=True, **query_params)
        resp = session.get(cls._resource, q.dict())
        return resp['count']

    @classmethod
    def all(
        cls: Type[Q], *, session: Session = global_session, **query_params
    ) -> Generator[Q, None, None]:
        session = session or global_session
        q = cls._query_params(**query_params)
        next_page_uri = f'{cls._resource}?{urlencode(q.dict())}'
        while next_page_uri:
            page = session.get(next_page_uri)
            yield from (cls._from_dict(item) for item in page['items'])
            next_page_uri = page['next_page_uri']


class Transaction(Retrievable, Queryable):
    _query_params: ClassVar = TransactionQuery

    user_id: str
    amount: int  # in centavos
    status: TransactionStatus
    descriptor: str  # how it appears for the customer


class Wallet(Creatable, Deactivable, Retrievable, Queryable):
    user_id: str
    balance: int

    @property
    def wallet_uri(self):
        return f'/{self._resource}/{self.id}'
