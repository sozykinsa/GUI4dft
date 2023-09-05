import math
import numpy as np

from src_gui4dft.program.siesta import TSIESTA
from core_gui_atomistic.helpers import lat_vectors_from_params


def test_lattice_constant(tests_path):
    f_name = str(tests_path / 'ref_data' / 'incorrect' / "siesta-no-lat_const.fdf")
    assert TSIESTA.lattice_constant(f_name) == 1

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    assert TSIESTA.lattice_constant(f_name) == 1.0


def test_siesta_lattice(tests_path):
    f_name = str(tests_path / 'ref_data' / "test_file_01.fdf")
    lats = TSIESTA.lattice_vectors(f_name)
    assert lats is None

    a = 1
    b = 2
    c = 3
    alpha = math.radians(90)
    lats = lat_vectors_from_params(a, b, c, alpha, alpha, alpha)
    assert lats[0][0] == a
    assert lats[2][2] == c

    lats = TSIESTA.lattice_parameters_abc_angles(f_name)
    assert np.array_equal(lats[0], np.array([90.0, 0.0, 0.0]))
    assert np.array_equal(lats[1], np.array([0.0, 90.0, 0.0]))
    assert np.array_equal(lats[2], np.array([0.0, 0.0, 12.2833]))

    f_name = str(tests_path / 'ref_data' / 'incorrect' / "siesta-no-lat_const.fdf")
    lats = TSIESTA.lattice_parameters_abc_angles(f_name)
    assert lats is None


def test_energy_tot(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    e_tot = TSIESTA.energy_tot(f_name)
    assert e_tot == -4965.062613

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta2.out")
    e_tot = TSIESTA.energy_tot(f_name)
    assert e_tot is None


def test_energies(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    energies = TSIESTA.energies(f_name)
    assert len(energies) == 8


def test_spin_polarized(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    assert not TSIESTA.spin_polarized(f_name)


def test_siesta_volume(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    assert TSIESTA.volume(f_name) == 6768.0

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    assert TSIESTA.volume(f_name) is None


def test_system_label(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    assert TSIESTA.system_label(f_name) == "siesta"

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    assert TSIESTA.system_label(f_name) == "siesta"


def test_type_of_run(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    assert TSIESTA.type_of_run(f_name) == "cg"

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    assert TSIESTA.type_of_run(f_name) == "cg"


def test_get_charges_for_atoms(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    mulliken = TSIESTA.get_charges_for_atoms(f_name, "Mulliken")
    assert mulliken[0] == []

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)spin_polarized' / "siesta.out")
    mulliken = TSIESTA.get_charges_for_atoms(f_name, "Mulliken")
    assert mulliken[0] == []

    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-ang-charges' / "siesta.out")
    mulliken = TSIESTA.get_charges_for_atoms(f_name, "Mulliken")
    assert mulliken[0] != []


def test_coord_type(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-scaled' / "siesta.fdf")
    coord_t = TSIESTA.atomic_coordinates_format(f_name)
    assert coord_t == "ScaledCartesian"

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    coord_t = TSIESTA.atomic_coordinates_format(f_name)
    assert coord_t == "NotScaledCartesianAng"
