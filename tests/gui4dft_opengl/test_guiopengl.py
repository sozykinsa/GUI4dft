from core_gui_atomistic.atomic_model import AtomicModel


def test_guiopengl(guiopengl_widget):
    widget = guiopengl_widget
    assert type(widget.main_model) == AtomicModel
