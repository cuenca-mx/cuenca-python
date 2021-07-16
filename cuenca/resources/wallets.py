import datetime as dt
from dataclasses import dataclass

from cuenca_validations.types import Currency, WalletType

from cuenca.resources.base import Queryable, Retrievable


@dataclass
class Wallet(Queryable, Retrievable):

    user_id: str
    balance: int
    currency: Currency
    type: WalletType
    deactivated_at: dt.datetime

    @property
    def is_active(self):
        return not self.deactivated_at
