import pytest
from ase.data import covalent_radii
from ase.data.colors import cpk_colors, jmol_colors


def test_periodic_table(period_table):
    assert "H" == period_table.get_let(1)


def test_get_color(period_table):
    if period_table.color_of_atoms_scheme == "cpk":
        assert period_table.get_color(6) == pytest.approx(cpk_colors[6])
    elif period_table.color_of_atoms_scheme == "jmol":
        assert period_table.get_color(6) == pytest.approx(jmol_colors[6])
    else:
        period_table.init_manual_colors()
        assert period_table.get_color(6) == pytest.approx(period_table.manual_colors[6])

    period_table.set_color_mode("cpk")
    assert period_table.get_color(6) == pytest.approx(cpk_colors[6])
    period_table.set_color_mode("jmol")
    assert period_table.get_color(6) == pytest.approx(jmol_colors[6])

    assert period_table.get_color(300) == pytest.approx(period_table.default_color)


def test_get_rad(period_table):
    assert period_table.get_rad(6) == covalent_radii[6] * 100.0
    assert period_table.get_rad(300) == period_table.default_radius


def test_get_covalent_radii(period_table):
    radii = period_table.get_covalent_radii([2, 4])
    assert len(radii) == 2


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

    period_table.set_color_mode("cpk")
    colors = period_table.get_all_colors()
    assert len(colors) == period_table.table_size

    period_table.set_color_mode("jmol")
    colors = period_table.get_all_colors()
    assert len(colors) == period_table.table_size


def test_set_manual_colors(period_table):
    period_table.set_color_mode("man")
    period_table.set_manual_color(0, (0.5, 0.4, 0.3))
    colors = period_table.get_all_colors()
    assert colors[0] == pytest.approx(period_table.default_color)
    period_table.set_manual_color(0, (0.5, 0.4, 0.3, 1.0))
    colors = period_table.get_all_colors()
    assert colors[0] == pytest.approx((0.5, 0.4, 0.3, 1.0))
    text = period_table.manual_color_to_text()
    assert len(text) == 1664
