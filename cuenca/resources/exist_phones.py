from typing import ClassVar

from pydantic_extra_types.phone_numbers import PhoneNumber

from .base import Retrievable


class ExistPhones(Retrievable):
    _resource: ClassVar = 'exist_phones'

    id: PhoneNumber
    exist: bool
