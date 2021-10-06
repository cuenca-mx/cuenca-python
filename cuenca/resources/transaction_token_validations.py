import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types.enums import TransactionTokenValidationStatus
from cuenca_validations.types.requests import (
    TransactionTokenValidationUpdateRequest,
)
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Retrievable, Updateable

from ..http import Session, session as global_session


@dataclass
class TransactionTokenValidation(Retrievable, Updateable):
    _resource: ClassVar = 'transaction_token_validations'

    created_at: dt.datetime
    deactivated_at: dt.datetime
    status: TransactionTokenValidationStatus

    @classmethod
    def update(
        cls,
        id: str,
        status: TransactionTokenValidationStatus,
        *,
        session: Session = global_session,
    ) -> 'TransactionTokenValidation':
        req = TransactionTokenValidationUpdateRequest(status=status)
        resp = cls._update(id, session=session, **req.dict())
        return cast('TransactionTokenValidation', resp)
