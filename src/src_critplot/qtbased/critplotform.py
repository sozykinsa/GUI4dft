# -*- coding: utf-8 -*-
import os

try:
    if os.environ["XDG_SESSION_TYPE"] == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
except Exception as e:
    pass
import math
import sys
from pathlib import Path
from copy import deepcopy
import numpy as np

from qtpy.QtCore import QSettings, Qt, QSize
from qtpy.QtGui import QAction, QColor, QIcon, QKeySequence, QStandardItem, QStandardItemModel, QShortcut
from qtpy.QtWidgets import QListWidgetItem, QDialog, QFileDialog, QMessageBox, QColorDialog
from qtpy.QtWidgets import QMainWindow, QTableWidgetItem

from src_critplot.qtbased.image3dexporter import Image3Dexporter

from core_atomistic.periodic_table import TPeriodTable
from core_atomistic import helpers

from src_critplot.interface.io import ImporterExporter

from src_critplot.ui_critplot.about import Ui_DialogAbout as Ui_about
if sys.platform.startswith('win'):
    #  sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
    from src_critplot.ui_critplot.form_win import Ui_MainWindow as Ui_form
else:
    from src_critplot.ui_critplot.form import Ui_MainWindow as Ui_form

sys.path.append('')

is_with_figure = True


