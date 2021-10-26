import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types.enums import (
    AuthorizerTransaction,
    CardFraudType,
    CardholderVerificationMethod,
    CardStatus,
    CardType,
    EcommerceIndicator,
    IssuerNetwork,
    PosCapability,
    TrackDataMethod,
)
from cuenca_validations.types.requests import FraudValidationRequest
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Retrievable

from ..http import Session, session as global_session


@dataclass
class FraudValidation(Retrievable, Creatable):
    _resource: ClassVar = 'fraud_validations'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    card_id: str
    user_id: str
    amount: int
    merchant_name: str
    merchant_type: str
    merchant_data: str
    currency_code: str
    prosa_transaction_id: str
    retrieval_reference: str
    card_type: CardType
    card_status: CardStatus
    transaction_type: AuthorizerTransaction
    authorizer_number: Optional[str]
    track_data_method: TrackDataMethod
    pos_capability: PosCapability
    logical_network: Optional[str]
    atm_fee: Optional[int]
    issuer: IssuerNetwork
    cardholder_verification_method: CardholderVerificationMethod
    ecommerce_indicator: EcommerceIndicator
    token_validation_id: Optional[str]
    result: Optional[CardFraudType]
    is_cvv: bool = False
    get_balance: bool = False

    @classmethod
    def create(
        cls,
        request: FraudValidationRequest,
        *,
        session: Session = global_session,
    ) -> 'FraudValidation':
        return cast(
            'FraudValidation', cls._create(session=session, **request.dict())
        )
