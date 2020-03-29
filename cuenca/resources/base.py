from dataclasses import dataclass
from typing import ClassVar

import iso8601


@dataclass
class Resource:
    _client: ClassVar['cuenca.Client']  # type: ignore
    _endpoint: ClassVar[str]

    def __post_init__(self) -> None:
        for attr, value in self.__dict__.items():
            if attr.endswith('_at'):
                setattr(self, attr, iso8601.parse_date(value))

    @classmethod
    def retrieve(cls, id: str) -> 'Resource':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)