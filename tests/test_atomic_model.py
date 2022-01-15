from utils.atomic_model import TAtomicModel


def test_atomic_model():
    model = TAtomicModel()
    assert len(model.atoms) == 0

