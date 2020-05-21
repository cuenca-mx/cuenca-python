from dataclasses import asdict, dataclass, fields
from typing import ClassVar, Dict, Generator, Optional, Type, Union
from urllib.parse import urlencode

from ..exc import MultipleResultsFound, NoResultFound
from ..http import session
from ..types import SantizedDict
from ..validators import QueryParams


@dataclass
class Resource:
    _endpoint: ClassVar[str]

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
    def retrieve(cls, id: str) -> Resource:
        resp = session.get(f'{cls._endpoint}/{id}')
        return cls._from_dict(resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def create(cls, **data) -> Resource:
        resp = session.post(cls._endpoint, data)
        return cls._from_dict(resp)


class Queryable(Resource):
    _query_params: ClassVar[Type[QueryParams]]

    @classmethod
    def one(cls, **query_params) -> Resource:
        cls._check_query_params(query_params)
        query_params['limit'] = 2
        resp = session.get(cls._endpoint, query_params)
        items = resp['items']
        len_items = len(items)
        if not len_items:
            raise NoResultFound
        if len_items > 1:
            raise MultipleResultsFound
        return cls._from_dict(items[0])

    @classmethod
    def first(cls, **query_params) -> Optional[Resource]:
        cls._check_query_params(query_params)
        query_params['limit'] = 1
        resp = session.get(cls._endpoint, query_params)
        try:
            item = resp['items'][0]
        except IndexError:
            ...
        else:
            return cls._from_dict(item)

    @classmethod
    def count(cls, **query_params) -> int:
        cls._check_query_params(query_params)
        query_params['count'] = 1
        resp = session.get(cls._endpoint, query_params)
        return resp['count']

    @classmethod
    def all(cls, **query_params) -> Generator[Resource, None, None]:
        cls._check_query_params(query_params)
        next_page_url = (
            f'{cls._endpoint}?{urlencode(SantizedDict(query_params))}'
        )
        while next_page_url:
            page = session.get(next_page_url)
            yield from (cls._from_dict(item) for item in page['items'])
            next_page_url = page['next_page_url']

    @classmethod
    def _check_query_params(cls, query_params):
        if not query_params:
            return
        cls._query_params(**query_params)
