from typing import Any, ClassVar, Dict

from cuenca_validations.types.enums import WebhookEvent

from .base import Queryable, Retrievable


class Webhook(Retrievable, Queryable):
    _resource: ClassVar = 'webhooks'

    payload: Dict[str, Any]
    event: WebhookEvent
