import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types.requests import ARPCRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable


@dataclass
class ARPC(Creatable):
    _resource: ClassVar = 'arpc'

    created_at: dt.datetime
    card_id: str
    is_valid_arqc: bool
    arpc: str

    @classmethod
    def create(
        cls,
        arqc: str,
        key_derivation_method: str,
        arpc_method: str,
        txn_data: str,
        *,
        session: Session = global_session,
        **data,
    ) -> 'ARPC':
        req = ARPCRequest(
            arqc=arqc,
            key_derivation_method=key_derivation_method,
            arpc_method=arpc_method,
            txn_data=txn_data,
            **data,
        )
        return cast('ARPC', cls._create(session=session, **req.dict()))
