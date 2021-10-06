import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.enums import CardFraudType
from cuenca_validations.types.requests import ChargeRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Retrievable

from ..http import Session, session as global_session


@dataclass
class FraudValidation(Retrievable, Creatable):
    _resource: ClassVar = 'fraud_validations'

    created_at: dt.datetime
    updated_at: dt.datetime
    request: ChargeRequest
    result: Optional[CardFraudType]

    @classmethod
    def create(
        cls, request: ChargeRequest, *, session: Session = global_session
    ) -> 'FraudValidation':
        return cast(
            'FraudValidation', cls._create(session=session, **request.dict())
        )
