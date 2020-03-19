import datetime as dt
from typing import ClassVar


class Resource:
    _client: ClassVar['cuenca.Client']  # type: ignore
    _endpoint: ClassVar[str]

    def __post_init__(self) -> None:
        for attr, value in self.__dict__.items():
            if attr.endswith('_at'):
                setattr(self, attr, dt.datetime.fromisoformat(value))
