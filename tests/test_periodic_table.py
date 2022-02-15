
def test_periodic_table(period_table):
    assert "H" == period_table.get_let(1)


def test_get_color(period_table):
    assert period_table.get_color(300) == period_table.default_color


def test_get_rad(period_table):
    assert period_table.get_rad(300) == period_table.default_radius
