from models.atomic_model import TAtomicModel


def test_guiopengl(guiopengl_widget):
    widget = guiopengl_widget
    assert type(widget.MainModel) == TAtomicModel


def test_guiopengl_copy(guiopengl_widget, guiopengl_model_widget):
    widget = guiopengl_widget
    widget.copy_state(guiopengl_model_widget)
    assert type(widget.MainModel) == TAtomicModel
