# -*- coding: utf-8 -*-
# ------------------------------------------------------
# ------------------ PyqtGraphWidget -------------------
# ------------------------------------------------------
#https://www.pythonguis.com/tutorials/pyside-plotting-pyqtgraph/

from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtGui import QFont
import pyqtgraph as pg  # pip install pyqtgraph
import numpy as np
from typing import List


class PyqtGraphWidget(QWidget):

    COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.graphWidget = pg.PlotWidget()
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.graphWidget)
        self.setLayout(vertical_layout)

        self.line_width = 2

        self.font_size_title = 20
        self.font_size_axes = 20
        self.font_size_legend = 20

        self.font_color = self.COLORS[0]
        self.font_pen = pg.mkPen(color=self.font_color)

        self.graphWidget.setBackground((255, 255, 255))
        self.legend_item = None

        self.styles = {"color": "#000", "font-size": str(self.font_size_axes) + "px"}

        self.title_font = QFont()
        self.legend_font = QFont()
        self.axes_font = QFont()

        self.title = ""
        self.x_title = ""
        self.y_title = ""

        self.apply_styles()

    def set_styles(self, font_size_t, font_size_a, font_size_l, line_width, font_color):
        self.font_size_title = font_size_t
        self.font_size_axes = font_size_a
        self.font_size_legend = font_size_l
        self.line_width = line_width
        self.font_color = font_color
        self.apply_styles()

    def apply_styles(self):
        self.font_pen = pg.mkPen(color=self.font_color)

        self.title_font.setPixelSize(self.font_size_title)
        self.legend_font.setPixelSize(self.font_size_legend)
        self.axes_font.setPixelSize(self.font_size_axes)

        self.graphWidget.getAxis("bottom").setStyle(tickFont=self.axes_font)
        self.graphWidget.getAxis("left").setStyle(tickFont=self.axes_font)
        self.graphWidget.getAxis("bottom").setTextPen(self.font_pen)
        self.graphWidget.getAxis("left").setTextPen(self.font_pen)

        self.styles = {"color": "#000", "font-size": str(self.font_size_axes) + "px"}

        self.add_title()
        self.add_axes_titles()

        if self.legend_item:
            self.legend_item.setLabelTextSize(str(self.font_size_legend) + 'pt')

    def clear(self):
        self.graphWidget.clear()

    def plot(self, x: List[List[float]], y: List[List[float]], labels: List[str],
             title: str, x_title: str, y_title: str, is_colored=True):
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.apply_styles()
        self.add_title()
        self.add_axes_titles()

        n_plots = len(y)
        for index in range(n_plots):
            pen = pg.mkPen(color=self.COLORS[index % len(self.COLORS) if is_colored else 0], width=self.line_width)
            self.graphWidget.plot(x[index % len(x)], y[index], name=labels[index % len(labels)],
                                  pen=pen, font=self.legend_font)

    def add_title(self):
        self.graphWidget.setTitle(self.title, color=self.font_color, size=str(self.font_size_title) + "pt")

    def add_scatter(self, xs, ys):
        scatter = pg.ScatterPlotItem(size=15, brush=pg.mkBrush(255, 255, 0, 190))
        spots = [{'pos': [xs[i], ys[i]], 'data': 1} for i in range(len(xs))]
        scatter.addPoints(spots)
        self.graphWidget.addItem(scatter)

    def add_axes_titles(self):
        # Add Axis Labels
        self.graphWidget.setLabel("left", self.y_title, **self.styles)
        self.graphWidget.setLabel("bottom", self.x_title, **self.styles)

    def add_line(self, _pos, _angle, _width, _style):
        # _style: Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine
        pen = pg.mkPen(color=self.COLORS[0], width=_width, style=_style)
        line = pg.InfiniteLine(pos=_pos, angle=_angle, pen=pen)
        self.graphWidget.addItem(line)

    def add_legend(self):
        self.legend_item = self.graphWidget.addLegend()
        self.legend_item.setLabelTextSize(str(self.font_size_legend) + 'pt')
        self.legend_item.setLabelTextColor(pg.mkColor(0, 0, 0))

    def set_xticks(self, ticks):
        self.graphWidget.getAxis("bottom").setTicks(ticks)

    def add_histogram(self, vals, num_bins, facecolor, x_title, y_title):
        self.apply_styles()
        y, x = np.histogram(vals, bins=num_bins)
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=facecolor)
        self.graphWidget.addItem(curve)
        self.x_title = x_title
        self.y_title = y_title
        self.add_axes_titles()

    def set_limits(self, x_min, x_max, y_min, y_max):
        self.graphWidget.setXRange(x_min, x_max, padding=0)
        self.graphWidget.setYRange(y_min, y_max, padding=0)

    def enable_auto_range(self):
        self.graphWidget.enableAutoRange()


class PyqtGraphWidgetImage(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.graphWidget = pg.GraphicsLayoutWidget()
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.graphWidget)
        self.setLayout(vertical_layout)
        self.graphWidget.setBackground((255, 255, 255))
        self.bar_width = 32
        self.bar_data = pg.colormap.modulatedBarData(width=self.bar_width)
        self.num_bars = 0

    def plot_mpl_colormap(self, title):
        self.graphWidget.clear()
        cmap = pg.colormap.get(title, source='matplotlib')
        imi = pg.ImageItem(self.bar_data)
        imi.setLookupTable(cmap.getLookupTable(alpha=True))
        vb = self.graphWidget.addViewBox(lockAspect=True, enableMouse=False)
        vb.addItem(imi)
        self.graphWidget.nextRow()
        self.graphWidget.setFixedHeight(self.bar_width + 5)

    def clear(self):
        self.graphWidget.clear()
