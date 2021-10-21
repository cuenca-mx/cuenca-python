import pytest

from cuenca.resources import UserPldRiskLevel


@pytest.mark.vcr
def test_create_user_pld_risk_level() -> None:
    risk = UserPldRiskLevel.create('US6D1wbTEdLuTjf227iF05js', 0.7)
    assert risk.level == 0.7
    assert risk.is_user_defined
