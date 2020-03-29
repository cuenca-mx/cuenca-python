import os
from typing import Any, ClassVar, Dict, Optional

from requests import Response, Session

from .resources import ApiKey, Transfer
from .resources.base import Resource
from .version import API_VERSION, CLIENT_VERSION

API_URL = 'https://api.cuenca.com'
SANDBOX_URL = 'https://sandbox.cuenca.com'


class Client:

    _base_url: str
    _api_key: str
    _api_secret: str
    _webhook_secret: str
    _headers: Dict[str, str]
    _session: Session

    # resources
    api_keys: ClassVar[type] = ApiKey
    transfers: ClassVar[type] = Transfer

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        api_version: str = API_VERSION,
        sandbox: bool = False,
    ):
        self._headers = {
            'X-Cuenca-Api-Version': api_version,
            'User-Agent': f'cuenca-python/{CLIENT_VERSION}',
        }
        self._session = Session()
        self._api_key = api_key or os.environ['CUENCA_API_KEY']
        self._api_secret = api_secret or os.environ['CUENCA_API_SECRET']
        self._webhook_secret = webhook_secret or os.getenv(
            'CUENCA_WEBHOOK_SECRET'
        )
        if sandbox:
            self._base_url = SANDBOX_URL
        else:
            self._base_url = API_URL
        Resource._client = self

    def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('get', endpoint, **kwargs)

    def post(
        self, endpoint: str, data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        return self.request('post', endpoint, data, **kwargs)

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        url = self._base_url + endpoint
        response = self._session.request(
            method,
            url,
            auth=(self._api_key, self._api_secret),
            headers=self._headers,
            json=data or {},
            **kwargs,
        )
        self._check_response(response)
        return response.json()

    def _check_response(self, response: Response):
        if response.ok:
            return
        response.raise_for_status()
