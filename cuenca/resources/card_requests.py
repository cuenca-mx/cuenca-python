import datetime as dt
from typing import ClassVar, Dict, Optional, cast

from cuenca_validations.types import DeliveryStatus, DeliveryType
from cuenca_validations.types.queries import QueryParams
from cuenca_validations.types.requests import (
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
    status: DeliveryStatus
    recipient_phone: str
    recipient_name: str
    recipient_email: str
    comment: Optional[str]
    tracking_url: Optional[str]
    provider_order_id: Optional[str]
    status_history: Optional[Dict]
    messenger_info: Optional[Dict]

    class Config:
        schema_extra = {
            'example': {
                '_id': 'CRxxne2Z5VSTKZm_w8Hzffcw',
                'created_at': '2023-01-01T22:00:00Z',
                'updated_at': '2023-01-01T22:00:00Z',
                'latitude': '19.432608',
                'longitude': '-99.133209',
                'external_number': '36',
                'street': 'C. Varsovia',
                'city': 'Ciudad de México',
                'colonia': 'Juárez',
                'postal_code': '06600',
                'full_address': 'C. Varsovia 36, Juárez, Cuauhtémoc,'
                ' 06600 Ciudad de México, CDMX',
                'delivery_type': 'local_next_day',
                'status': 'created',
                'phone': '5544332211',
                'name': 'Leonora Carrington',
                'email': 'leonora@cuenca.com',
            }
        }

    @classmethod
    def create(
        cls,
        user_id: str,
        delivery_type: DeliveryType,
        latitude: str,
        longitude: str,
        external_number: str,
        street: str,
        city: str,
        colonia: str,
        postal_code: str,
        full_address: str,
        recipient_phone: str,
        recipient_name: str,
        recipient_email: str,
        internal_number: Optional[str] = None,
        *,
        session: Session = global_session,
    ) -> 'CardRequest':
        req = CardRequestRequest(  # name?
            user_id=user_id,
            delivery_type=delivery_type,
            latitude=latitude,
            longitude=longitude,
            external_number=external_number,
            internal_number=internal_number,
            street=street,
            city=city,
            colonia=colonia,
            postal_code=postal_code,
            full_address=full_address,
            recipient_phone=recipient_phone,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
        )
        resp = cls._create(session=session, **req.dict())
        return cast('CardRequest', resp)

    @classmethod
    def update(
        cls,
        card_request_id: str,
        status: Optional[DeliveryStatus] = None,
        delivery_type: Optional[DeliveryType] = None,
        *,
        session: Session = global_session,
    ) -> 'CardRequest':
        req = CardRequestUpdateRequest(  # name?
            status=status,
            delivery_type=delivery_type,
        )
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
