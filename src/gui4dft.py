# -*- coding: utf-8 -*-
import os
try:
    if os.environ["XDG_SESSION_TYPE"] == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
except Exception as e:
    """  """
import math
import sys
from pathlib import Path
from copy import deepcopy
from operator import itemgetter
import matplotlib.pyplot as plt
#from pyqt_graph_widget.pygrwidget import PyqtGraphWidget
#import pyqtgraph as pg  # pip install pyqtgraph
import numpy as np
from utils import helpers
from models.atomic_model import TAtomicModel
from utils.calculators import Calculators as Calculator
from utils.calculators import gaps
from utils.critic2 import check_cro_file, model_to_critic_xyz_file
from models.models import TCapedSWNT
from models.models import TBiNT
from utils.fdfdata import TFDFFile
from models.models import TGraphene
from utils.periodic_table import TPeriodTable
from utils.siesta import TSIESTA
from models.models import TSWNT
from utils.vasp import fermi_energy_from_doscar, vasp_dos, model_to_vasp_poscar
from utils.importer import Importer
from utils.electronic_prop_reader import read_siesta_bands, dos_from_file
from PySide2.QtCore import QCoreApplication, QLocale, QSettings, Qt, QSize
import PySide2.QtCore as QtCore
#QtCore.QVariant = "QVariant"
from PySide2.QtGui import QColor, QIcon, QImage, QKeySequence, QPixmap, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QListWidgetItem, QAction, QApplication, QDialog, QFileDialog, QMessageBox, QColorDialog
from PySide2.QtWidgets import QDoubleSpinBox, QMainWindow, QShortcut, QTableWidgetItem, QTreeWidgetItem
from PySide2.QtWidgets import QTreeWidgetItemIterator
from guiopengl import GuiOpenGL
from atomidentifier import AtomsIdentifier
from image3dexporter import Image3Dexporter
from TInterface import TGaussianCube
from TInterface import TVolumericData
from TInterface import TXSF
from ui.about import Ui_DialogAbout as Ui_about
from ui.form import Ui_MainWindow as Ui_form

from utils import ase, critic2

sys.path.append('.')

is_with_figure = True


