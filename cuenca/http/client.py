import base64
import datetime as dt
import json
import os
from typing import Optional, Tuple, Union
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

API_HOST = 'api.cuenca.com'
SANDBOX_HOST = 'sandbox.cuenca.com'
AWS_DEFAULT_REGION = 'us-east-1'
AWS_SERVICE = 'execute-api'


class Session:

    host: str = API_HOST
    basic_auth: Tuple[str, str]
    jwt_token: Optional[str] = None
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

    @property
    def auth(self) -> Union[Tuple[str, str], str]:
        # preference to basic auth
        return (
            self.basic_auth
            if all(self.basic_auth) and not self.jwt_token
            else None
        )

    def configure(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        use_jwt: Optional[bool] = None,
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

        if use_jwt:
            self.set_jwt_headers()

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
        if self.jwt_token:
            self.set_jwt_headers()
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

    def set_jwt_headers(self):
        # Make sure the current token is still valid
        try:
            payload_encoded = self.jwt_token.split('.')[1]
            payload = json.loads(base64.b64decode(payload_encoded))
            # Get a new token if there's less than 5 mins for the actual
            # to be expired
            if payload['exp'] - dt.datetime.utcnow() <= dt.timedelta(
                minutes=5
            ):
                raise Exception('Expired token')
        except Exception:
            self.jwt_token = None

        # Get a new one otherwise
        if not self.jwt_token:
            self.jwt_token = self.post('/token')['token']

        # Set headers with valid token
        self.session.headers.update(
            {
                'X-Cuenca-Token': self.jwt_token,
            }
        )

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        raise CuencaResponseException(
            json=response.json(),
            status_code=response.status_code,
        )
