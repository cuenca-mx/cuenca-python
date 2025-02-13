import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import TransferNetwork

from .accounts import Account
from .base import Transaction
from .resources import retrieve_uri


class WhatsappTransfer(Transaction):
    _resource: ClassVar = 'whatsapp_transfers'

    updated_at: dt.datetime
    recipient_name: str
    phone_number: str
    claim_url: Optional[str] = None
    expires_at: dt.datetime
    # defined after the transfer has been claimed
    destination_uri: Optional[str] = None
    network: Optional[TransferNetwork] = None
    tracking_key: Optional[str] = None  # clave rastreo if network is SPEI

    @property  # type: ignore
    def destination(self) -> Optional[Account]:
        if self.destination_uri is None:
            dest = None
        else:
            dest = cast(Account, retrieve_uri(self.destination_uri))
        return dest
