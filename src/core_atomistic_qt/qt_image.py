# -*- coding: utf-8 -*-
# ------------------------------------------------------
# ------------------ PyqtGraphWidget -------------------
# ------------------------------------------------------
# https://www.pythonguis.com/tutorials/pyside-plotting-pyqtgraph/

from qtpy.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg  # pip install pyqtgraph


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

    def clear(self):  # pragma: no cover
        self.graphWidget.clear()
