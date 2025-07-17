import pytest

from cuenca import ExistPhone


@pytest.mark.vcr
def test_exist_phone_retrieve():
    phone_number = '+527331256958'
    exist_phone: ExistPhone = ExistPhone.retrieve(phone_number)
    assert exist_phone.id == phone_number
    assert exist_phone.exist
