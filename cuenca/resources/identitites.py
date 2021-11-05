import datetime as dt
from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Creatable, Retrievable, Updateable


@dataclass
class Identity(Creatable, Retrievable, Updateable):
    _resource: ClassVar = 'identities'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    name: str
    type: str  # enum UserType
    status: str  # enum UserStatus
    # default_ledger_account_id: str  # foreign key
    available_invitations: int
    beta_tester: bool
    login_attempts: bool
    pending_notifications: int
    last_login_at: dt.datetime

    @classmethod
    def create(cls):
        """
        Se va a crear el recurso con lo mínimo necesario.
        """
