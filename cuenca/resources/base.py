from dataclasses import dataclass
from typing import ClassVar, List
from urllib.parse import urlencode


@dataclass
class Resource:
    _client: ClassVar['cuenca.Client']  # noqa: F821
    _endpoint: ClassVar[str]
    _query_params: ClassVar[set]

    @classmethod
    def retrieve(cls, id: str) -> 'Resource':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)

    @classmethod
    def query(cls, **q) -> List['Resource']:
        """
        Accepted query parameters are defined in cls._query_params
        """
        url = cls._endpoint
        if q:
            unaccepted = set(q.keys()) - cls._query_params
            if unaccepted:
                raise ValueError(
                    f'{unaccepted} are not accepted query parameters'
                )
            url += '?' + urlencode(q)
        resp = cls._client.get(url)
        return [cls(**item) for item in resp]
