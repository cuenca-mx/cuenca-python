import pytest
from cuenca_validations.types import (
    ServiceProviderCategory,
    ServiceProviderFieldType,
)

from cuenca.resources import ServiceProvider


@pytest.mark.vcr
def test_service_provider():
    id_service_provider = 'SP01'
    service_provider = ServiceProvider.retrieve(id_service_provider)
    assert service_provider.id == id_service_provider

    # Check that all categories are in the Category Enum
    categories = service_provider.categories
    values = set(category.value for category in ServiceProviderCategory)
    assert all(category in values for category in categories)

    # Check that all fields are in the FieldType Enum
    fields = service_provider.fields
    values = set(field.value for field in ServiceProviderFieldType)
    assert all(field.type in values for field in fields)
