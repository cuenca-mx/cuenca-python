from typing import ClassVar, Optional, cast

from pydantic import BaseModel, Field, StrictStr
from pydantic.dataclasses import dataclass

from .base import Creatable, Queryable, Retrievable, Updateable


class TerminalRequest(BaseModel):  # TO-DO: Move to cuenca_validations
    brand_name: StrictStr
    brand_image: StrictStr
    slug: str = Field(regex=r'^[a-z0-9-_]{5,25}$')
    card_active: bool
    cash_active: bool
    spei_active: bool


@dataclass
class Terminal(Queryable, Retrievable, Creatable, Updateable):

    _resource: ClassVar = 'terminal'

    brand_name: str
    brand_image: str
    slug: str  # only alphanumeric, - or _ allowed
    card_active: bool
    cash_active: bool
    spei_active: bool
    stripe_ready: bool  # Stripe account setup has been fully completed?

    @classmethod
    def create(
        cls,
        brand_name: str,
        slug: str,
        brand_image: Optional[str] = '',
        card_active: Optional[bool] = False,
        cash_active: Optional[bool] = True,
        spei_active: Optional[bool] = True,
    ) -> 'Terminal':
        """
        :param brand_name: Commercial brand name for the merchant
        :param brand_image: URL of the image/logo
        :param slug: custom part of the payment URL i.e. cuenca.com/${slug}
        :param card_active: card payments enabled? (requires stripe_ready)
        :param cash_active: cash payments enabled?
        :param spei_active: spei payments enabled?
        :return: Terminal object
        """

        # TO-DO: Support https://feedme.cuenca.io/files

        req = TerminalRequest(
            brand_name=brand_name,
            brand_image=brand_image,
            slug=slug,
            card_active=card_active,
            cash_active=cash_active,
            spei_active=spei_active,
        )
        return cast('Terminal', cls._create(**req.dict()))

    def update(
        self,
        brand_name: Optional[str] = None,
        slug: Optional[str] = None,
        brand_image: Optional[str] = None,
        card_active: Optional[bool] = None,
        cash_active: Optional[bool] = None,
        spei_active: Optional[bool] = None,
    ) -> 'Terminal':
        """
        :param brand_name: Commercial brand name for the merchant
        :param brand_image: URL of the image/logo
        :param slug: custom part of the payment URL, i.e. cuenca.com/${slug}
        :param card_active: card payments enabled? (requires stripe_ready)
        :param cash_active: cash payments enabled?
        :param spei_active: spei payments enabled?
        :return: Terminal object
        """

        # TO-DO: Support https://feedme.cuenca.io/files

        req = TerminalRequest(
            brand_name=brand_name or self.brand_name,
            brand_image=brand_image or self.brand_image,
            slug=slug or self.slug,
            card_active=card_active or self.card_active,
            cash_active=cash_active or self.cash_active,
            spei_active=spei_active or self.spei_active,
        )
        return cast('Terminal', self._update(**req.dict()))
