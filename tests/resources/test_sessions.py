from typing import Dict

import pytest
from cuenca_validations.types import SessionType

import cuenca
from cuenca.resources import CurpValidation, Session, User


@pytest.mark.vcr
def test_create_session(curp_validation_request: Dict, user_request: Dict):
    curp_valdation = CurpValidation.create(**curp_validation_request)
    user_request['curp'] = curp_valdation.validated_curp
    user = User.create(**user_request)

    user_session = Session.create(
        user.id,
        SessionType.registration,
        success_url='https://example.com/succeeded_registration',
        failure_url='https://example.com/failed_registration',
    )

    ephimeral_cuenca_session = cuenca.Session()
    ephimeral_cuenca_session.configure(session_token=user_session.id)
    user = User.update(user.id, email_address='manu@example.com')
    assert user.email_address == 'manu@example.com'
