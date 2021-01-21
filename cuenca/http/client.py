import json
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
from ..jwt import Jwt
from ..version import API_VERSION, CLIENT_VERSION

API_HOST = 'stage.cuenca.com'
SANDBOX_HOST = 'sandbox.cuenca.com'
AWS_DEFAULT_REGION = 'us-east-1'
AWS_SERVICE = 'execute-api'


class Session:

    host: str = API_HOST
    basic_auth: Tuple[str, str]
    jwt_token: Optional[Jwt] = None
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
    def auth(self) -> Optional[Tuple[str, str]]:
        return self.basic_auth if all(self.basic_auth) else None

    def configure(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        use_jwt: Optional[bool] = False,
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
            self.jwt_token = Jwt.create(self)

    def get(
        self,
        endpoint: str,
        params: ClientRequestParams = None,
        **kwargs,
    ) -> DictStrAny:
        return self._request_json('get', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: DictStrAny, **kwargs) -> DictStrAny:
        return self._request_json('post', endpoint, data=data, **kwargs)

    def patch(self, endpoint: str, data: DictStrAny, **kwargs) -> DictStrAny:
        return self._request_json('patch', endpoint, data=data, **kwargs)

    def delete(
        self, endpoint: str, data: OptionalDict = None, **kwargs
    ) -> DictStrAny:
        return self._request_json('delete', endpoint, data=data, **kwargs)

    def download(
        self,
        endpoint: str,
        params: ClientRequestParams = None,
        **kwargs,
    ) -> bytes:
        return self.request('get', endpoint, params=params, **kwargs)

    def _request_json(self, *args, **kwargs) -> DictStrAny:
        return json.loads(self.request(*args, **kwargs))

    def request(
        self,
        method: str,
        endpoint: str,
        params: ClientRequestParams = None,
        data: OptionalDict = None,
        **kwargs,
    ) -> bytes:
        if self.jwt_token:
            if self.jwt_token.is_expired:
                self.jwt_token = Jwt.create(self)
            self.session.headers['X-Cuenca-Token'] = self.jwt_token.token
        resp = self.session.request(
            method=method,
            url='https://' + self.host + urljoin('/', endpoint),
            auth=self.auth,
            json=data,
            params=params,
            **kwargs,
        )
        self._check_response(resp)
        return resp.content

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        raise CuencaResponseException(
            json=response.json(),
            status_code=response.status_code,
        )
