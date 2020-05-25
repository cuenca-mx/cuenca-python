import re
from typing import Dict

from .base import Retrievable

ENDPOINT_RE = re.compile(r'.*/(?P<resource>[a-z]+)/(?P<id>.+)$')
RESOURCES: Dict[str, Retrievable] = {}  # set in ./__init__.py after imports


def retrieve_uri(uri: str) -> Retrievable:
    resource, id_ = ENDPOINT_RE.match(uri).groups()
    return RESOURCES[resource].retrieve(id_)
