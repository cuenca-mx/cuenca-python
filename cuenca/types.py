import datetime as dt
from enum import Enum


class CardNetwork(str, Enum):
    atm = 'atm'
    visa = 'visa'


class CardTransactionType(str, Enum):
    auth = 'auth'
    capture = 'capture'
    expiration = 'expiration'
    refund = 'refund'
    void = 'void'


class CardType(str, Enum):
    physical = 'physical'
    virtual = 'virtual'


class DepositNetwork(str, Enum):
    cash = 'cash'
    internal = 'internal'
    spei = 'spei'


class Status(str, Enum):
    created = 'created'
    submitted = 'submitted'
    succeeded = 'succeeded'
    failed = 'failed'


class TransferNetwork(str, Enum):
    internal = 'internal'
    spei = 'spei'


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
