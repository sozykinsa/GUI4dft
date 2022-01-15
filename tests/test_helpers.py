from utils.helpers import Helpers


def test_helpers_spacedel():
    row = " qws  sddd  as "
    assert "qws sddd as" == Helpers.spacedel(row)


def test_helpers_numbers_and_strings():
    assert "123.00000000" == Helpers.float_to_string(123.0)
    assert Helpers.is_number("3")
    assert Helpers.is_number("2.7")
    assert not Helpers.is_number("abc")
    assert Helpers.is_integer(3)
    assert Helpers.is_integer(-4)
    assert not Helpers.is_integer(3.4)
