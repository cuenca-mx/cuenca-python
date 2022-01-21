from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from .base import Queryable, Retrievable


@dataclass
class Webhook(Retrievable, Queryable):
    _resource: ClassVar = 'webhooks'

    payload: Dict[str, Any]
    event: WebhookEvent
