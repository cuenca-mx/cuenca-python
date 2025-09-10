import pytest
from cuenca_validations.types import Profession, SessionType
from pydantic import ValidationError

from cuenca.exc import CuencaResponseException
from cuenca.http import Session as ClientSession
from cuenca.resources import CurpValidation, Session, User


@pytest.mark.vcr
def test_session_create(curp_validation_request: dict, user_request: dict):
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

    ephimeral_cuenca_session = ClientSession()
    ephimeral_cuenca_session.configure(session_token=user_session.id)

    user = User.update(user.id, profession=Profession.comercio)
    assert user.profession == Profession.comercio


@pytest.mark.vcr
def test_session_create_with_resource_id(
    session_with_resource_id: Session,
) -> None:
    assert session_with_resource_id.user_id == 'USPR4JxMuwSG60u2h4gBpB6Q'
    assert session_with_resource_id.resource_id == '68b887f60c33abad1ea841d3'


@pytest.mark.vcr
def test_session_with_resource_id_authorized(
    client_authed_with_session: ClientSession,
) -> None:
    resource_id = '68b887f60c33abad1ea841d3'
    response = client_authed_with_session.get(
        f'onboarding_verifications/{resource_id}'
    )

    assert response['gov_id_document_number'] == '267202610'


@pytest.mark.vcr
def test_session_with_resource_id_unauthorized(
    client_authed_with_session: ClientSession,
) -> None:
    resource_id = '68b887f60c33abad1ea841d4'
    with pytest.raises(CuencaResponseException) as e:
        client_authed_with_session.get(
            f'onboarding_verifications/{resource_id}'
        )
    assert e.value.json['error'] == 'User has not enough permissions'
