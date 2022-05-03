import pytest

from cuenca import KYCVerification


@pytest.mark.vcr
def test_kyc_verification_create():
    kyc_verification: KYCVerification = KYCVerification.create(
        platform_id='PL01',
    )
    assert kyc_verification.id
