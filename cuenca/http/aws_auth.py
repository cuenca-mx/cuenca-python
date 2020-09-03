from pathlib import PurePosixPath
from urllib.parse import quote, unquote, urlparse

from aws_requests_auth.aws_auth import AWSRequestsAuth

AWS_ROUTES_DICT = dict(cards='knox/')
DEFAULT_ROUTE = 'oaxaca/'


class CuencaAWSRequestsAuth(AWSRequestsAuth):
    @classmethod
    def get_canonical_path(cls, r):
        """
        Create canonical URI--the part of the URI from domain to query
        string (use '/' if no path)
        """
        parsedurl = urlparse(r.url)

        # safe chars adapted from boto's use of urllib.parse.quote
        # https://github.com/boto/boto/blob/d9e5cfe900e1a58717e393c76a6e3580305f217a/boto/auth.py#L393
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
