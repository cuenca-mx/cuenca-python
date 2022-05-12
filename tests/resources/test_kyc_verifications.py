import pytest

from cuenca import KYCVerification


@pytest.mark.vcr
def test_kyc_verification_create():
    kyc_verification: KYCVerification = KYCVerification.create()
    assert kyc_verification.id


@pytest.mark.vcr
def test_kyc_verification_retrieve():
    kyc_verification = KYCVerification.retrieve('KYC01')
    assert kyc_verification.id


@pytest.mark.vcr
def test_kyc_verification_update():
    kyc_id = 'KYC01'
    changes = dict(curp='HEMA921130HNERNN05')
    kyc_verification = KYCVerification.update(kyc_id, **changes)
    assert all(
        item in kyc_verification.to_dict().items() for item in changes.items()
    )
