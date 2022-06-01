import base64
import binascii
import datetime as dt
import json
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .exc import MalformedJwtToken

if TYPE_CHECKING:
    from .http import Session


class Jwt(BaseModel):
    expires_at: dt.datetime
    token: str

    @property
    def is_expired(self) -> bool:
        return self.expires_at - dt.datetime.utcnow() <= dt.timedelta(
            minutes=5
        )

    @staticmethod
    def get_expiration_date(token: str) -> dt.datetime:
        """
        Jwt tokens contains the exp field in the payload data,
        this function extracts the date so we can validate the
        token before any request
        More info about JWT tokens at: https://jwt.io/
        """
        try:
            payload_encoded = token.split('.')[1]
            payload = json.loads(base64.b64decode(f'{payload_encoded}=='))
        except (IndexError, json.JSONDecodeError, binascii.Error):
            raise MalformedJwtToken(f'Invalid JWT: {token}')
        # Expiration timestamp can be found in the `exp` key in the payload
        exp_timestamp = payload['exp']
        return dt.datetime.utcfromtimestamp(exp_timestamp)

    @classmethod
    def create(cls, session: 'Session') -> 'Jwt':
        session.jwt_token = None
        session.session.headers.pop('X-Cuenca-Token', None)
        token = session.post('/token', dict())['token']
        expires_at = Jwt.get_expiration_date(token)
        return cls(expires_at=expires_at, token=token)
