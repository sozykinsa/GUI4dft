import numpy as np

from core_gui_atomistic import helpers


def test_helpers_spacedel():
    row = " qws  sddd  as "
    assert "qws sddd as" == helpers.spacedel(row)


def test_helpers_numbers_and_strings():
    assert "123.00000000" == helpers.float_to_string(123.0)
    assert "  0.00000000" == helpers.float_to_string(-1e-10)
    assert helpers.is_number("3")
    assert helpers.is_number("2.7")
    assert not helpers.is_number("abc")
    assert helpers.is_integer(3)
    assert helpers.is_integer(-4)
    assert not helpers.is_integer(3.4)


def test_utf8_letter():
    assert '\u0393' == helpers.utf8_letter(r'\Gamma')
    assert '\u0394' == helpers.utf8_letter(r'\Delta')
    assert '\u039B' == helpers.utf8_letter(r'\Lambda')
    assert '\u03A0' == helpers.utf8_letter(r'\Pi')
    assert '\u03A3' == helpers.utf8_letter(r'\Sigma')
    assert '\u03A9' == helpers.utf8_letter(r'\Omega')


def test_list_n2_split():
    data = [[0.0, 1.0], [2.3, 3.2], [4.1, 5.6]]
    x, y = helpers.list_n2_split(data)
    assert len(x) == 3
    assert len(y) == 3
    assert type(x) == np.ndarray


def test_getsubs():
    dirs, files = helpers.getsubs(".")
    assert len(dirs) > 0


def test_cdev():
    assert helpers.cdev(5, 3) == 1
    assert helpers.cdev(6, 3) == 3
    assert helpers.cdev(3, 6) == 3
