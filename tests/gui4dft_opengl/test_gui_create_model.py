from copy import deepcopy


def test_create_swnt(gui4dft_application):
    window = gui4dft_application
    window.create_swnt()
    assert len(window.models[-1].atoms) == 112

    window.ui.FormActionsPreRadioSWNTusecell.setChecked(True)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 28
    window.ui.FormActionsPreRadioSWNTuselen.setChecked(True)

    window.ui.FormActionsPreRadioSWNTcap.setChecked(True)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 132

    window.ui.FormActionsPreRadioSWNTcap_2.setChecked(True)
    window.ui.FormActionsPreRadioSWNTusecell.setChecked(True)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 96

    window.ui.createSWGNTradio.setChecked(True)
    window.create_swnt()
    assert len(window.models[-1].atoms) == 63


def test_create_graphene(gui4dft_application):
    window = gui4dft_application
    window.create_graphene()
    assert len(window.models[-1].atoms) == 112
