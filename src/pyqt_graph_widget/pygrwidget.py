# -*- coding: utf-8 -*-
# ------------------------------------------------------
# ------------------ PyqtGraphWidget -------------------
# ------------------------------------------------------
#https://www.pythonguis.com/tutorials/pyside-plotting-pyqtgraph/

from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtGui import QFont
import pyqtgraph as pg  # pip install pyqtgraph
import sys


class PyqtGraphWidget(QWidget):

    COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.graphWidget = pg.PlotWidget()
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.graphWidget)
        self.setLayout(vertical_layout)
        self.graphWidget.setBackground((255, 255, 255))
        self.styles = {"color": "#000", "font-size": "20px"}

    def clear(self):
        self.graphWidget.clear()

    def plot(self, x: list[list[float]], y: list[list[float]], labels: list[str],
             title: str, x_title: str, y_title: str):
        font = QFont()
        font.setPixelSize(20)
        self.graphWidget.getAxis("bottom").setStyle(tickFont=font)
        self.graphWidget.getAxis("bottom").setStyle(color=(0, 0, 0))
        self.graphWidget.getAxis("left").setStyle(tickFont=font)
        # Add Title
        self.graphWidget.setTitle(title, color=self.COLORS[0], size="20pt")
        # Add Axis Labels
        self.graphWidget.setLabel("left", y_title, **self.styles)
        self.graphWidget.setLabel("bottom", x_title, **self.styles)

        for index in range(len(x)):
            pen = pg.mkPen(color=self.COLORS[index], width=4)
            self.graphWidget.plot(x[index], y[index], name=labels[index], pen=pen, font=font)

    def add_line(self, _pos, _angle, _width, _style):
        # _style: Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine
        pen = pg.mkPen(color=self.COLORS[0], width=_width, style=_style)
        line = pg.InfiniteLine(pos=_pos, angle=_angle, pen=pen)
        self.graphWidget.addItem(line)

    def add_legend(self):
        self.graphWidget.addLegend(labelTextSize='15pt', **self.styles)
