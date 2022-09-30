from models.atomic_model import TAtomicModel
import pytest
import numpy as np
from copy import copy, deepcopy


def test_atomic_model():
    model = TAtomicModel()
    assert len(model.atoms) == 0


def test_atomic_model_quack_as_ase(h2o_model: TAtomicModel) -> None:
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
    assert model.get_cell()[0] == pytest.approx(model.lat_vector1)
    assert len(model.get_cell()) == 3
    assert model.get_cell().size == 9


def test_twist_z(h2o_model):
    model = h2o_model
    alpha = np.radians(90.0)
    model.twist_z(alpha)
    assert model.atoms[1].x == pytest.approx(-1.2)


def test_get_covalent_radii(h2o_model):
    model = h2o_model
    radii = model.get_covalent_radii()
    assert len(radii) == 2


def test_find_bonds_exact(h2o_model: TAtomicModel) -> None:
    model = h2o_model
    bonds = model.find_bonds_exact()
    assert len(bonds) == 2
    assert bonds[0][-1] == 1
    assert bonds[1][-1] == 2


def test_go_to_positive_coordinates(h2o_model: TAtomicModel) -> None:
    model = h2o_model
    model.go_to_positive_coordinates()
    assert model.atoms[1].x >= 0


def test_formula(h2o_model):
    model = h2o_model
    assert model.formula() == "H2O1"


def test_rotations(h2o_model: TAtomicModel) -> None:
    model_rot_x = copy(h2o_model)
    model_rot_x.rotate_x(30)
    assert model_rot_x.atoms[1].x == pytest.approx(-1.2)

    model_rot_y = copy(h2o_model)
    model_rot_y.rotate_y(30)
    assert model_rot_y.atoms[1].x == pytest.approx(-1.0392304845413265)

    model_rot_z = copy(h2o_model)
    model_rot_z.rotate_z(30)
    assert model_rot_z.atoms[1].x == pytest.approx(-0.9000)

    model_rot_xyz = copy(h2o_model)
    model_rot_xyz.rotate(20.0, 40.0, 50.0)
    assert model_rot_xyz.atoms[1].x == pytest.approx(0.24760705711548658)


def test_add_atom(h2o_model: TAtomicModel) -> None:
    model1 = deepcopy(h2o_model)
    model2 = deepcopy(h2o_model)
    model2.move(0.5, 0.3, 0.4)
    model1.add_atom(model2.atoms[0], 3.1)
    assert len(model1.atoms) == 3
    model1.add_atom(model2.atoms[0], 0.6)
    assert len(model1.atoms) == 4


def test_grow(h2o_model):
    model = h2o_model
    model_x = model.grow_x()
    assert len(model_x.atoms) == 6
    assert model_x.lat_vector1 == pytest.approx(2 * model.lat_vector1)

    model_y = model.grow_y()
    assert len(model_y.atoms) == 6
    assert model_y.lat_vector2 == pytest.approx(2 * model.lat_vector2)

    model_z = model.grow_z()
    assert len(model_z.atoms) == 6
    assert model_z.lat_vector3 == pytest.approx(2 * model.lat_vector3)

    model_xyz = model.grow()
    assert len(model_xyz.atoms) == 81


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


def test_set_lat_vectors(h2o_model):
    model = h2o_model
    model.set_lat_vectors([5, 0, 0], [0, 5, 0], [0, 5])
    model.set_lat_vectors([5, 0, 0], [0, 5, 0], [0, 0, 5])
    assert model.get_angle_gamma() == 90.0
