from typing import ClassVar, List, Optional, cast

from cuenca_validations.types import (
    WebhookEvent,
)
from cuenca_validations.types.requests import (
    EndpointRequest, EndpointUpdateRequest
)
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass

from cuenca.resources.base import Creatable, Queryable, Retrievable, Updateable

from ..http import Session, session as global_session


@dataclass
class Endpoint(Retrievable, Queryable, Creatable, Updateable):
    _resource: ClassVar = 'endpoints'

    platform_id: str
    url: HttpUrl
    events: List[WebhookEvent]
    is_active: bool

    @classmethod
    def create(
        cls,
        url: HttpUrl
        events: List[WebhookEvent],
        *,
        session: Session = global_session,
    ) -> 'Endpoint':
        """
        Assigns user_id and ledger_account_id to a existing virtual card

        :param url: HTTPS url to send webhooks
        :param events: list of enabled events
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

        :param card_id: existing endpoint_id
        :param url
        :param is_active
        :param session
        :return: Updated card object
        """
        req = EndpointUpdateRequest(url=url, is_active=is_active)
        resp = cls._update(endpoint_id, session=session, **req.dict())
        return cast('Endpoint', resp)

    @classmethod
    def deactivate(
        cls, endpoint_id: str, *, session: Session = global_session
    ) -> 'Endpoint':
        """
        Deactivates an Endpoint
        """
        url = f'{cls._resource}/{endpoint_id}'
        resp = session.delete(url)
        return cast('Endpoint', cls._from_dict(resp))
