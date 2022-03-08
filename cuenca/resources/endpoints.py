from typing import ClassVar, List, Optional, cast

from cuenca_validations.types.enums import WebhookEvent
from cuenca_validations.types.requests import (
    EndpointRequest,
    EndpointUpdateRequest,
)
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable


@dataclass()
class Endpoint(Creatable, Deactivable, Retrievable, Queryable, Updateable):
    _resource: ClassVar = 'endpoints'

    url: HttpUrl
    secret: str
    is_enable: bool
    events: List[WebhookEvent]

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
        return cast('Endpoint', cls._create(session=session, **req.dict()))

    @classmethod
    def update(
        cls,
        endpoint_id: str,
        url: Optional[HttpUrl] = None,
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
        req = EndpointUpdateRequest(url=url, is_enable=is_enable)
        resp = cls._update(endpoint_id, session=session, **req.dict())
        return cast('Endpoint', resp)