class mainWindow(QMainWindow):

    def __init__(self, *args):
        super(mainWindow, self).__init__(*args)
        self.ui = Ui_form()
        self.ui.setupUi(self)

        self.models = []
        selected_atom_info = [self.ui.FormActionsPreComboAtomsList, self.ui.FormActionsPreSpinAtomsCoordX,
                              self.ui.FormActionsPreSpinAtomsCoordY, self.ui.FormActionsPreSpinAtomsCoordZ,
                              self.ui.AtomPropertiesText]
        self.MainForm = GuiOpenGL(self.ui.openGLWidget)
        self.MainForm.set_form_elements(self.ui.FormSettingsViewCheckAtomSelection, selected_atom_info, 1)
        self.FDFData = TFDFFile()
        self.VolumericData = TVolumericData()
        self.VolumericData2 = TVolumericData()  # only for volumeric data difference
        self.PDOSdata = []
        self.filename = ""
        self.colors_cash = {}
        self.table_header_stylesheet = "::section{Background-color:rgb(190,190,190)}"
        self.is_scaled_colors_for_surface = True
        self.rotation_step = 1

        self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut.activated.connect(self.atom_delete)
        self.active_model = -1

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
        self.ui.FormActionsPreButSWNTGenerate.clicked.connect(self.create_swnt)
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
        self.ui.FormActionsButtonPlotBANDS.clicked.connect(self.plot_bands)
        self.ui.FormActionsButtonParseBANDS.clicked.connect(self.parse_bands)
        self.ui.FormActionsButtonPlotPDOSselected.clicked.connect(self.plot_selected_pdos)
        self.ui.FormModifyCellButton.clicked.connect(self.edit_cell)
        self.ui.FormActionsPostButGetBonds.clicked.connect(self.get_bonds)
        self.ui.PropertyAtomAtomDistanceGet.clicked.connect(self.get_bond)
        self.ui.FormStylesFor2DGraph.clicked.connect(self.set_2d_graph_styles)

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
        swnt_ind_type.appendRow(QStandardItem("(10,0)"))
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

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" /'Open.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'Open.png')), 'Open', self)
        else:
            openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.menu_open)
        self.ui.toolBar.addAction(openAction)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'Close.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'Close.png')), 'Export', self)
        else:
            openAction = QAction('Export', self)
        openAction.setShortcut('Ctrl+E')
        openAction.triggered.connect(self.menu_export)
        self.ui.toolBar.addAction(openAction)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'Save3D.png'):
            save_image_to_file_action = QAction(QIcon(str(Path(__file__).parent / "images" / 'Save3D.png')), 'SaveFigure3D', self)
        else:
            save_image_to_file_action = QAction('SaveFigure3D', self)
        save_image_to_file_action.triggered.connect(self.save_image_to_file)
        self.ui.toolBar.addAction(save_image_to_file_action)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoX.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoX.png')), 'RotateX-', self)
        else:
            openAction = QAction('RotateX-', self)
        openAction.triggered.connect(self.rotate_model_xm)
        self.ui.toolBar.addAction(openAction)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoX.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoX.png')), 'RotateX+', self)
        else:
            openAction = QAction('RotateX+', self)
        openAction.triggered.connect(self.rotate_model_xp)
        self.ui.toolBar.addAction(openAction)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'UndoY.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoY.png')), 'RotateY-', self)
        else:
            openAction = QAction('RotateY-', self)
        openAction.triggered.connect(self.rotate_model_ym)
        self.ui.toolBar.addAction(openAction)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoY.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoY.png')), 'RotateY+', self)
        else:
            openAction = QAction('RotateY+', self)
        openAction.triggered.connect(self.rotate_model_yp)
        self.ui.toolBar.addAction(openAction)
        self.ui.toolBar.addSeparator()

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" /'UndoZ.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'UndoZ.png')), 'RotateZ-', self)
        else:
            openAction = QAction('RotateZ-', self)
        openAction.triggered.connect(self.rotate_model_zm)
        self.ui.toolBar.addAction(openAction)

        if is_with_figure and os.path.exists(Path(__file__).parent / "images" / 'RedoZ.png'):
            openAction = QAction(QIcon(str(Path(__file__).parent / "images" / 'RedoZ.png')), 'RotateZ+', self)
        else:
            openAction = QAction('RotateZ+', self)
        openAction.triggered.connect(self.rotate_model_zp)
        self.ui.toolBar.addAction(openAction)
        self.ui.toolBar.addSeparator()

    def activate_fragment_selection_mode(self):
        if self.ui.ActivateFragmentSelectionModeCheckBox.isChecked():
            self.MainForm.setSelectedFragmentMode(self.ui.AtomsInSelectedFragment,
                                                  self.ui.ActivateFragmentSelectionTransp.value())
            self.ui.changeFragment1StatusByX.setEnabled(True)
            self.ui.changeFragment1StatusByY.setEnabled(True)
            self.ui.changeFragment1StatusByZ.setEnabled(True)
            self.ui.fragment1Clear.setEnabled(True)
        else:
            self.MainForm.setSelectedFragmentMode(None, self.ui.ActivateFragmentSelectionTransp.value())
            self.ui.changeFragment1StatusByX.setEnabled(False)
            self.ui.changeFragment1StatusByY.setEnabled(False)
            self.ui.changeFragment1StatusByZ.setEnabled(False)
            self.ui.fragment1Clear.setEnabled(False)

    def add_cell_param(self):
        """ add cell params"""
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
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
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
            self.work_dir = os.path.dirname(fname)

            if os.path.exists(fname):
                f = open(fname)
                rows = f.readlines()

                for i in range(2, len(rows)):
                    row = rows[i].split()
                    if len(row) > 1:
                        Energy = row[1]
                        Volume = row[0]
                        a = 0
                        if len(row) > 2:
                            a = row[2]
                        b = 0
                        if len(row) > 3:
                            b = row[3]
                        c = 0
                        if len(row) > 4:
                            c = row[4]
                        self.fill_cell_info_row(Energy, Volume, a, b, c)
                f.close()
        except Exception as e:
            self.show_error(e)

    def add_critic2_cro_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
            self.work_dir = os.path.dirname(fname)

            box_bohr, box_ang, box_deg, cps = check_cro_file(fname)
            al = math.radians(box_deg[0])
            be = math.radians(box_deg[1])
            ga = math.radians(box_deg[2])
            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lat_vectors_from_params(box_ang[0], box_ang[1], box_ang[2], al, be, ga)

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

    def show_error(self, e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        msg.exec_()

    def add_dos_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
            self.work_dir = os.path.dirname(fname)
            self.check_dos(fname)
        except Exception as e:
            self.show_error(e)

    def add_isosurface_color_to_table(self):
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        i = self.ui.IsosurfaceColorsTable.rowCount() + 1
        value = self.ui.FormActionsPostLabelSurfaceValue.text()
        self.ui.IsosurfaceColorsTable.setRowCount(i)  # и одну строку в таблице
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
        minv, maxv = self.VolumericData.min, self.VolumericData.max
        color = self.get_color(cmap, minv, maxv, float(value), color_scale)
        self.ui.IsosurfaceColorsTable.item(i - 1, 0).setBackground(
            QColor.fromRgbF(color[0], color[1], color[2], color[3]))

        self.ui.FormActionsPostButSurface.setEnabled(True)
        self.ui.FormActionsPostButSurfaceDelete.setEnabled(True)

    def set_part1_file(self) -> None:
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
        if os.path.exists(fname):
            self.ui.part1_file.setText(fname)

    def set_part2_file(self) -> None:
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
        if os.path.exists(fname):
            self.ui.part2_file.setText(fname)

    def create_model_from_parts(self) -> None:
        fname1 = self.ui.part1_file.text()
        fname2 = self.ui.part2_file.text()

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
        self.MainForm.add_new_atom()

    def atom_delete(self):
        if len(self.models) == 0:
            return
        self.MainForm.delete_selected_atom()
        self.models[-1] = self.MainForm.MainModel
        self.model_to_screen(-1)

    def atom_modify(self):
        if len(self.models) == 0:
            return
        self.MainForm.modify_selected_atom()
        self.models.append(self.MainForm.MainModel)
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
            self.ui.FormActionsButtonParseBANDS.setEnabled(True)

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

    def check_volumeric_data(self, fname):
        files = []
        if fname.endswith(".XSF"):
            files.append(fname)
        if fname.endswith(".cube"):
            files.append(fname)

        if fname.endswith(".out") or fname.endswith(".OUT"):
            label = TSIESTA.system_label(fname)
            dir = os.path.dirname(fname)
            dirs, content = helpers.getsubs(dir)
            for posFile in content:
                file_candidat = Path(posFile).name
                if file_candidat.startswith(label) and file_candidat.endswith(".cube"):
                    files.append(dir + "/" + file_candidat)

            files.append(dir + "/" + label + ".XSF")
        self.ui.FormActionsPostList3DData.clear()
        for file in files:
            if os.path.exists(file):
                self.ui.FormActionsPostList3DData.addItems([file])
                self.ui.FormActionsPostButSurfaceParse.setEnabled(True)
            self.ui.FormActionsPostList3DData.update()

    def change_fragment1_status_by_x(self):
        xmin = self.ui.xminborder.value()
        xmax = self.ui.xmaxborder.value()
        for at in self.MainForm.MainModel.atoms:
            if (at.x >= xmin) and (at.x <= xmax):
                at.fragment1 = True
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def change_fragment1_status_by_y(self):
        ymin = self.ui.yminborder.value()
        ymax = self.ui.ymaxborder.value()
        for at in self.MainForm.MainModel.atoms:
            if (at.y >= ymin) and (at.y <= ymax):
                at.fragment1 = True
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def change_fragment1_status_by_z(self):
        zmin = self.ui.zminborder.value()
        zmax = self.ui.zmaxborder.value()
        for at in self.MainForm.MainModel.atoms:
            if (at.z >= zmin) and (at.z <= zmax):
                at.fragment1 = True
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def fragment1_clear(self):
        for at in self.MainForm.MainModel.atoms:
            at.fragment1 = False
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def clearQTreeWidget(self, tree):
        iterator = QTreeWidgetItemIterator(tree, QTreeWidgetItemIterator.All)
        while iterator.value():
            iterator.value().takeChildren()
            iterator += 1
        i = tree.topLevelItemCount()
        while i > -1:
            tree.takeTopLevelItem(i)
            i -= 1

    def color_to_ui(self, ColorUi, state_Color):
        r = state_Color.split()[0]
        g = state_Color.split()[1]
        b = state_Color.split()[2]
        ColorUi.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

    def create_model_with_electrodes(self):
        try:
            left_file = self.ui.FormActionsPreLeftElectrode.text()
            scat_file = self.ui.FormActionsPreScatRegion.text()
            righ_file = self.ui.FormActionsPreRightElectrode.text()

            model_left, fdf_left = Importer.Import(left_file)
            model_scat, fdf_scat = Importer.Import(scat_file)
            model_righ, fdf_righ = Importer.Import(righ_file)

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

            model_scat.rotateX(scat_rotationX)
            model_scat.rotateY(scat_rotationY)
            model_scat.rotateZ(scat_rotationZ)

            scat_move_x = self.ui.FormActionsPreMoveScatX.value()
            scat_move_y = self.ui.FormActionsPreMoveScatY.value()
            model_scat.move(scat_move_x, scat_move_y, 0)

            """ end: parts transformation"""

            left_elec_max = model_left.maxZ()
            left_bord = model_scat.minZ()

            right_elec_min = model_righ.minZ()

            left_dist = self.ui.FormActionsPreSpinLeftElectrodeDist.value()
            righ_dist = self.ui.FormActionsPreSpinRightElectrodeDist.value()

            model = TAtomicModel()
            model.add_atomic_model(model_left)
            model_scat.move(0, 0, -(left_bord - left_elec_max) + left_dist)
            model.add_atomic_model(model_scat)
            righ_bord = model.maxZ()
            model_righ.move(0, 0, (righ_bord - right_elec_min) + righ_dist)
            model.add_atomic_model(model_righ)

            self.models.append(model)
            self.plot_model(-1)
            self.MainForm.add_atoms()
            self.fill_gui("SWNT-model")
        except Exception as e:
            self.show_error(e)

    def colors_of_atoms(self):
        atomscolor = [QTableWidgetItem(self.ui.ColorsOfAtomsTable.item(1, 0)).background().color().getRgbF()]
        for i in range(0, self.ui.ColorsOfAtomsTable.rowCount()):
            col = self.ui.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
        return atomscolor

    #def create_checkable_item(self, QuantumNumbersList, value):
    #    item = QStandardItem(value)
    #    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
    #    #item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
    #    QuantumNumbersList.appendRow(item)

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
        self.MainForm.MainModel.set_lat_vectors(v1, v2, v3)
        self.models.append(self.MainForm.MainModel)
        self.model_to_screen(-1)

    def export_volumeric_data_to_xsf(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "XSF files (*.XSF)")[0]
            self.export_volumeric_data_to_file(fname)
        except Exception as e:
            self.show_error(e)

    def export_volumeric_data_to_cube(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "cube files (*.cube)")[0]
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
        self.MainForm.volumeric_data_to_file(fname, self.VolumericData, x1, x2, y1, y2, z1, z2)
        self.work_dir = os.path.dirname(fname)
        self.save_active_folder()

    def fill_gui(self, title=""):
        fname = self.filename
        if title == "":
            self.fill_file_name(fname)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()
        self.check_volumeric_data(fname)

        self.ui.PropertyAtomAtomDistanceAt1.setMaximum(self.MainForm.MainModel.nAtoms())
        self.ui.PropertyAtomAtomDistanceAt2.setMaximum(self.MainForm.MainModel.nAtoms())
        self.ui.PropertyAtomAtomDistance.setText("")

        if Importer.check_format(fname) == "SIESTAout":
            self.check_dos(fname)
            self.check_pdos(fname)
            self.check_bands(fname)
            self.fill_cell_info(fname)

        if Importer.check_format(fname) == "SIESTAfdf":
            c = self.MainForm.MainModel.get_LatVect3_norm()
            self.ui.FormActionsPreZSizeFillSpace.setValue(c)

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
        model = self.MainForm.get_model().atoms
        self.ui.FormModelTableAtoms.setRowCount(len(model))

        for i in range(0, len(model)):
            self.ui.FormModelTableAtoms.setItem(i, 0, QTableWidgetItem(model[i].let))
            self.ui.FormModelTableAtoms.setItem(i, 1, QTableWidgetItem(helpers.float_to_string(model[i].x)))
            self.ui.FormModelTableAtoms.setItem(i, 2, QTableWidgetItem(helpers.float_to_string(model[i].y)))
            self.ui.FormModelTableAtoms.setItem(i, 3, QTableWidgetItem(helpers.float_to_string(model[i].z)))

    def fill_properties_table(self):
        properties = []

        model = self.MainForm.get_model()

        properties.append(["Natoms", str(len(model.atoms))])
        properties.append(["LatVect1", str(model.LatVect1)])
        properties.append(["LatVect2", str(model.LatVect2)])
        properties.append(["LatVect3", str(model.LatVect3)])

        self.ui.FormModelTableProperties.setRowCount(len(properties))

        for i in range(0, len(properties)):
            self.ui.FormModelTableProperties.setItem(i, 0, QTableWidgetItem(properties[i][0]))
            self.ui.FormModelTableProperties.setItem(i, 1, QTableWidgetItem(properties[i][1]))

        self.ui.FormModifyCellEditA1.setValue(model.LatVect1[0])
        self.ui.FormModifyCellEditA2.setValue(model.LatVect1[1])
        self.ui.FormModifyCellEditA3.setValue(model.LatVect1[2])
        self.ui.FormModifyCellEditB1.setValue(model.LatVect2[0])
        self.ui.FormModifyCellEditB2.setValue(model.LatVect2[1])
        self.ui.FormModifyCellEditB3.setValue(model.LatVect2[2])
        self.ui.FormModifyCellEditC1.setValue(model.LatVect3[0])
        self.ui.FormModifyCellEditC2.setValue(model.LatVect3[1])
        self.ui.FormModifyCellEditC3.setValue(model.LatVect3[2])

    def fill_volumeric_data(self, data, tree=" "):
        if tree == " ":
            tree = self.ui.FormActionsPostTreeSurface
        type = data.type
        data = data.blocks
        self.clearQTreeWidget(tree)

        if type == "TXSF":
            for dat in data:
                text = (dat[0].title.split('_')[3]).split(':')[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text) + "3D")
                for da in dat:
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(text + ':' + da.title.split(':')[1]))

        if type == "TGaussianCube":
            for dat in data:
                text = dat[0].title.split(".cube")[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text))

                child = QTreeWidgetItem(parent)
                child.setText(0, "{}".format(text))
        tree.show()

    def fill_bonds(self):
        c1, c2 = self.fill_bonds_charges()
        bonds = self.MainForm.MainModel.find_bonds_exact()
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

        models, FDFData = Importer.Import(fname)
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
        bonds = self.MainForm.MainModel.find_bonds_exact()
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
        bond = round(self.MainForm.MainModel.atom_atom_distance(i - 1, j - 1), 4)
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
                    color = mainWindow.get_color(cmap, minv, maxv, value, color_scale)
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

    def get_fdf_file_name(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir, "FDF files (*.fdf)")[0]
        if not fname.endswith(".fdf"):
            fname += ".fdf"
        return fname

    @staticmethod
    def get_color_from_setting(strcolor):
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor

    def load_settings(self) -> None:
        settings = QSettings()
        state_form_settings_opening_check_only_optimal = settings.value(SETTINGS_FormSettingsOpeningCheckOnlyOptimal,
                                                                        False, type=bool)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.setChecked(state_form_settings_opening_check_only_optimal)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.clicked.connect(self.save_state_open_only_optimal)
        state_FormSettingsParseAtomicProperties = settings.value(SETTINGS_FormSettingsParseAtomicProperties, False,
                                                                 type=bool)
        self.ui.FormSettingsParseAtomicProperties.setChecked(state_FormSettingsParseAtomicProperties)
        self.ui.FormSettingsParseAtomicProperties.clicked.connect(self.save_state_parse_atomic_properties)
        state_FormSettingsViewCheckShowAxes = settings.value(SETTINGS_FormSettingsViewCheckShowAxes, False, type=bool)
        self.ui.FormSettingsViewCheckShowAxes.setChecked(state_FormSettingsViewCheckShowAxes)
        self.ui.FormSettingsViewCheckShowAxes.clicked.connect(self.save_state_view_show_axes)
        state_FormSettingsViewCheckAtomSelection = settings.value(SETTINGS_FormSettingsViewCheckAtomSelection, False,
                                                                  type=bool)
        if state_FormSettingsViewCheckAtomSelection:
            self.ui.FormSettingsViewCheckAtomSelection.setChecked(True)
        else:
            self.ui.FormSettingsViewCheckModelMove.setChecked(True)
        self.ui.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_view_atom_selection)
        self.ui.FormSettingsViewCheckModelMove.clicked.connect(self.save_state_view_atom_selection)

        state_FormSettingsViewRadioColorBondsManual = settings.value(SETTINGS_FormSettingsViewRadioColorBondsManual,
                                                                     False, type=bool)
        if state_FormSettingsViewRadioColorBondsManual:
            self.ui.FormSettingsViewRadioColorBondsManual.setChecked(True)
        else:
            self.ui.FormSettingsViewRadioColorBondsByAtoms.setChecked(True)
        self.ui.FormSettingsViewRadioColorBondsManual.clicked.connect(self.save_state_view_bond_color)
        self.ui.FormSettingsViewRadioColorBondsByAtoms.clicked.connect(self.save_state_view_bond_color)

        state_FormSettingsViewCheckXYZasCritic2 = settings.value(SETTINGS_FormSettingsViewCheckXYZasCritic2, False,
                                                                  type=bool)
        self.ui.FormSettingsViewCheckXYZasCritic2.setChecked(state_FormSettingsViewCheckXYZasCritic2)
        self.ui.FormSettingsViewCheckXYZasCritic2.clicked.connect(self.save_state_xyz_as_critic2)

        state_FormSettingsViewCheckShowAtoms = settings.value(SETTINGS_FormSettingsViewCheckShowAtoms, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtoms.setChecked(state_FormSettingsViewCheckShowAtoms)
        self.ui.FormSettingsViewCheckShowAtoms.clicked.connect(self.save_state_view_show_atoms)

        state_FormSettingsViewCheckShowAtomNumber = settings.value(SETTINGS_FormSettingsViewCheckShowAtomNumber, True,
                                                                   type=bool)
        self.ui.FormSettingsViewCheckShowAtomNumber.setChecked(state_FormSettingsViewCheckShowAtomNumber)
        self.ui.FormSettingsViewCheckShowAtomNumber.clicked.connect(self.save_state_view_show_atom_number)

        state_FormSettingsViewCheckShowBox = settings.value(SETTINGS_FormSettingsViewCheckShowBox, False, type=bool)
        self.ui.FormSettingsViewCheckShowBox.setChecked(state_FormSettingsViewCheckShowBox)
        self.ui.FormSettingsViewCheckShowBox.clicked.connect(self.save_state_view_show_box)

        state_FormSettingsViewCheckShowBonds = settings.value(SETTINGS_FormSettingsViewCheckShowBonds, True, type=bool)
        self.ui.FormSettingsViewCheckShowBonds.setChecked(state_FormSettingsViewCheckShowBonds)
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
        state_form_settings_view_spin_contour_width = int(settings.value(SETTINGS_FormSettingsViewSpinContourWidth,
                                                                         '20'))
        self.ui.FormSettingsViewSpinContourWidth.setValue(state_form_settings_view_spin_contour_width)
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

    def menu_export(self):
        if self.MainForm.MainModel.nAtoms() > 0:
            try:
                long_name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir,
                    "FDF files (*.fdf);;XYZ files (*.xyz);;FireFly input files (*.inp);;VASP POSCAR file (POSCAR)")
                fname = long_name[0]
                self.models[self.active_model].export_to_file(fname)
                self.work_dir = os.path.dirname(fname)
                self.save_active_folder()
            except Exception as e:
                self.show_error(e)

    def menu_open(self):
        if len(self.models) > 0:
            self.action_on_start = 'Open'
            self.save_state_action_on_start()
            os.execl(sys.executable, sys.executable, *sys.argv)
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
        if os.path.exists(fname):
            self.filename = fname
            self.work_dir = os.path.dirname(fname)
            try:
                self.get_atomic_model_and_fdf(fname)
            except Exception as e:
                self.show_error(e)

            problem_atoms = []
            for structure in self.models:
                for at in structure:
                    if at.charge >= 200:
                        problem_atoms.append(at.charge)
            problem_atoms = set(problem_atoms)

            if len(problem_atoms) > 0:
                self.atomDialog = AtomsIdentifier(problem_atoms)
                self.atomDialog.show()
                ansv = self.atomDialog.ansv

                for structure in self.models:
                    structure.ModifyAtomsTypes(ansv)

            try:
                self.plot_last_model()
            except Exception as e:
                self.show_error(e)

    def get_atomic_model_and_fdf(self, fname):
        parse_properies = self.ui.FormSettingsParseAtomicProperties.isChecked()
        xyzcritic2 = self.ui.FormSettingsViewCheckXYZasCritic2.isChecked()
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            self.models, self.FDFData = Importer.Import(fname, 'opt', parse_properies, xyzcritic2)
        else:
            self.models, self.FDFData = Importer.Import(fname, 'all', parse_properies, xyzcritic2)

    def plot_last_model(self):
        if len(self.models) > 0:
            if len(self.models[-1].atoms) > 0:
                self.plot_model(-1)
                self.fill_gui()
                self.save_active_folder()

    def menu_ortho(self):
        self.MainForm.ViewOrtho = True
        self.ui.openGLWidget.update()

    def menu_perspective(self):
        self.MainForm.ViewOrtho = False
        self.ui.openGLWidget.update()

    def menu_show_box(self):
        self.ui.FormSettingsViewCheckShowBox.isChecked(True)
        self.MainForm.ViewBox = True
        self.ui.openGLWidget.update()

    def menu_hide_box(self):
        self.ui.FormSettingsViewCheckShowBox.isChecked(False)
        self.MainForm.ViewBox = False
        self.ui.openGLWidget.update()

    def menu_about(self):
        about_win = QDialog(self)
        about_win.ui = Ui_about()
        about_win.ui.setupUi(about_win)
        about_win.setFixedSize(QSize(550, 250))
        about_win.show()

    def critical_point_prop_to_form(self):
        text = self.ui.AtomPropertiesText.toPlainText().split("Selected critical point:")
        if len(text) > 1:
            text = text[1].split()[0]

            model = self.models[-1]

            ind1, ind2 = model.atoms_of_bond_path(int(text))
            atom1 = model.atoms[ind1].let + str(ind1)
            atom2 = model.atoms[ind2].let + str(ind2)
            title = text + ":" + atom1 + "-" + atom2

            self.ui.FormSelectedCP.setText(text)
            f = self.models[-1].bcp[int(text)].getProperty("field")
            self.ui.FormSelectedCP_f.setText(f)
            g = self.models[-1].bcp[int(text)].getProperty("grad")
            self.ui.FormSelectedCP_g.setText(g)
            l = self.models[-1].bcp[int(text)].getProperty("lap")
            self.ui.FormSelectedCP_lap.setText(l)

    def model_to_screen(self, value):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()
        self.MainForm.selected_atom_properties.setText("select")

        self.color_with_property_enabling()

    def color_with_property_enabling(self):
        if self.MainForm.MainModel.nAtoms() > 0:
            atom = self.MainForm.MainModel.atoms[0]
            atom_prop_type = QStandardItemModel()
            for key in atom.properties:
                atom_prop_type.appendRow(QStandardItem(str(key)))
            self.ui.PropertyForColorOfAtoms.setModel(atom_prop_type)

    def color_atoms_with_property(self):
        if self.ui.ColorAtomsWithProperty.isChecked():
            prop = self.ui.PropertyForColorOfAtoms.currentText()
            if len(prop) > 0:
                self.MainForm.color_atoms_with_property(prop)
            else:
                self.MainForm.color_atoms_with_charge()
        else:
            self.MainForm.color_atoms_with_charge()
        self.MainForm.update()

    def model_rotation(self):
        if self.MainForm.MainModel.nAtoms() == 0:
            return
        angle = self.ui.FormModifyRotationAngle.value()
        model = self.MainForm.MainModel
        if self.ui.FormModifyRotationCenter.isChecked():
            center = model.get_center_of_mass()
            model.move(center[0], center[1], center[2])
        if self.ui.FormModifyRotationX.isChecked():
            model.rotateX(angle)
        if self.ui.FormModifyRotationY.isChecked():
            model.rotateY(angle)
        if self.ui.FormModifyRotationZ.isChecked():
            model.rotateZ(angle)
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_x(self):
        if self.MainForm.MainModel.nAtoms() == 0:
            return
        model = self.MainForm.MainModel
        model = model.growX()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_y(self):
        if self.MainForm.MainModel.nAtoms() == 0:
            return
        model = self.MainForm.MainModel
        model = model.growY()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_z(self):
        if self.MainForm.MainModel.nAtoms() == 0:
            return
        model = self.MainForm.MainModel
        model = model.growZ()
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
        self.MainForm.set_atomic_structure(self.models[self.active_model], atomscolor, view_atoms, view_atom_numbers,
                                           view_box, boxcolor, view_bonds, bondscolor, bond_width,
                                           color_of_bonds_by_atoms, view_axes, axescolor, contour_width)
        self.prepare_form_actions_combo_pdos_species()
        self.prepare_form_actions_combo_pdos_indexes()

        self.color_with_property_enabling()

    def plot_surface(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.MainForm.ViewSurface = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.VolumericData.min, self.VolumericData.max
        if self.ui.FormActionsPostCheckSurface.isChecked():
            data = []
            for i in range(0, self.ui.IsosurfaceColorsTable.rowCount()):
                value = float(self.ui.IsosurfaceColorsTable.item(i, 0).text())
                verts, faces, normals = self.VolumericData.isosurface(value)
                transp = float(self.ui.IsosurfaceColorsTable.cellWidget(i, 1).text())
                if self.is_scaled_colors_for_surface:
                    color = self.get_color(cmap, minv, maxv, value, color_scale)
                else:
                    if __name__ == '__main__':
                        color = self.ui.IsosurfaceColorsTable.item(i, 0).background().color().getRgbF()
                color = (color[0], color[1], color[2], transp)
                data.append([verts, faces, color, normals])
            self.MainForm.add_surface(data)
        else:
            self.MainForm.update()

    def plot_contous_isovalues(self, n_contours, scale="Log"):
        minv, maxv = self.VolumericData.min, self.VolumericData.max
        isovalues = []
        if minv == maxv:
            return isovalues
        if scale == "Linear":
            isovalues = np.linspace(minv, maxv, n_contours + 2)
        if scale == "Log":
            zero = 1e-8
            if minv < zero:
                minv = zero
            isovalueslog = np.linspace(math.log10(minv), math.log10(maxv), n_contours + 2)
            isovalues = []
            for i in range(1, len(isovalueslog) - 1):
                item = isovalueslog[i]
                isovalues.append(math.exp(math.log(10) * item))
        return isovalues

    def plot_contour(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.VolumericData.Nx is None:
            return
        self.MainForm.ViewContour = False
        self.MainForm.ViewContourFill = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.VolumericData.min, self.VolumericData.max
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

            isovalues = self.plot_contous_isovalues(n_contours, color_scale)

            if self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, 'black')
            else:
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, color_scale)

            if self.ui.FormSettingsContourColorFixed.isChecked():
                color = self.get_color_from_setting(self.state_Color_Of_Contour)
                for i in range(0, len(colors)):
                    colors[i] = color

            if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                conts = self.VolumericData.contours(isovalues, plane, myslice)
                params.append([isovalues, conts, colors])

            if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                points = self.VolumericData.plane(plane, myslice)
                colors = self.get_color_of_plane(minv, maxv, points, cmap, color_scale)
                normal = [0, 0, 1]
                if plane == "xz":
                    normal = [0, -1, 0]
                if plane == "yz":
                    normal = [1, 0, 0]
                params_colored_plane.append([points, colors, normal])

        if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_contour(params)

        if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_colored_plane(params_colored_plane)

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

    def pdos_filter(self):
        atom_index = []
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'All':
            atom_index = range(1, self.MainForm.MainModel.nAtoms() + 1)
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected atom (3D View)':
            atom_index = [self.MainForm.MainModel.selected_atom + 1]
        if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected in list below':
            atom_index = (self.ui.FormActionsPDOSIndexes.toPlainText()).split()
            atom_index = helpers.list_str_to_int(atom_index)
        species = []
        if self.ui.FormActionsComboPDOSspecies.currentText() == 'All':
            mendeley = TPeriodTable()
            atoms_list = mendeley.get_all_letters()
            types_of_atoms = self.MainForm.MainModel.typesOfAtoms()
            for i in range(0, len(types_of_atoms)):
                species.append(str(atoms_list[types_of_atoms[i][0]]))
        if self.ui.FormActionsComboPDOSspecies.currentText() == 'Selected in list below':
            species = (self.ui.FormActionsPDOSSpecieces.text()).split()
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
        return atom_index, number_l, number_m, number_n, number_z, species

    def plot_bonds_histogram(self):
        self.ui.PyqtGraphWidget.set_xticks(None)
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        c1, c2 = self.fill_bonds_charges()
        bonds = self.MainForm.MainModel.find_bonds_exact()

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
            atom_index, number_l, number_m, number_n, number_z, species = self.pdos_filter()
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
            self.ui.FormActionsSpinBANDSxmin.setRange(kmin, kmax)
            self.ui.FormActionsSpinBANDSxmin.setValue(kmin)
            self.ui.FormActionsSpinBANDSxmax.setRange(kmin, kmax)
            self.ui.FormActionsSpinBANDSxmax.setValue(kmax)

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
            self.ui.FormActionsSpinBANDSemin.setRange(emin, emax)
            self.ui.FormActionsSpinBANDSemin.setValue(e_min_form)
            self.ui.FormActionsSpinBANDSemax.setRange(emin, emax)
            self.ui.FormActionsSpinBANDSemax.setValue(e_max_form)
            self.ui.FormActionsButtonPlotBANDS.setEnabled(True)

    def plot_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        kmin, kmax = self.ui.FormActionsSpinBANDSxmin.value(), self.ui.FormActionsSpinBANDSxmax.value()
        emin, emax = self.ui.FormActionsSpinBANDSemin.value(), self.ui.FormActionsSpinBANDSemax.value()
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
        if self.MainForm.isActive():
            r = self.state_Color_Of_Voronoi.split()[0]
            g = self.state_Color_Of_Voronoi.split()[1]
            b = self.state_Color_Of_Voronoi.split()[2]
            color = [float(r) / 255, float(g) / 255, float(b) / 255]
            maxDist = float(self.ui.FormActionsPostTextVoronoiMaxDist.value())
            atom_index, volume = self.MainForm.add_voronoi(color, maxDist)
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
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)=" + str(round(float(aprox[0]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0=" + str(round(float(aprox[1]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'=" + str(round(float(aprox[2]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0=" + str(round(float(aprox[3]), 2)))
                self.plot_cell_approx(image_path)
                self.plot_curv_and_points(LabelX, xs, ys, xs2, ys2)

            if (method == "BirchMurnaghan") and (len(items) > 4):
                aprox, xs2, ys2 = Calculator.approx_birch_murnaghan(items)
                image_path = str(Path(__file__).parent / 'images' / 'murnaghanbirch.png')  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)=" + str(round(float(aprox[0]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0=" + str(round(float(aprox[1]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'=" + str(round(float(aprox[2]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0=" + str(round(float(aprox[3]), 2)))
                self.plot_cell_approx(image_path)
                self.plot_curv_and_points(LabelX, xs, ys, xs2, ys2)

            if (method == "Parabola") and (len(items) > 2):
                aprox, xs2, ys2 = Calculator.approx_parabola(items)
                image_path = str(Path(__file__).parent / 'images' / 'parabola.png')  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("a=" + str(round(float(aprox[2]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("b=" + str(round(float(aprox[1]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText(
                    "x0=" + str(round(-float(aprox[1]) / float(2 * aprox[2]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("c=" + str(round(float(aprox[0]), 2)))
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

    def save_image_to_file(self):
        if len(self.models) == 0:
            return
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir,
                                           "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)")
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
                new_window.MainForm.copy_state(self.MainForm)

                new_window.MainForm.image3D_to_file(fname)
                new_window.destroy()
                self.work_dir = os.path.dirname(fname)
                self.save_active_folder()
        except Exception as e:
            self.show_error(e)

    def rotate_model_xp(self):
        self.MainForm.rotX += self.rotation_step
        self.MainForm.update()

    def rotate_model_xm(self):
        self.MainForm.rotX -= self.rotation_step
        self.MainForm.update()

    def rotate_model_yp(self):
        self.MainForm.rotY += self.rotation_step
        self.MainForm.update()

    def rotate_model_ym(self):
        self.MainForm.rotY -= self.rotation_step
        self.MainForm.update()

    def rotate_model_zp(self):
        self.MainForm.rotZ += self.rotation_step
        self.MainForm.update()

    def rotate_model_zm(self):
        self.MainForm.rotZ -= self.rotation_step
        self.MainForm.update()

    def save_active_folder(self):
        self.save_property(SETTINGS_Folder, self.work_dir)

    def save_state_open_only_optimal(self):
        self.save_property(SETTINGS_FormSettingsOpeningCheckOnlyOptimal,
                           self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked())

    def save_state_parse_atomic_properties(self):
        self.save_property(SETTINGS_FormSettingsParseAtomicProperties,
                           self.ui.FormSettingsParseAtomicProperties.isChecked())

    def save_state_view_show_axes(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAxes,
                           self.ui.FormSettingsViewCheckShowAxes.isChecked())
        self.MainForm.set_axes_visible(self.ui.FormSettingsViewCheckShowAxes.isChecked())

    def save_state_view_atom_selection(self):
        self.save_property(SETTINGS_FormSettingsViewCheckAtomSelection,
                           self.ui.FormSettingsViewCheckAtomSelection.isChecked())

    def save_state_view_bond_color(self):
        self.save_property(SETTINGS_FormSettingsViewRadioColorBondsManual,
                           self.ui.FormSettingsViewRadioColorBondsManual.isChecked())
        if self.MainForm:
            self.MainForm.set_bond_color(self.ui.FormSettingsViewRadioColorBondsManual.isChecked())

    def save_state_xyz_as_critic2(self):
        self.save_property(SETTINGS_FormSettingsViewCheckXYZasCritic2, self.ui.FormSettingsViewCheckXYZasCritic2.isChecked())

    def save_state_view_show_atoms(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAtoms, self.ui.FormSettingsViewCheckShowAtoms.isChecked())
        self.MainForm.set_atoms_visible(self.ui.FormSettingsViewCheckShowAtoms.isChecked())

    def save_state_view_show_atom_number(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAtomNumber, self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())
        self.MainForm.set_atoms_numbred(self.ui.FormSettingsViewCheckShowAtomNumber.isChecked())

    def save_state_action_on_start(self):
        self.save_property(SETTINGS_FormSettingsActionOnStart, self.action_on_start)

    def save_state_view_show_box(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.MainForm.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_view_show_bonds(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.MainForm.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

    def save_state_colors_fixed(self):
        self.save_property(SETTINGS_FormSettingsColorsFixed, self.ui.FormSettingsColorsFixed.isChecked())

    def save_state_view_spin_contour_width(self):
        self.save_property(SETTINGS_FormSettingsViewSpinContourWidth, self.ui.FormSettingsViewSpinContourWidth.text())
        self.MainForm.set_contour_width(self.ui.FormSettingsViewSpinContourWidth.value() / 1000)
        self.plot_contour()

    def save_state_colors_fixed_min(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMin, self.ui.FormSettingsColorsFixedMin.text())

    def save_state_view_spin_bond_width(self):
        self.save_property(SETTINGS_FormSettingsViewSpinBondWidth, self.ui.FormSettingsViewSpinBondWidth.text())
        self.MainForm.set_bond_width(self.ui.FormSettingsViewSpinBondWidth.value() * 0.005)

    def save_state_colors_fixed_max(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMax, self.ui.FormSettingsColorsFixedMax.text())

    def save_state_colors_scale(self):
        self.save_property(SETTINGS_FormSettingsColorsScale, self.ui.FormSettingsColorsScale.currentText())
        self.colors_cash = {}

    def save_state_colors_scale_type(self):
        self.save_property(SETTINGS_FormSettingsColorsScaleType, self.ui.FormSettingsColorsScaleType.currentText())
        self.colors_cash = {}

    def save_state_preferred_coordinates(self):
        self.save_property(SETTINGS_FormSettingsPreferredCoordinates,
                           self.ui.FormSettingsPreferredCoordinates.currentText())
        self.CoordType = self.ui.FormSettingsPreferredCoordinates.currentText()

    def save_state_preferred_units(self):
        self.save_property(SETTINGS_FormSettingsPreferredUnits,
                           self.ui.FormSettingsPreferredUnits.currentText())
        self.units_type = self.ui.FormSettingsPreferredUnits.currentText()

    def save_state_preferred_lattice(self):
        self.save_property(SETTINGS_FormSettingsPreferredLattice, self.ui.FormSettingsPreferredLattice.currentText())
        self.LatticeType = self.ui.FormSettingsPreferredLattice.currentText()

    @staticmethod
    def save_property(var_property, value):
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

    def fdf_data_to_form(self):
        try:
            model = self.MainForm.get_model()
            text = self.FDFData.get_all_data(model, self.CoordType, self.units_type, self.LatticeType)
            print(self.CoordType, self.units_type, self.LatticeType)
            self.ui.FormActionsPreTextFDF.setText(text)
        except Exception:
            print("There are no atoms in the model")

    def fdf_data_from_form_to_file(self):
        try:
            text = self.ui.FormActionsPreTextFDF.toPlainText()
            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "FDF files (*.fdf)")[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_script_create(self):
        if len(self.models) == 0:
            return
        try:
            model2 = deepcopy(self.models[self.active_model])
            text = ase.ase_raman_and_ir_script_create(model2, self.FDFData)

            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "Python file (*.py)")[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_parse(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
            if os.path.exists(fname):
                self.filename = fname
                self.work_dir = os.path.dirname(fname)
                raman_text, units_i, raman_inten, raman_en_ev, raman_en_cm, ir_inten, ir_en_ev, ir_en_cm = ase.ase_raman_and_ir_parse(fname)

                for i in range(0, len(raman_inten)):
                    raman_text += "{0:10.1f} {1:10.1f} {2:10.2f}\n".format(raman_en_ev[i], raman_en_cm[i], raman_inten[i])
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
                y_fig[j] += y[i] * math.exp(-math.pow(x[i] - x_fig[j], 2) / ( 2 * sigma) )

        title = "Spectrum"
        self.ui.PyqtGraphWidget.clear()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        self.ui.PyqtGraphWidget.plot([x_fig], [y_fig], [None], title, x_title, y_title, True)

    def d12_to_file(self):
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
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "Crystal d12 (*.d12)")[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def fill_space(self):
        if len(self.models) == 0:
            return
        mendeley = TPeriodTable()
        nAtoms = int(self.ui.FormActionsPreNAtomsFillSpace.value())
        charge = int(self.ui.FormActionsPreAtomChargeFillSpace.value())
        radAtom = mendeley.get_rad(charge)
        let = mendeley.get_let(charge)
        delta = float(self.ui.FormActionsPreDeltaFillSpace.value())
        n_prompts = int(self.ui.FormActionsPreNPromptsFillSpace.value())
        radTube = float(self.ui.FormActionsPreRadiusFillSpace.value())
        length = float(self.ui.FormActionsPreZSizeFillSpace.value())
        models = Calculator.FillTube(radTube, length, nAtoms, 0.01 * radAtom, delta, n_prompts, let, charge)

        filename = "."
        try:
            if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
                filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
                filename = filename.split(".fdf")[0]
        except Exception as e:
            self.show_error(e)

        myiter = 0
        for model in models:
            secondModel = deepcopy(self.MainForm.get_model())
            for at in model:
                secondModel.add_atom(at)
            self.models.append(secondModel)
            if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
                text = self.FDFData.get_all_data(secondModel.atoms)
                with open(filename + str(myiter) + '.fdf', 'w') as f:
                    f.write(text)
            myiter += 1
        self.fill_models_list()

    def parse_volumeric_data(self):
        if len(self.ui.FormActionsPostList3DData.selectedItems()) > 0:
            Selected = self.ui.FormActionsPostList3DData.selectedItems()[0].text()
            if Selected.endswith(".XSF"):
                self.VolumericData = TXSF()
            if Selected.endswith(".cube"):
                self.VolumericData = TGaussianCube()
            if self.VolumericData.parse(Selected):
                self.fill_volumeric_data(self.VolumericData)

            self.ui.FormActionsPostButSurfaceLoadData.setEnabled(True)
            self.clearQTreeWidget(self.ui.FormActionsPostTreeSurface2)
            self.ui.FormActionsPosEdit3DData2.setText("")
            self.clear_form_isosurface_data2_n()
            self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
            self.ui.CalculateTheVolumericDataSum.setEnabled(False)
            self.ui.VolumrricDataGrid2.setTitle("Grid")
            self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)

    def parse_volumeric_data2(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)
            if len(fname) > 0:
                fname = fname[0]
                if fname.endswith(".XSF"):
                    self.VolumericData2 = TXSF()
                if fname.endswith(".cube"):
                    self.VolumericData2 = TGaussianCube()
                if self.VolumericData2.parse(fname):
                    self.fill_volumeric_data(self.VolumericData2, self.ui.FormActionsPostTreeSurface2)

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

    def change_color_of_cell_prompt(self, table):
        i = table.selectedIndexes()[0].row()
        color = QColorDialog.getColor(initial=table.item(i, 0).background().color())
        if not color.isValid():
            return
        at_color = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        table.item(i, 0).setBackground(QColor.fromRgbF(at_color[0], at_color[1], at_color[2], 1))

    def select_isosurface_color(self):
        table = self.ui.IsosurfaceColorsTable
        self.change_color_of_cell_prompt(table)
        self.is_scaled_colors_for_surface = False

    def select_atom_color(self):
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
        if self.MainForm.MainModel.nAtoms() > 0:
            self.MainForm.set_color_of_atoms(atomscolor)

    def select_box_color(self):
        boxcolor = self.change_color(self.ui.ColorBox, SETTINGS_Color_Of_Box)
        self.MainForm.set_color_of_box(boxcolor)

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
            model = self.models[self.active_model]
            ind = int(new_cp)
            bcp_seleсted = model.bcp[ind]

    def delete_cp_from_list(self):
        itemrow = self.ui.FormCPlist.currentRow()
        self.ui.FormCPlist.takeItem(itemrow)

    def create_critic2_xyz_file(self):
        """ add code here"""
        name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir)
        fname = name[0]
        if len(fname) > 0:
            model = self.models[self.active_model]
            bcp = deepcopy(model.bcp)
            bcp_seleсted = []
            for i in range(0, self.ui.FormCPlist.count()):
                ind = int(self.ui.FormCPlist.item(i).text())
                bcp_seleсted.append(model.bcp[ind])
            is_with_selected = self.ui.radio_with_cp.isChecked()
            text = critic2.create_critic2_xyz_file(bcp, bcp_seleсted, is_with_selected, model)
            helpers.write_text_to_file(fname, text)

    def create_cri_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir)
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
            #f = open(fname_dir + "/POINTS.txt", 'w')
            #print(te, file=f)
            #f.close()

            helpers.write_text_to_file(fname_dir + "/POINTS.txt", te)

            #f = open(fname_dir + "/POINTSatoms.txt", 'w')
            #print(text, file=f)
            #f.close()
            helpers.write_text_to_file(fname_dir + "/POINTSatoms.txt", text)

    def select_voronoi_color(self):
        voronoicolor = self.change_color(self.ui.ColorVoronoi, SETTINGS_Color_Of_Voronoi)
        self.MainForm.set_color_of_voronoi(voronoicolor)

    def select_bond_color(self):
        bondscolor = self.change_color(self.ui.ColorBond, SETTINGS_Color_Of_Bonds)
        self.MainForm.set_color_of_bonds(bondscolor)

    def select_axes_color(self):
        axescolor = self.change_color(self.ui.ColorAxes, SETTINGS_Color_Of_Axes)
        self.MainForm.set_color_of_axes(axescolor)

    def select_contour_color(self):
        self.change_color(self.ui.ColorContour, SETTINGS_Color_Of_Contour)
        self.plot_contour()

    def create_graphene(self):
        n = self.ui.FormActionsPreLineGraphene_n.value()
        m = self.ui.FormActionsPreLineGraphene_m.value()
        leng = self.ui.FormActionsPreLineGraphene_len.value()

        model = TGraphene(n, m, leng)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("Graphene-model")

    def create_swnt(self):
        n = 0
        m = 0
        mytype = 0
        if self.ui.FormActionsPreRadioSWNT.isChecked():
            n = self.ui.FormActionsPreLineSWNTn.value()
            m = self.ui.FormActionsPreLineSWNTm.value()
        if self.ui.FormActionsPreRadioSWNTcap.isChecked() or self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            nm = self.ui.FormActionsPreComboSWNTind.currentText().split(",")
            n = int(nm[0].split("(")[1])
            m = int(nm[1].split(")")[0])
        if self.ui.FormActionsPreRadioSWNTcap.isChecked():
            mytype = 1
        if self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            mytype = 2
        if self.ui.FormActionsPreRadioSWNTuselen.isChecked():
            leng = float(self.ui.FormActionsPreLineSWNTlen.text())
            cells = 1
        else:
            leng = 0
            cells = float(self.ui.FormActionsPreLineSWNTcells.text())

        model = None
        if mytype == 0:
            model = TSWNT(n, m, leng, cells)

        if mytype == 1 or mytype == 2:
            dist1 = float(self.ui.FormCreateSpinFirstCapDist.value())
            angle1 = float(self.ui.FormCreateSpinFirstCapAngle.value())
            dist2 = float(self.ui.FormCreateSpinSecondCapDist.value())
            angle2 = float(self.ui.FormCreateSpinSecondCapAngle.value())
            model = TCapedSWNT(n, m, leng, cells, mytype, dist1, angle1, dist2, angle2)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("SWNT-model")

    def create_swgnt(self):
        """  to do """

    def create_bi_el_nt(self):  # pragma: no cover
        """ to do """
        n = self.ui.FormBiElementN.value()
        if self.ui.FormBiElementRadioArm.isChecked():
            m = n
        else:
            m = 0
        leng = self.ui.FormBiElementLen.value()
        t = self.ui.FormNanotypeTypeSelector.currentText()

        model = TBiNT(n, m, leng, t)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("Bi element NT-model")

    def swnt_type1_selected(self):   # pragma: no cover
        self.ui.FormActionsPreLineSWNTn.setEnabled(True)
        self.ui.FormActionsPreLineSWNTm.setEnabled(True)
        self.ui.FormActionsPreComboSWNTind.setEnabled(False)
        self.ui.FormCreateGroupFirstCap.setEnabled(False)
        self.ui.FormCreateGroupSecondCap.setEnabled(False)

    def swnt_type2_selected(self):   # pragma: no cover
        self.ui.FormActionsPreLineSWNTn.setEnabled(False)
        self.ui.FormActionsPreLineSWNTm.setEnabled(False)
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
        getSelected = self.ui.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if not (getSelected[0].parent() is None):
                getChildNode = getSelected[0].text(0)
                self.get_atomic_model_and_fdf(self.VolumericData.filename)
                self.VolumericData.load_data(getChildNode)

                self.plot_last_model()

                self.volumeric_data_max_min_to_form()
                self.ui.FormActionsPostButSurfaceAdd.setEnabled(True)
                self.ui.FormActionsPostButContour.setEnabled(True)
                self.ui.FormActionsPostButSurfaceParse2.setEnabled(True)

                self.ui.FormActionsPostSliderContourXY.setMaximum(self.VolumericData.Nz)
                self.ui.FormActionsPostSliderContourXZ.setMaximum(self.VolumericData.Ny)
                self.ui.FormActionsPostSliderContourYZ.setMaximum(self.VolumericData.Nx)

                self.ui.FormVolDataExportX1.setMaximum(self.VolumericData.Nx)
                self.ui.FormVolDataExportX2.setMaximum(self.VolumericData.Nx)
                self.ui.FormVolDataExportX2.setValue(self.VolumericData.Nx)
                self.ui.FormVolDataExportY1.setMaximum(self.VolumericData.Ny)
                self.ui.FormVolDataExportY2.setMaximum(self.VolumericData.Ny)
                self.ui.FormVolDataExportY2.setValue(self.VolumericData.Ny)
                self.ui.FormVolDataExportZ1.setMaximum(self.VolumericData.Nz)
                self.ui.FormVolDataExportZ2.setMaximum(self.VolumericData.Nz)
                self.ui.FormVolDataExportZ2.setValue(self.VolumericData.Nz)

    def volumeric_data_load2(self):   # pragma: no cover
        getSelected = self.ui.FormActionsPostTreeSurface2.selectedItems()
        if getSelected:
            if getSelected[0].parent() is not None:
                getChildNode = getSelected[0].text(0)
                self.VolumericData2.load_data(getChildNode)

                self.ui.FormActionsPostLabelSurfaceNx.setText("Nx: " + str(self.VolumericData2.Nx))
                self.ui.FormActionsPostLabelSurfaceNy.setText("Ny: " + str(self.VolumericData2.Ny))
                self.ui.FormActionsPostLabelSurfaceNz.setText("Nz: " + str(self.VolumericData2.Nz))

                if (self.VolumericData2.Nx == self.VolumericData.Nx) and (
                        self.VolumericData2.Ny == self.VolumericData.Ny) and (
                        self.VolumericData2.Nz == self.VolumericData.Nz):
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
        self.VolumericData.difference(self.VolumericData2)
        self.volumeric_data_max_min_to_form()

    def volumeric_data_sum(self):  # pragma: no cover
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.CalculateTheVolumericDataSum.setEnabled(False)
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)
        self.VolumericData.difference(self.VolumericData2, mult=-1)
        self.volumeric_data_max_min_to_form()

    def volumeric_data_max_min_to_form(self):  # pragma: no cover
        minv, maxv = self.VolumericData.min, self.VolumericData.max
        self.ui.FormActionsPostLabelSurfaceMax.setText("Max: " + str(round(maxv, 5)))
        self.ui.FormActionsPostLabelSurfaceMin.setText("Min: " + str(round(minv, 5)))
        self.ui.FormActionsPostLabelSurfaceValue.setRange(minv, maxv)
        self.ui.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))


ORGANIZATION_NAME = 'SUSU'
ORGANIZATION_DOMAIN = 'susu.ru'
APPLICATION_NAME = 'gui4dft'

SETTINGS_Folder = '\home'
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

QCoreApplication.setApplicationName(ORGANIZATION_NAME)
QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
QCoreApplication.setApplicationName(APPLICATION_NAME)

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)
window = mainWindow()
window.setup_ui()
if is_with_figure:
    window.setWindowIcon(QIcon(str(Path(__file__).parent / 'images' / 'ico.png')))
window.show()
window.start_program()

sys.exit(app.exec_())
