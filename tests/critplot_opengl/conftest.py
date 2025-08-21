from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtWidgets import QApplication
from src_critplot.qtbased.guiopengl_cp import GuiOpenGLCP
from src_critplot.qtbased.critplotform import MainForm
from src_critplot.models.cp_model import AtomicModelCP

import pytest


@pytest.fixture
def qsapp(qapp_session) -> QApplication:
    yield qapp_session
    qapp_session.processEvents()
    qapp_session.closeAllWindows()


@pytest.fixture
def get_guiopengl_widget(qsapp):

    def factory_function():
        widget = GuiOpenGLCP()
        widget.show()
        return widget

    return factory_function


@pytest.fixture(scope='session')
def qapp_session(qapp):
    return qapp


@pytest.fixture
def guiopengl_widget(get_guiopengl_widget):
    return get_guiopengl_widget()


@pytest.fixture
def get_guiopengl_model_widget(qapp, h2o_model):

    def factory_function():
        atomscolors = [[0.0, 0.0, 0.9], [0.0, 0.0, 0.9], [0.0, 0.0, 0.9], [0.0, 0.0, 0.9], [0.0, 0.0, 0.9],
                       [0.0, 0.0, 0.9], [0.0, 0.0, 0.9], [0.0, 0.0, 0.9], [0.0, 0.0, 0.9]]
        ViewAtoms = True
        ViewAtomNumbers = True
        ViewBox = True
        boxcolor = (0.0, 0.0, 0.0)
        ViewBonds = True
        bondscolor = (0.9, 0.0, 0.9)
        bondWidth = 2
        Bonds_by_atoms = True
        ViewAxes = True
        axescolor = (0.0, 0.0, 0.9)
        contour_width = 5
        widget = GuiOpenGLCP()
        widget.show()
        widget.set_atomic_structure(h2o_model, atomscolors, ViewAtoms, ViewAtomNumbers, ViewBox, boxcolor, ViewBonds,
                                    bondscolor, bondWidth, Bonds_by_atoms, ViewAxes, axescolor, contour_width)
        return widget

    return factory_function


@pytest.fixture
def guiopengl_model_widget(get_guiopengl_model_widget):
    return get_guiopengl_model_widget()


@pytest.fixture
def get_application(qsapp):

    def factory_function():
        ORGANIZATION_NAME = 'SUSU'
        ORGANIZATION_DOMAIN = 'susu.ru'
        APPLICATION_NAME = 'CritPlot'

        QCoreApplication.setApplicationName(ORGANIZATION_NAME)
        QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
        QCoreApplication.setApplicationName(APPLICATION_NAME)

        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        window = MainForm()
        window.setup_ui()
        window.show()
        window.start_program()
        return window

    return factory_function


@pytest.fixture
def critplot_application(get_application):
    return get_application()


@pytest.fixture
def h2o_model_cp() -> AtomicModelCP:
    #         x    y    z   let charge
    atoms = [[0.0, 0.0, 0.0, "O", 8], [-1.0, 0.0, 0.0, "H", 1], [1.0, 0.0, 0.0, "H", 1]]
    return AtomicModelCP(atoms)
