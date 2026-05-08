import pytest
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude

from cuenca import PasswordReset


@pytest.mark.vcr
def test_password_resets_create() -> None:
    password_reset = PasswordReset.create(
        location=Coordinate(
            latitude=Latitude(19.432608),
            longitude=Longitude(-99.133209),
        ),
    )
    assert password_reset.id.startswith('PR')


@pytest.mark.vcr
def test_password_resets_retrieve() -> None:
    password_reset = PasswordReset.retrieve('PRFOO')
    assert password_reset.id
    assert password_reset.flow_id


@pytest.mark.vcr
def test_password_resets_all() -> None:
    items = list(PasswordReset.all())
    assert items
