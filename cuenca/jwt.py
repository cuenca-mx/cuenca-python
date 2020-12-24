import base64
import binascii
import datetime as dt
import json
from dataclasses import dataclass

from .exc import MalformedJwtToken


@dataclass
class Jwt:
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
        this function extracts the date so we can't validate the
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
    def create(cls, session) -> 'Jwt':
        session.jwt_token = None
        token = session.post('/token', data=None)['token']
        expires_at = Jwt.get_expiration_date(token)
        return cls(expires_at, token)
