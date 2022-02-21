from mainwindow import mainWindow
from PySide2.QtWidgets import QApplication
import sys
from PySide2.QtCore import QCoreApplication, Qt


def test_gui4dft_run():
    ORGANIZATION_NAME = 'SUSU'
    ORGANIZATION_DOMAIN = 'susu.ru'
    APPLICATION_NAME = 'gui4dft'

    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = mainWindow()
    window.setup_ui()
    window.show()
    window.start_program()

    assert window.models == []
