from typing import ClassVar

from pydantic.dataclasses import dataclass

from .base import Queryable, Retrievable


@dataclass
class ServiceProvider(Retrievable, Queryable):
    _resource: ClassVar = 'service_providers'

    name: str
    provider_key: str