class MainForm(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.ui = Ui_form()
        self.ui.setupUi(self)

        self.models = []
        self.ui.openGLWidget.set_form_elements(self.ui.FormSettingsViewCheckAtomSelection,
                                               self.orientation_model_changed, self.selected_atom_position,
                                               self.selected_atom_changed, 1)
        self.filename: str = ""
        self.work_dir: str = None
        self.colors_cash = {}
        self.table_header_stylesheet = "::section{Background-color:rgb(190,190,190)}"
        self.is_scaled_colors_for_surface = True
        self.rotation_step: int = 1
        self.move_step: int = 1

        self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut.activated.connect(self.atom_delete)
        self.active_model_id: int = -1
        self.perspective_angle: int = 45

        self.state_Color_Of_Atoms = None
        self.color_of_atoms_scheme = "cpk"
        self.periodic_table = TPeriodTable()

        self.history_of_point_selection = []
        self.history_of_point_selection_xyz = []

        self.action_on_start: str = None

        self.color_type: str = 'rainbow'
        self.color_type_scale: str = 'Log'

    def start_program(self):  # pragma: no cover
        if self.action_on_start == 'Open':
            self.action_on_start = 'Nothing'
            self.save_state_action_on_start()
            self.menu_open()

    def setup_ui(self):  # pragma: no cover
        self.load_settings()
        self.ui.actionOpen.triggered.connect(self.menu_open)
        self.ui.actionExport.triggered.connect(self.menu_export)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionOrtho.triggered.connect(self.menu_ortho)
        self.ui.actionPerspective.triggered.connect(self.menu_perspective)
        self.ui.actionShowBox.triggered.connect(self.menu_show_box)
        self.ui.actionHideBox.triggered.connect(self.menu_hide_box)
        self.ui.actionAbout.triggered.connect(self.menu_about)
        self.ui.actionManual.triggered.connect(self.menu_manual)

        self.ui.FormModelComboModels.currentIndexChanged.connect(self.model_to_screen)
        self.ui.PropertyForBCPtext.currentIndexChanged.connect(self.show_cp_property)
        self.ui.show_bcp_text.stateChanged.connect(self.show_cp_property)
        self.ui.property_precision.valueChanged.connect(self.cp_property_precision_changed)
        self.ui.font_size_3d.valueChanged.connect(self.font_size_3d_changed)
        self.ui.property_shift_x.valueChanged.connect(self.property_position_changed)
        self.ui.property_shift_y.valueChanged.connect(self.property_position_changed)
        self.ui.show_bcp.stateChanged.connect(self.show_cps)
        self.ui.show_ccp.stateChanged.connect(self.show_cps)
        self.ui.show_rcp.stateChanged.connect(self.show_cps)
        self.ui.show_ncp.stateChanged.connect(self.show_cps)
        self.ui.show_nnatr.stateChanged.connect(self.show_cps)
        self.ui.show_bond_path.stateChanged.connect(self.show_bond_path)
        self.ui.bcp_for_figure.currentTextChanged.connect(self.update_bcp_figure_and_table)

        self.ui.FormAtomsList1.currentIndexChanged.connect(self.bond_len_to_screen)
        self.ui.FormAtomsList2.currentIndexChanged.connect(self.bond_len_to_screen)

        self.ui.ActivateFragmentSelectionModeCheckBox.toggled.connect(self.activate_fragment_selection_mode)
        self.ui.ActivateFragmentSelectionTransp.valueChanged.connect(self.activate_fragment_selection_mode)

        self.ui.model_rotation_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_scale.valueChanged.connect(self.model_orientation_changed)

        self.ui.bcp_table.clicked.connect(self.fill_cps_table)  # toggled
        self.ui.natr_table.clicked.connect(self.fill_cps_table)
        self.ui.rcp_table.clicked.connect(self.fill_cps_table)
        self.ui.ccp_table.clicked.connect(self.fill_cps_table)

        self.ui.bonds_histogram.clicked.connect(self.default_histogram_text)
        self.ui.bp_len_histogram.clicked.connect(self.default_histogram_text)
        self.ui.bcp_rho_histogram.clicked.connect(self.default_histogram_text)

        # buttons
        self.ui.plot_histogram.clicked.connect(self.plot_histogram_of_data)

        # colors
        self.ui.ColorBackgroundDialogButton.clicked.connect(self.select_background_color)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.color_bond_cp_button.clicked.connect(self.select_bcp_color)
        self.ui.color_ring_cp_button.clicked.connect(self.select_rcp_color)
        self.ui.color_cage_cp_button.clicked.connect(self.select_ccp_color)
        self.ui.color_bond_path_button.clicked.connect(self.select_bp_color)
        self.ui.ColorAxesDialogButton.clicked.connect(self.select_axes_color)
        self.ui.manual_colors_default.clicked.connect(self.set_manual_colors_default)
        self.ui.FormBondLenSpinBox.valueChanged.connect(self.bond_len_correct)

        self.ui.FormModifyCellButton.clicked.connect(self.edit_cell)
        self.ui.FormActionsPostButGetBonds.clicked.connect(self.get_bonds)
        self.ui.PropertyAtomAtomDistanceGet.clicked.connect(self.get_bond)
        self.ui.FormStylesFor2DGraph.clicked.connect(self.set_2d_graph_styles)

        self.ui.changeFragment1StatusByX.clicked.connect(self.change_fragment1_status_by_x)
        self.ui.changeFragment1StatusByY.clicked.connect(self.change_fragment1_status_by_y)
        self.ui.changeFragment1StatusByZ.clicked.connect(self.change_fragment1_status_by_z)
        self.ui.fragment1Clear.clicked.connect(self.fragment1_clear)
        # critical points
        self.ui.FormCreateCriXYZFile.clicked.connect(self.create_critic2_xyz_file)
        self.ui.delete_cp_from_list.clicked.connect(self.delete_cp_from_list)
        self.ui.clear_cp_list.clicked.connect(self.clear_cp_list)
        self.ui.add_cp_to_list.clicked.connect(self.add_cp_to_list)
        self.ui.delete_cp_from_model.clicked.connect(self.delete_cp_from_model)
        self.ui.leave_cp_in_model.clicked.connect(self.leave_cp_in_model)
        self.ui.export_cp_to_csv.clicked.connect(self.export_cp_to_csv)
        self.ui.hide_cps_min_rho.clicked.connect(self.hide_cps_min_rho)
        self.ui.hide_cps_eq_atoms.clicked.connect(self.hide_cps_eq_atoms)
        self.ui.cancel_cps_filters.clicked.connect(self.cancel_cps_filters)

        self.ui.FormActionsPreButDeleteAtom.clicked.connect(self.atom_delete)
        self.ui.FormActionsPreButModifyAtom.clicked.connect(self.atom_modify)
        self.ui.FormActionsPreButAddAtom.clicked.connect(self.atom_add)
        self.ui.atom_translation_1_plus.clicked.connect(self.atom_translation_1_plus)
        self.ui.atom_translation_1_minus.clicked.connect(self.atom_translation_1_minus)
        self.ui.atom_translation_2_plus.clicked.connect(self.atom_translation_2_plus)
        self.ui.atom_translation_2_minus.clicked.connect(self.atom_translation_2_minus)
        self.ui.atom_translation_3_plus.clicked.connect(self.atom_translation_3_plus)
        self.ui.atom_translation_3_minus.clicked.connect(self.atom_translation_3_minus)

        self.ui.add_xyz_critic_data.clicked.connect(self.add_critic2_xyz_file)
        self.ui.FormCreateCriFile.clicked.connect(self.create_cri_file)

        self.ui.FormModifyGoPositive.clicked.connect(self.model_go_to_positive)
        self.ui.FormModifyGoToCell.clicked.connect(self.model_go_to_cell)
        self.ui.modify_center_to_zero.clicked.connect(self.model_center_to_zero)
        self.ui.additional_atoms_delete.clicked.connect(self.model_additional_atoms_delete)
        self.ui.x_circular_shift.clicked.connect(self.model_x_circular_shift)
        self.ui.y_circular_shift.clicked.connect(self.model_y_circular_shift)
        self.ui.z_circular_shift.clicked.connect(self.model_z_circular_shift)

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        atoms_list = self.periodic_table.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))
        self.ui.FormActionsPreComboAtomsList.setModel(model)
        self.ui.FormAtomsList1.setModel(model)
        self.ui.FormAtomsList2.setModel(model)

        self.ui.FormModelTableAtoms.setColumnCount(4)
        self.ui.FormModelTableAtoms.setRowCount(100)
        self.ui.FormModelTableAtoms.setHorizontalHeaderLabels(["Atom", "x", "y", "z"])
        self.ui.FormModelTableAtoms.setColumnWidth(0, 60)
        self.ui.FormModelTableAtoms.setColumnWidth(1, 95)
        self.ui.FormModelTableAtoms.setColumnWidth(2, 95)
        self.ui.FormModelTableAtoms.setColumnWidth(3, 95)
        self.ui.FormModelTableAtoms.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormModelTableAtoms.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.ui.FormModelTableProperties.setColumnCount(2)
        self.ui.FormModelTableProperties.setRowCount(10)
        self.ui.FormModelTableProperties.setHorizontalHeaderLabels(["Property", "Value"])
        self.ui.FormModelTableProperties.setColumnWidth(0, 85)
        self.ui.FormModelTableProperties.setColumnWidth(1, 260)
        self.ui.FormModelTableProperties.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormModelTableProperties.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.ui.FormActionsPostComboBonds.currentIndexChanged.connect(self.fill_bonds)

        color_type = QStandardItemModel()
        color_types = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                       'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                       'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for t in color_types:
            color_type.appendRow(QStandardItem(t))

        self.ui.FormSettingsColorsScale.setModel(color_type)
        self.ui.FormSettingsColorsScale.setCurrentText(self.color_type)

        color_type_scale = QStandardItemModel()
        color_type_scale.appendRow(QStandardItem("Linear"))
        color_type_scale.appendRow(QStandardItem("Log"))
        self.ui.FormSettingsColorsScaleType.setModel(color_type_scale)
        self.ui.FormSettingsColorsScaleType.setCurrentText(self.color_type_scale)

        self.fill_cp_graph_types()

        self.ui.FormActionsPosTableBonds.setColumnCount(2)
        self.ui.FormActionsPosTableBonds.setHorizontalHeaderLabels(["Bond", "Lenght"])
        self.ui.FormActionsPosTableBonds.setColumnWidth(0, 120)
        self.ui.FormActionsPosTableBonds.setColumnWidth(1, 170)
        self.ui.FormActionsPosTableBonds.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormActionsPosTableBonds.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.setup_actions()

    def setup_actions(self):
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'ico.png'):
            self.setWindowIcon(QIcon(str(Path(__file__).parent / "images" / 'ico.png')))
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'Open.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'Open.png')), 'Open', self)
        else:
            open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.menu_open)
        self.ui.toolBar.addAction(open_action)
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'Close.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'Close.png')), 'Export', self)
        else:
            open_action = QAction('Export', self)
        open_action.setShortcut('Ctrl+E')
        open_action.triggered.connect(self.menu_export)
        self.ui.toolBar.addAction(open_action)
        self.ui.toolBar.addSeparator()
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'Save3D.png'):
            file_path = str(Path(__file__).parent / "images" / 'Save3D.png')
            save_image_to_file_action = QAction(QIcon(file_path), 'SaveFigure3D', self)
        else:
            save_image_to_file_action = QAction('SaveFigure3D', self)
        save_image_to_file_action.triggered.connect(self.save_image_to_file)
        self.ui.toolBar.addAction(save_image_to_file_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoX.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoX.png')), 'RotateX-', self)
        else:
            open_action = QAction('RotateX-', self)
        open_action.triggered.connect(self.rotate_model_xp)
        self.ui.toolBar.addAction(open_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoX.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoX.png')), 'RotateX+', self)
        else:
            open_action = QAction('RotateX+', self)
        open_action.triggered.connect(self.rotate_model_xm)
        self.ui.toolBar.addAction(open_action)
        self.ui.toolBar.addSeparator()
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoY.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoY.png')), 'RotateY-', self)
        else:
            open_action = QAction('RotateY-', self)
        open_action.triggered.connect(self.rotate_model_yp)
        self.ui.toolBar.addAction(open_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoY.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoY.png')), 'RotateY+', self)
        else:
            open_action = QAction('RotateY+', self)
        open_action.triggered.connect(self.rotate_model_ym)
        self.ui.toolBar.addAction(open_action)

        self.ui.toolBar.addSeparator()
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoZ.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoZ.png')), 'RotateZ-', self)
        else:
            open_action = QAction('RotateZ-', self)
        open_action.triggered.connect(self.rotate_model_zp)
        self.ui.toolBar.addAction(open_action)
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoZ.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoZ.png')), 'RotateZ+', self)
        else:
            open_action = QAction('RotateZ+', self)
        open_action.triggered.connect(self.rotate_model_zm)
        self.ui.toolBar.addAction(open_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'left.png'):
            to_left_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'left.png')), 'left', self)
        else:
            to_left_action = QAction('RotateX-', self)
        to_left_action.triggered.connect(self.move_model_left)
        self.ui.toolBar.addAction(to_left_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'right.png'):
            to_right_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'right.png')), 'right', self)
        else:
            to_right_action = QAction('RotateX+', self)
        to_right_action.triggered.connect(self.move_model_right)
        self.ui.toolBar.addAction(to_right_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'down.png'):
            to_up_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'down.png')), 'Y-', self)
        else:
            to_up_action = QAction('RotateY-', self)
        to_up_action.triggered.connect(self.move_model_down)
        self.ui.toolBar.addAction(to_up_action)
        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'up.png'):
            to_down_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'up.png')), 'Y+', self)
        else:
            to_down_action = QAction('RotateY+', self)
        to_down_action.triggered.connect(self.move_model_up)
        self.ui.toolBar.addAction(to_down_action)
        self.ui.toolBar.addSeparator()

    def activate_fragment_selection_mode(self):
        if self.ui.ActivateFragmentSelectionModeCheckBox.isChecked():
            self.ui.openGLWidget.set_selected_fragment_mode(self.ui.AtomsInSelectedFragment,
                                                            self.ui.ActivateFragmentSelectionTransp.value())
            self.ui.changeFragment1StatusByX.setEnabled(True)
            self.ui.changeFragment1StatusByY.setEnabled(True)
            self.ui.changeFragment1StatusByZ.setEnabled(True)
            self.ui.fragment1Clear.setEnabled(True)
        else:
            self.ui.openGLWidget.set_selected_fragment_mode(None, self.ui.ActivateFragmentSelectionTransp.value())
            self.ui.changeFragment1StatusByX.setEnabled(False)
            self.ui.changeFragment1StatusByY.setEnabled(False)
            self.ui.changeFragment1StatusByZ.setEnabled(False)
            self.ui.fragment1Clear.setEnabled(False)

    def add_critic2_xyz_file(self):
        """Add bond path data from *.xyz file to current model."""
        try:
            f_name = self.get_file_name_from_open_dialog("Critic xyz (*.xyz)")
            if os.path.exists(f_name):
                self.work_dir = os.path.dirname(f_name)
                model = self.models[-1]
                model.parse_bondpaths(f_name)
                self.plot_last_model()
        except Exception as exs:
            self.show_error(exs)

    @staticmethod
    def show_error(error_data: Exception):
        """error_data: Exception object for MessageBox """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(error_data))
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def model_part_prepare(cm_x_new, cm_y_new, cm_z_new, models, rot_x, rot_y, rot_z):
        part = models[-1]
        cm_old = - part.center_mass()
        part.move(*cm_old)
        part.rotate(rot_x, rot_y, rot_z)
        part.move(cm_x_new, cm_y_new, cm_z_new)
        return part

    def atom_add(self):
        if len(self.models) == 0:
            return
        charge, let, position = self.selected_atom_from_form()
        self.models[self.active_model_id].add_atom_with_data(position, charge)
        self.model_to_screen(self.active_model_id)

    def atom_delete(self):
        if len(self.models) == 0:
            return
        if self.ui.openGLWidget.selected_atom < 0:
            return
        self.models[self.active_model_id].delete_atom(self.ui.openGLWidget.selected_atom)
        self.history_of_point_selection = []
        self.history_of_point_selection_xyz = []
        self.model_to_screen(self.active_model_id)

    def atom_modify(self):
        if len(self.models) == 0:
            return
        if self.ui.openGLWidget.selected_atom < 0:
            return
        charge, let, position = self.selected_atom_from_form()
        self.models[self.active_model_id].atoms[self.ui.openGLWidget.selected_atom].xyz = position
        self.models[self.active_model_id].atoms[self.ui.openGLWidget.selected_atom].charge = charge
        self.models[self.active_model_id].atoms[self.ui.openGLWidget.selected_atom].let = let
        self.model_to_screen(self.active_model_id)

    def atom_translation_1_plus(self):
        self.translate_atom_or_cp(1, 0, 0)

    def atom_translation_1_minus(self):
        self.translate_atom_or_cp(-1, 0, 0)

    def atom_translation_2_plus(self):
        self.translate_atom_or_cp(0, 1, 0)

    def atom_translation_2_minus(self):
        self.translate_atom_or_cp(0, -1, 0)

    def atom_translation_3_plus(self):
        self.translate_atom_or_cp(0, 0, 1)

    def atom_translation_3_minus(self):
        self.translate_atom_or_cp(0, 0, -1)

    def translate_atom_or_cp(self, xp, yp, zp):
        if len(self.models) == 0:
            return
        if (self.ui.openGLWidget.selected_atom < 0) and (self.ui.openGLWidget.selected_cp < 0):
            return
        if self.ui.openGLWidget.selected_atom >= 0:
            self.models[self.active_model_id].translate_atom(self.ui.openGLWidget.selected_atom, xp, yp, zp)
            # atom = self.models[self.active_model].atoms[self.ui.openGLWidget.selected_atom]
            # atom.xyz += xp * self.models[self.active_model].lat_vector1 + \
            #             yp * self.models[self.active_model].lat_vector2 + \
            #             zp * self.models[self.active_model].lat_vector3
        if self.ui.openGLWidget.selected_cp >= 0:
            self.models[self.active_model_id].translate_cp(self.ui.openGLWidget.selected_cp, xp, yp, zp)
            # cp = self.models[self.active_model].cps[self.ui.openGLWidget.selected_cp]
            # self.models[self.active_model].move_cp(cp, xp * self.models[self.active_model].lat_vector1 +
            #                                        yp * self.models[self.active_model].lat_vector2 +
            #                                        zp * self.models[self.active_model].lat_vector3)
        self.model_to_screen(self.active_model_id)

    def selected_atom_from_form(self):
        charge = self.ui.FormActionsPreComboAtomsList.currentIndex()
        let = self.ui.FormActionsPreComboAtomsList.currentText()
        x = self.ui.FormActionsPreSpinAtomsCoordX.value()
        y = self.ui.FormActionsPreSpinAtomsCoordY.value()
        z = self.ui.FormActionsPreSpinAtomsCoordZ.value()
        position = np.array((x, y, z), dtype=float)
        return charge, let, position

    def bond_len_to_screen(self):
        let1 = self.ui.FormAtomsList1.currentIndex()
        let2 = self.ui.FormAtomsList2.currentIndex()

        if not ((let1 == 0) or (let2 == 0)):
            bond = self.periodic_table.Bonds[let1][let2]
        else:
            bond = 0
        self.ui.FormBondLenSpinBox.setValue(bond)

    # def clear_form_isosurface_data2_n(self):
    #     self.ui.FormActionsPostLabelSurfaceNx.setText("")
    #     self.ui.FormActionsPostLabelSurfaceNy.setText("")
    #     self.ui.FormActionsPostLabelSurfaceNz.setText("")

    def change_fragment1_status_by_x(self):
        x_min = self.ui.xminborder.value()
        x_max = self.ui.xmaxborder.value()
        model = self.ui.openGLWidget.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.x >= x_min) and (at.x <= x_max):
                self.ui.openGLWidget.main_model.atoms[ind].fragment1 = True
        self.fragment1_post_actions()

    def change_fragment1_status_by_y(self):
        y_min = self.ui.yminborder.value()
        y_max = self.ui.ymaxborder.value()
        model = self.ui.openGLWidget.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.y >= y_min) and (at.y <= y_max):
                self.ui.openGLWidget.main_model.atoms[ind].fragment1 = True
        self.fragment1_post_actions()

    def change_fragment1_status_by_z(self):
        z_min = self.ui.zminborder.value()
        z_max = self.ui.zmaxborder.value()
        model = self.ui.openGLWidget.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.z >= z_min) and (at.z <= z_max):
                self.ui.openGLWidget.main_model.atoms[ind].fragment1 = True
        self.fragment1_post_actions()

    def fragment1_clear(self):
        for at in self.ui.openGLWidget.main_model.atoms:
            at.fragment1 = False
        self.fragment1_post_actions()

    def fragment1_post_actions(self):
        self.ui.openGLWidget.atoms_of_selected_fragment_to_form()
        self.ui.openGLWidget.update_view()

    def color_to_ui(self, color_ui, state_color):
        state_color = state_color.replace(',', ' ')
        r = state_color.split()[0]
        g = state_color.split()[1]
        b = state_color.split()[2]
        color_ui.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

    def colors_of_atoms(self):
        return self.periodic_table.get_all_colors()

    def edit_cell(self):
        if len(self.models) == 0:
            return
        a1 = float(self.ui.FormModifyCellEditA1.text())
        a2 = float(self.ui.FormModifyCellEditA2.text())
        a3 = float(self.ui.FormModifyCellEditA3.text())
        v1 = [a1, a2, a3]
        b1 = float(self.ui.FormModifyCellEditB1.text())
        b2 = float(self.ui.FormModifyCellEditB2.text())
        b3 = float(self.ui.FormModifyCellEditB3.text())
        v2 = [b1, b2, b3]
        c1 = float(self.ui.FormModifyCellEditC1.text())
        c2 = float(self.ui.FormModifyCellEditC2.text())
        c3 = float(self.ui.FormModifyCellEditC3.text())
        v3 = [c1, c2, c3]
        self.ui.openGLWidget.main_model.set_lat_vectors(v1, v2, v3)
        self.models.append(self.ui.openGLWidget.main_model)
        self.model_to_screen(-1)

    def get_file_name_from_save_dialog(self, file_mask):  # pragma: no cover
        result = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, file_mask,
                                             options=QFileDialog.DontUseNativeDialog)

        if len(result[0]) == 0:
            return None

        file_name = result[0]
        mask = result[1]
        if file_name is not None:
            extension = mask.split("(*.")[1].split(")")[0]
            print(file_name.lower(), extension.lower())
            if not file_name.lower().endswith(extension.lower()):
                file_name += "." + extension.lower()
        if extension.lower() in ['png', 'jpg', 'bmp']:
            file_name = file_name.replace(extension.upper(), extension.lower())
        return file_name

    def get_file_name_from_open_dialog(self, file_mask):  # pragma: no cover
        return QFileDialog.getOpenFileName(self, 'Open file', self.work_dir, file_mask,
                                           options=QFileDialog.DontUseNativeDialog)[0]

    def fill_gui(self, title=""):
        file_name = self.filename
        if title == "":
            self.fill_file_name(file_name)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()
        self.fill_cps()
        self.poincare_hoff_rule()

        self.ui.PropertyAtomAtomDistanceAt1.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistanceAt2.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistance.setText("")
        self.plot_r_rho()

    def plot_r_rho(self) -> None:
        model = self.ui.openGLWidget.get_model()
        if model is None:
            return
        r = []
        rho = []
        n_types = self.ui.bcp_for_figure.count()
        title_types = {}
        for i in range(n_types):
            r.append([])
            rho.append([])
            title_types[self.ui.bcp_for_figure.itemText(i)] = i

        for cp in model.cps:
            if cp.let == "xb":
                dist = cp.get_property("cp_bp_len")
                if not dist is None:
                    if self.cp_need_to_gui(cp, model) and (float(cp.get_property("rho")) > 0):
                        k = self.cp_type_title(cp, model, title_types)
                        if k is not None:
                            ind = title_types[k]
                            r[ind].append(dist)
                            rho[ind].append(math.log(float(cp.get_property("rho"))))

        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.PyqtGraphWidget.clear()
        x_title = "r"
        y_title = "ln(rho)"
        title = "ln(rho(r))"
        if len(r) == 0:
            return

        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        self.ui.PyqtGraphWidget.plot([], [], [None], title, x_title, y_title)
        ind = self.ui.bcp_for_figure.currentIndex()
        if ind == 0:
            for i in range(1, n_types):
                col = self.ui.PyqtGraphWidget.COLORS[i % len(self.ui.PyqtGraphWidget.COLORS)]
                self.ui.PyqtGraphWidget.add_scatter(r[i], rho[i], color=col)
        else:
            self.ui.PyqtGraphWidget.set_xticks(None)
            self.ui.PyqtGraphWidget.clear()
            col = self.ui.PyqtGraphWidget.COLORS[ind % len(self.ui.PyqtGraphWidget.COLORS)]
            self.ui.PyqtGraphWidget.add_scatter(r[ind], rho[ind], color=col)
            if len(r[ind]) > 1:
                x_max = max(r[ind])
                x_min = min(r[ind])
                if (len(r[ind]) >= 2) and (x_max != x_min):
                    a, b = np.polyfit(r[ind], rho[ind], 1)
                    y_max = a * x_max + b
                    y_min = a * x_min + b
                    leg = str(round(a, 5)) + " x "
                    if b >= 0:
                        leg += "+"
                    leg += str(round(b, 5))
                    self.ui.PyqtGraphWidget.plot([[x_min, x_max]], [[y_min, y_max]], [leg], title, x_title, y_title)

    def cp_need_to_gui(self, cp, model):
        filt = self.ui.bcp_for_figure.currentText()
        f = cp.is_visible
        if (filt != "All") and f:
            title1, title2 = model.equivalent_titles(cp)
            f = (filt == title1) or (filt == title2)
        return f

    @staticmethod
    def cp_type_title(cp, model, title_types):
        title1, title2 = model.equivalent_titles(cp)
        if (title1 is None) or (title2 is None):
            return None
        if not title_types.get(title1) is None:
            return title1
        if not title_types.get(title2) is None:
            return title2
        return None

    def fill_file_name(self, f_name):
        self.ui.Form3Dand2DTabs.setItemText(0, "3D View: " + f_name)
        self.ui.Form3Dand2DTabs.update()

    def fill_models_list(self):
        model = QStandardItemModel()
        if len(self.models) == 1:
            model.appendRow(QStandardItem("single model"))
        else:
            for i in range(0, len(self.models)):
                model.appendRow(QStandardItem("model " + str(i)))
        self.ui.FormModelComboModels.currentIndexChanged.disconnect()
        self.ui.FormModelComboModels.setModel(model)
        self.ui.FormModelComboModels.setCurrentIndex(len(self.models) - 1)
        self.ui.FormModelComboModels.currentIndexChanged.connect(self.model_to_screen)

    def fill_atoms_table(self):
        model = self.ui.openGLWidget.get_model().atoms
        self.ui.FormModelTableAtoms.setRowCount(len(model))

        for i in range(0, len(model)):
            self.ui.FormModelTableAtoms.setItem(i, 0, QTableWidgetItem(model[i].let))
            self.ui.FormModelTableAtoms.setItem(i, 1, QTableWidgetItem(helpers.float_to_string(model[i].x)))
            self.ui.FormModelTableAtoms.setItem(i, 2, QTableWidgetItem(helpers.float_to_string(model[i].y)))
            self.ui.FormModelTableAtoms.setItem(i, 3, QTableWidgetItem(helpers.float_to_string(model[i].z)))

    def fill_properties_table(self):
        properties = []
        model = self.ui.openGLWidget.get_model()
        properties.append(["Atoms", str(model.n_atoms())])
        properties.append(["CPs", str(model.n_cps())])
        properties.append(["LatVect1", str(model.lat_vector1)])
        properties.append(["LatVect2", str(model.lat_vector2)])
        properties.append(["LatVect3", str(model.lat_vector3)])
        properties.append(["Formula", model.formula()])

        table = self.ui.FormModelTableProperties

        table.setRowCount(len(properties))
        for i in range(0, len(properties)):
            for j in range(len(properties[i])):
                table.setItem(i, j, QTableWidgetItem(properties[i][j]))

        self.ui.FormModifyCellEditA1.setValue(model.lat_vector1[0])
        self.ui.FormModifyCellEditA2.setValue(model.lat_vector1[1])
        self.ui.FormModifyCellEditA3.setValue(model.lat_vector1[2])
        self.ui.FormModifyCellEditB1.setValue(model.lat_vector2[0])
        self.ui.FormModifyCellEditB2.setValue(model.lat_vector2[1])
        self.ui.FormModifyCellEditB3.setValue(model.lat_vector2[2])
        self.ui.FormModifyCellEditC1.setValue(model.lat_vector3[0])
        self.ui.FormModifyCellEditC2.setValue(model.lat_vector3[1])
        self.ui.FormModifyCellEditC3.setValue(model.lat_vector3[2])

    def poincare_hoff_rule(self):
        model = self.ui.openGLWidget.get_model()
        rule_text, rule_int = model.poincare_hoff_rule()
        if rule_int == 1:
            text = " is true!"
        else:
            text = " is not followed (" + str(rule_int) + ")"
        self.ui.cps_rule.setText("Poincare-Hoff rule " + rule_text + "= 1" + text)

    def default_histogram_text(self):
        if self.ui.bonds_histogram.isChecked():
            self.ui.histogram_x_label.setText("Bond lenght, A")
            self.ui.histogram_y_label.setText("Number of bonds")
            self.ui.histogram_title.setText("Bonds")
        if self.ui.bp_len_histogram.isChecked():
            self.ui.histogram_x_label.setText("Atom-atom distance, A")
            self.ui.histogram_y_label.setText("Number of bonds")
            self.ui.histogram_title.setText("Atom-atom distance")
        if self.ui.bcp_rho_histogram.isChecked():
            self.ui.histogram_x_label.setText("RHO, a.u.")
            self.ui.histogram_y_label.setText("Number of BCP")
            self.ui.histogram_title.setText("BCPs")

    def fill_cps(self):
        model = self.ui.openGLWidget.get_model()
        cp_types = model.get_cp_types()
        self.fill_cp_graph_types(cp_types)
        self.fill_cps_table()

    def fill_cp_graph_types(self, cp_types=["All"]):
        cp_type_gr = QStandardItemModel()
        for item in cp_types:
            cp_type_gr.appendRow(QStandardItem(item))
        self.ui.bcp_for_figure.setModel(cp_type_gr)
        self.ui.bcp_for_figure.setCurrentText("All")

    def update_bcp_figure_and_table(self):
        self.fill_cps_table()
        self.plot_r_rho()

    def fill_cps_table(self):
        model = self.ui.openGLWidget.get_model()
        is_bcp = False
        title = ["Property", "Value"]
        if self.ui.bcp_table.isChecked():
            is_bcp = True
            let = "xb"
            title = ["cp", "atoms", "rho", "dist"]
        if self.ui.ccp_table.isChecked():
            let = "xc"
            title = ["cp", "rho"]
        if self.ui.rcp_table.isChecked():
            let = "xr"
            title = ["cp", "rho"]
        if self.ui.natr_table.isChecked():
            let = "attr"
            title = ["cp", "rho"]
        properties = []
        n_cols = len(title)
        if not (model is None):
            for cp in model.cps:
                if cp.let == let:
                    if is_bcp:
                        if self.cp_need_to_gui(cp, model) and (cp.get_property("cp_bp_len") is not None):
                            properties.append([cp.get_property("title"), cp.get_property("atom_to_atom"),
                                               cp.get_property("rho"),
                                               str(round(cp.get_property("cp_bp_len"), 4))])
                    else:
                        properties.append([cp.get_property("title"), cp.get_property("rho")])
        cps_table = self.ui.cps_table
        cps_table.clear()
        cps_table.setColumnCount(n_cols)
        cps_table.setHorizontalHeaderLabels(title)
        cps_table.setColumnWidth(0, 85)
        cps_table.setColumnWidth(1, 260)
        cps_table.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        cps_table.verticalHeader().setStyleSheet(self.table_header_stylesheet)
        cps_table.setRowCount(len(properties))
        for i in range(0, len(properties)):
            for j in range(len(properties[i])):
                cps_table.setItem(i, j, QTableWidgetItem(properties[i][j]))

    def fill_bonds(self):
        c1, c2 = self.fill_bonds_charges()
        self.ui.FormActionsPosTableBonds.setRowCount(0)

        bonds_ok, bonds_mean, bonds_err = self.ui.openGLWidget.main_model.get_bonds_for_charges(c1, c2)

        n = 0
        for bond in bonds_ok:
            self.ui.FormActionsPosTableBonds.setRowCount(self.ui.FormActionsPosTableBonds.rowCount() + 1)
            s = str(bond[3]) + str(bond[4]) + "-" + str(bond[5]) + str(bond[6])
            self.ui.FormActionsPosTableBonds.setItem(n, 0, QTableWidgetItem(s))
            self.ui.FormActionsPosTableBonds.setItem(n, 1, QTableWidgetItem(str(bond[2])))
            n += 1
        bonds_text = "Mean value: " + str(bonds_mean) + " \u00B1 " + str(bonds_err)
        self.ui.FormActionsPostLabelMeanBond.setText(bonds_text)

    def fill_bonds_charges(self):
        bonds_category = self.ui.FormActionsPostComboBonds.currentText()
        if bonds_category == "All":
            c1 = 0
            c2 = 0
        else:
            bonds_category = bonds_category.split('-')
            c1 = self.periodic_table.get_charge_by_letter(bonds_category[0])
            c2 = self.periodic_table.get_charge_by_letter(bonds_category[1])
        return c1, c2

    def get_bonds(self):
        bonds_type = QStandardItemModel()
        bonds_type.appendRow(QStandardItem("All"))
        bonds = self.ui.openGLWidget.main_model.find_bonds_exact()
        items = []
        for bond in bonds:
            st1 = bond[3] + "-" + bond[5]
            st2 = bond[5] + "-" + bond[3]
            if (st1 not in items) and (st2 not in items):
                items.append(st1)
        items.sort()
        for item in items:
            bonds_type.appendRow(QStandardItem(item))
        self.ui.FormActionsPostComboBonds.currentIndexChanged.disconnect()
        self.ui.FormActionsPostComboBonds.setModel(bonds_type)
        self.ui.FormActionsPostComboBonds.currentIndexChanged.connect(self.fill_bonds)

        self.fill_bonds()
        self.ui.bonds_histogram.setCheckable(True)
        self.ui.plot_histogram.setEnabled(True)

    def get_bond(self):  # pragma: no cover
        i = self.ui.PropertyAtomAtomDistanceAt1.value()
        j = self.ui.PropertyAtomAtomDistanceAt2.value()
        bond = round(self.ui.openGLWidget.main_model.atom_atom_distance(i - 1, j - 1), 4)
        self.ui.PropertyAtomAtomDistance.setText(str(bond) + " A")

    # def get_colors_list(self, minv, maxv, values, cmap, color_scale):
    #     n = len(values)
    #     colors = []
    #     for i in range(0, n):
    #         value = values[i]
    #         colors.append(self.get_color(cmap, minv, maxv, value, color_scale))
    #     return colors

    def set_2d_graph_styles(self):
        color_r = self.ui.Form2DFontColorR.value()
        color_g = self.ui.Form2DFontColorG.value()
        color_b = self.ui.Form2DFontColorB.value()
        color = [color_r, color_g, color_b]
        title_font_size = self.ui.FormTitleFontSize.value()
        label_font_size = self.ui.FormLabelFontSize.value()
        axes_font_size = self.ui.FormAxesFontSize.value()
        line_width = self.ui.Form2DLineWidth.value()
        self.ui.PyqtGraphWidget.set_styles(title_font_size, axes_font_size, label_font_size, line_width, color)

    @staticmethod
    def get_color(cmap, minv, maxv, value, scale):
        if scale == "black":
            return QColor.fromRgb(0, 0, 0, 1).getRgbF()
        if scale == "Linear":
            return cmap((value - minv) / (maxv - minv))
        if scale == "Log":
            if minv < 1e-8:
                minv = 1e-8
            if value < 1e-8:
                value = 1e-8
            return cmap((math.log10(value) - math.log10(minv)) / (math.log10(maxv) - math.log10(minv)))
        return QColor.fromRgb(0, 0, 0, 1).getRgbF()

    @staticmethod
    def get_color_from_setting(strcolor: str):
        strcolor = strcolor.replace(',', ' ')
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor

    def load_settings(self) -> None:
        settings = QSettings()
        state_check_show_axes = settings.value(SETTINGS_ViewCheckShowAxes, False, type=bool)
        self.ui.FormSettingsViewCheckShowAxes.setChecked(state_check_show_axes)
        self.ui.FormSettingsViewCheckShowAxes.clicked.connect(self.save_state_view_show_axes)
        state_check_atom_selection = settings.value(SETTINGS_ViewCheckAtomSelection, False, type=bool)
        if state_check_atom_selection:
            self.ui.FormSettingsViewCheckAtomSelection.setChecked(True)
        else:
            self.ui.FormSettingsViewCheckModelMove.setChecked(True)
        self.ui.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_view_atom_selection)
        self.ui.FormSettingsViewCheckModelMove.clicked.connect(self.save_state_view_atom_selection)

        state_color_bonds_manual = settings.value(SETTINGS_ViewRadioColorBondsManual, False, type=bool)
        if state_color_bonds_manual:
            self.ui.FormSettingsViewRadioColorBondsManual.setChecked(True)
        else:
            self.ui.FormSettingsViewRadioColorBondsByAtoms.setChecked(True)
        self.ui.FormSettingsViewRadioColorBondsManual.clicked.connect(self.save_state_view_bond_color)
        self.ui.FormSettingsViewRadioColorBondsByAtoms.clicked.connect(self.save_state_view_bond_color)

        state_show_atoms = settings.value(SETTINGS_ViewCheckShowAtoms, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtoms.setChecked(state_show_atoms)
        self.ui.FormSettingsViewCheckShowAtoms.clicked.connect(self.save_state_view_show_atoms)

        state_show_atom_number = settings.value(SETTINGS_ViewCheckShowAtomNumber, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtomNumber.setChecked(state_show_atom_number)
        self.ui.FormSettingsViewCheckShowAtomNumber.clicked.connect(self.save_state_view_show_atom_number)

        state_show_box = settings.value(SETTINGS_ViewCheckShowBox, False, type=bool)
        self.ui.FormSettingsViewCheckShowBox.setChecked(state_show_box)
        self.ui.FormSettingsViewCheckShowBox.clicked.connect(self.save_state_view_show_box)

        state_show_bonds = settings.value(SETTINGS_ViewCheckShowBonds, True, type=bool)
        self.ui.FormSettingsViewCheckShowBonds.setChecked(state_show_bonds)
        self.ui.FormSettingsViewCheckShowBonds.clicked.connect(self.save_state_view_show_bonds)

        state_gl_cull_face = settings.value(SETTINGS_GlCullFace, True, type=bool)
        self.ui.OpenGL_GL_CULL_FACE.setChecked(state_gl_cull_face)
        self.ui.OpenGL_GL_CULL_FACE.clicked.connect(self.save_state_gl_cull_face)

        state_add_translated = settings.value(SETTINGS_IS_ADD_TRANSLATED_ATOMS, True, type=bool)
        self.ui.is_add_translated_atoms.setChecked(state_add_translated)
        self.ui.is_add_translated_atoms.clicked.connect(self.save_state_add_translated)

        state_show_props_for_list = settings.value(SETTINGS_IS_SHOW_ONLY_CP_PROPS_FOR_LIST, False, type=bool)
        self.ui.is_show_props_for_cp_list.setChecked(state_show_props_for_list)
        self.ui.is_show_props_for_cp_list.clicked.connect(self.save_state_show_props_for_cp_list)

        self.work_dir = str(settings.value(SETTINGS_Folder_CP, "/home"))
        self.color_type = str(settings.value(SETTINGS_ColorsScale, 'rainbow'))
        self.ui.FormSettingsColorsScale.currentIndexChanged.connect(self.save_state_colors_scale)
        self.ui.FormSettingsColorsScale.currentTextChanged.connect(self.state_changed_form_settings_colors_scale)
        self.color_type_scale = str(settings.value(SETTINGS_ColorsScaleType, 'Log'))
        self.ui.FormSettingsColorsScaleType.currentIndexChanged.connect(self.save_state_colors_scale_type)
        state_form_settings_colors_fixed = settings.value(SETTINGS_ColorsFixed, False, type=bool)
        self.ui.FormSettingsColorsFixed.setChecked(state_form_settings_colors_fixed)
        self.ui.FormSettingsColorsFixed.clicked.connect(self.save_state_colors_fixed)
        state_form_settings_colors_fixed_min = settings.value(SETTINGS_ColorsFixedMin, '0.1')
        try:
            min_val = float(state_form_settings_colors_fixed_min)
        except Exception:
            min_val = 0.0001
        self.ui.FormSettingsColorsFixedMin.setValue(min_val)
        self.ui.FormSettingsColorsFixedMin.valueChanged.connect(self.save_state_colors_fixed_min)
        state_form_settings_colors_fixed_max = settings.value(SETTINGS_ColorsFixedMax, '0.2')
        self.ui.FormSettingsColorsFixedMax.setValue(float(state_form_settings_colors_fixed_max))
        self.ui.FormSettingsColorsFixedMax.valueChanged.connect(self.save_state_colors_fixed_max)
        state_form_settings_view_spin_bond_width = int(settings.value(SETTINGS_ViewSpinBondWidth, '20'))
        self.ui.FormSettingsViewSpinBondWidth.setValue(state_form_settings_view_spin_bond_width)
        self.ui.FormSettingsViewSpinBondWidth.valueChanged.connect(self.save_state_view_spin_bond_width)
        state_form_settings_bond_path_width = int(settings.value(SETTINGS_bond_path_width, '3'))
        self.ui.bond_path_width.setValue(state_form_settings_bond_path_width)
        self.ui.bond_path_width.valueChanged.connect(self.save_state_view_spin_bond_path_width)

        state_color_scheme = str(settings.value(SETTINGS_Color_Of_Atoms_Scheme, ''))
        self.ui.manual_colors_default.setEnabled(False)
        if (state_color_scheme == 'None') or (state_color_scheme == '') or (state_color_scheme == 'cpk'):
            self.ui.cpk_radio.setChecked(True)
            self.color_of_atoms_scheme = "cpk"
        elif state_color_scheme == 'jmol':
            self.ui.jmol_radio.setChecked(True)
            self.color_of_atoms_scheme = "jmol"
        else:
            self.ui.manual_colors_radio.setChecked(True)
            self.color_of_atoms_scheme = "manual"
            self.ui.manual_colors_default.setEnabled(True)

        self.ui.cpk_radio.clicked.connect(self.save_state_atom_color_scheme)
        self.ui.jmol_radio.clicked.connect(self.save_state_atom_color_scheme)
        self.ui.manual_colors_radio.clicked.connect(self.save_state_atom_color_scheme)

        self.periodic_table.set_color_mode(self.color_of_atoms_scheme)

        self.ui.ColorsOfAtomsTable.setColumnCount(1)
        self.ui.ColorsOfAtomsTable.setHorizontalHeaderLabels(["Color"])
        self.ui.ColorsOfAtomsTable.setColumnWidth(0, 250)
        self.ui.ColorsOfAtomsTable.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.ColorsOfAtomsTable.verticalHeader().setStyleSheet(self.table_header_stylesheet)
        self.state_Color_Of_Atoms = str(settings.value(SETTINGS_Color_Of_Atoms, ''))
        if (self.state_Color_Of_Atoms == 'None') or (self.state_Color_Of_Atoms == ''):
            self.periodic_table.init_manual_colors()
        else:
            colors = []
            col = self.state_Color_Of_Atoms.split('|')
            for item in col:
                it = helpers.list_str_to_float(item.split())
                colors.append(it)
            self.periodic_table.set_manual_colors(colors)

        self.fill_colors_of_atoms_table()
        self.ui.ColorsOfAtomsTable.doubleClicked.connect(self.select_atom_color)

        self.state_Color_Of_Bonds = str(settings.value(SETTINGS_Color_Of_Bonds, '0 0 255'))
        self.color_to_ui(self.ui.ColorBond, self.state_Color_Of_Bonds)

        state_color_of_background = str(settings.value(SETTINGS_Color_Of_Background, '255 255 255'))
        self.color_to_ui(self.ui.ColorBackground, state_color_of_background)
        background_color = self.get_color_from_setting(state_color_of_background)
        self.ui.openGLWidget.set_color_of_background(background_color)

        self.state_Color_Of_Box = str(settings.value(SETTINGS_Color_Of_Box, '0 0 0'))
        self.color_to_ui(self.ui.ColorBox, self.state_Color_Of_Box)

        self.state_Color_Of_Axes = str(settings.value(SETTINGS_Color_Of_Axes, '0 255 0'))
        self.color_to_ui(self.ui.ColorAxes, self.state_Color_Of_Axes)

        self.state_color_of_bcp = str(settings.value(SETTINGS_color_of_bcp, '255 0 0'))
        self.color_to_ui(self.ui.color_bond_cp, self.state_color_of_bcp)

        self.state_color_of_rcp = str(settings.value(SETTINGS_color_of_rcp, '255 255 0'))
        self.color_to_ui(self.ui.color_ring_cp, self.state_color_of_rcp)

        self.state_color_of_ccp = str(settings.value(SETTINGS_color_of_ccp, '255 255 255'))
        self.color_to_ui(self.ui.color_cage_cp, self.state_color_of_ccp)

        self.state_color_of_bp = str(settings.value(SETTINGS_color_of_bp, '0 255 0'))
        self.color_to_ui(self.ui.color_bond_path, self.state_color_of_bp)

        self.action_on_start = str(settings.value(SETTINGS_ActionOnStart, 'Nothing'))

        self.perspective_angle = int(settings.value(SETTINGS_perspective_angle, 45))
        self.ui.spin_perspective_angle.setValue(self.perspective_angle)
        self.ui.openGLWidget.set_perspective_angle(self.perspective_angle)
        self.ui.spin_perspective_angle.valueChanged.connect(self.perspective_angle_change)

        self.ui.font_size_3d.setValue(int(settings.value(SETTINGS_PropertyFontSize, 8)))
        self.ui.property_shift_x.setValue(int(settings.value(SETTINGS_PropertyShiftX, 0)))
        self.ui.property_shift_y.setValue(int(settings.value(SETTINGS_PropertyShiftY, 0)))

    def save_state_atom_color_scheme(self):
        self.ui.manual_colors_default.setEnabled(False)
        if self.ui.cpk_radio.isChecked():
            self.color_of_atoms_scheme = "cpk"
        elif self.ui.jmol_radio.isChecked():
            self.color_of_atoms_scheme = "jmol"
        else:
            self.color_of_atoms_scheme = "manual"
            self.ui.manual_colors_default.setEnabled(True)

        self.periodic_table.set_color_mode(self.color_of_atoms_scheme)
        self.save_property(SETTINGS_Color_Of_Atoms_Scheme, self.color_of_atoms_scheme)

        self.fill_colors_of_atoms_table()

        if self.ui.openGLWidget.main_model.n_atoms() > 0:
            self.ui.openGLWidget.set_color_of_atoms(self.periodic_table.get_all_colors())

    def fill_colors_of_atoms_table(self):
        lets = self.periodic_table.get_all_letters()
        colors = self.periodic_table.get_all_colors()
        edit_text = ""
        if self.color_of_atoms_scheme == "manual":
            edit_text = " double click to edit"

        for i in range(1, len(lets) - 1):
            self.ui.ColorsOfAtomsTable.setRowCount(i)
            self.ui.ColorsOfAtomsTable.setItem(i - 1, 0, QTableWidgetItem(lets[i] + edit_text))
            self.ui.ColorsOfAtomsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(*colors[i]))

    def perspective_angle_change(self):
        self.perspective_angle = self.ui.spin_perspective_angle.value()
        self.save_property(SETTINGS_perspective_angle, str(self.perspective_angle))
        self.ui.spin_perspective_angle.valueChanged.connect(self.perspective_angle_change)
        self.ui.openGLWidget.set_perspective_angle(self.perspective_angle)
        self.ui.openGLWidget.update()

    def menu_export(self):  # pragma: no cover
        if self.ui.openGLWidget.main_model.n_atoms() > 0:
            try:
                file_name = self.get_file_name_from_save_dialog("GUI4dft project (*.data)")

                if not file_name:
                    return

                ImporterExporter.export_to_file(self.models[self.active_model_id], file_name)
                self.work_dir = os.path.dirname(file_name)
                self.save_active_folder()
            except Exception as e:
                self.show_error(e)

    def menu_open(self, file_name=False):
        if len(self.models) > 0:  # pragma: no cover
            self.action_on_start = 'Open'
            self.save_state_action_on_start()
            if sys.platform.startswith('win'):
                os.execlp('python', 'python', *sys.argv)
            else:
                os.execlp('python3', 'python3', *sys.argv)
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if not file_name:
            name_filter = "All supported files (*.cro *.outp *.data);;Critic2 output (*.cro)"
            name_filter += ";;TOPOND output (*.outp);;CritPlot project file (*.data)"
            file_name = self.get_file_name_from_open_dialog(name_filter)
        if os.path.exists(file_name):
            self.filename = file_name
            self.work_dir = os.path.dirname(file_name)
            is_add_translations = self.ui.is_add_translated_atoms.isChecked()
            try:
                self.models, is_critic_open = ImporterExporter.import_from_file(file_name, is_add_translations)
                if is_critic_open:
                    self.ui.add_xyz_critic_data.setEnabled(True)
            except Exception as e:
                print("Incorrect file format")
                self.show_error(e)
            try:
                self.plot_last_model()
                self.ui.plot_histogram.setEnabled(True)
            except Exception as e:  # pragma: no cover
                self.show_error(e)

    def plot_last_model(self):
        if len(self.models) > 0:
            if self.models[-1].n_atoms() > 0:
                self.plot_model(-1)
                self.fill_gui()
                self.save_active_folder()

    def menu_ortho(self):  # pragma: no cover
        self.ui.openGLWidget.is_camera_ortho = True
        self.ui.openGLWidget.update()

    def menu_perspective(self):  # pragma: no cover
        self.ui.openGLWidget.is_camera_ortho = False
        self.ui.openGLWidget.update()

    def menu_show_box(self):  # pragma: no cover
        self.ui.FormSettingsViewCheckShowBox.isChecked(True)
        self.ui.openGLWidget.is_view_box = True
        self.ui.openGLWidget.update()

    def menu_hide_box(self):  # pragma: no cover
        self.ui.FormSettingsViewCheckShowBox.isChecked(False)
        self.ui.openGLWidget.is_view_box = False
        self.ui.openGLWidget.update()

    def menu_manual(self):  # pragma: no cover
        path = str(Path(__file__).parent.parent.parent / 'doc' / 'gui4dft.pdf')
        os.system(path)

    def menu_about(self):  # pragma: no cover
        about_win = QDialog(self)
        about_win.ui = Ui_about()
        about_win.ui.setupUi(about_win)
        about_win.setFixedSize(QSize(550, 250))
        about_win.show()

    def model_to_screen(self, value):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()
        self.show_property_enabling()

    def show_property_enabling(self):  # pragma: no cover
        standart_prop = ["bond1", "bond2", "bond1opt", "bond2opt", "atom1", "atom2"]
        standart_prop.extend(["text", "atom1_translation", "atom2_translation"])
        if len(self.ui.openGLWidget.main_model.cps) > 0:
            bcp = self.ui.openGLWidget.main_model.cps[0]
            bcp_prop_type = QStandardItemModel()
            for key in bcp.properties:
                if str(key) not in standart_prop:
                    bcp_prop_type.appendRow(QStandardItem(str(key)))
            self.ui.PropertyForBCPtext.setModel(bcp_prop_type)

    def cp_property_precision_changed(self):  # pragma: no cover
        self.ui.openGLWidget.property_precision_changed(self.ui.property_precision.value())
        self.show_cp_property()

    def font_size_3d_changed(self):  # pragma: no cover
        self.save_property(SETTINGS_PropertyFontSize, self.ui.font_size_3d.value())
        self.ui.openGLWidget.set_property_font_size(self.ui.font_size_3d.value())
        self.show_cp_property()

    def property_position_changed(self):  # pragma: no cover
        dx = self.ui.property_shift_x.value()
        dy = self.ui.property_shift_y.value()
        self.save_property(SETTINGS_PropertyShiftX, dx)
        self.save_property(SETTINGS_PropertyShiftY, dy)
        self.ui.openGLWidget.set_property_shift(dx, dy)
        self.show_cp_property()

    def show_cps(self):  # pragma: no cover
        self.ui.openGLWidget.set_property_show_cp(self.ui.show_bcp.isChecked(), self.ui.show_ccp.isChecked(),
                                                  self.ui.show_rcp.isChecked(), self.ui.show_ncp.isChecked(),
                                                  self.ui.show_nnatr.isChecked())
        self.show_cp_property()

    def show_bond_path(self):  # pragma: no cover
        self.ui.openGLWidget.set_property_bond_path(self.ui.show_bond_path.isChecked())
        self.show_cp_property()

    def show_cp_property(self):  # pragma: no cover
        self.ui.openGLWidget.set_is_bcp_property_for_all(self.ui.is_show_props_for_cp_list.isChecked())
        if self.ui.show_bcp_text.isChecked():
            prop = self.ui.PropertyForBCPtext.currentText()
            self.ui.openGLWidget.show_cp_property(prop)
            self.ui.openGLWidget.set_property_font_size(self.ui.font_size_3d.value())
            dx = self.ui.property_shift_x.value()
            dy = self.ui.property_shift_y.value()
            self.ui.openGLWidget.set_property_shift(dx, dy)
        else:
            self.ui.openGLWidget.show_cp_property()

    def model_x_circular_shift(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.models[self.active_model_id]
        step = self.ui.x_circular_shift_step.value()
        if step < 0:
            step = np.linalg.norm(model.lat_vector1) + step
        model.move(np.array([-step, 0, 0]))
        model.go_to_positive_coordinates_translate()
        self.add_model_and_show(model)

    def model_y_circular_shift(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.models[self.active_model_id]
        step = self.ui.y_circular_shift_step.value()
        if step < 0:
            step = np.linalg.norm(model.lat_vector2) + step
        model.move(np.array([0, -step, 0]))
        model.go_to_positive_coordinates_translate()
        self.add_model_and_show(model)

    def model_z_circular_shift(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.models[self.active_model_id]
        step = self.ui.z_circular_shift_step.value()
        if step < 0:
            step = np.linalg.norm(model.lat_vector3) + step
        model.move(np.array([0, 0, -step]))
        model.go_to_positive_coordinates_translate()
        self.add_model_and_show(model)

    def model_go_to_positive(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model.go_to_positive_coordinates_translate()
        self.add_model_and_show(model)

    def model_additional_atoms_delete(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model.translated_atoms_remove()
        model.find_bonds_fast()
        self.add_model_and_show(model)

    def model_go_to_cell(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model.move_atoms_to_cell()
        self.add_model_and_show(model)

    def model_center_to_zero(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model.move_atoms_to_zero()
        self.add_model_and_show(model)

    def add_model_and_show(self, model):  # pragma: no cover
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def plot_model(self, value):
        if len(self.models) < value:
            return
        if self.models[value].n_atoms() == 0:
            return
        self.active_model_id = value
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        view_atoms = self.ui.FormSettingsViewCheckShowAtoms.isChecked()
        view_atom_numbers = self.ui.FormSettingsViewCheckShowAtomNumber.isChecked()
        view_box = self.ui.FormSettingsViewCheckShowBox.isChecked()
        view_bonds = self.ui.FormSettingsViewCheckShowBonds.isChecked()
        bond_width = 0.005 * self.ui.FormSettingsViewSpinBondWidth.value()
        bonds_color = self.get_color_from_setting(self.state_Color_Of_Bonds)
        color_of_bonds_by_atoms = self.ui.FormSettingsViewRadioColorBondsManual.isChecked()
        axes_color = self.get_color_from_setting(self.state_Color_Of_Axes)
        view_axes = self.ui.FormSettingsViewCheckShowAxes.isChecked()
        box_color = self.get_color_from_setting(self.state_Color_Of_Box)
        atoms_color = self.colors_of_atoms()
        color_of_bcp = self.get_color_from_setting(self.state_color_of_bcp)
        color_of_rcp = self.get_color_from_setting(self.state_color_of_rcp)
        color_of_ccp = self.get_color_from_setting(self.state_color_of_ccp)
        color_of_bp = self.get_color_from_setting(self.state_color_of_bp)
        self.ui.openGLWidget.set_cp_related_colors(color_of_bcp, color_of_rcp, color_of_ccp, color_of_bp)
        self.show_cps()
        self.ui.openGLWidget.set_structure_parameters(atoms_color, view_atoms, view_atom_numbers, view_box, box_color,
                                                      view_bonds, bonds_color, bond_width, color_of_bonds_by_atoms,
                                                      view_axes, axes_color)
        self.ui.openGLWidget.set_cp_parameters(self.ui.show_bcp_text.isChecked())
        self.ui.openGLWidget.set_width_of_bp(self.ui.bond_path_width.value())
        self.ui.openGLWidget.set_atomic_structure(self.models[self.active_model_id])
        self.ui.AtomsInSelectedFragment.clear()

        self.show_property_enabling()

    def plot_histogram_of_data(self):
        self.ui.pyqt_hist_widget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        self.ui.pyqt_hist_widget.clear()
        b = []

        f1 = self.ui.bonds_histogram.isChecked()
        f2 = self.ui.bp_len_histogram.isChecked()
        f3 = self.ui.bcp_rho_histogram.isChecked()

        if f1:
            c1, c2 = self.fill_bonds_charges()
            bonds, bonds_mean, bonds_err = self.ui.openGLWidget.main_model.get_bonds_for_charges(c1, c2)
            for bond in bonds:
                b.append(bond[2])

        if f2 or f3:
            model = self.ui.openGLWidget.get_model()
            if not (model is None):
                for cp in model.cps:
                    if f2 and (cp.let == "xb") and (cp.get_property("cp_bp_len") is not None):
                        b.append(round(cp.get_property("cp_bp_len"), 4))
                    if f3 and (cp.let == "xb"):
                        b.append(float(cp.get_property("rho")))

        if f1 or f2 or f3:
            num_bins = self.ui.FormActionsPostPlotBondsHistogramN.value()
            x_title = self.ui.histogram_x_label.text()
            y_title = self.ui.histogram_y_label.text()
            title = self.ui.histogram_title.text()
            self.ui.pyqt_hist_widget.add_histogram(b, num_bins, (0, 0, 255, 90), title, x_title, y_title)

    @staticmethod
    def list_of_selected_items_in_combo(atom_index, combo):
        model = combo.model()
        maxi = combo.count()
        for i in range(0, maxi):
            if model.itemFromIndex(model.index(i, 0)).checkState() == Qt.Checked:
                atom_index.append(int(model.itemFromIndex(model.index(i, 0)).text()))

    def save_image_to_file(self, name=""):
        if len(self.models) == 0:
            return
        try:
            if not name:
                format_str = "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)"
                f_name = self.get_file_name_from_save_dialog(format_str)
                if f_name:
                    new_window = Image3Dexporter(5 * self.ui.openGLWidget.width(), 5 * self.ui.openGLWidget.height(), 5)
                    new_window.ui.openGLWidget.copy_state(self.ui.openGLWidget)
                    new_window.ui.openGLWidget.image3d_to_file(f_name)
                    new_window.destroy()
                    self.work_dir = os.path.dirname(f_name)
                    self.save_active_folder()
        except Exception as excep:
            self.show_error(excep)

    def move_model_left(self):  # pragma: no cover
        self.ui.openGLWidget.camera_position_change(np.array([-self.move_step, 0.0, 0.0]))
        self.ui.openGLWidget.update()

    def move_model_right(self):  # pragma: no cover
        self.ui.openGLWidget.camera_position_change(np.array([self.move_step, 0.0, 0.0]))
        self.ui.openGLWidget.update()

    def move_model_up(self):  # pragma: no cover
        self.ui.openGLWidget.camera_position_change(np.array([0.0, self.move_step, 0.0]))
        self.ui.openGLWidget.update()

    def move_model_down(self):  # pragma: no cover
        self.ui.openGLWidget.camera_position_change(np.array([0.0, -self.move_step, 0.0]))
        self.ui.openGLWidget.update()

    def rotate_model_xp(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([self.rotation_step, 0, 0]))
        self.ui.openGLWidget.update()

    def rotate_model_xm(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([-self.rotation_step, 0, 0]))
        self.ui.openGLWidget.update()

    def rotate_model_yp(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([0, self.rotation_step, 0]))
        self.ui.openGLWidget.update()

    def rotate_model_ym(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([0, -self.rotation_step, 0]))
        self.ui.openGLWidget.update()

    def rotate_model_zp(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([0, 0, self.rotation_step]))
        self.ui.openGLWidget.update()

    def rotate_model_zm(self):  # pragma: no cover
        self.ui.openGLWidget.rotation_angle_change(np.array([0, 0, -self.rotation_step]))
        self.ui.openGLWidget.update()

    def model_orientation_post(self):  # pragma: no cover
        self.ui.openGLWidget.update()
        self.orientation_model_changed()

    def save_active_folder(self):  # pragma: no cover
        self.save_property(SETTINGS_Folder_CP, self.work_dir)

    def save_state_view_show_axes(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckShowAxes, self.ui.FormSettingsViewCheckShowAxes.isChecked())
        self.ui.openGLWidget.set_axes_visible(self.ui.FormSettingsViewCheckShowAxes.isChecked())

    def save_state_view_atom_selection(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckAtomSelection, self.ui.FormSettingsViewCheckAtomSelection.isChecked())

    def save_state_view_bond_color(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewRadioColorBondsManual,
                           self.ui.FormSettingsViewRadioColorBondsManual.isChecked())
        self.ui.openGLWidget.set_bond_color(self.ui.FormSettingsViewRadioColorBondsManual.isChecked())

    def save_state_view_show_atoms(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckShowAtoms, self.ui.FormSettingsViewCheckShowAtoms.isChecked())
        self.ui.openGLWidget.set_atoms_visible(self.ui.FormSettingsViewCheckShowAtoms.isChecked())

    def save_state_view_show_atom_number(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckShowAtomNumber,
                           self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())
        self.ui.openGLWidget.set_atoms_numbered(self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())

    def save_state_add_translated(self):  # pragma: no cover
        self.save_property(SETTINGS_IS_ADD_TRANSLATED_ATOMS,
                           self.ui.is_add_translated_atoms.isChecked())

    def save_state_show_props_for_cp_list(self):  # pragma: no cover
        self.save_property(SETTINGS_IS_SHOW_ONLY_CP_PROPS_FOR_LIST,
                           self.ui.is_show_props_for_cp_list.isChecked())
        self.ui.openGLWidget.set_is_bcp_property_for_all(self.ui.is_show_props_for_cp_list.isChecked())

    def save_state_action_on_start(self):  # pragma: no cover
        self.save_property(SETTINGS_ActionOnStart, self.action_on_start)

    def save_state_to_run(self):
        self.save_property(SETTINGS_Executable, self.executable)
        self.save_property(SETTINGS_Argv, self.argv)
        print("Saving: \n")
        print(self.executable)
        print(self.argv)

    def save_state_view_show_box(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.ui.openGLWidget.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_view_show_bonds(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.ui.openGLWidget.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

    def save_state_gl_cull_face(self):  # pragma: no cover
        self.save_property(SETTINGS_GlCullFace, self.ui.OpenGL_GL_CULL_FACE.isChecked())
        self.ui.openGLWidget.set_gl_cull_face(self.ui.OpenGL_GL_CULL_FACE.isChecked())

    def save_state_colors_fixed(self):  # pragma: no cover
        self.save_property(SETTINGS_ColorsFixed, self.ui.FormSettingsColorsFixed.isChecked())

    def save_state_colors_fixed_min(self):  # pragma: no cover
        self.save_property(SETTINGS_ColorsFixedMin, self.ui.FormSettingsColorsFixedMin.text())

    def save_state_view_spin_bond_width(self):  # pragma: no cover
        self.save_property(SETTINGS_ViewSpinBondWidth, self.ui.FormSettingsViewSpinBondWidth.text())
        self.ui.openGLWidget.set_bond_width(self.ui.FormSettingsViewSpinBondWidth.value() * 0.005)

    def save_state_view_spin_bond_path_width(self):  # pragma: no cover
        self.save_property(SETTINGS_bond_path_width, self.ui.bond_path_width.text())
        self.ui.openGLWidget.set_width_of_bp(self.ui.bond_path_width.value())

    def save_state_colors_fixed_max(self):  # pragma: no cover
        self.save_property(SETTINGS_ColorsFixedMax, self.ui.FormSettingsColorsFixedMax.text())

    def save_state_colors_scale(self):  # pragma: no cover
        self.save_property(SETTINGS_ColorsScale, self.ui.FormSettingsColorsScale.currentText())
        self.colors_cash = {}

    def save_state_colors_scale_type(self):  # pragma: no cover
        self.save_property(SETTINGS_ColorsScaleType, self.ui.FormSettingsColorsScaleType.currentText())
        self.colors_cash = {}

    @staticmethod
    def save_property(var_property, value):  # pragma: no cover
        settings = QSettings()
        settings.setValue(var_property, value)
        settings.sync()

    def orientation_model_changed(self, rotation_angles, camera_position, scale_factor):
        """Update form from model"""
        self.ui.model_rotation_x.setValue(float(rotation_angles[0]))
        self.ui.model_rotation_y.setValue(float(rotation_angles[1]))
        self.ui.model_rotation_z.setValue(float(rotation_angles[2]))
        self.ui.camera_pos_x.setValue(float(camera_position[0]))
        self.ui.camera_pos_y.setValue(float(camera_position[1]))
        self.ui.camera_pos_z.setValue(float(camera_position[2]))
        self.ui.model_scale.setValue(float(scale_factor))

    def model_orientation_changed(self):
        """Update model from form"""
        rotation_angles = [self.ui.model_rotation_x.value(), self.ui.model_rotation_y.value(),
                           self.ui.model_rotation_z.value()]
        camera_position = [self.ui.camera_pos_x.value(), self.ui.camera_pos_y.value(), self.ui.camera_pos_z.value()]
        scale_factor = self.ui.model_scale.value()
        self.ui.openGLWidget.set_orientation(rotation_angles, camera_position, scale_factor)

    def selected_atom_position(self, element, position):
        self.ui.FormActionsPreComboAtomsList.setCurrentIndex(element)
        self.ui.FormActionsPreSpinAtomsCoordX.setValue(position[0])
        self.ui.FormActionsPreSpinAtomsCoordX.update()
        self.ui.FormActionsPreSpinAtomsCoordY.setValue(position[1])
        self.ui.FormActionsPreSpinAtomsCoordY.update()
        self.ui.FormActionsPreSpinAtomsCoordZ.setValue(position[2])
        self.ui.FormActionsPreSpinAtomsCoordZ.update()

    def selected_atom_changed(self, selected):
        selected_atom = selected[0]
        selected_cp = selected[1]
        model = self.models[self.active_model_id]
        text = ""
        text_sel = ""
        if (selected_atom == -1) and (selected_cp == -1):
            self.history_of_point_selection = []
            self.history_of_point_selection_xyz = []
            text = "Select any atom or critical point."
            self.selected_cp_clear()
        else:
            if selected_atom >= 0:
                sel_atom = model.atoms[selected_atom]
                self.history_of_point_selection.append(sel_atom.let + str(selected_atom + 1))
                self.history_of_point_selection_xyz.append(sel_atom.xyz)
            if selected_cp >= 0:
                cp = model.cps[selected_cp]
                self.history_of_point_selection.append(cp.let + str(selected_cp + 1))
                self.history_of_point_selection_xyz.append(cp.xyz)

            if len(self.history_of_point_selection) > 1:
                text_sel = "\nHistory of points selection: " + str(np.array(self.history_of_point_selection)) + "\n"
                text_sel += "Distance from " + self.history_of_point_selection[-1] + " to " + \
                            self.history_of_point_selection[-2] + " : "

                dist = model.point_point_distance(self.history_of_point_selection_xyz[-1],
                                                  self.history_of_point_selection_xyz[-2])
                text_sel += str(round(dist / 10, 6)) + " nm\n"

                if len(self.history_of_point_selection) > 2:
                    xyz1 = self.history_of_point_selection_xyz[-1]
                    xyz2 = self.history_of_point_selection_xyz[-2]
                    xyz3 = self.history_of_point_selection_xyz[-3]
                    if any(xyz1 != xyz2) and any(xyz3 != xyz2):
                        angle = helpers.angle_for_3_points(xyz1, xyz2, xyz3)
                        text_sel += "3 points: " + self.history_of_point_selection[-1] + " - " + \
                                    self.history_of_point_selection[-2] + " - " + \
                                    self.history_of_point_selection[-3] + "\n"
                        text_sel += "    angle " + str(round(math.degrees(angle), 3)) + " degrees\n"
                        plane = helpers.plane_for_3_points(xyz1, xyz2, xyz3)
                        text_sel += "    Plane :"
                        text_sel += str(round(plane[0], 6)) + "x "
                        if plane[1] > 0:
                            text_sel += "+"
                        text_sel += str(round(plane[1], 6)) + "y "
                        if plane[2] > 0:
                            text_sel += "+"
                        text_sel += str(round(plane[2], 6)) + "z "
                        if plane[3] > 0:
                            text_sel += "+"
                        str(round(plane[3], 6)) + "= 0\n"

            if selected_atom >= 0:
                model = self.models[self.active_model_id]
                text += "Selected atom: " + str(selected_atom + 1) + "\n"
                atom = model.atoms[selected_atom]
                text += "Element: " + atom.let + "\n"
                for key in atom.properties:
                    text += str(key) + ": " + str(atom.properties[key]) + "\n"

            if selected_cp >= 0:
                model = self.models[self.active_model_id]
                text = "Selected critical point: " + str(selected_cp + 1) + " ("
                cp = model.cps[selected_cp]

                bond1 = cp.bonds.get("bond1")
                bond2 = cp.bonds.get("bond2")

                ind1 = cp.get_property("atom1")
                ind2 = cp.get_property("atom2")

                atom_to_atom = cp.get_property("atom_to_atom")
                dist = cp.get_property("cp_bp_len")

                if (ind1 is not None) and (ind2 is not None):
                    text += atom_to_atom + ")\n"
                    if bond1 is not None and bond2 is not None:
                        text += "Bond critical path: " + str(len(bond1)) + " + " + str(len(bond2)) + " = "
                        text += str(len(bond1) + len(bond2)) + " points\n"
                    if dist is not None:
                        dist_line = round(dist, 4)
                        self.ui.selected_cp_bond_len.setText(str(dist_line) + " A")
                        self.ui.selectedCP_nuclei.setText(atom_to_atom)
                    else:
                        self.ui.selected_cp_bond_len.setText("...")
                        self.ui.selectedCP_nuclei.setText("...")
                else:
                    text += ")\n"

                self.ui.selectedCP.setText(str(selected_cp + 1))

                t = model.cps[selected_cp].get_property("title")
                self.ui.selected_cp_title.setText(t)
                f = model.cps[selected_cp].get_property("rho")
                self.ui.FormSelectedCP_f.setText(f)
                g = model.cps[selected_cp].get_property("grad")
                self.ui.FormSelectedCP_g.setText(g)
                lap = model.cps[selected_cp].get_property("lap")
                self.ui.FormSelectedCP_lap.setText(lap)

                for key in model.cps[selected_cp].properties:
                    text += str(key) + ": " + str(model.cps[selected_cp].get_property(key)) + "\n"

        self.ui.atom_and_cp_properties_text.setText(text + text_sel)

    def selected_cp_clear(self):
        self.ui.selectedCP.setText("...")
        self.ui.FormSelectedCP_f.setText("...")
        self.ui.FormSelectedCP_g.setText("...")
        self.ui.FormSelectedCP_lap.setText("...")
        self.ui.selected_cp_bond_len.setText("...")
        self.ui.selected_cp_title.setText("...")
        self.ui.selectedCP_nuclei.setText("...")

    def set_manual_colors_default(self):
        self.periodic_table.init_manual_colors()
        self.color_of_atoms_scheme = "manual"
        self.periodic_table.set_color_mode(self.color_of_atoms_scheme)
        self.save_property(SETTINGS_Color_Of_Atoms_Scheme, self.color_of_atoms_scheme)
        self.save_manual_colors()

        self.fill_colors_of_atoms_table()

        if self.ui.openGLWidget.main_model.n_atoms() > 0:
            self.ui.openGLWidget.set_color_of_atoms(self.periodic_table.get_all_colors())

    def save_manual_colors(self):
        text_color = self.periodic_table.manual_color_to_text()
        self.save_property(SETTINGS_Color_Of_Atoms, text_color)

    def state_changed_form_settings_colors_scale(self):
        if self.ui.FormSettingsColorsScale.currentText() == "":
            self.ui.ColorRow.clear()
        else:
            self.ui.ColorRow.plot_mpl_colormap(self.ui.FormSettingsColorsScale.currentText())

    @staticmethod
    def change_color_of_cell_prompt(table):  # pragma: no cover
        i = table.selectedIndexes()[0].row()
        color = QColorDialog.getColor(initial=table.item(i, 0).background().color())
        if not color.isValid():
            return
        at_color = color.getRgbF()
        table.item(i, 0).setBackground(QColor.fromRgbF(*at_color))
        return i, at_color

    def select_atom_color(self):  # pragma: no cover
        if self.color_of_atoms_scheme != "manual":
            return

        table = self.ui.ColorsOfAtomsTable
        i, at_color = self.change_color_of_cell_prompt(table)
        self.periodic_table.set_manual_color(i + 1, at_color)

        self.save_manual_colors()

        if self.ui.openGLWidget.main_model.n_atoms() > 0:
            self.ui.openGLWidget.set_color_of_atoms(self.periodic_table.get_all_colors())

    def select_box_color(self):  # pragma: no cover
        boxcolor = self.change_color(self.ui.ColorBox, SETTINGS_Color_Of_Box)
        self.ui.openGLWidget.set_color_of_box(boxcolor)

    def select_bcp_color(self):  # pragma: no cover
        bcp_color = self.change_color(self.ui.color_bond_cp, SETTINGS_color_of_bcp)
        self.ui.openGLWidget.set_color_of_bcp(bcp_color)

    def select_ccp_color(self):  # pragma: no cover
        ccp_color = self.change_color(self.ui.color_ring_cp, SETTINGS_color_of_rcp)
        self.ui.openGLWidget.set_color_of_ccp(ccp_color)

    def select_rcp_color(self):  # pragma: no cover
        rcp_color = self.change_color(self.ui.color_cage_cp, SETTINGS_color_of_ccp)
        self.ui.openGLWidget.set_color_of_rcp(rcp_color)

    def select_bp_color(self):  # pragma: no cover
        bp_color = self.change_color(self.ui.color_bond_path, SETTINGS_color_of_bp)
        self.ui.openGLWidget.set_color_of_bp(bp_color)

    def hide_cps_min_rho(self):
        if len(self.models) == 0:
            return
        min_rho = self.ui.min_rho_for_cps.value()
        for cp in self.ui.openGLWidget.main_model.cps:
            if float(cp.get_property("rho")) < min_rho:
                cp.is_visible = False
        self.ui.openGLWidget.add_all_elements()

    def hide_cps_eq_atoms(self):
        if len(self.models) == 0:
            return
        for cp in self.ui.openGLWidget.main_model.cps:
            at1 = cp.get_property("atom1")
            at2 = cp.get_property("atom2")
            if (at1 is not None) and (at2 is not None):
                if at1 == at2:
                    atom1_translation = cp.get_property("atom1_translation")
                    atom2_translation = cp.get_property("atom2_translation")
                    if all(atom1_translation == atom2_translation):
                        cp.is_visible = False
        self.ui.openGLWidget.add_all_elements()

    def cancel_cps_filters(self):
        if len(self.models) == 0:
            return
        for cp in self.ui.openGLWidget.main_model.cps:
            cp.is_visible = True
        self.ui.openGLWidget.add_all_elements()

    def cp_activate(self, cp):
        self.ui.openGLWidget.main_model.cps[int(cp) - 1].active = True

    def cp_deactivate(self, cp):
        self.ui.openGLWidget.main_model.cps[int(cp) - 1].active = False

    def add_cp_to_list(self):
        new_cp = self.ui.selectedCP.text()
        if new_cp == "...":
            return

        fl = True
        for i in range(0, self.ui.FormCPlist.count()):
            if self.ui.FormCPlist.item(i).text() == new_cp:
                fl = False
        if fl:
            QListWidgetItem(new_cp, self.ui.FormCPlist)
            self.cp_activate(new_cp)
            self.ui.openGLWidget.update()

    def delete_cp_from_list(self):  # pragma: no cover
        item_row = self.ui.FormCPlist.currentRow()
        if item_row >= 0:
            self.cp_deactivate(self.ui.FormCPlist.item(item_row).text())
            self.ui.FormCPlist.takeItem(item_row)
            self.ui.openGLWidget.update()

    def clear_cp_list(self):  # pragma: no cover
        for i in range(0, self.ui.FormCPlist.count()):
            self.cp_deactivate(self.ui.FormCPlist.item(i).text())
        self.ui.FormCPlist.clear()

    def delete_cp_from_model(self):
        model = self.models[self.active_model_id]
        bcp_selected = self.selected_cp()
        self.remove_cp_from_model(model, bcp_selected)
        self.plot_model(self.active_model_id)
        self.clear_cp_list()
        self.selected_cp_clear()

    def leave_cp_in_model(self):
        model = self.models[self.active_model_id]
        new_cps = []
        sel_cps = self.selected_cp()
        for cp in model.cps:
            f = False
            for b in sel_cps:
                if cp.to_string() == b.to_string():
                    f = True
            if (cp.let not in ["xb", "xr", "xc"]) or f:
                new_cps.append(cp)
        model.cps = new_cps
        self.ui.openGLWidget.selected_cp = -1
        self.clear_cp_list()
        self.selected_cp_clear()
        self.plot_model(self.active_model_id)

    @staticmethod
    def remove_cp_from_model(model, crit_points):
        bcp = deepcopy(model.cps)
        for b in crit_points:
            for cp in bcp:
                if cp.to_string() == b.to_string():
                    bcp.remove(cp)
        model.cps = bcp

    def selected_cp(self):
        bcp_selected = []
        if len(self.models) > 0:
            model = self.models[self.active_model_id]
            for i in range(0, self.ui.FormCPlist.count()):
                ind = int(self.ui.FormCPlist.item(i).text())
                bcp_selected.append(model.cps[ind - 1])
        return bcp_selected

    def create_critic2_xyz_file(self):  # pragma: no cover
        """ Create critic2 xyz file (with critical points)"""
        format_str = "xyz files (*.xyz)"
        f_name = self.get_file_name_from_save_dialog(format_str)
        is_with_selected = self.ui.radio_with_cp.isChecked()
        if f_name:
            model = self.models[self.active_model_id]
            bcp = deepcopy(model.cps)
            bcp_selected = self.selected_cp()
            text = model.create_critic2_xyz(bcp, bcp_selected, is_with_selected)
            helpers.write_text_to_file(f_name, text)

    def export_cp_to_csv(self):
        format_str = "csv files (*.csv)"
        f_name = self.get_file_name_from_save_dialog(format_str)

        if f_name is not None:
            model = self.models[self.active_model_id]

            cp_list = []
            if self.ui.form_critic_list.isChecked():
                for i in range(0, self.ui.FormCPlist.count()):
                    ind = int(self.ui.FormCPlist.item(i).text())
                    cp_list.append(ind)
            else:
                cp_list = range(1, len(model.cps) + 1)
            text = model.create_csv_file_cp(cp_list, self.ui.show_bcp.isChecked(), self.ui.show_ccp.isChecked(),
                                            self.ui.show_rcp.isChecked(), self.ui.show_ncp.isChecked(),
                                            self.ui.show_nnatr.isChecked())
            helpers.write_text_to_file(f_name, text)

    def create_cri_file(self):  # pragma: no cover
        fname = self.get_file_name_from_save_dialog("Critic2 input files (*.cri)")
        extra_points = self.ui.FormExtraPoints.value() + 1
        is_form_bp = self.ui.formCriticBPradio.isChecked()

        text_prop = ""
        if self.ui.form_critic_prop_gtf.isChecked():
            text_prop += 'POINTPROP GTF\n'
        if self.ui.form_critic_prop_vtf.isChecked():
            text_prop += 'POINTPROP VTF\n'
        if self.ui.form_critic_prop_htf.isChecked():
            text_prop += 'POINTPROP HTF\n'
        if self.ui.form_critic_prop_gtf_kir.isChecked():
            text_prop += 'POINTPROP GTF_KIR\n'
        if self.ui.form_critic_prop_vtf_kir.isChecked():
            text_prop += 'POINTPROP VTF_KIR\n'
        if self.ui.form_critic_prop_htf_kir.isChecked():
            text_prop += 'POINTPROP HTF_KIR\n'
        if self.ui.form_critic_prop_lag.isChecked():
            text_prop += 'POINTPROP LAG\n'
        if self.ui.form_critic_prop_lol_kir.isChecked():
            text_prop += 'POINTPROP LOL_KIR\n'
        if self.ui.form_critic_prop_rdg.isChecked():
            text_prop += 'POINTPROP RDG\n'

        if len(fname) > 0:
            model = self.models[self.active_model_id]

            cp_list = []
            if self.ui.form_critic_all_cp.isChecked():
                cp_list = range(len(model.cps))
            else:
                for i in range(0, self.ui.FormCPlist.count()):
                    ind = int(self.ui.FormCPlist.item(i).text())
                    cp_list.append(ind)
            textl, lines, te, text = model.create_cri_file(cp_list, extra_points, is_form_bp, text_prop)

            helpers.write_text_to_file(fname, textl + lines)

            fname_dir = os.path.dirname(fname)
            helpers.write_text_to_file(fname_dir + "/POINTS.txt", te)
            helpers.write_text_to_file(fname_dir + "/POINTSatoms.txt", text)

    def select_background_color(self):  # pragma: no cover
        background_color = self.change_color(self.ui.ColorBackground, SETTINGS_Color_Of_Background)
        self.ui.openGLWidget.set_color_of_background(background_color)

    def select_bond_color(self):  # pragma: no cover
        bondscolor = self.change_color(self.ui.ColorBond, SETTINGS_Color_Of_Bonds)
        self.ui.openGLWidget.set_color_of_bonds(bondscolor)

    def select_axes_color(self):  # pragma: no cover
        axescolor = self.change_color(self.ui.ColorAxes, SETTINGS_Color_Of_Axes)
        self.ui.openGLWidget.set_color_of_axes(axescolor)

    def change_color(self, color_ui, var_property):  # pragma: no cover
        color = QColorDialog.getColor()
        color_str = str(color.getRgb()[0]) + "," + str(color.getRgb()[1]) + "," + str(color.getRgb()[2])
        color_str_prop = str(color.getRgb()[0]) + " " + str(color.getRgb()[1]) + " " + str(color.getRgb()[2])
        color_ui.setStyleSheet("background-color:rgb(" + color_str + ")")
        new_color = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        self.save_property(var_property, color_str_prop )
        return new_color

    def bond_len_correct(self, d):
        let1 = self.ui.FormAtomsList1.currentText()
        let2 = self.ui.FormAtomsList2.currentText()
        self.ui.openGLWidget.bond_len_correct(let1, let2, d)
        print(let1, "-", let2, ": ", d)


SETTINGS_Folder_CP = 'home'
SETTINGS_ColorsScale = 'ColorsScale'
SETTINGS_ColorsFixed = 'ColorsFixed'
SETTINGS_ColorsFixedMin = 'ColorsFixedMin'
SETTINGS_ColorsFixedMax = 'ColorsFixedMax'
SETTINGS_ColorsScaleType = 'ColorsScaleType'
SETTINGS_ViewCheckAtomSelection = 'CheckAtomSelection'
SETTINGS_ViewRadioColorBondsManual = 'BondsColorType'
SETTINGS_ViewCheckShowAtoms = 'CheckShowAtoms'
SETTINGS_ViewCheckShowAtomNumber = 'CheckShowAtomNumber'
SETTINGS_ViewCheckShowBox = 'CheckShowBox'
SETTINGS_ViewCheckShowAxes = 'CheckShowAxes'
SETTINGS_ViewCheckShowBonds = 'CheckShowBonds'
SETTINGS_ViewSpinBondWidth = 'SpinBondWidth'
SETTINGS_bond_path_width = 'bond_path_width'
SETTINGS_ViewSpinContourWidth = 'SpinContourWidth'
SETTINGS_GlCullFace = 'GlCullFace'
SETTINGS_ActionOnStart = 'action/OnStart'
SETTINGS_Executable = ''
SETTINGS_Argv = ''
SETTINGS_PropertyFontSize = 'property/fontsize'
SETTINGS_PropertyShiftX = 'property/shiftx'
SETTINGS_PropertyShiftY = 'property/shifty'
SETTINGS_IS_ADD_TRANSLATED_ATOMS = 'atoms/addtranslated'
SETTINGS_IS_SHOW_ONLY_CP_PROPS_FOR_LIST = 'cps/showPropsStyle'

SETTINGS_CoordinatesStyle = 'model/FormSettingsPreferredCoordinatesStyle'
SETTINGS_Coordinates = 'model/FormSettingsPreferredCoordinates'
SETTINGS_Units = 'model/FormSettingsPreferred/units'
SETTINGS_Lattice = 'model/FormSettingsPreferredLattice'

SETTINGS_Color_Of_Atoms_Scheme = 'colors/scheme'
SETTINGS_Color_Of_Atoms = 'colors_atoms'
SETTINGS_Color_Of_Bonds = 'colors_bonds'
SETTINGS_Color_Of_Background = 'colors_background'
SETTINGS_Color_Of_Box = 'colors_box'
SETTINGS_Color_Of_Axes = 'colors_axes'
SETTINGS_color_of_bcp = 'colors_bcp'
SETTINGS_color_of_rcp = 'colors_rcp'
SETTINGS_color_of_ccp = 'colors_ccp'
SETTINGS_color_of_bp = 'colors_bp'
SETTINGS_perspective_angle = 'perspectiveangle'
