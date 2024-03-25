# -*- coding: utf-8 -*-
import os
try:
    if os.environ["XDG_SESSION_TYPE"] == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
except Exception as e:
    pass
import math
import sys
from multiprocessing import Pool
from time import time
from pathlib import Path
from copy import deepcopy
from operator import itemgetter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import numpy as np

from qtpy.QtCore import QLocale, QSettings, Qt, QSize
from qtpy.QtGui import QColor, QIcon, QImage, QKeySequence, QPixmap, QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QAction, QDialog, QFileDialog, QMessageBox, QColorDialog
from qtpy.QtWidgets import QDoubleSpinBox, QMainWindow, QShortcut, QTableWidgetItem, QTreeWidgetItem
from qtpy.QtWidgets import QTreeWidgetItemIterator

from ase.build import molecule, bulk

from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from core_atomistic.periodic_table import TPeriodTable
from core_atomistic import helpers

from models.capedswcnt import CapedSWNT
from models.bint import BiNT
from models.hexagonal_plane import HexagonalPlane, HexagonalPlaneHex
from models.meta_graphene import MetaGraphene
from models.swnt import SWNT
from models.swgnt import SWGNT
from models.gaussiancube import GaussianCube
from models.volumericdata import VolumericData
from models.xsf import XSF
from qtbased.image3dexporter import Image3Dexporter
from program.siesta import TSIESTA
from program.qe import model_to_qe_pw
from program.wien import model_to_wien_struct
from program.vasp import TVASP, vasp_dos, model_to_vasp_poscar, abc_from_outcar
from program.dftb import model_to_dftb_d0
from program.lammps import model_to_lammps_input
from program.octopus import model_to_octopus_input
from program import crystal
from program import ase
from program.fdfdata import TFDFFile
from utils.calculators import Calculators as Calculator
from utils.calculators import add_adatom, gaps, hops, fill_tube
from utils.importer_exporter import ImporterExporter
from utils.electronic_prop_reader import read_siesta_bands, dos_from_file
from ui.about import Ui_DialogAbout as Ui_about
from ui.form_hexa import Ui_MainWindow as Ui_form

sys.path.append('')

is_with_figure = True


