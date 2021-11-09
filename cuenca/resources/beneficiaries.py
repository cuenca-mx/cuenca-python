import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Deactivable, Queryable, Retrievable, Updateable


# pasar a cuenca-validations
class BeneficiaryRequest(BaseModel):
    user_id: Optional[str]
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int


@dataclass
class Beneficiary(Creatable, Retrievable, Updateable, Queryable, Deactivable):
    _resource: ClassVar = 'beneficiaries'

    id: str
    created_at: dt.datetime
    updated_at: dt.datetime
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int
    desctivated_at: dt.datetime

    user_uri: str

    @classmethod
    def create(
        cls,
        user_id: str,
        name: str,
        birth_date: dt.datetime,
        phone_number: str,
        user_relationship: str,
        percentage: int,
        *,
        session: Session = global_session,
    ):
        req = BeneficiaryRequest(
            user_id=user_id,
            name=name,
            birth_date=birth_date,
            phone_number=phone_number,
            user_relationship=user_relationship,
            percentage=percentage,
        )
        return cast('Beneficiary', cls._create(session=session, **req.dict()))
