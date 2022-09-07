import datetime as dt
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    BankAccountStatus,
    BankAccountValidationRequest,
    CurpField,
    Rfc,
)

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class BankAccountValidation(Creatable, Retrievable):
    _resource: ClassVar = 'bank_account_validations'

    created_at: dt.datetime
    account_number: Optional[str] = None
    account_holder: Optional[str] = None
    bank_code: Optional[str] = None
    status: Optional[BankAccountStatus] = None
    curp: Optional[CurpField] = None
    rfc: Optional[Rfc] = None

    class Config:
        fields = {
            'account_number': {
                'description': 'Account number for validation, can be CARD_NUMBER or CLABE'
            },
            'account_holder': {
                'description': 'The fullname of the owner from the account'
            },
            'bank_code': {
                'description': 'Code of the bank according to https://es.wikipedia.org/wiki/CLABE, this can '
                'be retrived from our library https://github.com/cuenca-mx/clabe-python'
            },
            'status': {
                'description': 'Initial status is submitted, then if everthing its fine or not the status can be '
                'succeeded or failed'
            },
        }
        schema_extra = {
            'example': {
                'id': 'CVNEUInh69SuKXXmK95sROwQ',
                'created_at': '2019-08-24T14:15:22Z',
                'account_number': '646180157098510917',
                'account_holder': 'Pedrito Sola',
                'bank_code': '90646',
                'status': 'succedded',
                'curp': 'GOCG650418HVZNML08',
                'rfc': 'GOCG650418HV9',
            }
        }

    @classmethod
    def create(
        cls,
        account_number: str,
        bank_code: str,
        session: Session = global_session,
    ) -> 'BankAccountValidation':
        req = BankAccountValidationRequest(
            account_number=account_number,
            bank_code=bank_code,
        )
        return cast(
            'BankAccountValidation',
            cls._create(session=session, **req.dict()),
        )
