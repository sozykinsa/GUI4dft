from utils import critic2
from utils.importer import Importer
import pytest
import numpy as np


def test_open_xyz_critic_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 301
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].atoms) == 3


def test_create_critic2_xyz_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].bcp) == 5
