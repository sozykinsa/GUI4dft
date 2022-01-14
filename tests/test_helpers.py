from utils.AdvancedTools import Helpers


def test_helpers_spacedel():
    row = " qws  sddd  as "
    assert "qws  sddd  as" == Helpers.spacedel(row)
