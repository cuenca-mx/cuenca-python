from enum import Enum

from pydantic import PositiveInt, StrictInt


class Status(str, Enum):
    pending = 'pending'
    succeeded = 'succeeded'
    failed = 'failed'


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...
