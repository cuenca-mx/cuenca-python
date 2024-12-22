import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.enums import TrackDataMethod
from cuenca_validations.types.requests import ARPCRequest

from ..http import Session, session as global_session
from .base import Creatable


class Arpc(Creatable):
    """
    An ARPC (Authorisation Response Cryptogram) is generated by the issuer
    to authorize EMV transactions (Chip, Contactless)

    The point of sales terminal or ATM generate an ARQC (Authorization Request
    Cryptogram) to obtain authorization for transactions.
    After, the issuer has to verified the ARQC and generate an ARPC.
    Finally the ARPC is sent back to the point of sales terminal to authorize
    the transaction and validate the issuer as authentic
    """

    _resource: ClassVar = 'arpc'

    created_at: dt.datetime
    card_uri: str
    is_valid_arqc: Optional[bool] = None
    arpc: Optional[str] = None

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
    ) -> 'Arpc':
        req = ARPCRequest(
            number=number,
            arqc=arqc,
            arpc_method=arpc_method,
            transaction_data=transaction_data,
            response_code=response_code,
            transaction_counter=transaction_counter,
            pan_sequence=pan_sequence,
            unique_number=unique_number,
            track_data_method=cast(TrackDataMethod, track_data_method),
        )
        return cast('Arpc', cls._create(session=session, **req.model_dump()))
