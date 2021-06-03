import pytest

from cuenca import PhoneVerification


@pytest.mark.vcr
def test_phone_verifications_create():
    pv = PhoneVerification.create()
    assert pv.id is not None
    assert pv.request_token is not None


@pytest.mark.vcr
def test_update_phone_verification():
    # It is obtained when the client receives
    # a response to his message on whatsapp
    access_token = '987654321'

    pv = PhoneVerification.create()
    fields_to_update = dict(
        request_token=pv.request_token, access_token=access_token
    )
    updated = PhoneVerification.update(pv.id, **fields_to_update)
    assert updated.request_token == fields_to_update['request_token']
    assert updated.phone_number is not None
