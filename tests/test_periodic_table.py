
def test_periodic_table(period_table):
    assert "H" == period_table.get_let(1)


def test_get_color(period_table):
    assert period_table.get_color(6) == period_table.Atoms[6].color
    assert period_table.get_color(300) == period_table.default_color


def test_get_rad(period_table):
    assert period_table.get_rad(6) == period_table.Atoms[6].radius
    assert period_table.get_rad(300) == period_table.default_radius


def test_get_let(period_table):
    assert period_table.get_let(6) == "C"
    assert period_table.get_let(300) == "Direct"


def test_get_get_charge_by_letter(period_table):
    assert 200 == period_table.get_charge_by_letter("Direct")
    assert 6 == period_table.get_charge_by_letter("C")


def test_get_all_letters(period_table):
    letters = period_table.get_all_letters()
    assert len(letters) == period_table.table_size
    assert letters[0] == " "
    assert letters[1] == "H"


def test_get_all_colors(period_table):
    colors = period_table.get_all_colors()
    assert len(colors) == period_table.table_size
