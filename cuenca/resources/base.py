from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Generator, Optional
from urllib.parse import urlencode

from ..exc import MultipleResultsFound, NoResultFound
from ..http import session


@dataclass
class Resource:
    _endpoint: ClassVar[str]


class Retrievable(Resource):
    @classmethod
    def retrieve(cls, id: str) -> 'Resource':
        resp = session.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def create(cls, data: Optional[Dict[str, Any]] = None):
        data = data or {}
        resp = session.post(cls._endpoint, data)
        return cls(**resp)


class Listable(Resource):
    _query_params: ClassVar[set]

    @classmethod
    def one(cls, **query_params) -> 'Resource':
        cls._check_query_params(query_params)
        query_params['page_size'] = 2
        resp = session.get(cls._endpoint, query_params)
        items = resp['items']
        len_items = len(items)
        if not len_items:
            raise NoResultFound
        if len_items > 1:
            raise MultipleResultsFound
        return items[0]

    @classmethod
    def first(cls, **query_params) -> Optional['Resource']:
        cls._check_query_params(query_params)
        query_params['page_size'] = 1
        resp = session.get(cls._endpoint, query_params)
        try:
            item = resp['items'][0]
        except IndexError:
            item = None
        return item

    @classmethod
    def count(cls, **query_params) -> int:
        cls._check_query_params(query_params)
        query_params['count'] = 1
        resp = session.get(cls._endpoint, query_params)
        return resp['count']

    @classmethod
    def all(cls, **query_params) -> Generator['Resource']:
        cls._check_query_params(query_params)
        next_page_url = f'{cls._endpoint}?{urlencode(query_params)}'
        while next_page_url:
            page = session.get(next_page_url)
            yield from (cls(**item) for item in page['items'])
            next_page_url = page['next']

    @classmethod
    def _check_query_params(cls, query_params):
        if not query_params:
            return
        unaccepted = set(query_params.keys()) - cls._query_params
        if unaccepted:
            raise ValueError(f'{unaccepted} are not accepted query parameters')
