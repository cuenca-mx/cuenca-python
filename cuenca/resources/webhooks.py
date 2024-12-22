from typing import Any, ClassVar, Dict

from cuenca_validations.types.enums import WebhookEvent
from pydantic import Field

from .base import Queryable, Retrievable


class Webhook(Retrievable, Queryable):
    _resource: ClassVar = 'webhooks'

    payload: Dict[str, Any] = Field(
        ..., description='object sent by the webhook'
    )
    event: WebhookEvent = Field(
        ..., description='type of event being reported'
    )
