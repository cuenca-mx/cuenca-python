import pytest

from cuenca.http.client import Session
from cuenca.resources import Agent, AgentVerification

@pytest.mark.vcr
def test_agent_create():
    verification = AgentVerification.create() # Created by user in APP
    agent_session = Session()
    agent_session.configure(sandbox=True)
    agent = Agent.create(
        pairing_code=verification.pairing_code,
        phone_number=verification.phone_number,
        device_info={'client': 'cursor', 'os': 'macOS'},
        session=agent_session,
    )
    assert agent.id
    assert agent.agent_verification_id == verification.id
    assert agent.session_id
    assert agent.user_id
    assert agent.platform_id
