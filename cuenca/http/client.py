import os
import re
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

API_URL = 'https://api.cuenca.com'
SANDBOX_URL = 'https://bxanq6vtyf.execute-api.us-east-1.amazonaws.com/api'
HOST_REGEX = r'\w+\.(\w|\d|-|\.)+'

BasicOrAws = Union[Tuple[str, str], AWSRequestsAuth]


class Session:

    base_url: str
    auth: BasicOrAws
    webhook_secret: Optional[str]
    session: requests.Session

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'X-Cuenca-Api-Version': API_VERSION,
                'User-Agent': f'cuenca-python/{CLIENT_VERSION}',
            }
        )
        self.base_url = API_URL
        api_key = os.getenv('CUENCA_API_KEY', '')
        api_secret = os.getenv('CUENCA_API_SECRET', '')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', '')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        aws_default_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

        self.webhook_secret = os.getenv('CUENCA_WEBHOOK_SECRET')
        if api_key and api_secret:
            self.configure_basic(api_key, api_secret)
        else:
            self.configure_aws(
                aws_access_key_id, aws_secret_access_key, aws_default_region
            )

    def configure(
        self,
        auth: Optional[BasicOrAws] = None,
        webhook_secret: Optional[str] = None,
        sandbox: Optional[bool] = None,
    ):
        """
        This allows us to instantiate the http client when importing the
        client library and configure it later. It's also useful when rolling
        the api key
        """
        self.auth = auth if auth else self.auth
        self.webhook_secret = webhook_secret or self.webhook_secret
        if sandbox is False:
            self.base_url = API_URL
        elif sandbox is True:
            self.base_url = SANDBOX_URL

    def configure_basic(
        self,
        api_key: str,
        api_secret,
        sandbox: Optional[bool] = None,
        **kwargs,
    ) -> None:
        self.configure(auth=(api_key, api_secret), sandbox=sandbox, **kwargs)

    def configure_aws(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str = 'us-east-1',
        sandbox: Optional[bool] = None,
        **kwargs,
    ):
        url = SANDBOX_URL if sandbox else API_URL
        host = re.findall(HOST_REGEX, url)[0]

        auth = AWSRequestsAuth(
            aws_access_key=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region=aws_default_region,
            aws_service='execute-api',
            aws_host=host,
        )
        self.configure(auth=auth, sandbox=sandbox, **kwargs)

    def get(
        self, endpoint: str, params: ClientRequestParams = None,
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
            url=self.base_url + urljoin('/', endpoint),
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
            json=response.json(), status_code=response.status_code,
        )
