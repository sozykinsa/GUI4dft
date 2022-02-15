import numpy as np

from utils import helpers


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
    assert '\u039B' == helpers.utf8_letter(r'\Lambda')


def test_list_n2_split():
    data = [[0.0, 1.0], [2.3, 3.2], [4.1, 5.6]]
    x, y = helpers.list_n2_split(data)
    assert len(x) == 3
    assert len(y) == 3
    assert type(x) == np.ndarray


def test_getsubs():
    dirs, files = helpers.getsubs(".")
    assert len(dirs) > 0
