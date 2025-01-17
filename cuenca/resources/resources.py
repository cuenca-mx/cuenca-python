import re

from .base import Retrievable

ENDPOINT_RE = re.compile(r'.*/(?P<resource>[a-z_]+)/(?P<id>.+)$')
RESOURCES: dict[str, Retrievable] = {}  # set in ./__init__.py after imports


def retrieve_uri(uri: str) -> Retrievable:
    m = ENDPOINT_RE.match(uri)
    if not m:
        raise ValueError(f'uri is not a valid format: {uri}')
    resource, id_ = m.groups()
    return RESOURCES[resource].retrieve(id_)


def retrieve_uris(uris: list[str]) -> list[Retrievable]:
    # Changed the implementation to use a simple for loop instead of
    # ThreadPoolExecutor. The list of URIs is small, so the performance
    # difference is negligible. Additionally, using ThreadPoolExecutor
    # caused issues with VCR tests, as the recordings were not retrieved
    # in the correct order, leading to unexpected HTTP calls instead of
    # using the mocked recordings.

    return [retrieve_uri(uri) for uri in uris]
