from typing import Dict

import pytest
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

from cuenca.resources import FraudValidation


@pytest.fixture
def fraud_validation_data() -> Dict:
    return dict(
        card_id='CA1234567890',
        user_id='US1234',
        amount=123,
        merchant_name='AMAZON MX MARKETPLACE MEXICO DF 000MX',
        merchant_type='wtype',
        merchant_data='0279288357            00012558',
        currency_code='458',
        card_type=CardType.virtual,
        card_status=CardStatus.active,
        transaction_type=AuthorizerTransaction.normal_purchase,
        track_data_method=TrackDataMethod.terminal,
        pos_capability=PosCapability.pin_accepted,
        is_cvv=True,
        issuer=IssuerNetwork.mastercard,
        cardholder_verification_method=CardholderVerificationMethod.signature,
        ecommerce_indicator=EcommerceIndicator.not_ecommerce,
    )


@pytest.mark.vcr
def test_create_fraud_validation(fraud_validation_data: Dict):
    charge_request = FraudValidationRequest(**fraud_validation_data)
    fraud_validation = FraudValidation.create(charge_request)
    assert all(
        getattr(fraud_validation, key) == value
        for key, value in fraud_validation_data.items()
    )
    assert fraud_validation.id


@pytest.mark.vcr
def test_retrieve_fraud_validation(fraud_validation_data):
    fraud_validation = FraudValidation.retrieve('FVDnqqjjbXQ92OvY6g0Jf9nQ')
    assert all(
        getattr(fraud_validation, key) == value
        for key, value in fraud_validation_data.items()
    )
    assert fraud_validation.result is CardFraudType.authorize
