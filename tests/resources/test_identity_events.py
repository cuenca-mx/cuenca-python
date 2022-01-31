import pytest
from cuenca_validations.types import EventType

from cuenca import IdentityEvent


@pytest.mark.vcr
def test_retrieve_identity_event():
    identity_id = 'IDEz-f3BebS4ejwWkdJr72Lg'
    identity_event = IdentityEvent.one(
        identity_id=identity_id, type=EventType.created.value
    )
    assert identity_event.id is not None
