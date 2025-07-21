import pytest

from cuenca import PhoneVerificationAssociation


@pytest.mark.vcr
def test_phone_verification_association_create():

    phone_verification_association = PhoneVerificationAssociation.create(
        verification_id='VEeCjasQQWQM-Hr-odTGoKoQ',
    )
    assert phone_verification_association.verification_id
    assert phone_verification_association.user_id
