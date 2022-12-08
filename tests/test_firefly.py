from src_gui4dft.program.firefly import atomic_model_to_firefly_inp
from src_gui4dft.models.swnt import SWNT


def test_atomic_model_to_firefly_inp():
    model = SWNT(3, 3)
    text = atomic_model_to_firefly_inp(model)
    assert len(text) == 714