import os
from typing import Optional, Tuple, Union
from urllib.parse import urljoin

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from cuenca_validations.typing import (
    ClientRequestParams,
    DictStrAny,
    OptionalDict,
)
from requests import Response

from ..exc import CuencaResponseException
from ..version import API_VERSION, CLIENT_VERSION

API_HOST = 'api.cuenca.com'
SANDBOX_HOST = 'sandbox.cuenca.com'
AWS_DEFAULT_REGION = 'us-east-1'
AWS_SERVICE = 'execute-api'


class Session:

    host: str = API_HOST
    basic_auth: Tuple[str, str]
    iam_auth: Optional[AWSRequestsAuth] = None
    session: requests.Session

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'X-Cuenca-Api-Version': API_VERSION,
                'User-Agent': f'cuenca-python/{CLIENT_VERSION}',
            }
        )

        # basic auth
        api_key = os.getenv('CUENCA_API_KEY', '')
        api_secret = os.getenv('CUENCA_API_SECRET', '')
        self.basic_auth = (api_key, api_secret)

        # IAM auth
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        aws_region = os.getenv('AWS_DEFAULT_REGION', AWS_DEFAULT_REGION)
        if aws_access_key and aws_secret_access_key:
            self.iam_auth = AWSRequestsAuth(
                aws_access_key=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_host=self.host,
                aws_region=aws_region,
                aws_service=AWS_SERVICE,
            )

    @property
    def auth(self) -> Union[AWSRequestsAuth, Tuple[str, str]]:
        # preference to basic auth
        return self.basic_auth if all(self.basic_auth) else self.iam_auth

    def configure(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: str = AWS_DEFAULT_REGION,
        sandbox: Optional[bool] = None,
    ):
        """
        This allows us to instantiate the http client when importing the
        client library and configure it later. It's also useful when rolling
        the api key
        """
        if sandbox is False:
            self.host = API_HOST
        elif sandbox is True:
            self.host = SANDBOX_HOST

        # basic auth
        self.basic_auth = (
            api_key or self.basic_auth[0],
            api_secret or self.basic_auth[1],
        )

        # IAM auth
        if self.iam_auth is not None:
            self.iam_auth.aws_access_key = (
                aws_access_key or self.iam_auth.aws_access_key
            )
            self.iam_auth.aws_secret_access_key = (
                aws_secret_access_key or self.iam_auth.aws_secret_access_key
            )
            self.iam_auth.aws_region = aws_region or self.iam_auth.aws_region
        elif aws_access_key and aws_secret_access_key:
            self.iam_auth = AWSRequestsAuth(
                aws_access_key=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_host=self.host,
                aws_region=aws_region,
                aws_service=AWS_SERVICE,
            )

    def get(
        self,
        endpoint: str,
        params: ClientRequestParams = None,
    ) -> DictStrAny:
        return self.request('get', endpoint, params=params)

    def post(self, endpoint: str, data: DictStrAny) -> DictStrAny:
        return self.request('post', endpoint, data=data)

    def patch(self, endpoint: str, data: DictStrAny) -> DictStrAny:
        return self.request('patch', endpoint, data=data)

    def delete(self, endpoint: str, data: OptionalDict = None) -> DictStrAny:
        return self.request('delete', endpoint, data=data)

    def request(
        self,
        method: str,
        endpoint: str,
        params: ClientRequestParams = None,
        data: OptionalDict = None,
        **kwargs,
    ) -> DictStrAny:
        resp = self.session.request(
            method=method,
            url='https://' + self.host + urljoin('/', endpoint),
            auth=self.auth,
            json=data,
            params=params,
            **kwargs,
        )
        self._check_response(resp)
        return resp.json()

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        raise CuencaResponseException(
            json=response.json(),
            status_code=response.status_code,
        )
