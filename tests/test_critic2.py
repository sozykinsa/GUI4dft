from utils import critic2
import pytest
import numpy as np


def test_create_critic2_xyz_file(tests_path):
    fname = tests_path / 'tmp_dir' / "critic_xyz_file.xyz"
    #critic2.create_critic2_xyz_file(bcp, bcp_seleсted, fname, is_with_selected, model)
    #lat1, lat2, lat3 = TSIESTA.lattice_vectors(tests_path / 'ref_data' / "test_file_01.fdf")
    #assert lat1 == [False, False, False]
    #a = 1
    #b = 2
    #c = 3
    #lat1, lat2, lat3 = TSIESTA.lat_vectors_from_params(a, b, c, 90, 90, 90)
    #assert lat1 == [1, 0, 0]

