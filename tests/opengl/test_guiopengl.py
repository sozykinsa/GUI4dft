from models.atomic_model import TAtomicModel


def test_guiopengl(guiopengl_widget):
    widget = guiopengl_widget
    assert type(widget.main_model) == TAtomicModel
