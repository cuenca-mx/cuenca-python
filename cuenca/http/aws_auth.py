"""
Based on https://github.com/DavidMuller/aws-requests-auth/blob/master/
aws_requests_auth/aws_auth.py
"""

import datetime
import hashlib
import hmac
from pathlib import PurePosixPath
from typing import Dict
from urllib.parse import quote, unquote, urlparse

import requests
from requests.models import PreparedRequest

ROUTE_CONFIGURATION = 'config/route_configuration.json'


def sign(key: bytes, msg: str) -> bytes:
    """
    Copied from https://docs.aws.amazon.com/general/latest/gr/
    sigv4-signed-request-examples.html
    """
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(
    key: str, date_stamp: str, region_name: str, service_name: str
) -> bytes:
    """
    Copied from https://docs.aws.amazon.com/general/latest/gr/
    sigv4-signed-request-examples.html
    """
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


class CuencaAWSRequestAuth(requests.auth.AuthBase):
    """
    Auth class that allows us to connect to AWS services
    via Amazon's signature version 4 signing process

    Adapted from https://docs.aws.amazon.com/general/latest/gr/
    sigv4-signed-request-examples.html
    """

    def __init__(
        self,
        aws_access_key: str,
        aws_secret_access_key: str,
        aws_host: str,
        aws_region: str,
        aws_service: str,
    ):
        """
        Example usage for talking to an AWS Elasticsearch Service:

        AWSRequestsAuth(aws_access_key='YOURKEY',
                        aws_secret_access_key='YOURSECRET',
                        aws_host='search-service-foobar.us-east-1.es.amazonaws.com',
                        aws_region='us-east-1',
                        aws_service='es',
                        aws_token='...')

        The aws_token is optional and is used only if you are using STS
        temporary credentials.
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_host = aws_host
        self.aws_region = aws_region
        self.service = aws_service

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """
        Adds the authorization headers required by Amazon's signature
        version 4 signing process to the request.

        Adapted from https://docs.aws.amazon.com/general/latest/gr/
        sigv4-signed-request-examples.html
        """
        aws_headers = self.get_aws_request_headers(request)
        request.headers.update(aws_headers)
        return request

    def get_aws_request_headers(
        self, request: PreparedRequest
    ) -> Dict[str, str]:
        """
        Returns a dictionary containing the necessary headers for Amazon's
        signature version 4 signing process. An example return value might
        look like

            {
                'Authorization': 'AWS4-HMAC-SHA256 Credential=YOURKEY/20160618/
                                 'us-east-1/es/aws4_request, '
                                 'SignedHeaders=host;x-amz-date, '
                                 'Signature=ca0a856286efce2a4bd96a978ca6c896605'
                                 '7e53184776c0685169d08abd74739',
                'x-amz-date': '20160618T220405Z',
            }
        """
        # Create a date for headers and the credential string
        time = datetime.datetime.utcnow()
        amzdate = time.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = time.strftime('%Y%m%d')  # For credential_scope

        canonical_uri = self.get_canonical_path(request)

        canonical_querystring = self.get_canonical_querystring(request)

        # Create the canonical headers and signed headers. Header names
        # and value must be trimmed and lowercase, and sorted in ASCII order.
        # Note that there is a trailing \n.
        canonical_headers = (
            'host:' + self.aws_host + '\n' + 'x-amz-date:' + amzdate + '\n'
        )

        # Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'host;x-amz-date'

        # Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ('').
        body = request.body if request.body else bytes()
        try:
            body = body.encode('utf-8')
        except (AttributeError, UnicodeDecodeError):
            body = body

        payload_hash = hashlib.sha256(body).hexdigest()

        # Combine elements to create create canonical request
        canonical_request = (
            (request.method or '')
            + '\n'
            + canonical_uri
            + '\n'
            + canonical_querystring
            + '\n'
            + canonical_headers
            + '\n'
            + signed_headers
            + '\n'
            + payload_hash
        )
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = (
            date_stamp
            + '/'
            + self.aws_region
            + '/'
            + self.service
            + '/'
            + 'aws4_request'
        )
        string_to_sign = (
            algorithm
            + '\n'
            + amzdate
            + '\n'
            + credential_scope
            + '\n'
            + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        )

        # Create the signing key using the function defined above.
        signing_key = get_signature_key(
            self.aws_secret_access_key,
            date_stamp,
            self.aws_region,
            self.service,
        )

        # Sign the string_to_sign using the signing_key
        string_to_sign_utf8 = string_to_sign.encode('utf-8')
        signature = hmac.new(
            signing_key, string_to_sign_utf8, hashlib.sha256
        ).hexdigest()

        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = (
            algorithm
            + ' '
            + 'Credential='
            + self.aws_access_key
            + '/'
            + credential_scope
            + ', '
            + 'SignedHeaders='
            + signed_headers
            + ', '
            + 'Signature='
            + signature
        )

        headers = {
            'Authorization': authorization_header,
            'x-amz-date': amzdate,
            'x-amz-content-sha256': payload_hash,
        }
        return headers

    def get_canonical_path(self, request: PreparedRequest) -> str:
        """
        Create canonical URI--the part of the URI from domain to query
        string (use '/' if no path), based on the path it prepends the
        correct route required for API Gateway depending on the root of the
        path (ej. /cards/ID => /knox/cards/ID). It uses the DEFAULT_ROUTE if
        nothing is found in the dict
        """
        parsed_url = urlparse(request.url)
        self.route_configuration = requests.get(
            f'https://{self.aws_host}/{ROUTE_CONFIGURATION}'
        ).json()

        canonical_path = '/'
        if parsed_url.path:
            path = str(parsed_url.path)
            root = PurePosixPath(unquote(path)).parts[1]
            try:
                canonical_path = self.route_configuration['routes'][root]
            except KeyError:
                canonical_path = self.route_configuration['default_route']
            finally:
                canonical_path += path
        return quote(canonical_path, safe='/-_.~')

    def get_canonical_querystring(self, request: PreparedRequest) -> str:
        """
        Create the canonical query string. According to AWS, by the
        end of this function our query string values must
        be URL-encoded (space=%20) and the parameters must be sorted
        by name.

        This method assumes that the query params in `r` are *already*
        url encoded.  If they are not url encoded by the time they make
        it to this function, AWS may complain that the signature for your
        request is incorrect.

        It appears elasticsearc-py url encodes query paramaters on its own:
            https://github.com/elastic/elasticsearch-py/blob/5dfd6985e5d32ea353d2b37d01c2521b2089ac2b/elasticsearch/connection/http_requests.py#L64

        If you are using a different client than elasticsearch-py, it
        will be your responsibility to urleconde your query params before
        this method is called.
        """
        canonical_querystring = ''

        parsed_url = urlparse(request.url)
        query = str(parsed_url.query)
        querystring_sorted = '&'.join(sorted(query.split('&')))

        for query_param in querystring_sorted.split('&'):
            key_val_split = query_param.split('=', 1)
            key = key_val_split[0]
            if len(key_val_split) > 1:
                val = key_val_split[1]
            else:
                val = ''

            if key:
                if canonical_querystring:
                    canonical_querystring += "&"
                canonical_querystring += u'='.join([key, val])
        return canonical_querystring
