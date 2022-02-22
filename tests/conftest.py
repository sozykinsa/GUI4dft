from pathlib import Path
from qtbased.pyqtgraphwidget import PyqtGraphWidget
from qtbased.pyqtgraphwidgetimage import PyqtGraphWidgetImage
from models.atomic_model import TAtomicModel
from utils.periodic_table import TPeriodTable

from qtbased.mainwindow import mainWindow
from PySide2.QtCore import QCoreApplication, Qt

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
def period_table() -> Path:
    return TPeriodTable()


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


@pytest.fixture
def get_application(qapp):

    def factory_function():
        ORGANIZATION_NAME = 'SUSU'
        ORGANIZATION_DOMAIN = 'susu.ru'
        APPLICATION_NAME = 'gui4dft'

        QCoreApplication.setApplicationName(ORGANIZATION_NAME)
        QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
        QCoreApplication.setApplicationName(APPLICATION_NAME)

        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        window = mainWindow()
        window.setup_ui()
        window.show()
        window.start_program()
        return window

    return factory_function


@pytest.fixture
def gui4dft_application(get_application):
    return get_application()
