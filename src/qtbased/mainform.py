# -*- coding: utf-8 -*-
import os
try:
    if os.environ["XDG_SESSION_TYPE"] == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
except Exception as e:
    print(str(e))
import math
import sys
from pathlib import Path
from copy import deepcopy
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from utils import helpers
from models.atomic_model import TAtomicModel
from utils.calculators import Calculators as Calculator
from utils.calculators import gaps
from models.capedswcnt import CapedSWNT
from models.bint import BiNT
from utils.fdfdata import TFDFFile
from models.graphene import Graphene
from utils.periodic_table import TPeriodTable
from utils.siesta import TSIESTA
from models.swnt import SWNT
from models.swgnt import SWGNT
from thirdparty.critic2 import check_cro_file
from thirdparty.vasp import vasp_dos
from utils.importer import Importer
from utils.electronic_prop_reader import read_siesta_bands, dos_from_file
from PySide2.QtCore import QLocale, QSettings, Qt, QSize
from PySide2.QtGui import QColor, QIcon, QImage, QKeySequence, QPixmap, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QListWidgetItem, QAction, QDialog, QFileDialog, QMessageBox, QColorDialog
from PySide2.QtWidgets import QDoubleSpinBox, QMainWindow, QShortcut, QTableWidgetItem, QTreeWidgetItem
from PySide2.QtWidgets import QTreeWidgetItemIterator
from qtbased.image3dexporter import Image3Dexporter
from models.gaussiancube import GaussianCube
from models.volumericdata import VolumericData
from models.xsf import XSF
from ui.about import Ui_DialogAbout as Ui_about
from ui.form import Ui_MainWindow as Ui_form
from thirdparty.firefly import atomic_model_to_firefly_inp

from thirdparty import ase, critic2

sys.path.append('.')

is_with_figure = True


