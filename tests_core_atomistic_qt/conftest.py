from core_atomistic.periodic_table import TPeriodTable
from core_atomistic_qt.qt_graph import PyqtGraphWidget
from core_atomistic_qt.qt_image import PyqtGraphWidgetImage
from qtpy.QtWidgets import QApplication
from pathlib import Path

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


@pytest.fixture
def period_table() -> TPeriodTable:
    return TPeriodTable()


@pytest.fixture
def get_graph_widget(qapp):

    def factory_function():
        widget = PyqtGraphWidget()
        widget.show()
        return widget

    return factory_function


@pytest.fixture
def qsapp(qapp_session) -> QApplication:
    yield qapp_session
    qapp_session.processEvents()
    qapp_session.closeAllWindows()


@pytest.fixture(scope='session')
def qapp_session(qapp):
    return qapp


@pytest.fixture
def graph_widget(get_graph_widget):
    return get_graph_widget()


@pytest.fixture
def get_graph_image_widget(qapp):

    def factory_function():
        widget = PyqtGraphWidgetImage()
        widget.show()
        return widget

    return factory_function


@pytest.fixture
def graph_image_widget(get_graph_image_widget):
    return get_graph_image_widget()
