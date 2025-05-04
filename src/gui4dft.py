# -*- coding: utf-8 -*-
import os
try:
    if os.environ["XDG_SESSION_TYPE"] == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
except Exception as e:
    print(str(e))
import sys
from pathlib import Path
import platform
from qtpy import PYSIDE_VERSION
from qtpy import PYQT_VERSION

from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication

from qtbased.gui4dftform import MainForm

print("Python version: ", platform.python_version())
if PYSIDE_VERSION is not None:
    print("PySide version: ", PYSIDE_VERSION)
if PYQT_VERSION is not None:
    print("PyQt version: ", PYQT_VERSION)

sys.path.append('.')

is_with_figure = True

ORGANIZATION_NAME = 'SUSU'
ORGANIZATION_DOMAIN = 'susu.ru'
APPLICATION_NAME = 'gui4dft'

QCoreApplication.setApplicationName(ORGANIZATION_NAME)
QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
QCoreApplication.setApplicationName(APPLICATION_NAME)

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)
window = MainForm()
window.setup_ui()
if is_with_figure:
    window.setWindowIcon(QIcon(str(Path(__file__).parent / 'images' / 'ico.png')))
window.show()
window.start_program()

sys.exit(app.exec_())
