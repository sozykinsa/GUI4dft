from pathlib import Path
from pyqtgraphwidget import PyqtGraphWidget
from utils.atomic_model import TAtomicModel

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


@pytest.fixture
def h2o_model() -> Path:
    #         x    y    z   let charge
    atoms = [[0.0, 0.0, 0.0, "O", 8], [-1.2, 0.0, 0.0, "H", 1], [1.2, 0.0, 0.0, "H", 1]]
    return TAtomicModel(atoms)


@pytest.fixture
def get_graph_widget(qapp):

    def factory_function():
        widget = PyqtGraphWidget()
        widget.show()
        return widget

    return factory_function


@pytest.fixture
def graph_widget(get_graph_widget):
    return get_graph_widget()