class MainForm(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.ui = Ui_form()
        self.ui.setupUi(self)

        self.program: str = "SIESTA"  # mode of operation fot program

        self.models = []
        self.ui.openGLWidget.set_form_elements(self.ui.FormSettingsViewCheckAtomSelection,
                                               self.orientation_model_changed, self.selected_atom_position,
                                               self.selected_atom_changed, 1)
        self.fdf_data = TFDFFile()
        self.volumeric_data = VolumericData()
        self.volumeric_data2 = VolumericData()  # only for volumeric data difference
        self.PDOSdata = []
        self.filename: str = ""
        self.work_dir: str = None
        self.colors_cash = {}
        self.table_header_stylesheet = "::section{Background-color:rgb(190,190,190)}"
        self.is_scaled_colors_for_surface = True
        self.rotation_step: int = 1
        self.move_step: int = 1

        self.active_model_id: int = -1
        self.perspective_angle: int = 45

        self.state_Color_Of_Atoms = None
        self.color_of_atoms_scheme = "cpk"
        self.periodic_table = TPeriodTable()

        self.history_of_atom_selection = []
        self.action_on_start: str = None
        self.coord_type: str = None
        self.units_type: str = None
        self.lattice_type: str = None

    def start_program(self):  # pragma: no cover
        if self.action_on_start == 'Open':
            self.action_on_start = 'Nothing'
            self.save_property(SETTINGS_FormSettingsActionOnStart, self.action_on_start)
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
        self.ui.PropertyForColorOfAtom.currentIndexChanged.connect(self.color_atoms_with_property)
        self.ui.ColorAtomsProperty.stateChanged.connect(self.color_atoms_with_property)

        self.ui.font_size_3d.valueChanged.connect(self.font_size_3d_changed)
        self.ui.property_shift_x.valueChanged.connect(self.property_position_changed)
        self.ui.property_shift_y.valueChanged.connect(self.property_position_changed)

        self.ui.FormAtomsList1.currentIndexChanged.connect(self.bond_len_to_screen)
        self.ui.FormAtomsList2.currentIndexChanged.connect(self.bond_len_to_screen)

        self.ui.activate_fragment_selection_mode.toggled.connect(self.activate_fragment_selection_mode)
        self.ui.ActivateFragmentSelectionTransp.valueChanged.connect(self.activate_fragment_selection_mode)

        self.ui.fill_space.clicked.connect(self.fill_space)
        self.ui.add_atoms_to_hexagons.clicked.connect(self.add_atoms_to_hexagons)
        self.ui.hops_analis.clicked.connect(self.hops_analyze)

        self.ui.model_rotation_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_scale.valueChanged.connect(self.model_orientation_changed)

        # colors
        self.ui.ColorBackgroundDialogButton.clicked.connect(self.select_background_color)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.ColorVoronoiDialogButton.clicked.connect(self.select_voronoi_color)
        self.ui.ColorAxesDialogButton.clicked.connect(self.select_axes_color)
        self.ui.ColorContourDialogButton.clicked.connect(self.select_contour_color)
        self.ui.manual_colors_default.clicked.connect(self.set_manual_colors_default)
        self.ui.FormBondLenSpinBox.valueChanged.connect(self.bond_len_correct)

        self.ui.PropertyAtomAtomDistanceGet.clicked.connect(self.get_bond)
        self.ui.FormStylesFor2DGraph.clicked.connect(self.set_2d_graph_styles)

        self.ui.changeFragment1StatusByX.clicked.connect(self.change_fragment1_status_by_x)
        self.ui.changeFragment1StatusByY.clicked.connect(self.change_fragment1_status_by_y)
        self.ui.changeFragment1StatusByZ.clicked.connect(self.change_fragment1_status_by_z)
        self.ui.fragment1Clear.clicked.connect(self.fragment1_clear)

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        mendeley = TPeriodTable()
        atoms_list = mendeley.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))
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

        form_settings_preferred_coordinates_type = QStandardItemModel()
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Cartesian"))
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Fractional"))
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Zmatrix Cartesian"))
        self.ui.FormSettingsPreferredCoordinates.setModel(form_settings_preferred_coordinates_type)
        self.ui.FormSettingsPreferredCoordinates.setCurrentText(self.coord_type)
        self.ui.FormSettingsPreferredCoordinates.currentIndexChanged.connect(
            self.save_state_preferred_coordinates)

        form_settings_preferred_units_type = QStandardItemModel()
        form_settings_preferred_units_type.appendRow(QStandardItem("Bohr"))
        form_settings_preferred_units_type.appendRow(QStandardItem("Ang"))
        self.ui.FormSettingsPreferredUnits.setModel(form_settings_preferred_units_type)
        self.ui.FormSettingsPreferredUnits.setCurrentText(self.units_type)
        self.ui.FormSettingsPreferredUnits.currentIndexChanged.connect(self.save_state_preferred_units)

        form_settings_preferred_lattice_type = QStandardItemModel()
        form_settings_preferred_lattice_type.appendRow(QStandardItem("LatticeParameters"))
        form_settings_preferred_lattice_type.appendRow(QStandardItem("LatticeVectors"))
        self.ui.FormSettingsPreferredLattice.setModel(form_settings_preferred_lattice_type)
        self.ui.FormSettingsPreferredLattice.setCurrentText(self.lattice_type)
        self.ui.FormSettingsPreferredLattice.currentIndexChanged.connect(self.save_state_preferred_lattice)

        fill_space_model = QStandardItemModel()
        fill_space_model.appendRow(QStandardItem("cylinder"))
        self.ui.FormActionsPreComboFillSpace.setModel(fill_space_model)

        ColorType = QStandardItemModel()
        color_types = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                       'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                       'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for t in color_types:
            ColorType.appendRow(QStandardItem(t))

        self.ui.FormSettingsColorsScale.setModel(ColorType)
        self.ui.FormSettingsColorsScale.setCurrentText(self.ColorType)

        color_type_scale = QStandardItemModel()
        color_type_scale.appendRow(QStandardItem("Linear"))
        color_type_scale.appendRow(QStandardItem("Log"))
        self.ui.FormSettingsColorsScaleType.setModel(color_type_scale)
        self.ui.FormSettingsColorsScaleType.setCurrentText(self.color_type_scale)

        self.setup_actions()

    def q_standard_item_model_init(self, data: list):
        model_type = QStandardItemModel()
        for row in data:
            model_type.appendRow(QStandardItem(row))
        return model_type

    def setup_actions(self):
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
        if self.ui.activate_fragment_selection_mode.isChecked():
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

    @property
    def active_model(self) -> AtomicModel:
        return self.models[self.active_model_id]

    @staticmethod
    def read_data_of_cell_params(f_name):
        row_data = []
        if os.path.exists(f_name):
            f = open(f_name)
            rows = f.readlines()

            for i in range(2, len(rows)):
                row = rows[i].split()
                if len(row) > 1:
                    energy = row[1]
                    volume = row[0]
                    a = 0
                    if len(row) > 2:
                        a = row[2]
                    b = 0
                    if len(row) > 3:
                        b = row[3]
                    c = 0
                    if len(row) > 4:
                        c = row[4]
                    row_data.append([energy, volume, a, b, c])
                    # self.fill_cell_info_row(energy, volume, a, b, c)
            f.close()
        return row_data

    @staticmethod
    def show_error(e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def model_part_prepare(cm_new, models, rot_x, rot_y, rot_z):
        part = models[-1]
        cm_old = - part.center_mass()
        part.move(cm_old)
        part.rotate(rot_x, rot_y, rot_z)
        part.move(cm_new)
        return part

    def selected_atom_from_form(self):
        coord_type = self.selected_atom_coord_type()
        charge = self.ui.atoms_list_all.currentIndex()
        let = self.ui.atoms_list_all.currentText()
        x, y, z = self.selected_atom_xyz_from_form()
        position = np.array((x, y, z), dtype=float)
        position = self.coords_to_ang(position, coord_type)
        return charge, let, position

    def coords_to_ang(self, position, coord_type):
        if coord_type == "A":
            return position
        if coord_type == "bohr":
            return position * 0.52917720859
        lat_vectors = self.models[self.active_model_id].lat_vectors
        return position[0] * lat_vectors[0] + position[1] * lat_vectors[1] + position[2] * lat_vectors[2]

    def ang_to_coords(self, position, coord_type):
        if coord_type == "A":
            return position
        if coord_type == "bohr":
            return position / 0.52917720859
        obr = np.linalg.inv(self.models[self.active_model_id].lat_vectors).transpose()
        return obr.dot(position)

    def selected_atom_coord_type(self):
        #coord_type = "direct"
        #if self.ui.is_cart_coord.isChecked():
        #    coord_type = "A"
        #if self.ui.is_cart_coord_bohr.isChecked():
        #    coord_type = "bohr"
        coord_type = "A"
        return coord_type

    def bond_len_to_screen(self):
        let1 = self.ui.FormAtomsList1.currentIndex()
        let2 = self.ui.FormAtomsList2.currentIndex()

        if not ((let1 == 0) or (let2 == 0)):
            bond = self.periodic_table.Bonds[let1][let2]
        else:
            bond = 0
        self.ui.FormBondLenSpinBox.setValue(bond)

    def clear_form_isosurface_data2_n(self):
        self.ui.FormActionsPostLabelSurfaceNx.setText("")
        self.ui.FormActionsPostLabelSurfaceNy.setText("")
        self.ui.FormActionsPostLabelSurfaceNz.setText("")

    def check_pdos(self, f_name: str) -> None:   # pragma: no cover
        pdos_file = ImporterExporter.check_pdos_file(f_name)
        if pdos_file:
            self.ui.FormActionsLinePDOSfile.setText(pdos_file)
            self.ui.FormActionsButtonPlotPDOS.setEnabled(True)

    def check_bands(self, f_name: str) -> None:   # pragma: no cover
        bands_file = ImporterExporter.check_bands_file(f_name)
        if bands_file:
            self.ui.FormActionsLineBANDSfile.setText(bands_file)
            self.ui.parse_bands.setEnabled(True)

    def check_dos(self, f_name: str) -> None:   # pragma: no cover
        dos_file, e_fermy = ImporterExporter.check_dos_file(f_name)
        if dos_file:
            i = self.ui.FormActionsTabeDOSProperty.rowCount() + 1
            self.ui.FormActionsTabeDOSProperty.setRowCount(i)
            line = "..." + str(dos_file)[-15:]
            q_tab_widg = QTableWidgetItem(line)
            q_tab_widg.setToolTip(dos_file)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 0, q_tab_widg)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 1, QTableWidgetItem(str(e_fermy)))
            # self.ui.FormActionsTabeDOSProperty.update()

    def change_fragment1_status_by_x(self):
        x_min = self.ui.xminborder.value()
        x_max = self.ui.xmaxborder.value()
        ogl = self.ui.openGLWidget
        model = ogl.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.x >= x_min) and (at.x <= x_max):
                ogl.main_model.atoms[ind].fragment1 = not ogl.main_model.atoms[ind].fragment1
        self.fragment1_post_actions()

    def change_fragment1_status_by_y(self):
        y_min = self.ui.yminborder.value()
        y_max = self.ui.ymaxborder.value()
        ogl = self.ui.openGLWidget
        model = ogl.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.y >= y_min) and (at.y <= y_max):
                ogl.main_model.atoms[ind].fragment1 = not ogl.main_model.atoms[ind].fragment1
        self.fragment1_post_actions()

    def change_fragment1_status_by_z(self):
        z_min = self.ui.zminborder.value()
        z_max = self.ui.zmaxborder.value()
        ogl = self.ui.openGLWidget
        model = ogl.get_model()
        for ind, at in enumerate(model.atoms):
            if (at.z >= z_min) and (at.z <= z_max):
                ogl.main_model.atoms[ind].fragment1 = not ogl.main_model.atoms[ind].fragment1
        self.fragment1_post_actions()

    def fragment1_clear(self):
        for at in self.ui.openGLWidget.main_model.atoms:
            at.fragment1 = False
        self.fragment1_post_actions()

    def fragment1_post_actions(self):
        self.ui.openGLWidget.atoms_of_selected_fragment_to_form()
        self.ui.openGLWidget.update_view()

    @staticmethod
    def clear_qtree_widget(tree):
        iterator = QTreeWidgetItemIterator(tree, QTreeWidgetItemIterator.All)
        while iterator.value():
            iterator.value().takeChildren()
            iterator += 1
        i = tree.topLevelItemCount()
        while i > -1:
            tree.takeTopLevelItem(i)
            i -= 1

    @staticmethod
    def color_to_ui(color_ui, state_color):
        r = state_color.split()[0]
        g = state_color.split()[1]
        b = state_color.split()[2]
        color_ui.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

    def colors_of_atoms(self):
        return self.periodic_table.get_all_colors()

    def get_file_name_from_save_dialog(self, file_mask):  # pragma: no cover
        result = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, file_mask,
                                             options=QFileDialog.DontUseNativeDialog)

        if result[0] == "":
            return None

        file_name = result[0]
        mask = result[1]
        if file_name is not None:
            extention = mask.split("(*.")[1].split(")")[0]
            if not file_name.lower().endswith(extention.lower()):
                file_name += "." + extention.lower()
        if extention.lower() in ['png', 'jpg', 'bmp']:
            file_name = file_name.replace(extention.upper(), extention.lower())
        return file_name

    def get_file_name_from_open_dialog(self, file_mask):  # pragma: no cover
        return QFileDialog.getOpenFileName(self, 'Open file', self.work_dir, file_mask,
                                           options=QFileDialog.DontUseNativeDialog)[0]

    def export_volumeric_data_to_file_form_elements(self, mask):
        try:
            f_name = self.get_file_name_from_save_dialog(mask)
            x1 = self.ui.FormVolDataExportX1.value()
            x2 = self.ui.FormVolDataExportX2.value()
            y1 = self.ui.FormVolDataExportY1.value()
            y2 = self.ui.FormVolDataExportY2.value()
            z1 = self.ui.FormVolDataExportZ1.value()
            z2 = self.ui.FormVolDataExportZ2.value()
            self.volumeric_data_to_file(f_name, self.volumeric_data, x1, x2, y1, y2, z1, z2)
            self.work_dir = os.path.dirname(f_name)
            self.save_active_folder()
        except Exception as e:
            self.show_error(e)

    def volumeric_data_to_file(self, f_name, volumeric_data, x1, x2, y1, y2, z1, z2):
        model = self.ui.openGLWidget.get_model()
        if f_name.find(".XSF") >= 0:
            text = volumeric_data.to_xsf_text(model, x1, x2, y1, y2, z1, z2)
            helpers.write_text_to_file(f_name, text)

        if f_name.find(".cube") >= 0:
            text = volumeric_data.to_cube_text(model, x1, x2, y1, y2, z1, z2)
            helpers.write_text_to_file(f_name, text)

    def fill_gui(self, title=""):
        file_name = self.filename
        if title == "":
            self.fill_file_name(file_name)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()

        self.ui.PropertyAtomAtomDistanceAt1.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistanceAt2.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistance.setText("")

        if helpers.check_format(file_name) == "siesta_out":
            self.check_dos(file_name)
            self.check_pdos(file_name)
            self.check_bands(file_name)
            self.fill_cell_info(file_name)
            energies = TSIESTA.energies(file_name)
            self.fill_energies(energies)

        if helpers.check_format(file_name) == "CRYSTALout":
            energies = crystal.energies(file_name)
            self.fill_energies(energies)

        if helpers.check_format(file_name) == "SIESTAfdf":
            c = np.linalg.norm(self.ui.openGLWidget.main_model.lat_vector3)
            self.ui.FormActionsPreZSizeFillSpace.setValue(c)

    def fill_energies(self, energies: list[float]) -> None:
        """Plot energies for steps of output."""
        if len(energies) == 0:
            return
        energies_min = min(energies)
        energies -= energies_min
        self.ui.PyqtGraphWidget.set_xticks(None)

        x_title = "Step"
        y_title = "Energy (+" + str(-energies_min) + "), eV"
        title = "Energies"

        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        if len(energies) > 1:
            self.ui.PyqtGraphWidget.plot([np.arange(0, len(energies))], [energies], [None], title, x_title, y_title)
        else:
            self.ui.PyqtGraphWidget.add_scatter([0], [0])

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

        properties.append(["Natoms", str(len(model.atoms))])
        properties.append(["LatVect1", str(model.lat_vector1)])
        properties.append(["LatVect2", str(model.lat_vector2)])
        properties.append(["LatVect3", str(model.lat_vector3)])
        properties.append(["Formula", model.formula()])

        self.ui.FormModelTableProperties.setRowCount(len(properties))

        for i in range(0, len(properties)):
            self.ui.FormModelTableProperties.setItem(i, 0, QTableWidgetItem(properties[i][0]))
            self.ui.FormModelTableProperties.setItem(i, 1, QTableWidgetItem(properties[i][1]))

    def fill_volumeric_data(self, data, tree=" "):
        if tree == " ":
            tree = self.ui.FormActionsPostTreeSurface
        data_type = data.type
        data = data.blocks
        self.clear_qtree_widget(tree)

        if data_type == "TXSF":
            for dat in data:
                text = (dat[0].title.split('_')[3]).split(':')[0].rstrip()
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text) + "3D")
                for da in dat:
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(text + ':' + da.title.split(':')[1]))

        if data_type == "TGaussianCube":
            for dat in data:
                text = dat[0].title.split(".cube")[0].rstrip()
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text))

                child = QTreeWidgetItem(parent)
                child.setText(0, "{}".format(text))
        tree.show()

    def fill_bonds_charges(self):
        bonds_category = self.ui.FormActionsPostComboBonds.currentText()
        if bonds_category == "All":
            c1 = 0
            c2 = 0
        else:
            bonds_category = bonds_category.split('-')
            mendeley = TPeriodTable()
            c1 = mendeley.get_charge_by_letter(bonds_category[0])
            c2 = mendeley.get_charge_by_letter(bonds_category[1])
        return c1, c2

    def fill_cell_info(self, f_name, sourse="siesta_out"):
        volume = 0.0
        energy = 0.0
        a, b, c = 0.0, 0.0, 0.0

        if sourse == "siesta_out":
            volume = TSIESTA.volume(f_name)
            energy = TSIESTA.energy_tot(f_name)
            models, fdf_data = ImporterExporter.import_from_file(f_name)
            model = models[-1]
            a = np.linalg.norm(model.lat_vector1)
            b = np.linalg.norm(model.lat_vector2)
            c = np.linalg.norm(model.lat_vector3)
        if sourse == "vasp_outcar":
            volume = TVASP.volume(f_name)
            energy, is_conv, iteration = TVASP.energy_tot(f_name)
            a, b, c = abc_from_outcar(f_name)

        self.fill_cell_info_row(energy, volume, a, b, c)
        self.ui.FormActionsPreZSizeFillSpace.setValue(c)
        self.work_dir = os.path.dirname(f_name)
        self.save_active_folder()

    def fill_cell_info_row(self, energy, volume, a, b, c):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        if i > 1:
            if self.ui.FormActionsPostTableCellParam.item(i - 2, 1) is None:
                i -= 1

        self.ui.FormActionsPostTableCellParam.setRowCount(i)
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 0, QTableWidgetItem(str(volume)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 1, QTableWidgetItem(str(energy)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 2, QTableWidgetItem(str(a)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 3, QTableWidgetItem(str(b)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 4, QTableWidgetItem(str(c)))

    def get_bond(self):   # pragma: no cover
        i = self.ui.PropertyAtomAtomDistanceAt1.value()
        j = self.ui.PropertyAtomAtomDistanceAt2.value()
        bond = round(self.ui.openGLWidget.main_model.atom_atom_distance(i - 1, j - 1), 4)
        self.ui.PropertyAtomAtomDistance.setText(str(bond) + " A")

    def get_colors_list(self, minv, maxv, values, cmap, color_scale):
        n = len(values)
        colors = []
        for i in range(0, n):
            value = values[i]
            colors.append(self.get_color(cmap, minv, maxv, value, color_scale))
        return colors

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

    def get_color_of_plane(self, minv, maxv, points, cmap, color_scale):
        Nx = len(points)
        Ny = len(points[0])
        minv = float(minv)
        maxv = float(maxv)
        colors = []
        if maxv == minv:
            return colors
        for i in range(0, Nx):
            row = []
            for j in range(0, Ny):
                value = float(points[i][j][3])
                prev = self.colors_cash.get(value)
                if prev is None:
                    color = MainForm.get_color(cmap, minv, maxv, value, color_scale)
                    self.colors_cash[value] = [color[0], color[1], color[2]]
                    row.append([color[0], color[1], color[2]])
                else:
                    row.append(prev)
            colors.append(row)
        return colors

    @staticmethod
    def get_color(cmap, minv, maxv, value, scale):
        if minv == maxv:
            scale == "black"
        if scale == "black":
            return QColor.fromRgb(0, 0, 0, 1).getRgbF()
        if scale == "Log":
            if (minv < 0) or (maxv < 0):
                scale = "Linear"
            else:
                if minv < 1e-8:
                    minv = 1e-8
                if value < 1e-8:
                    value = 1e-8
                return cmap((math.log10(value) - math.log10(minv)) / (math.log10(maxv) - math.log10(minv)))
        if scale == "Linear":
            return cmap((value - minv) / (maxv - minv))
        return QColor.fromRgb(0, 0, 0, 1).getRgbF()

    def get_fdf_file_name(self):  # pragma: no cover
        fname = self.get_file_name_from_open_dialog("FDF files (*.fdf)")
        if not fname.endswith(".fdf"):
            fname += ".fdf"
        return fname

    @staticmethod
    def get_color_from_setting(strcolor: str):
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor

    def load_settings(self) -> None:
        settings = QSettings()
        state_check_only_optimal = settings.value(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, False, type=bool)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.setChecked(state_check_only_optimal)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.clicked.connect(self.save_state_open_only_optimal)
        state_parse_atomic_properties = settings.value(SETTINGS_FormSettingsParseAtomicProperties, False, type=bool)
        self.ui.FormSettingsParseAtomicProperties.setChecked(state_parse_atomic_properties)
        self.ui.FormSettingsParseAtomicProperties.clicked.connect(self.save_state_parse_atomic_properties)
        state_check_show_axes = settings.value(SETTINGS_FormSettingsViewCheckShowAxes, False, type=bool)
        self.ui.FormSettingsViewCheckShowAxes.setChecked(state_check_show_axes)
        self.ui.FormSettingsViewCheckShowAxes.clicked.connect(self.save_state_view_show_axes)
        state_check_atom_selection = settings.value(SETTINGS_FormSettingsViewCheckAtomSelection, False, type=bool)
        if state_check_atom_selection:
            self.ui.FormSettingsViewCheckAtomSelection.setChecked(True)
        else:
            self.ui.FormSettingsViewCheckModelMove.setChecked(True)
        self.ui.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_view_atom_selection)
        self.ui.FormSettingsViewCheckModelMove.clicked.connect(self.save_state_view_atom_selection)

        state_color_bonds_manual = settings.value(SETTINGS_FormSettingsViewRadioColorBondsManual, False, type=bool)
        if state_color_bonds_manual:
            self.ui.FormSettingsViewRadioColorBondsManual.setChecked(True)
        else:
            self.ui.FormSettingsViewRadioColorBondsByAtoms.setChecked(True)
        self.ui.FormSettingsViewRadioColorBondsManual.clicked.connect(self.save_state_view_bond_color)
        self.ui.FormSettingsViewRadioColorBondsByAtoms.clicked.connect(self.save_state_view_bond_color)

        state_show_atoms = settings.value(SETTINGS_FormSettingsViewCheckShowAtoms, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtoms.setChecked(state_show_atoms)
        self.ui.FormSettingsViewCheckShowAtoms.clicked.connect(self.save_state_view_show_atoms)

        state_show_atom_number = settings.value(SETTINGS_FormSettingsViewCheckShowAtomNumber, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtomNumber.setChecked(state_show_atom_number)
        self.ui.FormSettingsViewCheckShowAtomNumber.clicked.connect(self.save_state_view_show_atom_number)

        state_show_box = settings.value(SETTINGS_FormSettingsViewCheckShowBox, False, type=bool)
        self.ui.FormSettingsViewCheckShowBox.setChecked(state_show_box)
        self.ui.FormSettingsViewCheckShowBox.clicked.connect(self.save_state_view_show_box)

        state_show_bonds = settings.value(SETTINGS_FormSettingsViewCheckShowBonds, True, type=bool)
        self.ui.FormSettingsViewCheckShowBonds.setChecked(state_show_bonds)
        self.ui.FormSettingsViewCheckShowBonds.clicked.connect(self.save_state_view_show_bonds)

        state_gl_cull_face = settings.value(SETTINGS_GlCullFace, True, type=bool)
        self.ui.OpenGL_GL_CULL_FACE.setChecked(state_gl_cull_face)
        self.ui.OpenGL_GL_CULL_FACE.clicked.connect(self.save_state_gl_cull_face)

        self.work_dir = str(settings.value(SETTINGS_Folder, "/home"))
        self.ColorType = str(settings.value(SETTINGS_FormSettingsColorsScale, 'rainbow'))
        self.ui.FormSettingsColorsScale.currentIndexChanged.connect(self.save_state_colors_scale)
        self.ui.FormSettingsColorsScale.currentTextChanged.connect(self.state_changed_form_settings_colors_scale)
        self.color_type_scale = str(settings.value(SETTINGS_FormSettingsColorsScaleType, 'Log'))
        self.ui.FormSettingsColorsScaleType.currentIndexChanged.connect(self.save_state_colors_scale_type)
        state_form_settings_colors_fixed = settings.value(SETTINGS_FormSettingsColorsFixed, False, type=bool)
        self.ui.FormSettingsColorsFixed.setChecked(state_form_settings_colors_fixed)
        self.ui.FormSettingsColorsFixed.clicked.connect(self.save_state_colors_fixed)
        state_form_settings_colors_fixed_min = settings.value(SETTINGS_FormSettingsColorsFixedMin, '0.1')
        try:
            min_val = float(state_form_settings_colors_fixed_min)
        except Exception:
            min_val = 0.0001
        self.ui.FormSettingsColorsFixedMin.setValue(min_val)
        self.ui.FormSettingsColorsFixedMin.valueChanged.connect(self.save_state_colors_fixed_min)
        state_form_settings_colors_fixed_max = settings.value(SETTINGS_FormSettingsColorsFixedMax, '0.2')
        self.ui.FormSettingsColorsFixedMax.setValue(float(state_form_settings_colors_fixed_max))
        self.ui.FormSettingsColorsFixedMax.valueChanged.connect(self.save_state_colors_fixed_max)
        state_form_settings_view_spin_bond_width = int(settings.value(SETTINGS_FormSettingsViewSpinBondWidth, '20'))
        self.ui.FormSettingsViewSpinBondWidth.setValue(state_form_settings_view_spin_bond_width)
        self.ui.FormSettingsViewSpinBondWidth.valueChanged.connect(self.save_state_view_spin_bond_width)
        state_contour_width = int(settings.value(SETTINGS_FormSettingsViewSpinContourWidth, '20'))
        self.ui.FormSettingsViewSpinContourWidth.setValue(state_contour_width)
        self.ui.FormSettingsViewSpinContourWidth.valueChanged.connect(self.save_state_view_spin_contour_width)

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

        self.state_Color_Of_Voronoi = str(settings.value(SETTINGS_Color_Of_Voronoi, '255 0 0'))
        self.color_to_ui(self.ui.ColorVoronoi, self.state_Color_Of_Voronoi)

        self.state_Color_Of_Axes = str(settings.value(SETTINGS_Color_Of_Axes, '0 255 0'))
        self.color_to_ui(self.ui.ColorAxes, self.state_Color_Of_Axes)

        self.state_Color_Of_Contour = str(settings.value(SETTINGS_Color_Of_Contour, '0 255 0'))
        self.color_to_ui(self.ui.ColorContour, self.state_Color_Of_Contour)

        self.coord_type = str(settings.value(SETTINGS_FormSettingsPreferredCoordinates, 'Cartesian'))
        self.units_type = str(settings.value(SETTINGS_FormSettingsPreferredUnits, 'Ang'))
        self.lattice_type = str(settings.value(SETTINGS_FormSettingsPreferredLattice, 'LatticeParameters'))

        self.action_on_start = str(settings.value(SETTINGS_FormSettingsActionOnStart, 'Nothing'))

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
                file_format = "FDF files (*.fdf);;XYZ files (*.xyz);;FireFly input files (*.inp)"
                file_format += ";;VASP POSCAR file (*.POSCAR);;GUI4dft project file (*.data)"
                file_name = self.get_file_name_from_save_dialog(file_format)

                if not file_name:
                    return

                ImporterExporter.export_to_file(self.models[self.active_model_id], file_name)
                self.work_dir = os.path.dirname(file_name)
                self.save_active_folder()
            except Exception as e:
                self.show_error(e)

    def menu_open(self, file_name=False):
        if len(self.models) > 0:   # pragma: no cover
            self.action_on_start = 'Open'
            self.save_property(SETTINGS_FormSettingsActionOnStart, self.action_on_start)
            if sys.platform.startswith('win'):
                os.execlp('python', 'python', *sys.argv)
            else:
                os.execlp('python3', 'python3', *sys.argv)

        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if not file_name:
            file_name = self.get_file_name_from_open_dialog("All files (*)")
        if os.path.exists(file_name):
            self.filename = file_name
            self.work_dir = os.path.dirname(file_name)
            try:
                self.get_atomic_model_and_fdf(file_name)
            except Exception as e:
                print("Incorrect file format")
                self.show_error(e)
            try:
                self.plot_last_model()
            except Exception as e:  # pragma: no cover
                self.show_error(e)

    def get_atomic_model_and_fdf(self, fname):
        parse_properies = self.ui.FormSettingsParseAtomicProperties.isChecked()
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            self.models, self.fdf_data = ImporterExporter.import_from_file(fname, 'opt', parse_properies)
        else:
            self.models, self.fdf_data = ImporterExporter.import_from_file(fname, 'all', parse_properies)

    def plot_last_model(self):
        if len(self.models) > 0:
            if len(self.models[-1].atoms) > 0:
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
        if self.ui.openGLWidget.main_model.n_atoms() > 0:
            atom = self.ui.openGLWidget.main_model.atoms[0]
            atom_prop_type = QStandardItemModel()
            for key in atom.properties:
                atom_prop_type.appendRow(QStandardItem(str(key)))
            self.ui.PropertyForColorOfAtom.setModel(atom_prop_type)

    def color_atoms_with_property(self):  # pragma: no cover
        if self.ui.ColorAtomsProperty.isChecked():
            prop = self.ui.PropertyForColorOfAtom.currentText()
            if len(prop) > 0:
                self.ui.openGLWidget.color_atoms_with_property(prop)
            else:
                self.ui.openGLWidget.color_atoms_with_property()
        else:
            self.ui.openGLWidget.color_atoms_with_property()
        self.ui.openGLWidget.update()

    def cp_property_precision_changed(self):  # pragma: no cover
        self.ui.openGLWidget.property_precision_changed(self.ui.property_precision.value())
        self.show_property()

    def font_size_3d_changed(self):  # pragma: no cover
        self.save_property(SETTINGS_PropertyFontSize, self.ui.font_size_3d.value())
        self.ui.openGLWidget.set_property_font_size(self.ui.font_size_3d.value())
        self.show_property()

    def property_position_changed(self):  # pragma: no cover
        dx = self.ui.property_shift_x.value()
        dy = self.ui.property_shift_y.value()
        self.save_property(SETTINGS_PropertyShiftX, dx)
        self.save_property(SETTINGS_PropertyShiftY, dy)
        self.ui.openGLWidget.set_property_shift(dx, dy)
        self.show_property()

    def show_property(self):  # pragma: no cover
        if self.ui.show_property_text.isChecked():
            prop = self.ui.PropertyForColorOfAtom.currentText()
            self.ui.openGLWidget.show_property(prop)
            self.ui.openGLWidget.set_property_font_size(self.ui.font_size_3d.value())
            dx = self.ui.property_shift_x.value()
            dy = self.ui.property_shift_y.value()
            self.ui.openGLWidget.set_property_shift(dx, dy)
        else:
            self.ui.openGLWidget.show_property()

    def add_model_and_show(self, model):  # pragma: no cover
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def plot_model(self, value):
        if len(self.models) < value:
            return
        if len(self.models[value].atoms) == 0:
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
        contour_width = (self.ui.FormSettingsViewSpinContourWidth.value()) / 1000.0
        self.ui.openGLWidget.set_atomic_structure(self.models[self.active_model_id], atoms_color, view_atoms,
                                                  view_atom_numbers, view_box, box_color, view_bonds, bonds_color,
                                                  bond_width, color_of_bonds_by_atoms,
                                                  view_axes, axes_color, contour_width)
        self.ui.AtomsInSelectedFragment.clear()

        self.show_property_enabling()

    @staticmethod
    def list_of_selected_items_in_combo(atom_index, combo):
        model = combo.model()
        maxi = combo.count()
        for i in range(0, maxi):
            if model.itemFromIndex(model.index(i, 0)).checkState() == Qt.Checked:
                atom_index.append(int(model.itemFromIndex(model.index(i, 0)).text()))

    def delta_dipole(self, f, q, r):
        dp = q * r
        if self.ui.activate_fragment_selection_mode.isChecked():
            dp *= f
        return dp

    def plot_curv_and_points(self, xs, ys, xs2, ys2):
        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        x_title = self.ui.cell_parameter_label_x.text()
        y_title = self.ui.cell_parameter_label_y.text()
        title = self.ui.cell_parameter_title.text()
        self.ui.PyqtGraphWidget.plot([xs2], [ys2], [None], title, x_title, y_title)
        self.ui.PyqtGraphWidget.add_scatter(xs, ys)

    def plot_cell_approx(self, image_path):
        image_profile = QImage(image_path)
        image_profile = image_profile.scaled(320, 54, aspectMode=Qt.KeepAspectRatio,
                                             mode=Qt.SmoothTransformation)
        self.ui.FormActionsPostLabelCellParamFig.setPixmap(QPixmap.fromImage(image_profile))

    def save_image_to_file(self, name=""):
        if len(self.models) == 0:
            return
        try:
            if not name:
                format_str = "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)"
                fname = self.get_file_name_from_save_dialog(format_str)
                if fname:
                    new_window = Image3Dexporter(5 * self.ui.openGLWidget.width(), 5 * self.ui.openGLWidget.height(), 5)
                    new_window.ui.openGLWidget.copy_state(self.ui.openGLWidget)

                    new_window.ui.openGLWidget.image3d_to_file(fname)
                    new_window.destroy()
                    self.work_dir = os.path.dirname(fname)
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
        self.save_property(SETTINGS_Folder, self.work_dir)

    def save_state_open_only_optimal(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsOpeningCheckOnlyOptimal,
                           self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked())

    def save_state_parse_atomic_properties(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsParseAtomicProperties,
                           self.ui.FormSettingsParseAtomicProperties.isChecked())

    def save_state_view_show_axes(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowAxes,
                           self.ui.FormSettingsViewCheckShowAxes.isChecked())
        self.ui.openGLWidget.set_axes_visible(self.ui.FormSettingsViewCheckShowAxes.isChecked())

    def save_state_view_atom_selection(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckAtomSelection,
                           self.ui.FormSettingsViewCheckAtomSelection.isChecked())

    def save_state_view_bond_color(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewRadioColorBondsManual,
                           self.ui.FormSettingsViewRadioColorBondsManual.isChecked())
        self.ui.openGLWidget.set_bond_color(self.ui.FormSettingsViewRadioColorBondsManual.isChecked())

    def save_state_xyz_as_critic2(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckXYZasCritic2,
                           self.ui.FormSettingsViewCheckXYZasCritic2.isChecked())

    def save_state_view_show_atoms(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowAtoms, self.ui.FormSettingsViewCheckShowAtoms.isChecked())
        self.ui.openGLWidget.set_atoms_visible(self.ui.FormSettingsViewCheckShowAtoms.isChecked())

    def save_state_view_show_atom_number(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowAtomNumber,
                           self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())
        self.ui.openGLWidget.set_atoms_numbered(self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())

    def save_state_view_show_box(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.ui.openGLWidget.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_view_show_bonds(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.ui.openGLWidget.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

    def save_state_gl_cull_face(self):  # pragma: no cover
        self.save_property(SETTINGS_GlCullFace, self.ui.OpenGL_GL_CULL_FACE.isChecked())
        self.ui.openGLWidget.set_gl_cull_face(self.ui.OpenGL_GL_CULL_FACE.isChecked())

    def save_state_colors_fixed(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsColorsFixed, self.ui.FormSettingsColorsFixed.isChecked())

    def save_state_view_spin_contour_width(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewSpinContourWidth, self.ui.FormSettingsViewSpinContourWidth.text())
        self.ui.openGLWidget.set_contour_width(self.ui.FormSettingsViewSpinContourWidth.value() / 1000)
        self.plot_contour()

    def save_state_colors_fixed_min(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsColorsFixedMin, self.ui.FormSettingsColorsFixedMin.text())

    def save_state_view_spin_bond_width(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewSpinBondWidth, self.ui.FormSettingsViewSpinBondWidth.text())
        self.ui.openGLWidget.set_bond_width(self.ui.FormSettingsViewSpinBondWidth.value() * 0.005)

    def save_state_colors_fixed_max(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsColorsFixedMax, self.ui.FormSettingsColorsFixedMax.text())

    def save_state_colors_scale(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsColorsScale, self.ui.FormSettingsColorsScale.currentText())
        self.colors_cash = {}

    def save_state_colors_scale_type(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsColorsScaleType, self.ui.FormSettingsColorsScaleType.currentText())
        self.colors_cash = {}

    def save_state_preferred_coordinates(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredCoordinates,
                           self.ui.FormSettingsPreferredCoordinates.currentText())
        self.coord_type = self.ui.FormSettingsPreferredCoordinates.currentText()

    def save_state_preferred_coordinates_style(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredCoordinatesStyle,
                           self.ui.PreferredCoordinatesTypeSimple.isChecked())
        if self.ui.PreferredCoordinatesTypeSimple.isChecked():
            self.ui.FormSettingsPreferredCoordinates.setEnabled(True)
        else:
            self.ui.FormSettingsPreferredCoordinates.setEnabled(False)

    def save_state_preferred_units(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredUnits,
                           self.ui.FormSettingsPreferredUnits.currentText())
        self.units_type = self.ui.FormSettingsPreferredUnits.currentText()

    def save_state_preferred_lattice(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredLattice, self.ui.FormSettingsPreferredLattice.currentText())
        self.lattice_type = self.ui.FormSettingsPreferredLattice.currentText()

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
        coord_type = self.selected_atom_coord_type()
        position = self.ang_to_coords(position, coord_type)
        self.ui.atoms_list_all.setCurrentIndex(element)
        self.ui.FormActionsPreSpinAtomsCoordX.setValue(position[0])
        self.ui.FormActionsPreSpinAtomsCoordX.update()
        self.ui.FormActionsPreSpinAtomsCoordY.setValue(position[1])
        self.ui.FormActionsPreSpinAtomsCoordY.update()
        self.ui.FormActionsPreSpinAtomsCoordZ.setValue(position[2])
        self.ui.FormActionsPreSpinAtomsCoordZ.update()
        x, y, z = self.selected_atom_xyz_from_form()
        self.ui.selected_atom_coords.setText("{0:6}    {1:6}    {2:6}".format(x, y, z))

    def selected_atom_xyz_from_form(self):
        x = self.ui.FormActionsPreSpinAtomsCoordX.value()
        y = self.ui.FormActionsPreSpinAtomsCoordY.value()
        z = self.ui.FormActionsPreSpinAtomsCoordZ.value()
        return x, y, z

    def selected_atom_changed(self, selected):
        selected_atom = selected[0]
        if selected_atom == -1:
            self.history_of_atom_selection = []
        else:
            self.history_of_atom_selection.append(selected_atom)

        text = ""
        if selected_atom >= 0:
            model = self.models[self.active_model_id]
            text += "Selected atom: " + str(selected_atom + 1) + "\n"
            atom = model.atoms[selected_atom]
            text += "Element: " + atom.let + "\n"
            for key in atom.properties:
                text += str(key) + ": " + str(atom.properties[key]) + "\n"

            if len(self.history_of_atom_selection) > 1:
                text += "\n\nHistory of atoms selection: " + str(np.array(self.history_of_atom_selection) + 1) + "\n"
                text += "Distance from atom " + str(self.history_of_atom_selection[-1] + 1) + " to atom " + \
                        str(self.history_of_atom_selection[-2] + 1) + " : "
                dist = model.atom_atom_distance(self.history_of_atom_selection[-1], self.history_of_atom_selection[-2])
                text += str(round(dist / 10, 6)) + " nm\n"

                if (len(self.history_of_atom_selection) > 2) and \
                        (self.history_of_atom_selection[-1] != self.history_of_atom_selection[-2]) \
                        and (self.history_of_atom_selection[-3] != self.history_of_atom_selection[-2]):
                    x1 = model.atoms[self.history_of_atom_selection[-1]].x
                    y1 = model.atoms[self.history_of_atom_selection[-1]].y
                    z1 = model.atoms[self.history_of_atom_selection[-1]].z

                    x2 = model.atoms[self.history_of_atom_selection[-2]].x
                    y2 = model.atoms[self.history_of_atom_selection[-2]].y
                    z2 = model.atoms[self.history_of_atom_selection[-2]].z

                    x3 = model.atoms[self.history_of_atom_selection[-3]].x
                    y3 = model.atoms[self.history_of_atom_selection[-3]].y
                    z3 = model.atoms[self.history_of_atom_selection[-3]].z

                    vx1 = x1 - x2
                    vy1 = y1 - y2
                    vz1 = z1 - z2

                    vx2 = x3 - x2
                    vy2 = y3 - y2
                    vz2 = z3 - z2

                    a = vx1 * vx2 + vy1 * vy2 + vz1 * vz2
                    b = math.sqrt(vx1 * vx1 + vy1 * vy1 + vz1 * vz1)
                    c = math.sqrt(vx2 * vx2 + vy2 * vy2 + vz2 * vz2)

                    arg = a / (b * c)
                    if math.fabs(arg) > 1:
                        arg = 1

                    angle = math.acos(arg)

                    text += "Angle " + str(self.history_of_atom_selection[-1] + 1) + " - " + \
                            str(self.history_of_atom_selection[-2] + 1) + " - " + \
                            str(self.history_of_atom_selection[-3] + 1) + " : " + \
                            str(round(math.degrees(angle), 3)) + " degrees\n"
        if selected_atom < 0:
            text += "Select any atom."
        self.ui.AtomPropertiesText.setText(text)

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

    def fill_space(self):
        if len(self.models) == 0:
            return
        mendeley = TPeriodTable()
        n_atoms = int(self.ui.FormActionsPreNAtomsFillSpace.value())
        charge = int(self.ui.FormActionsPreAtomChargeFillSpace.value())
        rad_atom = mendeley.get_rad(charge)
        let = mendeley.get_let(charge)
        delta = float(self.ui.FormActionsPreDeltaFillSpace.value())
        n_prompts = int(self.ui.FormActionsPreNPromptsFillSpace.value())
        rad_tube = float(self.ui.FormActionsPreRadiusFillSpace.value())
        length = float(self.ui.FormActionsPreZSizeFillSpace.value())
        models = fill_tube(rad_tube, length, n_atoms, 0.01 * rad_atom, delta, n_prompts, let, charge)

        filename = ""
        try:
            if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
                filename = QFileDialog.getSaveFileName(self, 'Save File', options=QFileDialog.DontUseNativeDialog)[0]
                filename = filename.split(".fdf")[0]
        except Exception as exc:
            self.show_error(exc)

        myiter = 0
        for model in models:
            second_model = deepcopy(self.ui.openGLWidget.get_model())
            for at in model:
                second_model.add_atom(at)
            self.models.append(second_model)
            if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
                text = self.fdf_data.get_all_data(second_model.atoms, self.coord_type, self.units_type, self.lattice_type)
                with open(filename + str(myiter) + '.fdf', 'w') as f:
                    f.write(text)
            myiter += 1
        self.fill_models_list()

    def add_atoms_to_hexagons(self) -> None:
        if len(self.models) == 0:
            return
        n = self.ui.number_of_atoms_to_add.value()
        print("Add ", n, " Li atoms")
        print("Not implemented")
        model1 = deepcopy(self.ui.openGLWidget.get_model())
        models = add_adatom(model1, n)
        for model in models:
            self.models.append(model)
        self.fill_models_list()

    def hops_analyze(self) -> None:
        if len(self.models) == 0:
            return
        hops(self.models)


    def parse_volumeric_data_selected(self, filename: str = ""):
        if filename.endswith(".XSF"):
            self.volumeric_data = XSF()
        if filename.endswith(".cube"):
            self.volumeric_data = GaussianCube()
        if self.volumeric_data.parse(filename):
            self.fill_volumeric_data(self.volumeric_data)
        self.ui.FormActionsPostButSurfaceLoadData.setEnabled(True)
        self.clear_qtree_widget(self.ui.FormActionsPostTreeSurface2)
        self.ui.FormActionsPosEdit3DData2.setText("")
        self.clear_form_isosurface_data2_n()
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.CalculateTheVolumericDataSum.setEnabled(False)
        self.ui.VolumrricDataGrid2.setTitle("Grid")
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)

    @staticmethod
    def change_color_of_cell_prompt(table):  # pragma: no cover
        i = table.selectedIndexes()[0].row()
        color = QColorDialog.getColor(initial=table.item(i, 0).background().color())
        if not color.isValid():
            return
        at_color = color.getRgbF()
        table.item(i, 0).setBackground(QColor.fromRgbF(*at_color))
        return i, at_color

    def select_isosurface_color(self):  # pragma: no cover
        table = self.ui.IsosurfaceColorsTable
        self.change_color_of_cell_prompt(table)
        self.is_scaled_colors_for_surface = False

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

    def select_voronoi_color(self):  # pragma: no cover
        voronoicolor = self.change_color(self.ui.ColorVoronoi, SETTINGS_Color_Of_Voronoi)
        self.ui.openGLWidget.set_color_of_voronoi(voronoicolor)

    def select_background_color(self):  # pragma: no cover
        background_color = self.change_color(self.ui.ColorBackground, SETTINGS_Color_Of_Background)
        self.ui.openGLWidget.set_color_of_background(background_color)

    def select_bond_color(self):  # pragma: no cover
        bondscolor = self.change_color(self.ui.ColorBond, SETTINGS_Color_Of_Bonds)
        self.ui.openGLWidget.set_color_of_bonds(bondscolor)

    def select_axes_color(self):  # pragma: no cover
        axescolor = self.change_color(self.ui.ColorAxes, SETTINGS_Color_Of_Axes)
        self.ui.openGLWidget.set_color_of_axes(axescolor)

    def select_contour_color(self):  # pragma: no cover
        self.change_color(self.ui.ColorContour, SETTINGS_Color_Of_Contour)
        self.plot_contour()

    def bond_len_correct(self, d):
        let1 = self.ui.FormAtomsList1.currentText()
        let2 = self.ui.FormAtomsList2.currentText()
        self.ui.openGLWidget.bond_len_correct(let1, let2, d)
        print(let1, "-", let2, ": ", d)

    def change_color(self, colorUi, var_property):   # pragma: no cover
        color = QColorDialog.getColor()
        color_str = str(color.getRgb()[0]) + "," + str(color.getRgb()[1]) + "," + str(color.getRgb()[2])
        colorUi.setStyleSheet("background-color:rgb(" + color_str + ")")
        newcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        self.save_property(var_property, color_str)
        return newcolor

SETTINGS_Folder = 'home'
SETTINGS_FormSettingsColorsScale = 'colors/ColorsScale'
SETTINGS_FormSettingsColorsFixed = 'colors/ColorsFixed'
SETTINGS_FormSettingsColorsFixedMin = 'colors/ColorsFixedMin'
SETTINGS_FormSettingsColorsFixedMax = 'colors/ColorsFixedMax'
SETTINGS_FormSettingsColorsScaleType = 'colors/ColorsScaleType'
SETTINGS_FormSettingsOpeningCheckOnlyOptimal = 'open/CheckOnlyOptimal'
SETTINGS_FormSettingsParseAtomicProperties = 'open/ParseAtomicProperties'
SETTINGS_FormSettingsViewCheckAtomSelection = 'view/CheckAtomSelection'
SETTINGS_FormSettingsViewRadioColorBondsManual = 'view/BondsColorType'
SETTINGS_FormSettingsViewCheckXYZasCritic2 = 'mode/XYZasCritic2'
SETTINGS_FormSettingsViewCheckShowAtoms = 'view/CheckShowAtoms'
SETTINGS_FormSettingsViewCheckShowAtomNumber = 'view/CheckShowAtomNumber'
SETTINGS_FormSettingsViewCheckShowBox = 'view/CheckShowBox'
SETTINGS_FormSettingsViewCheckShowAxes = 'view/CheckShowAxes'
SETTINGS_FormSettingsViewCheckShowBonds = 'view/CheckShowBonds'
SETTINGS_FormSettingsViewSpinBondWidth = 'view/SpinBondWidth'
SETTINGS_FormSettingsViewSpinContourWidth = 'view/SpinContourWidth'
SETTINGS_GlCullFace = 'view/GlCullFace'
SETTINGS_FormSettingsActionOnStart = 'action/OnStart'
SETTINGS_PropertyFontSize = 'property/fontsize'
SETTINGS_PropertyShiftX = 'property/shiftx'
SETTINGS_PropertyShiftY = 'property/shifty'

SETTINGS_FormSettingsPreferredCoordinatesStyle = 'model/FormSettingsPreferredCoordinatesStyle'
SETTINGS_FormSettingsPreferredCoordinates = 'model/FormSettingsPreferredCoordinates'
SETTINGS_FormSettingsPreferredUnits = 'model/FormSettingsPreferred/units'
SETTINGS_FormSettingsPreferredLattice = 'model/FormSettingsPreferredLattice'

SETTINGS_Color_Of_Atoms_Scheme = 'colors/scheme'
SETTINGS_Color_Of_Atoms = 'colors/atoms'
SETTINGS_Color_Of_Bonds = 'colors/bonds'
SETTINGS_Color_Of_Background = 'colors/background'
SETTINGS_Color_Of_Box = 'colors/box'
SETTINGS_Color_Of_Voronoi = 'colors/voronoi'
SETTINGS_Color_Of_Axes = 'colors/axes'
SETTINGS_Color_Of_Contour = 'colors/contour'
SETTINGS_perspective_angle = 'perspectiveangle'
