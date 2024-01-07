from pathlib import Path
from core_atomistic.atomic_model import AtomicModel
from core_atomistic.periodic_table import TPeriodTable

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


@pytest.fixture
def period_table() -> TPeriodTable:
    return TPeriodTable()


@pytest.fixture
def h2o_model() -> AtomicModel:
    #         x    y    z   let charge
    atoms = [[0.0, 0.0, 0.0, "O", 8], [-1.0, 0.0, 0.0, "H", 1], [1.0, 0.0, 0.0, "H", 1]]
    return AtomicModel(atoms)


@pytest.fixture
def swnt_33() -> AtomicModel:
    #         x    y    z   let charge
    atoms = [[-0.70056811, 1.92479506, - 0.61920816, "C", 6], [-1.31663736, - 1.56910731, - 0.61920816, "C", 6],
             [-2.01720547, - 0.35568775, - 0.61920816, "C", 6], [2.01720547, - 0.35568775, - 0.61920816, "C", 6],
             [1.31663736, - 1.56910731, - 0.61920816, "C", 6], [0.70056811, 1.92479506, - 0.61920816, "C", 6],
             [-1.31663736, 1.56910731, 0.61920816, "C", 6], [-0.70056811, - 1.92479506, 0.61920816, "C", 6],
             [-2.01720547, 0.35568775, 0.61920816, "C", 6], [2.01720547, 0.35568775, 0.61920816, "C", 6],
             [0.70056811, - 1.92479506, 0.61920816, "C", 6], [1.31663736, 1.56910731, 0.61920816, "C", 6]]
    return AtomicModel(atoms)
