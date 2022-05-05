import pytest

from cuenca import KYCVerification


@pytest.mark.vcr
def test_kyc_verification_create():
    kyc_verification: KYCVerification = KYCVerification.create()
    assert kyc_verification.id


@pytest.mark.vcr
def test_kyc_verification_retrieve():
    kyc_verification: KYCVerification = KYCVerification.retrieve('KYC01')
    assert kyc_verification.id
