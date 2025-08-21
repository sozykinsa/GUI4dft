from src_critplot.models.cp_model import AtomicModelCP


def test_guiopengl(guiopengl_widget):
    widget = guiopengl_widget
    assert type(widget.main_model) == AtomicModelCP
