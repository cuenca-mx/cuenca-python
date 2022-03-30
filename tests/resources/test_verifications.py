import pytest
from cuenca_validations.types import VerificationType

from cuenca import Verification
from cuenca.exc import CuencaResponseException


@pytest.mark.vcr
def test_verification_email_create():
    verification: Verification = Verification.create(
        recipient='mail@cuenca.com',
        type=VerificationType.email,
        platform_id='PL01',
    )
    assert verification.id


@pytest.mark.vcr
def test_verification_phone_create():
    verification: Verification = Verification.create(
        recipient='+525555555555',
        type=VerificationType.phone,
        platform_id='PL01',
    )
    assert verification.id


@pytest.mark.vcr
def test_verification_verify():
    verification = Verification.verify(id='VE02', code='299566')
    assert verification.id


@pytest.mark.vcr
def test_verification_verify_fail():
    with pytest.raises(CuencaResponseException) as exc:
        Verification.verify(id='VE01', code='222222')
        assert exc.status_code == 400
        assert exc.json['error'] == 'Invalid code.'


@pytest.mark.vcr
def test_verification_verify_fail_max_attempt():
    with pytest.raises(CuencaResponseException) as exc:
        Verification.verify(id='VE01', code='333333')
        assert exc.status_code == 400
        assert exc.json['error'] == 'Max Retries reached.'


@pytest.mark.vcr
def test_verification_verify_deactivated_verification():
    with pytest.raises(CuencaResponseException) as exc:
        Verification.verify(id='VE01', code='333333')
        assert exc.status_code == 403
        assert exc.json['error'] == (
            'You can not validate a deactivated Verification.'
        )
