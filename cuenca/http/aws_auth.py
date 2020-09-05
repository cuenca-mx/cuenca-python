from pathlib import PurePosixPath
from urllib.parse import quote, unquote, urlparse

from requests.models import Request

AWS_ROUTES_DICT = dict(cards='/knox')
DEFAULT_ROUTE = '/oaxaca'


def get_canonical_path(r: Request) -> str:
    """
    Create canonical URI--the part of the URI from domain to query
    string (use '/' if no path), based on the path it prepends the
    correct route required for API Gateway depending on the root of the
    path (ej. /cards/ID => /knox/cards/ID). It uses the DEFAULT_ROUTE if
    nothing is found in the dict
    """
    parsedurl = urlparse(r.url)

    canonical_path = '/'
    if parsedurl.path:
        root = PurePosixPath(unquote(parsedurl.path)).parts[1]
        try:
            canonical_path = AWS_ROUTES_DICT[root]
        except KeyError:
            canonical_path = DEFAULT_ROUTE
        finally:
            canonical_path += parsedurl.path
    return quote(canonical_path, safe='/-_.~')
