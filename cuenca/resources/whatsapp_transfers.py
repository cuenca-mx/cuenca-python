import datetime as dt
from functools import lru_cache
from typing import ClassVar, Optional, cast

from pydantic.dataclasses import dataclass

from ..types import TransferNetwork
from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


@dataclass
class WhatsappTransfer(Transaction):
    _resource: ClassVar = 'whatsapp_transfers'

    updated_at: dt.datetime
    recipient_name: str
    phone_number: str
    claim_url: str
    expires_at: dt.datetime
    # defined after the transfer has been claimed
    destination_uri: Optional[str]
    network: Optional[TransferNetwork]
    tracking_key: Optional[str]  # clave rastreo if network is SPEI

    @property  # type: ignore
    @lru_cache()
    def destination(self) -> Optional[Account]:
        if self.destination_uri is None:
            dest = None
        else:
            dest = cast(Account, retrieve_uri(self.destination_uri))
        return dest

    def __hash__(self):
        return hash((self._resource, self.id, self.destination_uri))
