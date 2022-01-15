from utils.models import TSWNT, TGraphene, TBiNT, TCapedSWNT


def test_swnt():
    model = TSWNT(7, 7, 0, 1)
    assert len(model.atoms) == 28
    model = TSWNT(7, 0, 0, 1)
    assert len(model.atoms) == 28


def test_graphene():
    model = TGraphene(7, 7, 5)
    assert len(model.atoms) == 56


def test_tbint():
    model = TBiNT(7, 7, 5, tubetype="BN")
    assert len(model.atoms) == 70


def test_caped_swnt():
    model = TCapedSWNT(6, 6, 10, 1, 1, 2, 0, 2, 0)
    assert len(model.atoms) == 144
    model = TCapedSWNT(6, 6, 10, 1, 2, 2, 0, 2, 0)
    assert len(model.atoms) == 180
