import os
from typing import Optional, Tuple
from urllib.parse import urljoin

import requests
from cuenca_validations.typing import (
    ClientRequestParams,
    DictStrAny,
    OptionalDict,
)
from requests import Response

from ..exc import CuencaResponseException
from ..version import API_VERSION, CLIENT_VERSION

API_URL = 'https://api.cuenca.com'
SANDBOX_URL = 'https://sandbox.cuenca.com'


class Session:

    base_url: str
    auth: Tuple[str, str]
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
        self.webhook_secret = os.getenv('CUENCA_WEBHOOK_SECRET')
        self.auth = (api_key, api_secret)

    def configure(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        sandbox: Optional[bool] = None,
    ):
        """
        This allows us to instantiate the http client when importing the
        client library and configure it later. It's also useful when rolling
        the api key
        """
        self.auth = (api_key or self.auth[0], api_secret or self.auth[1])
        self.webhook_secret = webhook_secret or self.webhook_secret
        if sandbox is False:
            self.base_url = API_URL
        elif sandbox is True:
            self.base_url = SANDBOX_URL

    def get(
        self, endpoint: str, params: ClientRequestParams = None,
    ) -> DictStrAny:
        return self.request('get', endpoint, params=params)

    def post(self, endpoint: str, data: DictStrAny) -> DictStrAny:
        return self.request('post', endpoint, data=data)

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
