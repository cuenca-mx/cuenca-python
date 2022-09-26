import pytest

from cuenca import KYCValidation


@pytest.mark.vcr
def test_kyc_verification_create():
    kyc_validation: KYCValidation = KYCValidation.create()
    assert kyc_validation.id


@pytest.mark.vcr
def test_kyc_verification_retrieve():
    kyc_validation = KYCValidation.retrieve('KYC01')
    assert kyc_validation.id
