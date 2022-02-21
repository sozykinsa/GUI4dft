from models.atomic_model import TAtomicModel
import pytest
import numpy as np
from copy import deepcopy


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
    cm = model.get_center_of_mass()
    assert type(cm) == np.ndarray
    assert cm == pytest.approx(np.array([0.0,  0.0,  0.0]))
    tags = model.get_tags()
    assert tags == []


def test_find_bonds_exact(h2o_model):
    model = h2o_model
    bonds = model.find_bonds_exact()
    assert len(bonds) == 2
    assert bonds[0][-1] == 1
    assert bonds[1][-1] == 2


def test_grow(h2o_model):
    model = h2o_model
    model_x = model.grow_x()
    assert len(model_x.atoms) == 6
    assert model_x.LatVect1 == pytest.approx(2 * model.LatVect1)

    model_y = model.grow_y()
    assert len(model_y.atoms) == 6
    assert model_y.LatVect2 == pytest.approx(2 * model.LatVect2)

    model_z = model.grow_z()
    assert len(model_z.atoms) == 6
    assert model_z.LatVect3 == pytest.approx(2 * model.LatVect3)


def test_move(h2o_model):
    model = h2o_model
    model_move = deepcopy(h2o_model)
    model_move.move(1.0, 2.0, 3.0)
    assert model.atoms[0].x + 1.0 == model_move.atoms[0].x
    assert model.atoms[0].y + 2.0 == model_move.atoms[0].y
    assert model.atoms[0].z + 3.0 == model_move.atoms[0].z


def test_atom_atom_distance(h2o_model):
    model = h2o_model
    assert round(model.atom_atom_distance(0, 1), 4) == 1.2
    assert round(model.atom_atom_distance(1, 2), 4) == 2.4
