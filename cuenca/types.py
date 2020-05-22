import datetime as dt
from enum import Enum


class Status(str, Enum):
    created = 'created'
    submitted = 'submitted'
    succeeded = 'succeeded'
    failed = 'failed'


class Network(str, Enum):
    spei = 'spei'
    internal = 'internal'


def sanitize_dict(d: dict):
    for k, v in d.items():
        if isinstance(v, dt.date):
            d[k] = v.isoformat()
        elif isinstance(v, Enum):
            d[k] = v.value


class SantizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)
