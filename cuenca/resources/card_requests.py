import datetime as dt
from typing import ClassVar, Dict, Optional, cast

from cuenca_validations.types import (
    DeliveryType,
    MessengerInfo,
    StatusDeliveryType,
)
from cuenca_validations.types.queries import QueryParams
from cuenca_validations.types.requests import (  # ?
    CardRequestRequest,
    CardRequestUpdateRequest,
)

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable, Updateable


class CardRequest(Creatable, Queryable, Retrievable, Updateable):
    _resource: ClassVar = 'card_requests'
    _query_params: ClassVar = QueryParams

    deactivated_at: Optional[dt.datetime]
    user_id: str
    latitude: str
    longitude: str
    external_number: str
    internal_number: Optional[str]
    street: str
    city: str
    colonia: str
    postal_code: str
    full_address: str
    delivery_type: DeliveryType
    status: StatusDeliveryType
    phone: str
    name: str
    email: str
    comment: Optional[str]
    tracking_url: Optional[str]
    provider_order_id: Optional[str]  # ?
    status_history: Optional[Dict]
    messenger_info: Optional[MessengerInfo]
    is_replacement: bool  # ?

    class Config:
        schema_extra = {'example': {}}

    @classmethod
    def create(cls, *, session: Session = global_session) -> 'CardRequest':
        req = CardRequestRequest()  # ?
        resp = cls._create(session=session, **req.dict())
        return cast('CardRequest', resp)

    @classmethod
    def update(
        cls,
        card_request_id: str,
        *,
        session: Session = global_session,
    ) -> 'CardRequest':
        req = CardRequestUpdateRequest()  # ?
        resp = cls._update(card_request_id, session=session, **req.dict())
        return cast('CardRequest', resp)

    @classmethod
    def deactivate(
        cls,
        card_request_id: str,
        *,
        session: Session = global_session,
    ) -> 'CardRequest':
        url = f'{cls._resource}/{card_request_id}'
        resp = session.delete(url)
        return cast('CardRequest', cls._from_dict(resp))
