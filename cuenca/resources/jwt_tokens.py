import datetime as dt
from typing import Annotated, ClassVar

from cuenca_validations.types import LogConfig
from pydantic import ConfigDict

from ..http import Session, session as global_session
from .base import Creatable


class JwtToken(Creatable):
    _resource: ClassVar = 'token'

    id: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    token: Annotated[str, LogConfig(masked=True, unmasked_chars_length=4)]
    created_at: dt.datetime
    api_key_uri: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': (
                    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzgzNjI'
                    '4NzcsImlhdCI6MTczNzc1ODA3Nywic3ViIjoiQUtzY3p5N3RzaVJkMkl'
                    'iakxfbllGb2xRIiwidWlkIjoiNjRiZmQ0OTItZGFhMy0xMWVmLWEyMWU'
                    'tMGE1OGE5ZmVhYzAyIn0.Er8kDsw4rtGkwAXpEgUhwyXFiBjYlwDVTGF'
                    'tYW7o0go'
                ),
                'token': (
                    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzgzNjI'
                    '4NzcsImlhdCI6MTczNzc1ODA3Nywic3ViIjoiQUtzY3p5N3RzaVJkMkl'
                    'iakxfbllGb2xRIiwidWlkIjoiNjRiZmQ0OTItZGFhMy0xMWVmLWEyMWU'
                    'tMGE1OGE5ZmVhYzAyIn0.Er8kDsw4rtGkwAXpEgUhwyXFiBjYlwDVTGF'
                    'tYW7o0go'
                ),
                'created_at': '2025-01-24T22:34:37.659667',
                'api_key_uri': '/api_key/AKsczy7tsiRd2IbjL_nYFolQ',
            }
        }
    )

    @classmethod
    def create(cls, session: Session = global_session) -> 'JwtToken':
        return cls._create(session=session)
