import pytest
from cuenca_validations.types import KYCValidationSource

from cuenca import KYCValidation


@pytest.mark.vcr
def test_validation_create():
    kyc_validation: KYCValidation = KYCValidation.create(
        user_id="USFOOBAR",
        source_type=KYCValidationSource.server,
    )
    assert kyc_validation.id
    assert kyc_validation.verification_id


@pytest.mark.vcr
def test_validation_retrieve():
    kyc_validation = KYCValidation.retrieve('KVFOO')
    assert kyc_validation.id
    assert kyc_validation.verification_id
