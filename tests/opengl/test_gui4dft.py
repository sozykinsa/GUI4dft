
def test_gui4dft_run(gui4dft_application, h2o_model):
    window = gui4dft_application
    assert window.models == []
    window.models.append(h2o_model)
    window.plot_model(-1)
    assert len(window.ui.openGLWidget.MainModel.atoms) == 3


def test_create_swnt(gui4dft_application):
    window = gui4dft_application
    window.create_swnt()
    assert len(window.models[-1].atoms) == 112

    window.ui.FormActionsPreRadioSWNTcap.setChecked(True)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 132

    window.ui.FormActionsPreRadioSWNTcap_2.setChecked(True)
    window.ui.FormActionsPreRadioSWNTuselen.setChecked(False)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 96


def test_create_graphene(gui4dft_application):
    window = gui4dft_application
    window.create_graphene()
    assert len(window.models[-1].atoms) == 112
