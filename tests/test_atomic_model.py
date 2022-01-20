from utils.atomic_model import TAtomicModel
import numpy as np


def test_atomic_model():
    model = TAtomicModel()
    assert len(model.atoms) == 0


def test_atomic_model_quack_as_ase():
    #         x    y    z   let charge
    atoms = [[0.0, 0.0, 0.0, "O", 8], [-1.2, 0.0, 0.0, "H", 1], [1.2, 0.0, 0.0, "H", 1]]
    model = TAtomicModel(atoms)
    assert len(model.atoms) == 3
    pos = model.get_positions()
    assert type(pos) == np.ndarray
    assert len(pos) == 3
    num = model.get_atomic_numbers()
    assert type(num) == np.ndarray
    assert len(num) == 3
