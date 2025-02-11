import pytest

from cuenca import Signature


@pytest.mark.vcr
def test_signature_create():
    signature: Signature = Signature.create(user_id="USFOOBAR")
    assert signature.id
    assert signature.signature_id
