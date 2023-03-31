

def test_graph_image_widget_constructor(graph_image_widget):
    widget = graph_image_widget
    widget.plot_mpl_colormap("rainbow")
    assert widget.bar_width == 32
