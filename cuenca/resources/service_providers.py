from dataclasses import dataclass
from typing import ClassVar, List

from cuenca_validations.types import (
    ServiceProviderCategory,
    ServiceProviderQuery,
)

from .base import Queryable, Retrievable


@dataclass
class ServiceProvider(Retrievable, Queryable):
    _resource: ClassVar = 'service_providers'
    _query_params: ClassVar = ServiceProviderQuery

    name: str
    provider_key: str
    categories: List[ServiceProviderCategory]
