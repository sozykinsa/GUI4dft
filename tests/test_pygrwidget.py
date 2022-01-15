import pytest
from pyqt_graph_widget.pygrwidget import PyqtGraphWidget


def test_graph_widget_constructor(graph_widget):
    widget = graph_widget
    assert widget.font_color == (0, 0, 0)
    assert widget.font_size_title == 20


def test_graph_widget_styles(graph_widget):
    widget = graph_widget
    font_size_t = 15
    font_size_a = 15
    font_size_l = 15
    line_width = 15
    font_color = (25, 25, 25)
    widget.set_styles(font_size_t, font_size_a, font_size_l, line_width, font_color)

    assert widget.font_size_title == font_size_t
    widget.clear()


def test_graph_widget_plot(graph_widget):
    widget = graph_widget
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    labels = ["test graph"]
    title = ["Title"]
    x_title = "x_axe"
    y_title = "y_axe"
    widget.plot([x], [y], labels, title, x_title, y_title)


def test_graph_widget_scatter(graph_widget):
    widget = graph_widget
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    widget.add_scatter(xs, ys)
