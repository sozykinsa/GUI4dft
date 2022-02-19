from models.atom import Atom


def test_atom():
    data = [1.2, 2.3, 3.4, "He", 2]
    model = Atom(data)
    assert model.x == 1.2
    assert model.charge == 2
