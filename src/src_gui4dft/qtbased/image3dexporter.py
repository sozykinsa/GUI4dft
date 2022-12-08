# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QSize
from src_gui4dft.ui.image3D import Ui_MainWindow as Ui_image3D


class Image3Dexporter(QMainWindow):
    def __init__(self, width, height, quality):
        super().__init__()
        self.ui = Ui_image3D()
        self.ui.setupUi(self)
        self.setFixedSize(QSize(width, height))

        self.ui.openGLWidget.set_form_elements(quality=quality)
        self.ui.openGLWidget.filter = None
        self.show()
