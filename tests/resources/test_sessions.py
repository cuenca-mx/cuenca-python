from typing import Dict

import pytest
from cuenca_validations.types import SessionType
from pydantic import ValidationError

import cuenca
from cuenca.resources import CurpValidation, Session, User


@pytest.mark.vcr
def test_session_create(curp_validation_request: Dict, user_request: Dict):
    curp_valdation = CurpValidation.create(**curp_validation_request)
    user_request['curp'] = curp_valdation.validated_curp
    user = User.create(**user_request)

    success_url = 'no url'
    with pytest.raises(ValidationError):
        user_session = Session.create(
            user.id,
            SessionType.registration,
            success_url=success_url,
        )

    success_url = 'https://example.com/succeeded_registration'
    failure_url = 'https://example.com/failed_registration'

    user_session = Session.create(
        user.id,
        SessionType.registration,
        success_url=success_url,
        failure_url=failure_url,
    )

    assert user_session.user_id == user.id
    assert user_session.type == SessionType.registration
    assert user_session.success_url == success_url
    assert user_session.failure_url == failure_url

    ephimeral_cuenca_session = cuenca.http.Session()
    ephimeral_cuenca_session.configure(session_token=user_session.id)
    user = User.update(user.id, email_address='manu@example.com')
    assert user.email_address == 'manu@example.com'
