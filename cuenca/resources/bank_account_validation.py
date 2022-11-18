import datetime as dt
from typing import ClassVar, Optional, cast

from clabe import Clabe
from cuenca_validations.types import (
    BankAccountStatus,
    BankAccountValidationQuery,
    BankAccountValidationRequest,
    Country,
    CurpField,
    Gender,
    Rfc,
    State,
)

from ..http import Session, session as global_session
from .base import Creatable, Queryable, Retrievable


class BankAccountValidation(Creatable, Retrievable, Queryable):
    _resource: ClassVar = 'bank_account_validations'
    _query_params: ClassVar = BankAccountValidationQuery

    updated_at: dt.datetime
    status: BankAccountStatus
    platform_id: str
    clabe: Clabe
    transfer_id: str
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    curp: Optional[CurpField] = None
    rfc: Optional[Rfc] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[dt.date] = None
    state_of_birth: Optional[State] = None
    nationality: Optional[Country] = None
    country_of_birth: Optional[Country] = None

    class Config:
        schema_extra = {
            'example': {
                'id': 'BAbUFjZTUbR3Oqj3vvzHcwBg',
                'created_at': '2022-11-16T17:15:35.288128',
                'updated_at': '2022-11-16T17:15:35.288128',
                'status': 'succeeded',
                'platform_id': 'PT-123',
                'clabe': '127841000000000003',
                'transfer_id': 'TR-123',
                'names': 'José',
                'first_surname': 'López',
                'second_surname': 'Pérez',
                'curp': 'LOPJ900101HDFPRS04',
                'rfc': 'LOPJ9001016S5',
                'gender': 'male',
                'date_of_birth': '1990-01-01',
                'state_of_birth': 'DF',
                'nationality': 'MX',
                'country_of_birth': 'MX',
            }
        }

    @classmethod
    def create(
        cls,
        clabe: Clabe,
        session: Session = global_session,
    ) -> 'BankAccountValidation':
        req = BankAccountValidationRequest(clabe=clabe)
        return cast(
            'BankAccountValidation',
            cls._create(session=session, **req.dict()),
        )
