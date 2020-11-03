from typing import ClassVar, List

from cuenca_validations.types import ServiceProviderCategory
from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class ServiceProvider(Retrievable, Queryable):
    _resource: ClassVar = 'service_providers'

    name: str
    provider_key: str
    categories: List[ServiceProviderCategory]
