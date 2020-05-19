import datetime as dt
from enum import Enum
from typing import Dict, Optional, Union

from pydantic import PositiveInt, StrictInt

OptionalDict = Optional[Dict[str, Union[int, str]]]


class Status(str, Enum):
    pending = 'pending'
    succeeded = 'succeeded'
    failed = 'failed'


class Network(str, Enum):
    spei = 'spei'
    internal = 'internal'


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...


class SantizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dt.date):
                self[k] = v.isoformat()
            elif isinstance(v, Enum):
                self[k] = v.value
