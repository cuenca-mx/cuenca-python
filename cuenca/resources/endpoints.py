import datetime as dt
from typing import ClassVar, List, Optional, cast

from cuenca_validations.types.enums import WebhookEvent
from cuenca_validations.types.requests import (
    EndpointRequest,
    EndpointUpdateRequest,
)
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable

from ..http import Session, session as global_session


@dataclass
class Endpoint(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'endpoints'

    url: HttpUrl
    secret: str
    is_active: bool
    events: List[WebhookEvent]
    deactivated_at: Optional[dt.datetime]

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
        is_active: Optional[bool] = None,
        *,
        session: Session = global_session,
    ) -> 'Endpoint':
        """
        Updates endpoint properties. It allows reconfigure properties
        like url and is_active.

        :param endpoint_id: existing endpoint_id
        :param url
        :param is_active
        :param session
        :return: Updated endpoint object
        """
        req = EndpointUpdateRequest(url=url, is_active=is_active)
        resp = cls._update(endpoint_id, session=session, **req.dict())
        return cast('Endpoint', resp)

    @classmethod
    def deactivate(
        cls, endpoint_id: str, *, session: Session = global_session
    ) -> 'Endpoint':
        """
        Deactivates an Endpoint. There is no way to activate this endpoint
        again

        :param endpoint_id: existing endpoint_id
        :param session
        :return: Deactivated endpoint object
        """
        resp = session.delete(f'{cls._resource}/{endpoint_id}')
        return cast('Endpoint', cls._from_dict(resp))
