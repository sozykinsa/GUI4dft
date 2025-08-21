from copy import deepcopy


def test_critplot_run(critplot_application, h2o_model_cp):
    window = critplot_application
    assert window.models == []
    window.models.append(h2o_model_cp)
    window.plot_model(-1)
    assert len(window.ui.openGLWidget.main_model.atoms) == 3


def test_menu_open(critplot_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    assert len(window.models) == 1


def test_actions_rotate(critplot_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    rot = deepcopy(window.ui.openGLWidget.rotation_angles)
    window.rotate_model_xp()
    assert window.ui.openGLWidget.rotation_angles[0] == rot[0] + window.rotation_step
    window.rotate_model_xm()
    assert window.ui.openGLWidget.rotation_angles[0] == rot[0]
    window.rotate_model_yp()
    assert window.ui.openGLWidget.rotation_angles[1] == rot[1] + window.rotation_step
    window.rotate_model_ym()
    assert window.ui.openGLWidget.rotation_angles[1] == rot[1]
    window.rotate_model_zp()
    assert window.ui.openGLWidget.rotation_angles[2] == rot[2] + window.rotation_step
    window.rotate_model_zm()
    assert window.ui.openGLWidget.rotation_angles[2] == rot[2]


def test_actions_move(critplot_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    cam_pos = deepcopy(window.ui.openGLWidget.camera_position)
    window.move_model_right()
    assert window.ui.openGLWidget.camera_position[0] == cam_pos[0] + window.move_step
    window.move_model_left()
    assert window.ui.openGLWidget.camera_position[0] == cam_pos[0]
    window.move_model_up()
    assert window.ui.openGLWidget.camera_position[1] == cam_pos[1] + window.move_step
    window.move_model_down()
    assert window.ui.openGLWidget.camera_position[1] == cam_pos[1]


def test_selected_atom_from_form(critplot_application, tests_path):
    window = critplot_application
    charge, let, position = window.selected_atom_from_form()
    assert charge == 0
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    window.ui.openGLWidget.selected_atom = 2
    window.ui.openGLWidget.selected_atom_changed()
    window.ui.openGLWidget.update()
    charge, let, position = window.selected_atom_from_form()
    assert charge == 8
    assert window.ui.openGLWidget.main_model.n_atoms() == 6
    window.atom_add()
    assert window.ui.openGLWidget.main_model.n_atoms() == 7
    window.ui.openGLWidget.selected_atom = 2
    window.atom_delete()
    assert window.ui.openGLWidget.main_model.n_atoms() == 6
