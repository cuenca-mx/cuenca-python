import pytest

from cuenca.resources import ServiceProvider


@pytest.mark.vcr
def test_service_provider():
    id_service_provider = 'SP01'
    service_provider = ServiceProvider.retrieve(id_service_provider)
    assert service_provider.id == id_service_provider
