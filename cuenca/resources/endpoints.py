from typing import Annotated, ClassVar, List, Optional, cast

from cuenca_validations.types.enums import WebhookEvent
from cuenca_validations.types.requests import (
    EndpointRequest,
    EndpointUpdateRequest,
)
from pydantic import AfterValidator, ConfigDict, Field, HttpUrl

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable

# In Pydantic v2, URL fields like `HttpUrl` are stored as internal objects
# instead of `str`, which can break compatibility with code expecting str.
# Using `HttpUrlString` ensures the field is validated as a URL but stored as
# a `str` for compatibility.
# https://github.com/pydantic/pydantic/discussions/6395

HttpUrlString = Annotated[HttpUrl, AfterValidator(str)]


class Endpoint(Creatable, Deactivable, Retrievable, Queryable, Updateable):
    _resource: ClassVar = 'endpoints'

    url: HttpUrlString = Field(..., description='HTTPS url to send webhooks')
    secret: str = Field(
        ...,
        description='token to verify the webhook is sent by Cuenca '
        'using HMAC algorithm',
    )
    is_enable: bool = Field(
        ...,
        description='Allows user to turn-off the endpoint without the '
        'need of deleting it',
    )
    events: List[WebhookEvent] = Field(
        ...,
        description='list of enabled events. If None, all events will '
        'be enabled for this Endpoint',
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                '_id': 'ENxxne2Z5VSTKZm_w8Hzffcw',
                'platform_id': 'PTZoPrrPT6Ts-9myamq5h1bA',
                'created_at': '2022-06-29T22:00:00Z',
                'updated_at': '2022-06-29T22:00:00Z',
                'secret': '1234',
                'url': 'https://webhook.site/714ed1d8',
                'events': [
                    'transaction.create',
                    'transaction.update',
                    'user.create',
                    'user.update',
                    'user.delete',
                ],
                'is_enable': True,
            }
        },
    )

    @classmethod
    def create(
        cls,
        url: HttpUrl,
        events: Optional[List[WebhookEvent]] = None,
        *,
        session: Session = global_session,
    ) -> 'Endpoint':
        """
        Creates and Endpoint, allowing to recieve Webhooks with the specified
        events.
        :param url: HTTPS url to send webhooks
        :param events: list of enabled events. If None, all events will be
            enabled for this Endpoint
        :param session:
        :return: New active endpoint
        """
        req = EndpointRequest(url=url, events=events)
        return cast('Endpoint', cls._create(session=session, **req.model_dump()))

    @classmethod
    def update(
        cls,
        endpoint_id: str,
        url: Optional[HttpUrl] = None,
        events: Optional[List[WebhookEvent]] = None,
        is_enable: Optional[bool] = None,
        *,
        session: Session = global_session,
    ) -> 'Endpoint':
        """
        Updates endpoint properties. It allows reconfigure properties
        like url and is_active.
        :param endpoint_id: existing endpoint_id
        :param url
        :param is_enable
        :param session
        :return: Updated endpoint object
        """
        req = EndpointUpdateRequest(
            url=url, is_enable=is_enable, events=events
        )
        resp = cls._update(endpoint_id, session=session, **req.model_dump())
        return cast('Endpoint', resp)
