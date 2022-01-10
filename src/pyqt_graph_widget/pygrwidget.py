# -*- coding: utf-8 -*-
# ------------------------------------------------------
# ------------------ PyqtGraphWidget -------------------
# ------------------------------------------------------
#https://www.pythonguis.com/tutorials/pyside-plotting-pyqtgraph/

from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtGui import QFont
import pyqtgraph as pg  # pip install pyqtgraph


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
        self.legend_item = None

    def clear(self):
        self.graphWidget.clear()

    def plot_dos(self, x: list[list[float]], y: list[list[float]], labels: list[str],
             title: str, x_title: str, y_title: str):
        font = QFont()
        font.setPixelSize(20)
        self.graphWidget.getAxis("bottom").setStyle(tickFont=font)
        self.graphWidget.getAxis("left").setStyle(tickFont=font)
        # Add Title
        self.graphWidget.setTitle(title, color=self.COLORS[0], size="20pt")
        # Add Axis Labels
        self.graphWidget.setLabel("left", y_title, **self.styles)
        self.graphWidget.setLabel("bottom", x_title, **self.styles)

        n_plots = len(y)
        for index in range(n_plots):
            pen = pg.mkPen(color=self.COLORS[index], width=4)
            self.graphWidget.plot(x[index], y[index], name=labels[index],  pen=pen, font=font)

    def plot(self, x: list[list[float]], y: list[list[float]], labels: list[str],
             title: str, x_title: str, y_title: str, is_colored=True):
        # Axis
        font = QFont()
        font.setPixelSize(20)
        self.graphWidget.getAxis("bottom").setStyle(tickFont=font)
        self.graphWidget.getAxis("left").setStyle(tickFont=font)
        pen = pg.mkPen(color=self.COLORS[0])
        self.graphWidget.getAxis("bottom").setTextPen(pen)
        self.graphWidget.getAxis("left").setTextPen(pen)
        # Add Title
        self.graphWidget.setTitle(title, color=self.COLORS[0], size="20pt")
        # Add Axis Labels
        self.graphWidget.setLabel("left", y_title, **self.styles)
        self.graphWidget.setLabel("bottom", x_title, **self.styles)

        n_plots = len(y)
        for index in range(n_plots):
            pen = pg.mkPen(color=self.COLORS[index % len(self.COLORS) if is_colored else 0], width=4)
            self.graphWidget.plot(x[index % len(x)], y[index], name=labels[index % len(labels)],  pen=pen, font=font)

    def add_line(self, _pos, _angle, _width, _style):
        # _style: Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine
        pen = pg.mkPen(color=self.COLORS[0], width=_width, style=_style)
        line = pg.InfiniteLine(pos=_pos, angle=_angle, pen=pen)
        self.graphWidget.addItem(line)

    def add_legend(self):
        self.legend_item = self.graphWidget.addLegend()
        self.legend_item.setLabelTextSize('15pt')
        self.legend_item.setLabelTextColor(pg.mkColor(0, 0, 0))

    def set_limits(self, x_min, x_max, y_min, y_max):
        self.graphWidget.setXRange(x_min, x_max, padding=0)
        self.graphWidget.setYRange(y_min, y_max, padding=0)

    def enableAutoRange(self):
        self.graphWidget.enableAutoRange()

    def set_xticks(self, ticks):
        self.graphWidget.getAxis("bottom").setTicks(ticks)
