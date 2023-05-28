from core_gui_atomistic_qt.pyqtgraphwidget import PyqtGraphWidget
from core_gui_atomistic_qt.pyqtgraphwidgetimage import PyqtGraphWidgetImage

import pytest


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
