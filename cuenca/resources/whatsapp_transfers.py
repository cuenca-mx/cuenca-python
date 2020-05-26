import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Transaction


@dataclass
class WhatsappTransfer(Transaction):
    _resource: ClassVar = 'whatsapp_transfers'

    shared_url: str
    expires_at: dt.datetime
