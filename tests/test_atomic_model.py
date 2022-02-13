from utils.atomic_model import TAtomicModel
import numpy as np


def test_atomic_model():
    model = TAtomicModel()
    assert len(model.atoms) == 0


def test_atomic_model_quack_as_ase(h2o_model):
    model = h2o_model
    assert len(model.atoms) == 3
    pos = model.get_positions()
    assert type(pos) == np.ndarray
    assert len(pos) == 3
    num = model.get_atomic_numbers()
    assert type(num) == np.ndarray
    assert len(num) == 3


def test_find_bonds_exact(h2o_model):
    model = h2o_model
    bonds = model.find_bonds_exact()
    assert len(bonds) == 2
    assert bonds[0][-1] == 1
    assert bonds[1][-1] == 2


def test_atom_atom_distance(h2o_model):
    model = h2o_model
    assert round(model.atom_atom_distance(0, 1), 4) == 1.2
    assert round(model.atom_atom_distance(1, 2), 4) == 2.4
