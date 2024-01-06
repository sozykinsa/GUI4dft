from core_atomistic.atom import Atom


def test_atom():
    data = [1.2, 2.3, 3.4, "He", 2]
    model = Atom(data)
    assert model.x == 1.2
    assert model.charge == 2
    assert not model.is_selected()
    model.set_selected(True)
    assert model.is_selected()
    assert model.to_string() == "He    1.20000000    2.30000000    3.40000000"
