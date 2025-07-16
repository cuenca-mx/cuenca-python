import pytest

from cuenca.resources import UserTOSAgreement


@pytest.mark.vcr
def test_user_tos_agreements_create() -> None:
    tos = UserTOSAgreement.create(
        location="9.3953792,-99.139584",
        tos_id="TS67f5bf03c1fc891bdf36090d",
    )
    assert tos.id
