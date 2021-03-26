import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable
from .tmp import CardValidationRequest


@dataclass
class CardValidations(Creatable):
    _resource: ClassVar = 'card_validations'

    created_at: dt.datetime
    card_id: str
    is_valid_arqc: bool
    arpc: str

    @classmethod
    def create(
        cls,
        number: str,
        cvv: Optional[str] = None,
        cvv2: Optional[str] = None,
        icvv: Optional[str] = None,
        exp_date: Optional[str] = None,
        pin_block: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'CardValidations':
        req = CardValidationRequest(
            number=number,
            cvv=cvv,
            cvv2=cvv2,
            icvv=icvv,
            exp_date=exp_date,
            pin_block=pin_block,
        )
        return cast(
            'CardValidations', cls._create(session=session, **req.dict())
        )
