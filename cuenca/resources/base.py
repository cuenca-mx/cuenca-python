from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Resource:
    _client: ClassVar['cuenca.Client']  # noqa: F821
    _endpoint: ClassVar[str]

    @classmethod
    def retrieve(cls, id: str) -> 'Resource':
        resp = cls._client.get(f'{cls._endpoint}/{id}')
        return cls(**resp)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)
