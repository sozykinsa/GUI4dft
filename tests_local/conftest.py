from pathlib import Path
from pyqt_graph_widget.pyqtgraphwidget import PyqtGraphWidget

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


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
