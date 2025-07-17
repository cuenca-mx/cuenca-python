from typing import ClassVar

from pydantic_extra_types.phone_numbers import PhoneNumber

from .base import Retrievable


class ExistPhone(Retrievable):
    _resource: ClassVar = 'exist_phone'

    id: PhoneNumber
    exist: bool
