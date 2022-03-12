import pytest
from cuenca_validations.types import VerificationType

from cuenca import Verification


@pytest.mark.vcr
def test_verification_email_create():
    verification: Verification = Verification.create(
        sender='mail@cuenca.com', type=VerificationType.email_verification
    )
    assert verification.id


@pytest.mark.vcr
def test_verification_phone_create():
    verification: Verification = Verification.create(
        sender='+525555555555', type=VerificationType.phone_verification
    )
    assert verification.id


@pytest.mark.vcr
def test_verification_verify():
    verification: Verification = Verification.verify(id='VE01', code='111111')
    assert verification.id
