import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.requests import ARPCRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable


@dataclass
class ARPC(Creatable):
    _resource: ClassVar = 'arpc'

    created_at: dt.datetime
    card_uri: str
    is_valid_arqc: Optional[bool]
    arpc: Optional[str]
    err: Optional[str]

    @classmethod
    def create(
        cls,
        number: str,
        arqc: str,
        arpc_method: str,
        transaction_data: str,
        response_code: str,
        transaction_counter: str,
        pan_sequence: str,
        unique_number: str,
        track_data_method: str,
        *,
        session: Session = global_session,
    ) -> 'ARPC':
        req = ARPCRequest(
            number=number,
            arqc=arqc,
            arpc_method=arpc_method,
            transaction_data=transaction_data,
            response_code=response_code,
            transaction_counter=transaction_counter,
            pan_sequence=pan_sequence,
            unique_number=unique_number,
            track_data_method=track_data_method,
        )
        return cast('ARPC', cls._create(session=session, **req.dict()))
