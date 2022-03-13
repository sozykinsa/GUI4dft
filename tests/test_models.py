from models.capedswcnt import CapedSWNT
from models.graphene import Graphene
from models.bint import BiNT
from models.swnt import SWNT


def test_swnt():
    model = SWNT(7, 7, 0, 1)
    assert len(model.atoms) == 28
    model = SWNT(7, 0, 0, 1)
    assert len(model.atoms) == 28


def test_graphene():
    model = Graphene(7, 7, 5)
    assert len(model.atoms) == 56


def test_tbint():
    model = BiNT(7, 7, 5, tube_type="BN")
    assert len(model.atoms) == 70

    model = BiNT(7, 0, 5, tube_type="BC")
    assert len(model.atoms) == 35


def test_caped_swnt():
    model = CapedSWNT(6, 6, 10, 1, 1, 2, 0, 2, 0)
    assert len(model.atoms) == 144

    model = CapedSWNT(6, 6, 10, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 180

    model = CapedSWNT(6, 6, 0, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 96

    model = CapedSWNT(10, 0, 0, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 90

    model = CapedSWNT(10, 10, 0, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 260

    model = CapedSWNT(19, 0, 0, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 345

