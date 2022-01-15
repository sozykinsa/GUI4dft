from utils.periodic_table import TPeriodTableAtom, TPeriodTable


def test_periodic_table():
    mendeley = TPeriodTable()
    assert "H" == mendeley.get_let(1)

