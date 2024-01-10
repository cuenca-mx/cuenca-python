import pytest

from cuenca import Questionnaires


@pytest.mark.vcr
def test_create_questionnaire():
    qn = Questionnaires.create(
        user_id='US2aaB809x842cq8PxhhdgyC',
        token='some_token',
        form_id='some_form',
    )
    assert qn.id
    assert qn.user_id
    assert qn.form_id
    assert qn.token
