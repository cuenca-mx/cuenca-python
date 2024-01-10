import datetime as dt
from typing import ClassVar, cast

from cuenca_validations.types import QuestionnairesRequest

from ..http import Session, session as global_session
from .base import Creatable, Retrievable


class Questionnaires(Creatable, Retrievable):
    _resource: ClassVar = 'questionnaires'

    created_at: dt.datetime
    token: str
    form_id: str
    user_id: str

    class Config:
        schema_extra = {
            'example': {
                'user_id': 'US234i23jh23h4h23',
                'token': '3223j23ij23ij3',
                'alert_id': 'ALewifjwiejf',
            }
        }

    @classmethod
    def create(
        cls,
        user_id: str,
        token: str,
        form_id: str,
        *,
        session: Session = global_session,
    ) -> 'Questionnaires':
        req = QuestionnairesRequest(
            user_id=user_id,
            token=token,
            form_id=form_id,
        )
        return cast(
            'Questionnaires', cls._create(session=session, **req.dict())
        )
