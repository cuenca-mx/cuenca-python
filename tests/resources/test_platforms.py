import pytest

from cuenca.resources import Platform


@pytest.mark.vcr
def test_platforms_create() -> None:
    platform = Platform.create(name='Test')
    assert platform.id
    assert platform.name == 'Test'
