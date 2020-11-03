import asyncio
import re
from typing import Dict, List, cast

from .base import Retrievable

ENDPOINT_RE = re.compile(r'.*/(?P<resource>[a-z_]+)/(?P<id>.+)$')
RESOURCES: Dict[str, Retrievable] = {}  # set in ./__init__.py after imports


def retrieve_uri(uri: str) -> Retrievable:
    m = ENDPOINT_RE.match(uri)
    if not m:
        raise ValueError(f'uri is not a valid format: {uri}')
    resource, id_ = m.groups()
    return cast(Retrievable, RESOURCES[resource].retrieve(id_))


def retrieve_uris(uris: List[str]) -> Retrievable:
    async def async_retrieve_uri(uri):
        return retrieve_uri(uri)

    async def main():
        return await asyncio.gather(*[async_retrieve_uri(uri) for uri in uris])

    return asyncio.run(main())
