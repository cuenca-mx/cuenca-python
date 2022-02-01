import pytest
from cuenca_validations.types import EventType

from cuenca import UserEvent


@pytest.mark.vcr
def test_retrieve_user_event():
    user_id = 'US7Xdn8jjsQgev8t9z5CyvZA'
    user_event = UserEvent.one(user_id=user_id, type=EventType.created)
    assert user_event.id is not None
