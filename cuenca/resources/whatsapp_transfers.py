import datetime as dt
from functools import lru_cache
from typing import ClassVar, Optional

from pydantic.dataclasses import dataclass

from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


@dataclass
class WhatsappTransfer(Transaction):
    _resource: ClassVar = 'whatsapp_transfers'

    claim_url: str
    expires_at: dt.datetime
    # defined after the transfer has been claimed
    destination_uri: Optional[str]

    @property  # type: ignore
    @lru_cache()
    def destination(self) -> Optional[Account]:
        if self.destination_uri is None:
            dest = None
        else:
            dest = retrieve_uri(self.destination_uri)
        return dest

    def __hash__(self):
        return hash((self._resource, self.id, self.destination_uri))
