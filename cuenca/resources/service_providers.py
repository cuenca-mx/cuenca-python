from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class ServiceProvider(Retrievable, Queryable):
    _resource: ClassVar = 'service_providers'

    category: str
    provider_key: str
    provider_type: str
