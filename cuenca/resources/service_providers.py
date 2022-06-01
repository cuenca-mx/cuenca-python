from typing import ClassVar, List

from cuenca_validations.types import ServiceProviderCategory

from .base import Queryable, Retrievable


class ServiceProvider(Retrievable, Queryable):
    _resource: ClassVar = 'service_providers'

    name: str
    provider_key: str
    categories: List[ServiceProviderCategory]
