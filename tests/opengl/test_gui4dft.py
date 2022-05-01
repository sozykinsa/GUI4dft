from copy import deepcopy

import pytest
from thirdparty.critic2 import parse_cp_properties


def test_gui4dft_run(gui4dft_application, h2o_model):
    window = gui4dft_application
    assert window.models == []
    window.models.append(h2o_model)
    window.plot_model(-1)
    assert len(window.ui.openGLWidget.main_model.atoms) == 3


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


def test_xsf_operations(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    window = gui4dft_application
    window.menu_open(f_name)
    assert len(window.models) == 1

    selected = window.ui.FormActionsPostList3DData.item(0).text()
    window.parse_volumeric_data_selected(selected)

    selected_items = window.ui.FormActionsPostTreeSurface.itemAt(0, 0).child(0)
    window.volumeric_data_load_selected([selected_items])
    assert window.ui.FormVolDataExportX2.value() == 30

    window.ui.FormActionsPostCheckSurface.setChecked(True)
    window.add_isosurface_color_to_table()
    assert window.ui.IsosurfaceColorsTable.rowCount() == 1

    window.plot_contour()
    window.ui.FormActionsPostCheckContourXY.setChecked(True)
    window.ui.FormActionsPostCheckContourYZ.setChecked(True)
    window.ui.FormActionsPostCheckContourXZ.setChecked(True)
    window.plot_contour()

    window.ui.FormActionsPostRadioColorPlane.setChecked(True)
    window.plot_contour()

    window.ui.FormActionsPostRadioColorPlaneContours.setChecked(True)
    window.plot_contour()


def test_plot_dos(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    window = gui4dft_application
    window.menu_open(f_name)
    window.plot_dos()
    window.plot_pdos()
    window.parse_bands()
    window.plot_bands()
    assert len(window.models) == 1


def test_actions_rotate(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    window = gui4dft_application
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


def test_actions_move(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    window = gui4dft_application
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


def test_cell_param(gui4dft_application, tests_path):
    f_name1 = str(tests_path / 'ref_data' / 'cell_param' / '2-85' / "siesta.out")
    gui4dft_application.fill_cell_info(f_name1)
    f_name2 = str(tests_path / 'ref_data' / 'cell_param' / '2-86' / "siesta.out")
    gui4dft_application.fill_cell_info(f_name2)
    f_name3 = str(tests_path / 'ref_data' / 'cell_param' / '2-87' / "siesta.out")
    gui4dft_application.fill_cell_info(f_name3)
    f_name4 = str(tests_path / 'ref_data' / 'cell_param' / '2-88' / "siesta.out")
    gui4dft_application.fill_cell_info(f_name4)
    f_name5 = str(tests_path / 'ref_data' / 'cell_param' / '2-89' / "siesta.out")
    gui4dft_application.fill_cell_info(f_name5)

    gui4dft_application.ui.FormActionsPostComboCellParam.setCurrentIndex(1)
    gui4dft_application.plot_volume_param_energy()
    method = gui4dft_application.ui.FormActionsPostComboCellParam.currentText()
    if method == "Murnaghan":
        assert gui4dft_application.ui.FormActionsPostLabelCellParamOptimExpr4.text() == "V0=11.9"

    gui4dft_application.ui.FormActionsPostComboCellParam.setCurrentIndex(0)
    gui4dft_application.plot_volume_param_energy()
    method = gui4dft_application.ui.FormActionsPostComboCellParam.currentText()
    if method == "BirchMurnaghan":
        assert gui4dft_application.ui.FormActionsPostLabelCellParamOptimExpr4.text() == "V0=11.9"

    gui4dft_application.ui.FormActionsPostComboCellParam.setCurrentIndex(2)
    gui4dft_application.plot_volume_param_energy()
    method = gui4dft_application.ui.FormActionsPostComboCellParam.currentText()
    if method == "Parabola":
        assert gui4dft_application.ui.FormActionsPostLabelCellParamOptimExpr4.text() == "x0=11.891"


def test_critic2_section(gui4dft_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    window = gui4dft_application
    window.ui.FormSettingsViewCheckXYZasCritic2.setChecked(True)
    window.menu_open(f_name)
    model = window.models[-1]
    assert len(model.bcp) == 5
    assert "field" not in model.bcp[0].properties
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "siesta-1-cp.cro")
    parse_cp_properties(f_name, model)
    assert float(model.bcp[0].properties["field"]) == pytest.approx(1.68288239)
    window.selected_cp_changed(1)
    assert window.ui.selectedCP_nuclei.text() == "O2-O2"


def test_simple_calls(gui4dft_application):
    gui4dft_application.save_image_to_file("1.png")
    gui4dft_application.activate_fragment_selection_mode()
