import pytest
from cuenca_validations.types import SignatureFile

from cuenca import Signature


@pytest.mark.vcr
def test_signature_create():
    signature_file = SignatureFile(
        uri="https://www.google.com/image.png",
        ip="192.168.1.100",
        location="19.432608, -99.133209",
        hash="1234567890",
    )
    signature: Signature = Signature.create(
        user_id="USFOOBAR",
        signature=signature_file,
    )
    assert signature.id
    assert signature.signature_id
