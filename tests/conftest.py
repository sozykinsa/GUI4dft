from pathlib import Path
from pyqt_graph_widget.pygrwidget import PyqtGraphWidget

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


@pytest.fixture
def graph_widget(qapp):
    widget = PyqtGraphWidget()
    return widget
