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
