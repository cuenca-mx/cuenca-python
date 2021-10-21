import pytest
from cuenca_validations.types.enums import TransactionTokenValidationStatus

from cuenca.resources import TransactionTokenValidation, UserLogin


@pytest.mark.vcr
def test_retrieve_transaction_token_validation() -> None:
    UserLogin.create(password='111111')
    token: TransactionTokenValidation = TransactionTokenValidation.retrieve(
        'TKSEZmmXa-SXuAMv6516sRKw'
    )
    assert token.status is TransactionTokenValidationStatus.pending


@pytest.mark.vcr
def test_update_transaction_token_validation() -> None:
    UserLogin.create(password='111111')
    token = TransactionTokenValidation.update(
        'TKSEZmmXa-SXuAMv6516sRKw', TransactionTokenValidationStatus.accepted
    )
    assert token.status is TransactionTokenValidationStatus.accepted
