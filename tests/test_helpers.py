from utils import helpers


def test_helpers_spacedel():
    row = " qws  sddd  as "
    assert "qws sddd as" == helpers.spacedel(row)


def test_helpers_numbers_and_strings():
    assert "123.00000000" == helpers.float_to_string(123.0)
    assert helpers.is_number("3")
    assert helpers.is_number("2.7")
    assert not helpers.is_number("abc")
    assert helpers.is_integer(3)
    assert helpers.is_integer(-4)
    assert not helpers.is_integer(3.4)
