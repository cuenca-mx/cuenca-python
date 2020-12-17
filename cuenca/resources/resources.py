import re
from concurrent.futures import ThreadPoolExecutor
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


def retrieve_uris(uris: List[str]) -> List[Retrievable]:
    with ThreadPoolExecutor(max_workers=len(uris)) as executor:
        return [obj for obj in executor.map(retrieve_uri, uris)]
