from thirdparty.crystal import model_1d_to_d12, model_2d_to_d12
from thirdparty.crystal import number_of_atoms_from_outp, get_cell, atomic_data_from_output
from utils.importer import Importer
import numpy as np
import pytest


def test_model_1d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model_1d_to_d12(model[0])) == 16285


def test_model_2d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model_2d_to_d12(model[0])) == 17854


def test_number_of_atoms_from_outp(tests_path):
    f_name = str(tests_path / 'ref_data' / 'topond' / "topond-I.outp")
    n = number_of_atoms_from_outp(f_name)
    assert n == 4


def test_get_cell(tests_path):
    f_name = str(tests_path / 'ref_data' / 'topond' / "topond-I.outp")
    cell = get_cell(f_name)
    assert len(cell) == 3
    assert np.array(cell[0]) == pytest.approx(np.array([3.57945, 2.34575, 0.00000]))


def test_atomic_data_from_output(tests_path):
    f_name = str(tests_path / 'ref_data' / 'topond' / "topond-I.outp")
    models = atomic_data_from_output(f_name)
    pos = models[0].get_positions()
    assert len(pos) == 4
