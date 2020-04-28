from dataclasses import dataclass
from typing import ClassVar

from ..http import session


@dataclass
class Resource:
    _endpoint: ClassVar[str]
    _query_params: ClassVar[set]

    @classmethod
    def retrieve(cls, id: str) -> 'Resource':
        resp = session.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)
