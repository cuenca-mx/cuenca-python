import asyncio
import re
from typing import Dict, List, cast

from ..http.utils import create_awaitable
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
    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(
        asyncio.gather(*[create_awaitable(retrieve_uri, uri) for uri in uris])
    )
    return results