class MainForm(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.ui = Ui_form()
        self.ui.setupUi(self)

        self.models = []
        selected_atom_info = [self.ui.FormActionsPreComboAtomsList, self.ui.FormActionsPreSpinAtomsCoordX,
                              self.ui.FormActionsPreSpinAtomsCoordY, self.ui.FormActionsPreSpinAtomsCoordZ,
                              self.ui.AtomPropertiesText]
        self.ui.openGLWidget.set_form_elements(self.ui.FormSettingsViewCheckAtomSelection, selected_atom_info, 1)
        self.fdf_data = TFDFFile()
        self.volumeric_data = VolumericData()
        self.volumeric_data2 = VolumericData()  # only for volumeric data difference
        self.PDOSdata = []
        self.filename = ""
        self.colors_cash = {}
        self.table_header_stylesheet = "::section{Background-color:rgb(190,190,190)}"
        self.is_scaled_colors_for_surface = True
        self.rotation_step = 1

        self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut.activated.connect(self.atom_delete)
        self.active_model = -1
        self.perspective_angle = 45

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

        self.ui.AtomPropertiesText.textChanged.connect(self.critical_point_prop_to_form)

        self.ui.FormModelComboModels.currentIndexChanged.connect(self.model_to_screen)
        self.ui.FormActionsPostTreeSurface.itemSelectionChanged.connect(self.type_of_surface)
        self.ui.PropertyForColorOfAtoms.currentIndexChanged.connect(self.color_atoms_with_property)
        self.ui.ColorAtomsWithProperty.stateChanged.connect(self.color_atoms_with_property)

        self.ui.FormAtomsList1.currentIndexChanged.connect(self.bond_len_to_screen)
        self.ui.FormAtomsList2.currentIndexChanged.connect(self.bond_len_to_screen)

        self.ui.FormActionsPreRadioSWNT.toggled.connect(self.swnt_type1_selected)
        self.ui.FormActionsPreRadioSWNTcap.toggled.connect(self.swnt_type2_selected)
        self.ui.FormActionsPreRadioSWNTcap_2.toggled.connect(self.swnt_type2_selected)

        self.ui.ActivateFragmentSelectionModeCheckBox.toggled.connect(self.activate_fragment_selection_mode)
        self.ui.ActivateFragmentSelectionTransp.valueChanged.connect(self.activate_fragment_selection_mode)

        # buttons
        self.ui.FormActionsPostButPlotBondsHistogram.clicked.connect(self.plot_bonds_histogram)
        self.ui.FormActionsPreButFDFGenerate.clicked.connect(self.fdf_data_to_form)
        self.ui.FormActionsPreButFDFToFile.clicked.connect(self.fdf_data_from_form_to_file)
        self.ui.FormActionsPreButFillSpace.clicked.connect(self.fill_space)
        self.ui.but_create_nanotube.clicked.connect(self.create_swnt)
        self.ui.FormActionsPreButBiElementGenerate.clicked.connect(self.create_bi_el_nt)
        self.ui.FormActionsPreButGrapheneGenerate.clicked.connect(self.create_graphene)
        self.ui.FormActionsPostButSurface.clicked.connect(self.plot_surface)
        self.ui.FormActionsPostButSurfaceParse.clicked.connect(self.parse_volumeric_data)
        self.ui.FormActionsPostButSurfaceParse2.clicked.connect(self.parse_volumeric_data2)
        self.ui.FormActionsPostButSurfaceLoadData.clicked.connect(self.volumeric_data_load)
        self.ui.FormActionsPostButSurfaceLoadData2.clicked.connect(self.volumeric_data_load2)
        self.ui.CalculateTheVolumericDataDifference.clicked.connect(self.volumeric_data_difference)
        self.ui.CalculateTheVolumericDataSum.clicked.connect(self.volumeric_data_sum)
        self.ui.ExportTheVolumericDataXSF.clicked.connect(self.export_volumeric_data_to_xsf)
        self.ui.ExportTheVolumericDataCube.clicked.connect(self.export_volumeric_data_to_cube)
        self.ui.FormActionsPostButContour.clicked.connect(self.plot_contour)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.ColorVoronoiDialogButton.clicked.connect(self.select_voronoi_color)
        self.ui.ColorAxesDialogButton.clicked.connect(self.select_axes_color)
        self.ui.ColorContourDialogButton.clicked.connect(self.select_contour_color)
        self.ui.FormActionsPostButSurfaceAdd.clicked.connect(self.add_isosurface_color_to_table)
        self.ui.FormActionsPostButSurfaceDelete.clicked.connect(self.delete_isosurface_color_from_table)
        self.ui.FormActionsButtonPlotPDOS.clicked.connect(self.plot_pdos)
        self.ui.plot_bands.clicked.connect(self.plot_bands)
        self.ui.parse_bands.clicked.connect(self.parse_bands)
        self.ui.FormActionsButtonPlotPDOSselected.clicked.connect(self.plot_selected_pdos)
        self.ui.FormModifyCellButton.clicked.connect(self.edit_cell)
        self.ui.FormActionsPostButGetBonds.clicked.connect(self.get_bonds)
        self.ui.PropertyAtomAtomDistanceGet.clicked.connect(self.get_bond)
        self.ui.FormStylesFor2DGraph.clicked.connect(self.set_2d_graph_styles)
        self.ui.FormModifyTwist.clicked.connect(self.twist_model)

        self.ui.FormSelectPart1File.clicked.connect(self.set_part1_file)
        self.ui.FormSelectPart2File.clicked.connect(self.set_part2_file)
        self.ui.CreateModelFromParts.clicked.connect(self.create_model_from_parts)

        self.ui.FormIEd12Generate.clicked.connect(self.d12_to_file)

        self.ui.FormASERamanAndIRscriptCreate.clicked.connect(self.ase_raman_and_ir_script_create)
        self.ui.FormASERamanAndIRscriptParse.clicked.connect(self.ase_raman_and_ir_parse)
        self.ui.FormASERamanAndIRscriptPlot.clicked.connect(self.ase_raman_and_ir_plot)

        self.ui.changeFragment1StatusByX.clicked.connect(self.change_fragment1_status_by_x)
        self.ui.changeFragment1StatusByY.clicked.connect(self.change_fragment1_status_by_y)
        self.ui.changeFragment1StatusByZ.clicked.connect(self.change_fragment1_status_by_z)
        self.ui.fragment1Clear.clicked.connect(self.fragment1_clear)
        self.ui.FormCreateCriXYZFile.clicked.connect(self.create_critic2_xyz_file)
        self.ui.FormCPdeleteFromList.clicked.connect(self.delete_cp_from_list)
        self.ui.FormCPaddToList.clicked.connect(self.add_cp_to_list)

        self.ui.FormActionsPreButDeleteAtom.clicked.connect(self.atom_delete)
        self.ui.FormActionsPreButModifyAtom.clicked.connect(self.atom_modify)
        self.ui.FormActionsPreButAddAtom.clicked.connect(self.atom_add)

        self.ui.FormActionsPreButSelectLeftElectrode.clicked.connect(self.add_left_electrode_file)
        self.ui.FormActionsPreButSelectScatRegione.clicked.connect(self.add_scat_region_file)
        self.ui.FormActionsPreButSelectRightElectrode.clicked.connect(self.add_right_electrode_file)
        self.ui.FormActionsPreButCreateModelWithElectrodes.clicked.connect(self.create_model_with_electrodes)

        self.ui.FormActionsButtonAddDOSFile.clicked.connect(self.add_dos_file)
        self.ui.FormActionsButtonPlotDOS.clicked.connect(self.plot_dos)
        self.ui.FormActionsButtonClearDOS.clicked.connect(self.clear_dos)

        self.ui.FormButtonAddCroData.clicked.connect(self.add_critic2_cro_file)
        self.ui.FormCreateCriFile.clicked.connect(self.create_cri_file)

        self.ui.FormActionsPostButPlusCellParam.clicked.connect(self.add_cell_param)
        self.ui.FormActionsPostButAddRowCellParam.clicked.connect(self.add_cell_param_row)
        self.ui.FormActionsPostButDeleteRowCellParam.clicked.connect(self.delete_cell_param_row)
        self.ui.FormActionsPostButPlusDataCellParam.clicked.connect(self.add_data_cell_param)

        self.ui.FormModifyRotation.clicked.connect(self.model_rotation)
        self.ui.FormModifyGrowX.clicked.connect(self.model_grow_x)
        self.ui.FormModifyGrowY.clicked.connect(self.model_grow_y)
        self.ui.FormModifyGrowZ.clicked.connect(self.model_grow_z)

        self.ui.FormActionsPostButVoronoi.clicked.connect(self.plot_voronoi)
        self.ui.FormActionsPostButOptimizeCellParam.clicked.connect(self.plot_volume_param_energy)

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        mendeley = TPeriodTable()
        atoms_list = mendeley.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))
        self.ui.FormActionsPreComboAtomsList.setModel(model)
        self.ui.FormAtomsList1.setModel(model)
        self.ui.FormAtomsList2.setModel(model)

        # sliders
        self.ui.FormActionsPostSliderContourXY.valueChanged.connect(self.set_xsf_z_position)
        self.ui.FormActionsPostSliderContourXZ.valueChanged.connect(self.set_xsf_y_position)
        self.ui.FormActionsPostSliderContourYZ.valueChanged.connect(self.set_xsf_x_position)

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

        self.ui.IsosurfaceColorsTable.setColumnCount(2)
        self.ui.IsosurfaceColorsTable.setHorizontalHeaderLabels(["Value", "Transparancy"])
        self.ui.IsosurfaceColorsTable.setColumnWidth(0, 120)
        self.ui.IsosurfaceColorsTable.setColumnWidth(1, 150)
        self.ui.IsosurfaceColorsTable.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.IsosurfaceColorsTable.verticalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.IsosurfaceColorsTable.doubleClicked.connect(self.select_isosurface_color)

        cell_prediction_type = QStandardItemModel()
        cell_prediction_type.appendRow(QStandardItem("Murnaghan"))
        cell_prediction_type.appendRow(QStandardItem("BirchMurnaghan"))
        cell_prediction_type.appendRow(QStandardItem("Parabola"))
        self.ui.FormActionsPostComboCellParam.setModel(cell_prediction_type)

        form_settings_preferred_coordinates_type = QStandardItemModel()
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Cartesian"))
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Fractional"))
        form_settings_preferred_coordinates_type.appendRow(QStandardItem("Zmatrix Cartesian"))
        self.ui.FormSettingsPreferredCoordinates.setModel(form_settings_preferred_coordinates_type)
        self.ui.FormSettingsPreferredCoordinates.setCurrentText(self.CoordType)
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
        self.ui.FormSettingsPreferredLattice.setCurrentText(self.LatticeType)
        self.ui.FormSettingsPreferredLattice.currentIndexChanged.connect(self.save_state_preferred_lattice)

        self.ui.FormActionsPostComboBonds.currentIndexChanged.connect(self.fill_bonds)

        swnt_ind_type = QStandardItemModel()
        swnt_ind_type.appendRow(QStandardItem("(6,6)"))
        swnt_ind_type.appendRow(QStandardItem("(10,10)"))
        swnt_ind_type.appendRow(QStandardItem("(10,0)"))
        swnt_ind_type.appendRow(QStandardItem("(19,0)"))
        self.ui.FormActionsPreComboSWNTind.setModel(swnt_ind_type)

        fill_space_model = QStandardItemModel()
        fill_space_model.appendRow(QStandardItem("cylinder"))
        self.ui.FormActionsPreComboFillSpace.setModel(fill_space_model)

        self.prepare_form_actions_combo_pdos_indexes()
        self.prepare_form_actions_combo_pdos_species()

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

        bi_element_type_tube = QStandardItemModel()
        bi_element_type_tube.appendRow(QStandardItem("BN"))
        bi_element_type_tube.appendRow(QStandardItem("BC"))
        self.ui.FormNanotypeTypeSelector.setModel(bi_element_type_tube)
        self.ui.FormNanotypeTypeSelector.setCurrentIndex(0)

        self.ui.FormActionsPostTableCellParam.setColumnCount(5)
        self.ui.FormActionsPostTableCellParam.setHorizontalHeaderLabels(["volume", "Energy", "a", "b", "c"])
        self.ui.FormActionsPostTableCellParam.setColumnWidth(0, 60)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(1, 70)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(2, 70)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(3, 70)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(4, 70)
        self.ui.FormActionsPostTableCellParam.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormActionsPostTableCellParam.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        argsCell = QStandardItemModel()
        argsCell.appendRow(QStandardItem("V"))
        argsCell.appendRow(QStandardItem("E"))
        argsCell.appendRow(QStandardItem("a"))
        argsCell.appendRow(QStandardItem("b"))
        argsCell.appendRow(QStandardItem("c"))
        self.ui.FormActionsPostComboCellParamX.setModel(argsCell)

        self.ui.FormActionsTabeDOSProperty.setColumnCount(2)
        self.ui.FormActionsTabeDOSProperty.setHorizontalHeaderLabels(["Path", "EFermy"])
        self.ui.FormActionsTabeDOSProperty.setColumnWidth(0, 200)
        self.ui.FormActionsTabeDOSProperty.setColumnWidth(1, 80)
        self.ui.FormActionsTabeDOSProperty.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormActionsTabeDOSProperty.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.ui.FormActionsPosTableBonds.setColumnCount(2)
        self.ui.FormActionsPosTableBonds.setHorizontalHeaderLabels(["Bond", "Lenght"])
        self.ui.FormActionsPosTableBonds.setColumnWidth(0, 120)
        self.ui.FormActionsPosTableBonds.setColumnWidth(1, 170)
        self.ui.FormActionsPosTableBonds.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormActionsPosTableBonds.verticalHeader().setStyleSheet(self.table_header_stylesheet)

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
        open_action.triggered.connect(self.rotate_model_xm)
        self.ui.toolBar.addAction(open_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoX.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoX.png')), 'RotateX+', self)
        else:
            open_action = QAction('RotateX+', self)
        open_action.triggered.connect(self.rotate_model_xp)
        self.ui.toolBar.addAction(open_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoY.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoY.png')), 'RotateY-', self)
        else:
            open_action = QAction('RotateY-', self)
        open_action.triggered.connect(self.rotate_model_ym)
        self.ui.toolBar.addAction(open_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoY.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoY.png')), 'RotateY+', self)
        else:
            open_action = QAction('RotateY+', self)
        open_action.triggered.connect(self.rotate_model_yp)
        self.ui.toolBar.addAction(open_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoZ.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoZ.png')), 'RotateZ-', self)
        else:
            open_action = QAction('RotateZ-', self)
        open_action.triggered.connect(self.rotate_model_zm)
        self.ui.toolBar.addAction(open_action)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoZ.png'):
            open_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoZ.png')), 'RotateZ+', self)
        else:
            open_action = QAction('RotateZ+', self)
        open_action.triggered.connect(self.rotate_model_zp)
        self.ui.toolBar.addAction(open_action)
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

    def add_cell_param(self):
        """ add cell params"""
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)[0]
            if Importer.check_format(fname) == "SIESTAout":
                self.fill_cell_info(fname)
        except Exception as e:
            self.show_error(e)

    def add_cell_param_row(self):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)

    def add_data_cell_param(self):
        """ add cell params from file"""
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)[0]
            self.work_dir = os.path.dirname(fname)

            if os.path.exists(fname):
                f = open(fname)
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
                        self.fill_cell_info_row(energy, volume, a, b, c)
                f.close()
        except Exception as e:
            self.show_error(e)

    def add_critic2_cro_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)[0]
            self.work_dir = os.path.dirname(fname)

            box_bohr, box_ang, box_deg, cps = check_cro_file(fname)
            al = math.radians(box_deg[0])
            be = math.radians(box_deg[1])
            ga = math.radians(box_deg[2])
            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lat_vectors_from_params(box_ang[0], box_ang[1], box_ang[2],
                                                                                 al, be, ga)

            model = self.models[-1]
            model.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)

            k = 0
            for cp in model.bcp:
                for cp1 in cps:
                    d1 = (cp.x - cp1[1]) ** 2
                    d2 = (cp.y - cp1[2]) ** 2
                    d3 = (cp.z - cp1[3]) ** 2
                    if math.sqrt(d1 + d2 + d3) < 1e-5:
                        cp.setProperty("field", cp1[4])
                        cp.setProperty("grad", cp1[5])
                        cp.setProperty("lap", cp1[6])
                        k += 1
            self.plot_last_model()
        except Exception as e:
            self.show_error(e)

    @staticmethod
    def show_error(e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        msg.exec_()

    def add_dos_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)[0]
            self.work_dir = os.path.dirname(fname)
            self.check_dos(fname)
        except Exception as e:
            self.show_error(e)

    def add_isosurface_color_to_table(self):
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        i = self.ui.IsosurfaceColorsTable.rowCount() + 1
        value = self.ui.FormActionsPostLabelSurfaceValue.text()
        self.ui.IsosurfaceColorsTable.setRowCount(i)
        color_cell = QTableWidgetItem(value)
        color_cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.ui.IsosurfaceColorsTable.setItem(i - 1, 0, color_cell)
        transp_cell = QDoubleSpinBox()
        transp_cell.setRange(0, 1)
        transp_cell.setValue(1)
        transp_cell.setSingleStep(0.1)
        transp_cell.setDecimals(2)
        transp_cell.setLocale(QLocale(QLocale.English))
        transp_cell.setMaximumWidth(145)
        self.ui.IsosurfaceColorsTable.setCellWidget(i - 1, 1, transp_cell)
        minv, maxv = self.volumeric_data.min, self.volumeric_data.max
        color = self.get_color(cmap, minv, maxv, float(value), color_scale)
        self.ui.IsosurfaceColorsTable.item(i - 1, 0).setBackground(
            QColor.fromRgbF(color[0], color[1], color[2], color[3]))

        self.ui.FormActionsPostButSurface.setEnabled(True)
        self.ui.FormActionsPostButSurfaceDelete.setEnabled(True)

    def set_part1_file(self) -> None:
        fname = self.get_file_name_from_save_dialog("All files (*.*)")
        if os.path.exists(fname):
            self.ui.part1_file.setText(fname)

    def set_part2_file(self) -> None:
        fname = self.get_file_name_from_save_dialog("All files (*.*)")
        if os.path.exists(fname):
            self.ui.part2_file.setText(fname)

    def create_model_from_parts(self) -> None:
        file_name1 = self.ui.part1_file.text()
        file_name2 = self.ui.part2_file.text()
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            models1, fdf_data1 = Importer.import_from_file(file_name1, 'opt', False, False)
        else:
            models1, fdf_data1 = Importer.import_from_file(file_name1, 'all', False, False)

        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            models2, fdf_data2 = Importer.import_from_file(file_name2, 'opt', False, False)
        else:
            models2, fdf_data2 = Importer.import_from_file(file_name2, 'all', False, False)

        combo_model = TAtomicModel()
        if len(models1) > 0:
            part1 = models1[-1]
            cm_old = - part1.centr_mass()
            part1.move(*cm_old)
            rot_x = self.ui.FormPart1RotX.value()
            rot_y = self.ui.FormPart1RotY.value()
            rot_z = self.ui.FormPart1RotZ.value()
            part1.rotate(rot_x, rot_y, rot_z)

            cm_x_new = self.ui.FormPart1CMx.value()
            cm_y_new = self.ui.FormPart1CMy.value()
            cm_z_new = self.ui.FormPart1CMz.value()
            part1.move(cm_x_new, cm_y_new, cm_z_new)

            combo_model.add_atomic_model(part1)

        if len(models2) > 0:
            part2 = models2[-1]

            cm_old = - part2.centr_mass()
            part2.move(*cm_old)
            rot_x = self.ui.FormPart2RotX.value()
            rot_y = self.ui.FormPart2RotY.value()
            rot_z = self.ui.FormPart2RotZ.value()
            part2.rotate(rot_x, rot_y, rot_z)

            cm_x_new = self.ui.FormPart2CMx.value()
            cm_y_new = self.ui.FormPart2CMy.value()
            cm_z_new = self.ui.FormPart2CMz.value()
            part2.move(cm_x_new, cm_y_new, cm_z_new)

            combo_model.add_atomic_model(part2)

        self.models.append(combo_model)
        self.plot_last_model()

    def add_left_electrode_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.work_dir = os.path.dirname(fname)
            self.save_active_folder()
            self.ui.FormActionsPreLeftElectrode.setText(fname)

    def add_right_electrode_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.work_dir = os.path.dirname(fname)
            self.save_active_folder()
            self.ui.FormActionsPreRightElectrode.setText(fname)

    def add_scat_region_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.work_dir = os.path.dirname(fname)
            self.save_active_folder()
            self.ui.FormActionsPreScatRegion.setText(fname)

    def atom_add(self):
        if len(self.models) == 0:
            return
        self.ui.openGLWidget.add_new_atom()

    def atom_delete(self):
        if len(self.models) == 0:
            return
        self.ui.openGLWidget.delete_selected_atom()
        self.models[-1] = self.ui.openGLWidget.main_model
        self.model_to_screen(-1)

    def atom_modify(self):
        if len(self.models) == 0:
            return
        self.ui.openGLWidget.modify_selected_atom()
        self.models.append(self.ui.openGLWidget.main_model)
        self.model_to_screen(-1)

    def bond_len_to_screen(self):
        let1 = self.ui.FormAtomsList1.currentIndex()
        let2 = self.ui.FormAtomsList2.currentIndex()

        if not ((let1 == 0) or (let2 == 0)):
            mendeley = TPeriodTable()
            bond = mendeley.Bonds[let1][let2]
        else:
            bond = 0
        self.ui.FormBondLenSpinBox.setValue(bond)

    def clear_form_isosurface_data2_n(self):
        self.ui.FormActionsPostLabelSurfaceNx.setText("")
        self.ui.FormActionsPostLabelSurfaceNy.setText("")
        self.ui.FormActionsPostLabelSurfaceNz.setText("")

    def check_pdos(self, f_name: str) -> None:   # pragma: no cover
        pdos_file = Importer.check_pdos_file(f_name)
        if pdos_file:
            self.ui.FormActionsLinePDOSfile.setText(pdos_file)
            self.ui.FormActionsButtonPlotPDOS.setEnabled(True)

    def check_bands(self, f_name: str) -> None:   # pragma: no cover
        bands_file = Importer.check_bands_file(f_name)
        if bands_file:
            self.ui.FormActionsLineBANDSfile.setText(bands_file)
            self.ui.parse_bands.setEnabled(True)

    def check_dos(self, f_name: str) -> None:   # pragma: no cover
        dos_file, e_fermy = Importer.check_dos_file(f_name)
        if dos_file:
            i = self.ui.FormActionsTabeDOSProperty.rowCount() + 1
            self.ui.FormActionsTabeDOSProperty.setRowCount(i)
            line = "..." + str(dos_file)[-15:]
            q_tab_widg = QTableWidgetItem(line)
            q_tab_widg.setToolTip(dos_file)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 0, q_tab_widg)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 1, QTableWidgetItem(str(e_fermy)))
            self.ui.FormActionsTabeDOSProperty.update()

    def check_volumeric_data(self, file_name):
        files = []
        if file_name.endswith(".XSF"):
            files.append(file_name)
        if file_name.endswith(".cube"):
            files.append(file_name)

        if file_name.endswith(".out") or file_name.endswith(".OUT"):
            label = TSIESTA.system_label(file_name)
            directory = os.path.dirname(file_name)
            dirs, content = helpers.getsubs(directory)
            for posFile in content:
                file_candidat = Path(posFile).name
                if file_candidat.startswith(label) and file_candidat.endswith(".cube"):
                    files.append(directory + "/" + file_candidat)

            files.append(directory + "/" + label + ".XSF")
        self.ui.FormActionsPostList3DData.clear()
        for file in files:
            if os.path.exists(file):
                self.ui.FormActionsPostList3DData.addItems([file])
                self.ui.FormActionsPostButSurfaceParse.setEnabled(True)
            self.ui.FormActionsPostList3DData.update()

    def change_fragment1_status_by_x(self):
        xmin = self.ui.xminborder.value()
        xmax = self.ui.xmaxborder.value()
        for at in self.ui.openGLWidget.main_model.atoms:
            if (at.x >= xmin) and (at.x <= xmax):
                at.fragment1 = True
        self.ui.openGLWidget.atoms_of_selected_fragment_to_form()
        self.ui.openGLWidget.update_view()

    def change_fragment1_status_by_y(self):
        ymin = self.ui.yminborder.value()
        ymax = self.ui.ymaxborder.value()
        for at in self.ui.openGLWidget.main_model.atoms:
            if (at.y >= ymin) and (at.y <= ymax):
                at.fragment1 = True
        self.ui.openGLWidget.atoms_of_selected_fragment_to_form()
        self.ui.openGLWidget.update_view()

    def change_fragment1_status_by_z(self):
        zmin = self.ui.zminborder.value()
        zmax = self.ui.zmaxborder.value()
        for at in self.ui.openGLWidget.main_model.atoms:
            if (at.z >= zmin) and (at.z <= zmax):
                at.fragment1 = True
        self.ui.openGLWidget.atoms_of_selected_fragment_to_form()
        self.ui.openGLWidget.update_view()

    def fragment1_clear(self):
        for at in self.ui.openGLWidget.main_model.atoms:
            at.fragment1 = False
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

    def color_to_ui(self, color_ui, state_color):
        r = state_color.split()[0]
        g = state_color.split()[1]
        b = state_color.split()[2]
        color_ui.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

    def create_model_with_electrodes(self):
        try:
            left_file = self.ui.FormActionsPreLeftElectrode.text()
            scat_file = self.ui.FormActionsPreScatRegion.text()
            righ_file = self.ui.FormActionsPreRightElectrode.text()

            model_left, fdf_left = Importer.import_from_file(left_file)
            model_scat, fdf_scat = Importer.import_from_file(scat_file)
            model_righ, fdf_righ = Importer.import_from_file(righ_file)

            model_left = model_left[0]
            model_scat = model_scat[0]
            model_righ = model_righ[0]

            """ start: parts transformation"""
            left_move_x = self.ui.FormActionsPreMoveLeftElectrodeX.value()
            left_move_y = self.ui.FormActionsPreMoveLeftElectrodeY.value()
            model_left.move(left_move_x, left_move_y, 0)

            righ_move_x = self.ui.FormActionsPreMoveRightElectrodeX.value()
            righ_move_y = self.ui.FormActionsPreMoveRightElectrodeY.value()
            model_righ.move(righ_move_x, righ_move_y, 0)

            scat_rotationX = self.ui.FormActionsPreSpinScatRotX.value()
            scat_rotationY = self.ui.FormActionsPreSpinScatRotY.value()
            scat_rotationZ = self.ui.FormActionsPreSpinScatRotZ.value()

            model_scat.rotate_x(scat_rotationX)
            model_scat.rotate_y(scat_rotationY)
            model_scat.rotate_z(scat_rotationZ)

            scat_move_x = self.ui.FormActionsPreMoveScatX.value()
            scat_move_y = self.ui.FormActionsPreMoveScatY.value()
            model_scat.move(scat_move_x, scat_move_y, 0)

            """ end: parts transformation"""

            left_elec_max = model_left.maxZ()
            left_bord = model_scat.minZ()

            right_elec_min = model_righ.minZ()

            left_dist = self.ui.FormActionsPreSpinLeftElectrodeDist.value()
            right_dist = self.ui.FormActionsPreSpinRightElectrodeDist.value()

            model = TAtomicModel()
            model.add_atomic_model(model_left)
            model_scat.move(0, 0, -(left_bord - left_elec_max) + left_dist)
            model.add_atomic_model(model_scat)
            right_bord = model.maxZ()
            model_righ.move(0, 0, (right_bord - right_elec_min) + right_dist)
            model.add_atomic_model(model_righ)

            self.models.append(model)
            self.plot_model(-1)
            self.ui.openGLWidget.add_atoms()
            self.fill_gui("SWNT-model")
        except Exception as e:
            self.show_error(e)

    def colors_of_atoms(self):
        atoms_color = [QTableWidgetItem(self.ui.ColorsOfAtomsTable.item(1, 0)).background().color().getRgbF()]
        for i in range(0, self.ui.ColorsOfAtomsTable.rowCount()):
            col = self.ui.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atoms_color.append(col)
        return atoms_color

    def delete_cell_param_row(self):
        row = self.ui.FormActionsPostTableCellParam.currentRow()
        self.ui.FormActionsPostTableCellParam.removeRow(row)

    def delete_isosurface_color_from_table(self):
        row = self.ui.IsosurfaceColorsTable.currentRow()
        self.ui.IsosurfaceColorsTable.removeRow(row)

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
        return QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, file_mask,
                                           options=QFileDialog.DontUseNativeDialog)[0]

    def get_file_name_from_open_dialog(self, file_mask):  # pragma: no cover
        return QFileDialog.getOpenFileName(self, 'Open file', self.work_dir, file_mask,
                                           options=QFileDialog.DontUseNativeDialog)[0]

    def export_volumeric_data_to_xsf(self):
        try:
            fname = self.get_file_name_from_save_dialog("XSF files (*.XSF)")
            x1 = self.ui.FormVolDataExportX1.value()
            x2 = self.ui.FormVolDataExportX2.value()
            y1 = self.ui.FormVolDataExportY1.value()
            y2 = self.ui.FormVolDataExportY2.value()
            z1 = self.ui.FormVolDataExportZ1.value()
            z2 = self.ui.FormVolDataExportZ2.value()
            self.export_volumeric_data_to_file(fname, x1, x2, y1, y2, z1, z2)
        except Exception as e:
            self.show_error(e)

    def export_volumeric_data_to_cube(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "cube files (*.cube)",
                                                options=QFileDialog.DontUseNativeDialog)[0]
            x1 = self.ui.FormVolDataExportX1.value()
            x2 = self.ui.FormVolDataExportX2.value()
            y1 = self.ui.FormVolDataExportY1.value()
            y2 = self.ui.FormVolDataExportY2.value()
            z1 = self.ui.FormVolDataExportZ1.value()
            z2 = self.ui.FormVolDataExportZ2.value()
            self.export_volumeric_data_to_file(fname, x1, x2, y1, y2, z1, z2)
        except Exception as e:
            self.show_error(e)

    def export_volumeric_data_to_file(self, fname, x1, x2, y1, y2, z1, z2):
        self.ui.openGLWidget.volumeric_data_to_file(fname, self.volumeric_data, x1, x2, y1, y2, z1, z2)
        self.work_dir = os.path.dirname(fname)
        self.save_active_folder()

    def fill_gui(self, title=""):
        file_name = self.filename
        if title == "":
            self.fill_file_name(file_name)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()
        self.check_volumeric_data(file_name)

        self.ui.PropertyAtomAtomDistanceAt1.setMaximum(self.ui.openGLWidget.main_model.nAtoms())
        self.ui.PropertyAtomAtomDistanceAt2.setMaximum(self.ui.openGLWidget.main_model.nAtoms())
        self.ui.PropertyAtomAtomDistance.setText("")

        if Importer.check_format(file_name) == "SIESTAout":
            self.check_dos(file_name)
            self.check_pdos(file_name)
            self.check_bands(file_name)
            self.fill_cell_info(file_name)
            self.fill_energies(file_name)

        if Importer.check_format(file_name) == "SIESTAfdf":
            c = self.ui.openGLWidget.main_model.get_LatVect3_norm()
            self.ui.FormActionsPreZSizeFillSpace.setValue(c)

    def fill_energies(self, f_name: str) -> None:
        """Plot energies for steps of output"""
        energies = TSIESTA.energies(f_name)
        self.ui.PyqtGraphWidget.set_xticks(None)

        x_title = "Step"
        y_title = "Energy, eV"
        title = "Energies"

        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        self.ui.PyqtGraphWidget.plot([np.arange(0, len(energies))], [energies], [None], title, x_title, y_title)

    def fill_file_name(self, fname):
        self.ui.Form3Dand2DTabs.setItemText(0, "3D View: " + fname)
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

        self.ui.FormModelTableProperties.setRowCount(len(properties))

        for i in range(0, len(properties)):
            self.ui.FormModelTableProperties.setItem(i, 0, QTableWidgetItem(properties[i][0]))
            self.ui.FormModelTableProperties.setItem(i, 1, QTableWidgetItem(properties[i][1]))

        self.ui.FormModifyCellEditA1.setValue(model.lat_vector1[0])
        self.ui.FormModifyCellEditA2.setValue(model.lat_vector1[1])
        self.ui.FormModifyCellEditA3.setValue(model.lat_vector1[2])
        self.ui.FormModifyCellEditB1.setValue(model.lat_vector2[0])
        self.ui.FormModifyCellEditB2.setValue(model.lat_vector2[1])
        self.ui.FormModifyCellEditB3.setValue(model.lat_vector2[2])
        self.ui.FormModifyCellEditC1.setValue(model.lat_vector3[0])
        self.ui.FormModifyCellEditC2.setValue(model.lat_vector3[1])
        self.ui.FormModifyCellEditC3.setValue(model.lat_vector3[2])

    def fill_volumeric_data(self, data, tree=" "):
        if tree == " ":
            tree = self.ui.FormActionsPostTreeSurface
        data_type = data.type
        data = data.blocks
        self.clear_qtree_widget(tree)

        if data_type == "TXSF":
            for dat in data:
                text = (dat[0].title.split('_')[3]).split(':')[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text) + "3D")
                for da in dat:
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(text + ':' + da.title.split(':')[1]))

        if data_type == "TGaussianCube":
            for dat in data:
                text = dat[0].title.split(".cube")[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text))

                child = QTreeWidgetItem(parent)
                child.setText(0, "{}".format(text))
        tree.show()

    def fill_bonds(self):
        c1, c2 = self.fill_bonds_charges()
        bonds = self.self.ui.openGLWidget.main_model.find_bonds_exact()
        self.ui.FormActionsPosTableBonds.setRowCount(0)

        mean = 0
        n = 0

        for bond in bonds:
            if ((c1 == 0) or (c2 == 0)) or ((c1 == bond[0]) and (c2 == bond[1])) or (
                    (c1 == bond[1]) and (c2 == bond[2])):
                self.ui.FormActionsPosTableBonds.setRowCount(self.ui.FormActionsPosTableBonds.rowCount() + 1)
                s = str(bond[3]) + str(bond[4]) + "-" + str(bond[5]) + str(bond[6])
                self.ui.FormActionsPosTableBonds.setItem(n, 0, QTableWidgetItem(s))
                self.ui.FormActionsPosTableBonds.setItem(n, 1, QTableWidgetItem(str(bond[2])))
                mean += bond[2]
                n += 1
        if n > 0:
            self.ui.FormActionsPostLabelMeanBond.setText("Mean value: " + str(round(mean / n, 5)))

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

    def fill_cell_info(self, fname):
        volume = TSIESTA.volume(fname)
        energy = TSIESTA.energy_tot(fname)

        models, fdf_data = Importer.import_from_file(fname)
        model = models[-1]
        a = model.get_LatVect1_norm()
        b = model.get_LatVect2_norm()
        c = model.get_LatVect3_norm()
        self.fill_cell_info_row(energy, volume, a, b, c)
        self.ui.FormActionsPreZSizeFillSpace.setValue(c)
        self.work_dir = os.path.dirname(fname)
        self.save_active_folder()

    def fill_cell_info_row(self, energy, volume, a, b, c):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)  # и одну строку в таблице
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 0, QTableWidgetItem(str(volume)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 1, QTableWidgetItem(str(energy)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 2, QTableWidgetItem(str(a)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 3, QTableWidgetItem(str(b)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 4, QTableWidgetItem(str(c)))

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
        self.ui.FormActionsPostButPlotBondsHistogram.setEnabled(True)

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

        state_check_xyz_as_critic2 = settings.value(SETTINGS_FormSettingsViewCheckXYZasCritic2, False, type=bool)
        self.ui.FormSettingsViewCheckXYZasCritic2.setChecked(state_check_xyz_as_critic2)
        self.ui.FormSettingsViewCheckXYZasCritic2.clicked.connect(self.save_state_xyz_as_critic2)

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
        self.ui.ColorsOfAtomsTable.setColumnCount(1)
        self.ui.ColorsOfAtomsTable.setHorizontalHeaderLabels(["Color"])
        self.ui.ColorsOfAtomsTable.setColumnWidth(0, 250)
        self.ui.ColorsOfAtomsTable.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.ColorsOfAtomsTable.verticalHeader().setStyleSheet(self.table_header_stylesheet)
        mendeley = TPeriodTable()
        self.state_Color_Of_Atoms = str(settings.value(SETTINGS_Color_Of_Atoms, ''))
        if (self.state_Color_Of_Atoms == 'None') or (self.state_Color_Of_Atoms == ''):
            colors = mendeley.get_all_colors()
        else:
            colors = []
            col = self.state_Color_Of_Atoms.split('|')
            for item in col:
                it = helpers.list_str_to_float(item.split())
                colors.append(it)
        lets = mendeley.get_all_letters()
        for i in range(1, len(lets) - 1):
            self.ui.ColorsOfAtomsTable.setRowCount(i)  # и одну строку в таблице
            self.ui.ColorsOfAtomsTable.setItem(i - 1, 0, QTableWidgetItem(lets[i] + " double click to edit"))
            color = colors[i]
            self.ui.ColorsOfAtomsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], 1))
        self.ui.ColorsOfAtomsTable.doubleClicked.connect(self.select_atom_color)

        self.state_Color_Of_Bonds = str(settings.value(SETTINGS_Color_Of_Bonds, '0 0 255'))
        self.color_to_ui(self.ui.ColorBond, self.state_Color_Of_Bonds)

        self.state_Color_Of_Box = str(settings.value(SETTINGS_Color_Of_Box, '0 0 0'))
        self.color_to_ui(self.ui.ColorBox, self.state_Color_Of_Box)

        self.state_Color_Of_Voronoi = str(settings.value(SETTINGS_Color_Of_Voronoi, '255 0 0'))
        self.color_to_ui(self.ui.ColorVoronoi, self.state_Color_Of_Voronoi)

        self.state_Color_Of_Axes = str(settings.value(SETTINGS_Color_Of_Axes, '0 255 0'))
        self.color_to_ui(self.ui.ColorAxes, self.state_Color_Of_Axes)

        self.state_Color_Of_Contour = str(settings.value(SETTINGS_Color_Of_Contour, '0 255 0'))
        self.color_to_ui(self.ui.ColorContour, self.state_Color_Of_Contour)

        self.CoordType = str(settings.value(SETTINGS_FormSettingsPreferredCoordinates, 'Cartesian'))
        self.units_type = str(settings.value(SETTINGS_FormSettingsPreferredUnits, 'Ang'))

        self.LatticeType = str(settings.value(SETTINGS_FormSettingsPreferredLattice, 'LatticeParameters'))

        self.action_on_start = str(settings.value(SETTINGS_FormSettingsActionOnStart, 'Nothing'))

        self.perspective_angle = int(settings.value(SETTINGS_perspective_angle, 45))
        self.ui.spin_perspective_angle.setValue(self.perspective_angle)
        self.ui.openGLWidget.set_perspective_angle(self.perspective_angle)
        self.ui.spin_perspective_angle.valueChanged.connect(self.perspective_angle_change)

    def perspective_angle_change(self):
        self.perspective_angle = self.ui.spin_perspective_angle.value()
        self.save_property(SETTINGS_perspective_angle, str(self.perspective_angle))
        self.ui.spin_perspective_angle.valueChanged.connect(self.perspective_angle_change)
        self.ui.openGLWidget.set_perspective_angle(self.perspective_angle)
        self.ui.openGLWidget.update()

    def menu_export(self):  # pragma: no cover
        if self.ui.openGLWidget.main_model.nAtoms() > 0:
            try:
                format = "FDF files (*.fdf);;XYZ files (*.xyz);;FireFly input files (*.inp);;VASP POSCAR file (POSCAR)"
                fname = self.get_file_name_from_save_dialog(format)
                self.export_to_file(self.models[self.active_model], fname)
                self.work_dir = os.path.dirname(fname)
                self.save_active_folder()
            except Exception as e:
                self.show_error(e)

    @staticmethod
    def export_to_file(model, fname):  # pragma: no cover
        if fname.find("POSCAR") >= 0:
            fname = fname.split(".")[0]
            model.toVASPposcar(fname)
        if fname.endswith(".inp"):
            atomic_model_to_firefly_inp(model, fname)
        if fname.endswith(".fdf"):
            model.toSIESTAfdf(fname)
        if fname.endswith(".xyz"):
            model.toSIESTAxyz(fname)

    def menu_open(self, file_name=False):
        if len(self.models) > 0:   # pragma: no cover
            self.action_on_start = 'Open'
            self.save_state_action_on_start()
            os.execl(sys.executable, sys.executable, *sys.argv)
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if not file_name:
            file_name = self.get_file_name_from_open_dialog("All files (*.*)")
        if os.path.exists(file_name):
            self.filename = file_name
            self.work_dir = os.path.dirname(file_name)
            try:
                self.get_atomic_model_and_fdf(file_name)
            except Exception as e:
                self.show_error(e)

            try:
                self.plot_last_model()
            except Exception as e:
                self.show_error(e)

    def get_atomic_model_and_fdf(self, fname):
        parse_properies = self.ui.FormSettingsParseAtomicProperties.isChecked()
        xyzcritic2 = self.ui.FormSettingsViewCheckXYZasCritic2.isChecked()
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            self.models, self.fdf_data = Importer.import_from_file(fname, 'opt', parse_properies, xyzcritic2)
        else:
            self.models, self.fdf_data = Importer.import_from_file(fname, 'all', parse_properies, xyzcritic2)

    def plot_last_model(self):
        if len(self.models) > 0:
            if len(self.models[-1].atoms) > 0:
                self.plot_model(-1)
                self.fill_gui()
                self.save_active_folder()

    def menu_ortho(self):  # pragma: no cover
        self.ui.openGLWidget.is_orthographic = True
        self.ui.openGLWidget.auto_zoom()
        self.ui.openGLWidget.update()

    def menu_perspective(self):  # pragma: no cover
        self.ui.openGLWidget.is_orthographic = False
        self.ui.openGLWidget.auto_zoom()
        self.ui.openGLWidget.update()

    def menu_show_box(self):  # pragma: no cover
        self.ui.FormSettingsViewCheckShowBox.isChecked(True)
        self.ui.openGLWidget.ViewBox = True
        self.ui.openGLWidget.update()

    def menu_hide_box(self):  # pragma: no cover
        self.ui.FormSettingsViewCheckShowBox.isChecked(False)
        self.ui.openGLWidget.ViewBox = False
        self.ui.openGLWidget.update()

    def menu_about(self):  # pragma: no cover
        about_win = QDialog(self)
        about_win.ui = Ui_about()
        about_win.ui.setupUi(about_win)
        about_win.setFixedSize(QSize(550, 250))
        about_win.show()

    def critical_point_prop_to_form(self):
        text = self.ui.AtomPropertiesText.toPlainText().split("Selected critical point:")
        if len(text) > 1:
            text = text[1].split()[0]

            self.ui.FormSelectedCP.setText(text)
            f = self.models[-1].bcp[int(text)].getProperty("field")
            self.ui.FormSelectedCP_f.setText(f)
            g = self.models[-1].bcp[int(text)].getProperty("grad")
            self.ui.FormSelectedCP_g.setText(g)
            lap = self.models[-1].bcp[int(text)].getProperty("lap")
            self.ui.FormSelectedCP_lap.setText(lap)

    def model_to_screen(self, value):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()
        self.ui.openGLWidget.selected_atom_properties.setText("select")

        self.color_with_property_enabling()

    def color_with_property_enabling(self):
        if self.ui.openGLWidget.main_model.nAtoms() > 0:
            atom = self.ui.openGLWidget.main_model.atoms[0]
            atom_prop_type = QStandardItemModel()
            for key in atom.properties:
                atom_prop_type.appendRow(QStandardItem(str(key)))
            self.ui.PropertyForColorOfAtoms.setModel(atom_prop_type)

    def color_atoms_with_property(self):
        if self.ui.ColorAtomsWithProperty.isChecked():
            prop = self.ui.PropertyForColorOfAtoms.currentText()
            if len(prop) > 0:
                self.ui.openGLWidget.color_atoms_with_property(prop)
            else:
                self.ui.openGLWidget.color_atoms_with_charge()
        else:
            self.ui.openGLWidget.color_atoms_with_charge()
        self.ui.openGLWidget.update()

    def model_rotation(self):
        if self.ui.openGLWidget.main_model.nAtoms() == 0:
            return
        angle = self.ui.FormModifyRotationAngle.value()
        model = self.ui.openGLWidget.main_model
        if self.ui.FormModifyRotationCenter.isChecked():
            center = model.get_center_of_mass()
            model.move(center[0], center[1], center[2])
        if self.ui.FormModifyRotationX.isChecked():
            model.rotate_x(angle)
        if self.ui.FormModifyRotationY.isChecked():
            model.rotate_y(angle)
        if self.ui.FormModifyRotationZ.isChecked():
            model.rotate_z(angle)
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_x(self):
        if self.ui.openGLWidget.main_model.nAtoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_x()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_y(self):
        if self.ui.openGLWidget.main_model.nAtoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_y()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_z(self):
        if self.ui.openGLWidget.main_model.nAtoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_z()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def plot_model(self, value):
        self.active_model = value
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        view_atoms = self.ui.FormSettingsViewCheckShowAtoms.isChecked()
        view_atom_numbers = self.ui.FormSettingsViewCheckShowAtomNumber.isChecked()
        view_box = self.ui.FormSettingsViewCheckShowBox.isChecked()
        view_bonds = self.ui.FormSettingsViewCheckShowBonds.isChecked()
        bond_width = 0.005 * self.ui.FormSettingsViewSpinBondWidth.value()
        bondscolor = self.get_color_from_setting(self.state_Color_Of_Bonds)
        color_of_bonds_by_atoms = self.ui.FormSettingsViewRadioColorBondsManual.isChecked()
        axescolor = self.get_color_from_setting(self.state_Color_Of_Axes)
        view_axes = self.ui.FormSettingsViewCheckShowAxes.isChecked()
        boxcolor = self.get_color_from_setting(self.state_Color_Of_Box)
        atomscolor = self.colors_of_atoms()
        contour_width = (self.ui.FormSettingsViewSpinContourWidth.value()) / 1000.0
        self.ui.openGLWidget.set_atomic_structure(self.models[self.active_model], atomscolor, view_atoms,
                                                  view_atom_numbers, view_box, boxcolor, view_bonds, bondscolor,
                                                  bond_width, color_of_bonds_by_atoms,
                                                  view_axes, axescolor, contour_width)
        self.prepare_form_actions_combo_pdos_species()
        self.prepare_form_actions_combo_pdos_indexes()

        self.color_with_property_enabling()

    def plot_surface(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.ui.openGLWidget.is_view_surface = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.volumeric_data.min, self.volumeric_data.max
        if self.ui.FormActionsPostCheckSurface.isChecked():
            data = []
            for i in range(0, self.ui.IsosurfaceColorsTable.rowCount()):
                value = float(self.ui.IsosurfaceColorsTable.item(i, 0).text())
                verts, faces, normals = self.volumeric_data.isosurface(value)
                transp = float(self.ui.IsosurfaceColorsTable.cellWidget(i, 1).text())
                if self.is_scaled_colors_for_surface:
                    color = self.get_color(cmap, minv, maxv, value, color_scale)
                else:
                    if __name__ == '__main__':
                        color = self.ui.IsosurfaceColorsTable.item(i, 0).background().color().getRgbF()
                color = (color[0], color[1], color[2], transp)
                data.append([verts, faces, color, normals])
            self.ui.openGLWidget.add_surface(data)
        else:
            self.ui.openGLWidget.update()

    def plot_contours_isovalues(self, n_contours, scale="Log"):
        min_v, max_v = self.volumeric_data.min, self.volumeric_data.max
        isovalues = []
        if min_v == max_v:
            return isovalues
        if scale == "Linear":
            isovalues = np.linspace(min_v, max_v, n_contours + 2)
        if scale == "Log":
            zero = 1e-8
            if min_v < zero:
                min_v = zero
            isovalueslog = np.linspace(math.log10(min_v), math.log10(max_v), n_contours + 2)
            isovalues = []
            for i in range(1, len(isovalueslog) - 1):
                item = isovalueslog[i]
                isovalues.append(math.exp(math.log(10) * item))
        return isovalues

    def plot_contour(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.volumeric_data.Nx is None:
            return
        self.ui.openGLWidget.is_view_contour = False
        self.ui.openGLWidget.is_view_contour_fill = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.volumeric_data.min, self.volumeric_data.max
        params = []
        params_colored_plane = []

        if maxv == minv:
            return

        planes = []
        if self.ui.FormActionsPostCheckContourXY.isChecked():
            planes.append("xy")
        if self.ui.FormActionsPostCheckContourXZ.isChecked():
            planes.append("xz")
        if self.ui.FormActionsPostCheckContourYZ.isChecked():
            planes.append("yz")

        for plane in planes:
            self.make_plane(cmap, color_scale, maxv, minv, params, params_colored_plane, plane)

        if self.ui.FormActionsPostRadioContour.isChecked() or \
                self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.ui.openGLWidget.add_contour(params)

        if self.ui.FormActionsPostRadioColorPlane.isChecked() or \
                self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.ui.openGLWidget.add_colored_plane(params_colored_plane)

    def make_plane(self, cmap, color_scale, maxv, minv, params, params_colored_plane, plane):
        n_contours = 0
        myslice = 0
        if plane == "xy":
            n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursXY.text())
            myslice = int(self.ui.FormActionsPostSliderContourXY.value())
        if plane == "xz":
            n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursXZ.text())
            myslice = int(self.ui.FormActionsPostSliderContourXZ.value())
        if plane == "yz":
            n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursYZ.text())
            myslice = int(self.ui.FormActionsPostSliderContourYZ.value())
        isovalues = self.plot_contours_isovalues(n_contours, color_scale)
        if self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            colors = self.get_colors_list(minv, maxv, isovalues, cmap, 'black')
        else:
            colors = self.get_colors_list(minv, maxv, isovalues, cmap, color_scale)
        if self.ui.FormSettingsContourColorFixed.isChecked():
            color = self.get_color_from_setting(self.state_Color_Of_Contour)
            for i in range(0, len(colors)):
                colors[i] = color
        if self.ui.FormActionsPostRadioContour.isChecked() or \
                self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            conts = self.volumeric_data.contours(isovalues, plane, myslice)
            params.append([isovalues, conts, colors])
        if self.ui.FormActionsPostRadioColorPlane.isChecked() or \
                self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            points = self.volumeric_data.plane(plane, myslice)
            colors = self.get_color_of_plane(minv, maxv, points, cmap, color_scale)
            normal = [0, 0, 1]
            if plane == "xz":
                normal = [0, -1, 0]
            if plane == "yz":
                normal = [1, 0, 0]
            params_colored_plane.append([points, colors, normal])

    def prepare_form_actions_combo_pdos_indexes(self):
        model = QStandardItemModel()
        model.appendRow(QStandardItem("All"))
        model.appendRow(QStandardItem("Selected atom (3D View)"))
        model.appendRow(QStandardItem("Selected in list below"))
        self.ui.FormActionsComboPDOSIndexes.setModel(model)

    def prepare_form_actions_combo_pdos_species(self):
        model = QStandardItemModel()
        model.appendRow(QStandardItem("All"))
        model.appendRow(QStandardItem("Selected in list below"))
        self.ui.FormActionsComboPDOSspecies.setModel(model)

    def get_filter_atom(self):
        atom_index = []
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'All':
            atom_index = range(1, self.ui.openGLWidget.main_model.nAtoms() + 1)
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected atom (3D View)':
            atom_index = [self.ui.openGLWidget.main_model.selected_atom + 1]
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected in list below':
            atom_index = (self.ui.FormActionsPDOSIndexes.toPlainText()).split()
            atom_index = helpers.list_str_to_int(atom_index)
        return atom_index

    def get_filter_species(self):
        species = []
        if self.ui.FormActionsComboPDOSspecies.currentText() == 'All':
            mendeley = TPeriodTable()
            atoms_list = mendeley.get_all_letters()
            types_of_atoms = self.ui.openGLWidget.main_model.types_of_atoms()
            for i in range(0, len(types_of_atoms)):
                species.append(str(atoms_list[types_of_atoms[i][0]]))
        if self.ui.FormActionsComboPDOSspecies.currentText() == 'Selected in list below':
            species = (self.ui.FormActionsPDOSSpecieces.text()).split()
        return species

    def get_filter_z(self):
        number_z = []
        if self.ui.FormActionsComboPDOSz1.isChecked():
            number_z.append(1)
        if self.ui.FormActionsComboPDOSz2.isChecked():
            number_z.append(2)
        if self.ui.FormActionsComboPDOSz3.isChecked():
            number_z.append(3)
        if self.ui.FormActionsComboPDOSz4.isChecked():
            number_z.append(4)
        if self.ui.FormActionsComboPDOSz5.isChecked():
            number_z.append(5)
        return number_z

    def get_filter_m(self):
        number_m = []
        if self.ui.FormActionsComboPDOSMm7.isChecked():
            number_m.append(-7)
        if self.ui.FormActionsComboPDOSMm6.isChecked():
            number_m.append(-6)
        if self.ui.FormActionsComboPDOSMm5.isChecked():
            number_m.append(-5)
        if self.ui.FormActionsComboPDOSMm4.isChecked():
            number_m.append(-4)
        if self.ui.FormActionsComboPDOSMm3.isChecked():
            number_m.append(-3)
        if self.ui.FormActionsComboPDOSMm2.isChecked():
            number_m.append(-2)
        if self.ui.FormActionsComboPDOSMm1.isChecked():
            number_m.append(-1)
        if self.ui.FormActionsComboPDOSMp0.isChecked():
            number_m.append(0)
        if self.ui.FormActionsComboPDOSMp1.isChecked():
            number_m.append(1)
        if self.ui.FormActionsComboPDOSMp2.isChecked():
            number_m.append(2)
        if self.ui.FormActionsComboPDOSMp3.isChecked():
            number_m.append(3)
        if self.ui.FormActionsComboPDOSMp4.isChecked():
            number_m.append(4)
        if self.ui.FormActionsComboPDOSMp5.isChecked():
            number_m.append(5)
        if self.ui.FormActionsComboPDOSMp6.isChecked():
            number_m.append(6)
        if self.ui.FormActionsComboPDOSMp7.isChecked():
            number_m.append(7)
        return number_m

    def get_filter_l(self):
        number_l = []
        if self.ui.FormActionsComboPDOSL0.isChecked():
            number_l.append(0)
        if self.ui.FormActionsComboPDOSL1.isChecked():
            number_l.append(1)
        if self.ui.FormActionsComboPDOSL2.isChecked():
            number_l.append(2)
        if self.ui.FormActionsComboPDOSL3.isChecked():
            number_l.append(3)
        if self.ui.FormActionsComboPDOSL4.isChecked():
            number_l.append(4)
        if self.ui.FormActionsComboPDOSL5.isChecked():
            number_l.append(5)
        if self.ui.FormActionsComboPDOSL6.isChecked():
            number_l.append(6)
        if self.ui.FormActionsComboPDOSL7.isChecked():
            number_l.append(7)
        return number_l

    def get_filter_n(self):
        number_n = []
        if self.ui.FormActionsComboPDOSn1.isChecked():
            number_n.append(1)
        if self.ui.FormActionsComboPDOSn2.isChecked():
            number_n.append(2)
        if self.ui.FormActionsComboPDOSn3.isChecked():
            number_n.append(3)
        if self.ui.FormActionsComboPDOSn4.isChecked():
            number_n.append(4)
        if self.ui.FormActionsComboPDOSn5.isChecked():
            number_n.append(5)
        if self.ui.FormActionsComboPDOSn6.isChecked():
            number_n.append(6)
        if self.ui.FormActionsComboPDOSn7.isChecked():
            number_n.append(7)
        if self.ui.FormActionsComboPDOSn8.isChecked():
            number_n.append(8)
        return number_n

    def plot_bonds_histogram(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        c1, c2 = self.fill_bonds_charges()
        bonds = self.ui.openGLWidget.main_model.find_bonds_exact()

        self.ui.PyqtGraphWidget.clear()
        b = []
        for bond in bonds:
            if ((c1 == 0) or (c2 == 0)) or ((c1 == bond[0]) and (c2 == bond[1])) or (
                    (c1 == bond[1]) and (c2 == bond[2])):
                b.append(bond[2])

        num_bins = self.ui.FormActionsPostPlotBondsHistogramN.value()
        x_label = "Bond lenght"
        y_label = "Number of bonds"
        self.ui.PyqtGraphWidget.add_histogram(b, num_bins, (0, 0, 255, 90), x_label, y_label)

    def plot_pdos(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        file = self.ui.FormActionsLinePDOSfile.text()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        if os.path.exists(file):
            atom_index = self.get_filter_atom()
            species = self.get_filter_species()
            number_n = self.get_filter_n()
            number_l = self.get_filter_l()
            number_m = self.get_filter_m()
            number_z = self.get_filter_z()
            pdos, energy = TSIESTA.calc_pdos(file, atom_index, species, number_l, number_m, number_n, number_z)
            e_fermi = TSIESTA.FermiEnergy(self.filename)
            energy -= e_fermi
            labels = [None]

            ys = [pdos[0]]
            sign = 1
            if self.ui.FormActionsCheckPDOS_2.isChecked():
                sign = -1
            if (len(pdos) > 1) and self.ui.FormActionsCheckPDOS.isChecked():
                ys.append(sign * pdos[1])
                labels = ["spin_up", "spin_down"]

            self.ui.PyqtGraphWidget.clear()

            title = "PDOS"
            x_title = "Energy, eV"
            y_title = "PDOS, states/eV"
            self.ui.PyqtGraphWidget.plot([energy], ys, labels, title, x_title, y_title, True)

            if self.ui.FormActionsCheckBANDSfermyShow_2.isChecked():
                self.ui.PyqtGraphWidget.add_line(0, 90, 2, Qt.DashLine)
            self.ui.PyqtGraphWidget.add_line(0, 0, 2, Qt.SolidLine)

            if len(pdos) > 1:
                self.PDOSdata.append([energy, pdos[0], pdos[1]])
            else:
                self.PDOSdata.append([energy, pdos[0], np.zeros((len(pdos[0])))])

            title = self.ui.FormActionsEditPDOSLabel.text()
            if len(title) == 0:
                title = str(self.ui.FormActionsComboPDOSIndexes.currentText()) + ";  " + str(
                    self.ui.FormActionsComboPDOSspecies.currentText())

            self.ui.FormActionsListPDOS.addItems([str(len(self.PDOSdata)) + ": " + title])
            self.ui.FormActionsButtonPlotPDOSselected.setEnabled(True)

    def plot_selected_pdos(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)

        selected = self.ui.FormActionsListPDOS.selectedItems()
        x = []
        y = []
        labels = []
        for item in selected:
            ind = int(item.text().split(':')[0]) - 1

            energy, spin_up, spin_down = self.PDOSdata[ind][0], self.PDOSdata[ind][1], self.PDOSdata[ind][2]

            if self.ui.FormActionsCheckPDOS_2.isChecked():
                spin_down *= -1

            x.append(energy)
            y.append(spin_up)
            labels.append(item.text() + "_up")

            if self.ui.FormActionsCheckPDOS.isChecked():
                x.append(energy)
                y.append(spin_down)
                labels.append(item.text() + "_down")

        title = "PDOS"
        x_title = "Energy, eV"
        y_title = "PDOS, states/eV"
        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.plot(x, y, labels, title, x_title, y_title, True)

        if self.ui.FormActionsCheckBANDSfermyShow_2.isChecked():
            self.ui.PyqtGraphWidget.add_line(0, 90, 2, Qt.DashLine)
        self.ui.PyqtGraphWidget.add_line(0, 0, 2, Qt.SolidLine)

    @staticmethod
    def list_of_selected_items_in_combo(atom_index, combo):
        model = combo.model()
        maxi = combo.count()
        for i in range(0, maxi):
            if model.itemFromIndex(model.index(i, 0)).checkState() == Qt.Checked:
                atom_index.append(int(model.itemFromIndex(model.index(i, 0)).text()))

    def parse_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        if os.path.exists(file):
            f = open(file)
            e_fermi = float(f.readline())
            str1 = f.readline().split()
            str1 = helpers.list_str_to_float(str1)
            kmin, kmax = float(str1[0]), float(str1[1])
            self.ui.spin_bands_xmin.setRange(kmin, kmax)
            self.ui.spin_bands_xmin.setValue(kmin)
            self.ui.spin_bands_xmax.setRange(kmin, kmax)
            self.ui.spin_bands_xmax.setValue(kmax)

            str1 = f.readline().split()
            str1 = helpers.list_str_to_float(str1)
            emin = float(str1[0]) - e_fermi
            emax = float(str1[1]) - e_fermi
            str1 = f.readline().split()
            f.close()
            str1 = helpers.list_str_to_int(str1)
            nspins = float(str1[1])
            if nspins == 2:
                self.ui.FormActionsGrBoxBANDSspin.setEnabled(True)
            else:
                self.ui.FormActionsGrBoxBANDSspin.setEnabled(False)

            e_min_form = -2 if emin < -2 else emin
            e_max_form = 2 if emax > 2 else emax
            self.ui.spin_bands_emin.setRange(emin, emax)
            self.ui.spin_bands_emin.setValue(e_min_form)
            self.ui.spin_bands_emax.setRange(emin, emax)
            self.ui.spin_bands_emax.setValue(e_max_form)
            self.ui.plot_bands.setEnabled(True)

    def plot_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        kmin, kmax = self.ui.spin_bands_xmin.value(), self.ui.spin_bands_xmax.value()
        emin, emax = self.ui.spin_bands_emin.value(), self.ui.spin_bands_emax.value()
        is_check_bands_spin = self.ui.FormActionsCheckBANDSspinUp.isChecked()
        if os.path.exists(file):
            bands, emaxf, eminf, homo, kmesh, lumo, xticklabels, xticks = read_siesta_bands(file, is_check_bands_spin,
                                                                                            kmax, kmin)
            self.ui.PyqtGraphWidget.clear()
            delta = 0.05 * (kmax - kmin)
            self.ui.PyqtGraphWidget.set_limits(kmin - delta, kmax + delta, emin, emax)
            title = "Bands"
            x_title = "k"
            y_title = "Energy, eV"
            self.ui.PyqtGraphWidget.plot([kmesh], bands, [None], title, x_title, y_title, False)
            major_tick = []
            for index in range(len(xticks)):
                self.ui.PyqtGraphWidget.add_line(xticks[index], 90, 2, Qt.DashLine)
                major_tick.append((xticks[index], xticklabels[index]))

            self.ui.PyqtGraphWidget.set_xticks([major_tick])
            if self.ui.FormActionsCheckBANDSfermyShow.isChecked():
                self.ui.PyqtGraphWidget.add_line(0, 0, 2, Qt.SolidLine)

            gap, gap_ind = gaps(bands, emaxf, eminf, homo, lumo)

            self.ui.FormActionsLabelBANDSgap.setText(
                "Band gap = " + str(round(gap, 3)) + "  " + "Indirect gap = " + str(round(gap_ind, 3)))

    def plot_dos(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)

        is_fermi_level_show = self.ui.FormActionsCheckBANDSfermyShow_3.isChecked()
        is_invert_spin_down = self.ui.FormActionsCheckDOS_2.isChecked()
        is_spin_down_needed = self.ui.FormActionsCheckDOS.isChecked()

        path_efermy_list = []
        for index in range(self.ui.FormActionsTabeDOSProperty.rowCount()):
            path_efermy_list.append([self.ui.FormActionsTabeDOSProperty.item(index, 0).toolTip(),
                                    float(self.ui.FormActionsTabeDOSProperty.item(index, 1).text())])

        x = []
        y = []
        labels = []

        for index in range(len(path_efermy_list)):
            path = path_efermy_list[index][0]

            if os.path.exists(path):
                if path.endswith("DOSCAR"):
                    spin_up, spin_down, energy = vasp_dos(path)
                else:
                    spin_up, spin_down, energy = dos_from_file(path)

                energy -= path_efermy_list[index][1]
                if is_invert_spin_down:
                    spin_down *= -1
                x.append(energy)
                y.append(spin_up)
                labels.append("spin_up")
                if is_spin_down_needed:
                    x.append(energy)
                    y.append(spin_down)
                    labels.append("spin_down")

        x_title = "Energy, eV"
        y_title = "DOS, states/eV"
        title = "DOS"

        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        self.ui.PyqtGraphWidget.plot(x, y, labels, title, x_title, y_title)

        if is_fermi_level_show:
            self.ui.PyqtGraphWidget.add_line(0, 90, 2, Qt.DashLine)
        self.ui.PyqtGraphWidget.add_line(0, 0, 2, Qt.SolidLine)

    def plot_voronoi(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.ui.openGLWidget.isActive():
            r = self.state_Color_Of_Voronoi.split()[0]
            g = self.state_Color_Of_Voronoi.split()[1]
            b = self.state_Color_Of_Voronoi.split()[2]
            color = [float(r) / 255, float(g) / 255, float(b) / 255]
            maxDist = float(self.ui.FormActionsPostTextVoronoiMaxDist.value())
            atom_index, volume = self.ui.openGLWidget.add_voronoi(color, maxDist)
            if atom_index >= 0:
                self.ui.FormActionsPostLabelVoronoiAtom.setText("Atom: " + str(atom_index))
                self.ui.FormActionsPostLabelVoronoiVolume.setText("volume: " + str(volume))
            else:
                self.ui.FormActionsPostLabelVoronoiAtom.setText("Atom: ")
                self.ui.FormActionsPostLabelVoronoiVolume.setText("volume: ")

    def clear_dos(self):
        self.ui.FormActionsTabeDOSProperty.setRowCount(0)
        self.ui.FormActionsTabeDOSProperty.update()

    def plot_volume_param_energy(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        items = []
        prec = 3
        method = self.ui.FormActionsPostComboCellParam.currentText()
        xi = self.ui.FormActionsPostComboCellParamX.currentIndex()
        LabelX = self.ui.FormActionsPostComboCellParamX.currentText()
        yi = 1

        for index in range(self.ui.FormActionsPostTableCellParam.rowCount()):
            x = self.ui.FormActionsPostTableCellParam.item(index, xi).text()
            y = self.ui.FormActionsPostTableCellParam.item(index, yi).text()
            items.append([float(x), float(y)])

        if len(items):
            items = sorted(items, key=itemgetter(0))

            xs = []
            ys = []

            for i in range(0, len(items)):
                xs.append(items[i][0])
                ys.append(items[i][1])

            if (method == "Murnaghan") and (len(items) > 4):
                aprox, xs2, ys2 = Calculator.approx_murnaghan(items)
                image_path = str(Path(__file__).parent / 'images' / 'murnaghan.png')  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)=" + str(round(float(aprox[0]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0=" + str(round(float(aprox[1]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'=" + str(round(float(aprox[2]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0=" + str(round(float(aprox[3]), prec)))
                self.plot_cell_approx(image_path)
                self.plot_curv_and_points(LabelX, xs, ys, xs2, ys2)

            if (method == "BirchMurnaghan") and (len(items) > 4):
                aprox, xs2, ys2 = Calculator.approx_birch_murnaghan(items)
                image_path = str(Path(__file__).parent / 'images' / 'murnaghanbirch.png')  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)=" + str(round(float(aprox[0]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0=" + str(round(float(aprox[1]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'=" + str(round(float(aprox[2]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0=" + str(round(float(aprox[3]), prec)))
                self.plot_cell_approx(image_path)
                self.plot_curv_and_points(LabelX, xs, ys, xs2, ys2)

            if (method == "Parabola") and (len(items) > 2):
                aprox, xs2, ys2 = Calculator.approx_parabola(items)
                image_path = str(Path(__file__).parent / 'images' / 'parabola.png')  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("a=" + str(round(float(aprox[2]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("b=" + str(round(float(aprox[1]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("c=" + str(round(float(aprox[0]), prec)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText(
                    "x0=" + str(round(-float(aprox[1]) / float(2 * aprox[2]), prec)))
                self.plot_cell_approx(image_path)
                self.plot_curv_and_points(LabelX, xs, ys, xs2, ys2)

    def plot_curv_and_points(self, x_title, xs, ys, xs2, ys2):
        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        title = "Cell param"
        y_title = "Energy"
        self.ui.PyqtGraphWidget.plot([xs2], [ys2], [None], title, x_title, y_title)
        self.ui.PyqtGraphWidget.add_scatter(xs, ys)

    def plot_cell_approx(self, image_path):
        image_profile = QImage(image_path)
        image_profile = image_profile.scaled(320, 54, aspectRatioMode=Qt.KeepAspectRatio,
                                             transformMode=Qt.SmoothTransformation)
        self.ui.FormActionsPostLabelCellParamFig.setPixmap(QPixmap.fromImage(image_profile))

    def save_image_to_file(self, name=""):
        if len(self.models) == 0:
            return
        try:
            if not name:
                format_str = "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)"
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, format_str,
                                                   options=QFileDialog.DontUseNativeDialog)
            fname = name[0]
            ext = ""
            if name[1] == "PNG files (*.png)":
                ext = "png"
            if name[1] == "JPG files (*.jpg)":
                ext = "jpg"
            if name[1] == "BMP files (*.bmp)":
                ext = "bmp"
            if not fname.endswith(ext):
                fname += "." + ext

            if fname:
                new_window = Image3Dexporter(5 * self.ui.openGLWidget.width(), 5 * self.ui.openGLWidget.height(), 5)
                new_window.ui.openGLWidget.copy_state(self.ui.openGLWidget)

                new_window.ui.openGLWidget.image3D_to_file(fname)
                new_window.destroy()
                self.work_dir = os.path.dirname(fname)
                self.save_active_folder()
        except Exception as excep:
            self.show_error(excep)

    def rotate_model_xp(self):
        self.ui.openGLWidget.rotX += self.rotation_step
        self.ui.openGLWidget.update()

    def rotate_model_xm(self):
        self.ui.openGLWidget.rotX -= self.rotation_step
        self.ui.openGLWidget.update()

    def rotate_model_yp(self):
        self.ui.openGLWidget.rotY += self.rotation_step
        self.ui.openGLWidget.update()

    def rotate_model_ym(self):
        self.ui.openGLWidget.rotY -= self.rotation_step
        self.ui.openGLWidget.update()

    def rotate_model_zp(self):
        self.ui.openGLWidget.rotZ += self.rotation_step
        self.ui.openGLWidget.update()

    def rotate_model_zm(self):
        self.ui.openGLWidget.rotZ -= self.rotation_step
        self.ui.openGLWidget.update()

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
        self.ui.openGLWidget.set_atoms_numbred(self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())

    def save_state_action_on_start(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsActionOnStart, self.action_on_start)

    def save_state_view_show_box(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.ui.openGLWidget.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_view_show_bonds(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.ui.openGLWidget.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

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
        self.CoordType = self.ui.FormSettingsPreferredCoordinates.currentText()

    def save_state_preferred_units(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredUnits,
                           self.ui.FormSettingsPreferredUnits.currentText())
        self.units_type = self.ui.FormSettingsPreferredUnits.currentText()

    def save_state_preferred_lattice(self):  # pragma: no cover
        self.save_property(SETTINGS_FormSettingsPreferredLattice, self.ui.FormSettingsPreferredLattice.currentText())
        self.LatticeType = self.ui.FormSettingsPreferredLattice.currentText()

    @staticmethod
    def save_property(var_property, value):  # pragma: no cover
        settings = QSettings()
        settings.setValue(var_property, value)
        settings.sync()

    def state_changed_form_settings_colors_scale(self):
        if self.ui.FormSettingsColorsScale.currentText() == "":
            self.ui.ColorRow.clear()
        else:
            self.ui.ColorRow.plot_mpl_colormap(self.ui.FormSettingsColorsScale.currentText())

    def type_of_surface(self):
        self.ui.FormActionsPostLabelSurfaceMin.setText("")
        self.ui.FormActionsPostLabelSurfaceMax.setText("")
        self.ui.FormActionsPostLabelSurfaceValue.setValue(0)
        self.ui.FormActionsPostButSurface.setEnabled(False)
        self.ui.FormActionsPostButContour.setEnabled(False)

    def twist_model(self):
        angle = math.radians(self.ui.ModifyTwistAngle.value())
        self.models[self.active_model].twist_z(angle)
        self.plot_model(self.active_model)

    def fdf_data_to_form(self):
        try:
            model = self.ui.openGLWidget.get_model()
            text = self.fdf_data.get_all_data(model, self.CoordType, self.units_type, self.LatticeType)
            print(self.CoordType, self.units_type, self.LatticeType)
            self.ui.FormActionsPreTextFDF.setText(text)
        except Exception:
            print("There are no atoms in the model")

    def fdf_data_from_form_to_file(self):  # pragma: no cover
        try:
            text = self.ui.FormActionsPreTextFDF.toPlainText()
            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "FDF files (*.fdf)",
                                                   options=QFileDialog.DontUseNativeDialog)[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_script_create(self):  # pragma: no cover
        if len(self.models) == 0:
            return
        try:
            model2 = deepcopy(self.models[self.active_model])
            text = ase.ase_raman_and_ir_script_create(model2, self.fdf_data)

            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "Python file (*.py)",
                                                   options=QFileDialog.DontUseNativeDialog)[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_parse(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)[0]
            if os.path.exists(fname):
                self.filename = fname
                self.work_dir = os.path.dirname(fname)
                raman_text, units_i, raman_inten, raman_en_ev, raman_en_cm, ir_inten, ir_en_ev, ir_en_cm = \
                    ase.ase_raman_and_ir_parse(fname)

                for i in range(0, len(raman_inten)):
                    raman_text += "{0:10.1f} {1:10.1f} {2:10.2f}\n".format(raman_en_ev[i], raman_en_cm[i],
                                                                           raman_inten[i])
                self.ui.FormRamanSpectraText.setPlainText(raman_text)

                ir_text = "meV cm^-1 Intensity " + units_i + "\n"
                for i in range(0, len(ir_inten)):
                    ir_text += "{0:10.1f} {1:10.1f} {2:10.4f}\n".format(ir_en_ev[i], ir_en_cm[i], ir_inten[i])
                self.ui.FormIrSpectraText.setPlainText(ir_text)

        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_plot(self):
        if self.ui.form_raman_radio.isChecked():
            data = self.ui.FormRamanSpectraText.toPlainText()
            y_title = "Raman"
        else:
            data = self.ui.FormIrSpectraText.toPlainText()
            y_title = "IR"

        col = 1
        x_title = "cm^-1"
        if self.ui.form_spectra_mev_radio.isChecked():
            col = 0
            x_title = "meV"

        x = []
        y = []

        rows = data.split("\n")
        for i in range(1, len(rows)):
            row = rows[i].split()
            if len(row) > 2:
                x.append(float(row[col]))
                y.append(math.log(float(row[2])))

        x_max = max(x)
        n = 1000
        x_fig = np.linspace(0, x_max, n)
        y_fig = np.zeros(n)

        sigma = self.ui.formGaussWidth.value()

        for i in range(0, len(x)):
            for j in range(0, n):
                y_fig[j] += y[i] * math.exp(-math.pow(x[i] - x_fig[j], 2) / (2 * sigma))

        title = "Spectrum"
        self.ui.PyqtGraphWidget.clear()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        self.ui.PyqtGraphWidget.plot([x_fig], [y_fig], [None], title, x_title, y_title, True)

    def d12_to_file(self):  # pragma: no cover
        if len(self.models) == 0:
            return
        try:
            text = "crystal\n"
            if self.ui.crystal_d12_1d.isChecked():
                text += "POLYMER\n"
                model1 = deepcopy(self.models[self.active_model])
                model2 = deepcopy(self.models[self.active_model])
                model2.convert_from_cart_to_direct()
                nat = model1.nAtoms()
                text += "1\n"
                text += str(model1.get_LatVect3_norm()) + "\n"
                text += str(nat) + "\n"
                for i in range(0, nat):
                    ch = model1.atoms[i].charge
                    x = str(model2.atoms[i].z)
                    y = str(model1.atoms[i].x)
                    z = str(model1.atoms[i].y)
                    text += "2" + str(ch) + "   " + x + "   " + y + "   " + z + "\n"
            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "Crystal d12 (*.d12)",
                                                   options=QFileDialog.DontUseNativeDialog)[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

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
        models = Calculator.fill_tube(rad_tube, length, n_atoms, 0.01 * rad_atom, delta, n_prompts, let, charge)

        filename = "."
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
                text = self.fdf_data.get_all_data(second_model.atoms, self.CoordType, self.units_type, self.LatticeType)
                with open(filename + str(myiter) + '.fdf', 'w') as f:
                    f.write(text)
            myiter += 1
        self.fill_models_list()

    def parse_volumeric_data(self):
        if len(self.ui.FormActionsPostList3DData.selectedItems()) > 0:
            selected = self.ui.FormActionsPostList3DData.selectedItems()[0].text()
            self.parse_volumeric_data_selected(selected)

    def parse_volumeric_data_selected(self, selected):
        if selected.endswith(".XSF"):
            self.volumeric_data = XSF()
        if selected.endswith(".cube"):
            self.volumeric_data = GaussianCube()
        if self.volumeric_data.parse(selected):
            self.fill_volumeric_data(self.volumeric_data)
        self.ui.FormActionsPostButSurfaceLoadData.setEnabled(True)
        self.clear_qtree_widget(self.ui.FormActionsPostTreeSurface2)
        self.ui.FormActionsPosEdit3DData2.setText("")
        self.clear_form_isosurface_data2_n()
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.CalculateTheVolumericDataSum.setEnabled(False)
        self.ui.VolumrricDataGrid2.setTitle("Grid")
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)

    def parse_volumeric_data2(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir,
                                                options=QFileDialog.DontUseNativeDialog)
            if len(fname) > 0:
                fname = fname[0]
                if fname.endswith(".XSF"):
                    self.volumeric_data2 = XSF()
                if fname.endswith(".cube"):
                    self.volumeric_data2 = GaussianCube()
                if self.volumeric_data2.parse(fname):
                    self.fill_volumeric_data(self.volumeric_data2, self.ui.FormActionsPostTreeSurface2)

                self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(True)
                self.ui.FormActionsPosEdit3DData2.setText(fname)
                self.clear_form_isosurface_data2_n()
                self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
                self.ui.CalculateTheVolumericDataSum.setEnabled(False)
                self.ui.ExportTheVolumericDataXSF.setEnabled(False)
                self.ui.ExportTheVolumericDataCube.setEnabled(False)
                self.ui.VolumrricDataGrid2.setTitle("Grid")
        except Exception as e:
            self.show_error(e)

    def set_xsf_z_position(self):
        value = int(self.ui.FormActionsPostSliderContourXY.value())
        self.ui.FormActionsPostLabelContourXYposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourXY.maximum()))

    def set_xsf_y_position(self):
        value = int(self.ui.FormActionsPostSliderContourXZ.value())
        self.ui.FormActionsPostLabelContourXZposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourXZ.maximum()))

    def set_xsf_x_position(self):
        value = int(self.ui.FormActionsPostSliderContourYZ.value())
        self.ui.FormActionsPostLabelContourYZposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourYZ.maximum()))

    @staticmethod
    def change_color_of_cell_prompt(table):
        i = table.selectedIndexes()[0].row()
        color = QColorDialog.getColor(initial=table.item(i, 0).background().color())
        if not color.isValid():
            return
        at_color = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        table.item(i, 0).setBackground(QColor.fromRgbF(at_color[0], at_color[1], at_color[2], 1))

    def select_isosurface_color(self):  # pragma: no cover
        table = self.ui.IsosurfaceColorsTable
        self.change_color_of_cell_prompt(table)
        self.is_scaled_colors_for_surface = False

    def select_atom_color(self):  # pragma: no cover
        table = self.ui.ColorsOfAtomsTable
        self.change_color_of_cell_prompt(table)

        text_color = ""
        atomscolor = []
        col = table.item(0, 0).background().color().getRgbF()
        atomscolor.append(col)
        text_color += str(col[0]) + " " + str(col[1]) + " " + str(col[2]) + "|"
        for i in range(0, table.rowCount()):
            col = table.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
            text_color += str(col[0]) + " " + str(col[1]) + " " + str(col[2]) + "|"

        self.save_property(SETTINGS_Color_Of_Atoms, text_color)
        if self.ui.openGLWidget.main_model.nAtoms() > 0:
            self.ui.openGLWidget.set_color_of_atoms(atomscolor)

    def select_box_color(self):  # pragma: no cover
        boxcolor = self.change_color(self.ui.ColorBox, SETTINGS_Color_Of_Box)
        self.ui.openGLWidget.set_color_of_box(boxcolor)

    def add_cp_to_list(self):
        new_cp = self.ui.FormSelectedCP.text()
        if new_cp == "...":
            return

        fl = True

        for i in range(0, self.ui.FormCPlist.count()):
            if self.ui.FormCPlist.item(i).text() == new_cp:
                fl = False
        if fl:
            QListWidgetItem(new_cp, self.ui.FormCPlist)

    def delete_cp_from_list(self):
        itemrow = self.ui.FormCPlist.currentRow()
        self.ui.FormCPlist.takeItem(itemrow)

    def create_critic2_xyz_file(self):  # pragma: no cover
        """ add code here"""
        name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, options=QFileDialog.DontUseNativeDialog)
        fname = name[0]
        if len(fname) > 0:
            model = self.models[self.active_model]
            bcp = deepcopy(model.bcp)
            bcp_selected = []
            for i in range(0, self.ui.FormCPlist.count()):
                ind = int(self.ui.FormCPlist.item(i).text())
                bcp_selected.append(model.bcp[ind])
            is_with_selected = self.ui.radio_with_cp.isChecked()
            text = critic2.create_critic2_xyz_file(bcp, bcp_selected, is_with_selected, model)
            helpers.write_text_to_file(fname, text)

    def create_cri_file(self):  # pragma: no cover
        name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, options=QFileDialog.DontUseNativeDialog)
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

        fname = name[0]
        if len(fname) > 0:
            model = self.models[self.active_model]

            cp_list = []
            if self.ui.form_critic_all_cp.isChecked():
                cp_list = range(model.bcp)
            else:
                for i in range(0, self.ui.FormCPlist.count()):
                    ind = int(self.ui.FormCPlist.item(i).text())
                    cp_list.append(ind)
            textl, lines, te, text = critic2.create_cri_file(cp_list, extra_points, is_form_bp, model, text_prop)

            helpers.write_text_to_file(fname, textl + lines)

            fname_dir = os.path.dirname(fname)
            helpers.write_text_to_file(fname_dir + "/POINTS.txt", te)
            helpers.write_text_to_file(fname_dir + "/POINTSatoms.txt", text)

    def select_voronoi_color(self):  # pragma: no cover
        voronoicolor = self.change_color(self.ui.ColorVoronoi, SETTINGS_Color_Of_Voronoi)
        self.ui.openGLWidget.set_color_of_voronoi(voronoicolor)

    def select_bond_color(self):  # pragma: no cover
        bondscolor = self.change_color(self.ui.ColorBond, SETTINGS_Color_Of_Bonds)
        self.ui.openGLWidget.set_color_of_bonds(bondscolor)

    def select_axes_color(self):  # pragma: no cover
        axescolor = self.change_color(self.ui.ColorAxes, SETTINGS_Color_Of_Axes)
        self.ui.openGLWidget.set_color_of_axes(axescolor)

    def select_contour_color(self):  # pragma: no cover
        self.change_color(self.ui.ColorContour, SETTINGS_Color_Of_Contour)
        self.plot_contour()

    def create_graphene(self):
        n = self.ui.FormActionsPreLineGraphene_n.value()
        m = self.ui.FormActionsPreLineGraphene_m.value()
        leng = self.ui.FormActionsPreLineGraphene_len.value()

        model = Graphene(n, m, leng)

        self.models.append(model)
        self.plot_model(-1)
        self.ui.openGLWidget.add_atoms()
        self.fill_gui("Graphene-model")

    def create_swnt(self):
        tube_type = 0
        n = self.ui.spin_swnt_index_n.value()
        m = self.ui.spin_swnt_index_m.value()
        if self.ui.FormActionsPreRadioSWNTcap.isChecked() or self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            nm = self.ui.FormActionsPreComboSWNTind.currentText().split(",")
            n = int(nm[0].split("(")[1])
            m = int(nm[1].split(")")[0])
        if self.ui.FormActionsPreRadioSWNTcap.isChecked():
            tube_type = 1
        if self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            tube_type = 2
        if self.ui.createSWGNTradio.isChecked():
            tube_type = 3
        if self.ui.FormActionsPreRadioSWNTuselen.isChecked():
            leng = float(self.ui.spin_swnt_len.text())
            cells = 1
        else:
            leng = 0
            cells = int(self.ui.spin_swnt_cells.text())

        model = None
        if tube_type == 0:
            model = SWNT(n, m, leng, cells)

        if tube_type == 1 or tube_type == 2:
            dist1 = float(self.ui.FormCreateSpinFirstCapDist.value())
            angle1 = float(self.ui.FormCreateSpinFirstCapAngle.value())
            dist2 = float(self.ui.FormCreateSpinSecondCapDist.value())
            angle2 = float(self.ui.FormCreateSpinSecondCapAngle.value())
            model = CapedSWNT(n, m, leng, cells, tube_type, dist1, angle1, dist2, angle2)

        if tube_type == 3:
            model = SWGNT(n, m, leng, cells)

        self.models.append(model)
        self.plot_model(-1)
        self.ui.openGLWidget.add_atoms()
        self.fill_gui("SWNT-model")

    def create_bi_el_nt(self):  # pragma: no cover
        """ to do """
        n = self.ui.FormBiElementN.value()
        if self.ui.FormBiElementRadioArm.isChecked():
            m = n
        else:
            m = 0
        leng = self.ui.FormBiElementLen.value()
        t = self.ui.FormNanotypeTypeSelector.currentText()

        model = BiNT(n, m, leng, t)

        self.models.append(model)
        self.plot_model(-1)
        self.ui.openGLWidget.add_atoms()
        self.fill_gui("Bi element NT-model")

    def swnt_type1_selected(self):
        self.ui.spin_swnt_index_n.setEnabled(True)
        self.ui.spin_swnt_index_m.setEnabled(True)
        self.ui.FormActionsPreComboSWNTind.setEnabled(False)
        self.ui.FormCreateGroupFirstCap.setEnabled(False)
        self.ui.FormCreateGroupSecondCap.setEnabled(False)

    def swnt_type2_selected(self):
        self.ui.spin_swnt_index_n.setEnabled(False)
        self.ui.spin_swnt_index_m.setEnabled(False)
        self.ui.FormActionsPreComboSWNTind.setEnabled(True)
        self.ui.FormCreateGroupFirstCap.setEnabled(True)
        if self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            self.ui.FormCreateGroupSecondCap.setEnabled(True)
        else:
            self.ui.FormCreateGroupSecondCap.setEnabled(False)

    def change_color(self, colorUi, var_property):   # pragma: no cover
        color = QColorDialog.getColor()
        colorUi.setStyleSheet(
            "background-color:rgb(" + str(color.getRgb()[0]) + "," + str(color.getRgb()[1]) + "," + str(
                color.getRgb()[2]) + ")")
        newcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        self.save_property(var_property,
                           str(color.getRgb()[0]) + " " + str(color.getRgb()[1]) + " " + str(color.getRgb()[2]))
        return newcolor

    def volumeric_data_load(self):   # pragma: no cover
        selected_items = self.ui.FormActionsPostTreeSurface.selectedItems()
        self.volumeric_data_load_selected(selected_items)

    def volumeric_data_load_selected(self, selected_items):
        if selected_items:
            if not (selected_items[0].parent() is None):
                child_node = selected_items[0].text(0)
                self.get_atomic_model_and_fdf(self.volumeric_data.filename)
                self.volumeric_data.load_data(child_node)

                self.plot_last_model()

                self.volumeric_data_max_min_to_form()
                self.ui.FormActionsPostButSurfaceAdd.setEnabled(True)
                self.ui.FormActionsPostButContour.setEnabled(True)
                self.ui.FormActionsPostButSurfaceParse2.setEnabled(True)

                self.ui.FormActionsPostSliderContourXY.setMaximum(self.volumeric_data.Nz)
                self.ui.FormActionsPostSliderContourXZ.setMaximum(self.volumeric_data.Ny)
                self.ui.FormActionsPostSliderContourYZ.setMaximum(self.volumeric_data.Nx)

                self.ui.FormVolDataExportX1.setMaximum(self.volumeric_data.Nx)
                self.ui.FormVolDataExportX2.setMaximum(self.volumeric_data.Nx)
                self.ui.FormVolDataExportX2.setValue(self.volumeric_data.Nx)
                self.ui.FormVolDataExportY1.setMaximum(self.volumeric_data.Ny)
                self.ui.FormVolDataExportY2.setMaximum(self.volumeric_data.Ny)
                self.ui.FormVolDataExportY2.setValue(self.volumeric_data.Ny)
                self.ui.FormVolDataExportZ1.setMaximum(self.volumeric_data.Nz)
                self.ui.FormVolDataExportZ2.setMaximum(self.volumeric_data.Nz)
                self.ui.FormVolDataExportZ2.setValue(self.volumeric_data.Nz)

    def volumeric_data_load2(self):   # pragma: no cover
        selected_items = self.ui.FormActionsPostTreeSurface2.selectedItems()
        if selected_items:
            if selected_items[0].parent() is not None:
                child_node = selected_items[0].text(0)
                self.volumeric_data2.load_data(child_node)

                self.ui.FormActionsPostLabelSurfaceNx.setText("Nx: " + str(self.volumeric_data2.Nx))
                self.ui.FormActionsPostLabelSurfaceNy.setText("Ny: " + str(self.volumeric_data2.Ny))
                self.ui.FormActionsPostLabelSurfaceNz.setText("Nz: " + str(self.volumeric_data2.Nz))

                if (self.volumeric_data2.Nx == self.volumeric_data.Nx) and (
                        self.volumeric_data2.Ny == self.volumeric_data.Ny) and (
                        self.volumeric_data2.Nz == self.volumeric_data.Nz):
                    self.ui.VolumrricDataGridCalculate.setEnabled(True)
                    self.ui.CalculateTheVolumericDataDifference.setEnabled(True)
                    self.ui.CalculateTheVolumericDataSum.setEnabled(True)
                    self.ui.VolumrricDataGridExport.setEnabled(True)
                    self.ui.ExportTheVolumericDataXSF.setEnabled(True)
                    self.ui.ExportTheVolumericDataCube.setEnabled(True)
                    self.ui.VolumrricDataGrid2.setTitle("Grid: correct")
                else:
                    self.ui.VolumrricDataGrid2.setTitle("Grid: incorrect")

    def volumeric_data_difference(self):   # pragma: no cover
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.CalculateTheVolumericDataSum.setEnabled(False)
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)
        self.volumeric_data.difference(self.volumeric_data2)
        self.volumeric_data_max_min_to_form()

    def volumeric_data_sum(self):  # pragma: no cover
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.CalculateTheVolumericDataSum.setEnabled(False)
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)
        self.volumeric_data.difference(self.volumeric_data2, mult=-1)
        self.volumeric_data_max_min_to_form()

    def volumeric_data_max_min_to_form(self):  # pragma: no cover
        minv, maxv = self.volumeric_data.min, self.volumeric_data.max
        self.ui.FormActionsPostLabelSurfaceMax.setText("Max: " + str(round(maxv, 5)))
        self.ui.FormActionsPostLabelSurfaceMin.setText("Min: " + str(round(minv, 5)))
        self.ui.FormActionsPostLabelSurfaceValue.setRange(minv, maxv)
        self.ui.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))


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
SETTINGS_FormSettingsActionOnStart = 'action/OnStart'

SETTINGS_FormSettingsPreferredCoordinates = 'model/FormSettingsPreferredCoordinates'
SETTINGS_FormSettingsPreferredUnits = 'model/FormSettingsPreferred/units'
SETTINGS_FormSettingsPreferredLattice = 'model/FormSettingsPreferredLattice'

SETTINGS_Color_Of_Atoms = 'colors/atoms'
SETTINGS_Color_Of_Bonds = 'colors/bonds'
SETTINGS_Color_Of_Box = 'colors/box'
SETTINGS_Color_Of_Voronoi = 'colors/voronoi'
SETTINGS_Color_Of_Axes = 'colors/axes'
SETTINGS_Color_Of_Contour = 'colors/contour'
SETTINGS_perspective_angle = 'perspectiveangle'
