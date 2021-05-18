import datetime as dt

import pytest

from cuenca import PhoneVerification


@pytest.mark.vcr
def test_phone_verifications_create():
    pv = PhoneVerification.create()
    assert pv.id is not None
    assert pv.token is not None


@pytest.mark.vcr
def test_update_phone_verification():
    # It is obtained when the client receives
    # a response to his message on whatsapp
    token_secret = '987654321'

    pv = PhoneVerification.create()
    fields_to_update = dict(
        token=pv.token,token_secret=token_secret
    )
    updated = PhoneVerification.update(pv.id, **fields_to_update)
    assert updated.token == fields_to_update['token']
    assert updated.phone_number is not None
