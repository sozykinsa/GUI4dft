# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QSize
from ui.image3D import Ui_MainWindow as Ui_image3D
from qtbased.guiopengl import GuiOpenGL


class Image3Dexporter(QMainWindow):
    def __init__(self, windowsWidth, windowsHeight, quality):
        super(Image3Dexporter, self).__init__()
        self.ui = Ui_image3D()
        self.ui.setupUi(self)
        self.setFixedSize(QSize(windowsWidth, windowsHeight))

        self.MainForm = GuiOpenGL(self.ui.openGLWidget)
        self.MainForm.set_form_elements(quality=quality)
        self.MainForm.filter = None
        self.show()
