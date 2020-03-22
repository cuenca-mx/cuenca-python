from enum import Enum


class Status(str, Enum):
    pending = 'pending'
    succeeded = 'succeeded'
    failed = 'failed'
