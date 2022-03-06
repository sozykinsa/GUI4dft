
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


def test_plot_voronoi(gui4dft_application):
    window = gui4dft_application
    window.create_swnt()
    window.ui.openGLWidget.selected_atom = 2
    window.plot_voronoi()
    assert window.ui.FormActionsPostLabelVoronoiAtom.text() == "Atom: 2"


def test_menu_open(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    window = gui4dft_application
    window.menu_open(f_name)
    assert len(window.models) == 1


def test_plot_dos(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    window = gui4dft_application
    window.menu_open(f_name)
    window.plot_dos()
    window.plot_pdos()
    window.parse_bands()
    window.plot_bands()
    assert len(window.models) == 1


def test_save_image_to_file(gui4dft_application):
    gui4dft_application.save_image_to_file("1.png")
