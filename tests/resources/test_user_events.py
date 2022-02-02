import pytest
from cuenca_validations.types import EventType

from cuenca import UserEvent


@pytest.mark.vcr
def test_user_event_retrieve():
    user_id = 'US2v9UT-ESS-yozbtx3W6tOg'
    user_event = UserEvent.one(user_id=user_id, type=EventType.created)
    assert user_event.id is not None
