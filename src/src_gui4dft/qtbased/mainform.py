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

from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel
from src_gui4dft.models.capedswcnt import CapedSWNT
from src_gui4dft.models.bint import BiNT
from src_gui4dft.models.graphene import Graphene
from src_gui4dft.models.bn_plane import BNplane
from src_gui4dft.models.swnt import SWNT
from src_gui4dft.models.swgnt import SWGNT
from src_gui4dft.models.gaussiancube import GaussianCube
from src_gui4dft.models.volumericdata import VolumericData
from src_gui4dft.models.xsf import XSF

from PySide2.QtCore import QLocale, QSettings, Qt, QSize
from PySide2.QtGui import QColor, QIcon, QImage, QKeySequence, QPixmap, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QAction, QDialog, QFileDialog, QMessageBox, QColorDialog
from PySide2.QtWidgets import QDoubleSpinBox, QMainWindow, QShortcut, QTableWidgetItem, QTreeWidgetItem
from PySide2.QtWidgets import QTreeWidgetItemIterator
from src_gui4dft.qtbased.image3dexporter import Image3Dexporter

from src_gui4dft.program.siesta import TSIESTA
from src_gui4dft.program.crystal import model_1d_to_d12, model_2d_to_d12
from src_gui4dft.program.vasp import vasp_dos
from src_gui4dft.program.vasp import model_to_vasp_poscar
from src_gui4dft.program import ase

from src_gui4dft.utils.importer_exporter import ImporterExporter
from src_gui4dft.utils.electronic_prop_reader import read_siesta_bands, dos_from_file
from core_gui_atomistic.periodic_table import TPeriodTable
from src_gui4dft.utils.fdfdata import TFDFFile
from src_gui4dft.utils.calculators import Calculators as Calculator
from src_gui4dft.utils.calculators import gaps
from core_gui_atomistic import helpers

from src_gui4dft.ui.about import Ui_DialogAbout as Ui_about
from src_gui4dft.ui.form import Ui_MainWindow as Ui_form

from ase.build import molecule, bulk
from ase.cluster.cubic import FaceCenteredCubic

from src_gui4dft.program.vasp import VaspDataFromXml

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

        self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut.activated.connect(self.atom_delete)
        self.active_model: int = -1
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
        self.ui.FormActionsPostTreeSurface.itemSelectionChanged.connect(self.type_of_surface)
        self.ui.PropertyForColorOfAtom.currentIndexChanged.connect(self.color_atoms_with_property)
        self.ui.ColorAtomsProperty.stateChanged.connect(self.color_atoms_with_property)

        self.ui.font_size_3d.valueChanged.connect(self.font_size_3d_changed)
        self.ui.property_shift_x.valueChanged.connect(self.property_position_changed)
        self.ui.property_shift_y.valueChanged.connect(self.property_position_changed)

        self.ui.FormAtomsList1.currentIndexChanged.connect(self.bond_len_to_screen)
        self.ui.FormAtomsList2.currentIndexChanged.connect(self.bond_len_to_screen)

        self.ui.FormActionsPreRadioSWNT.toggled.connect(self.swnt_type1_selected)
        self.ui.FormActionsPreRadioSWNTcap.toggled.connect(self.swnt_type2_selected)
        self.ui.FormActionsPreRadioSWNTcap_2.toggled.connect(self.swnt_type2_selected)

        self.ui.ActivateFragmentSelectionModeCheckBox.toggled.connect(self.activate_fragment_selection_mode)
        self.ui.ActivateFragmentSelectionTransp.valueChanged.connect(self.activate_fragment_selection_mode)

        # buttons
        self.ui.FormActionsPostButPlotBondsHistogram.clicked.connect(self.plot_bonds_histogram)
        self.ui.FormActionsPreButFillSpace.clicked.connect(self.fill_space)

        # models generation
        self.ui.get_0d_molecula_list.clicked.connect(self.get_0d_molecula_list)
        self.ui.generate_0d_molecula.clicked.connect(self.generate_0d_molecula)
        self.ui.generate_0d_cluster.clicked.connect(self.generate_0d_cluster)
        self.ui.but_create_nanotube.clicked.connect(self.create_swnt)
        self.ui.FormActionsPreButBiElementGenerate.clicked.connect(self.create_bi_el_nt)
        self.ui.generate_2d_graphene.clicked.connect(self.create_graphene)
        self.ui.generate_2d_bn.clicked.connect(self.create_2d_bn)
        self.ui.generate_3d_bulk.clicked.connect(self.generate_3d_bulk)

        data = ["sc", "fcc", "bcc", "tetragonal", "bct", "hcp", "rhombohedral", "orthorhombic", "mcl", "diamond"]
        data.extend(["zincblende", "rocksalt", "cesiumchloride", "fluorite", "wurtzite"])
        crystalstructure_type = self.q_standard_item_model_init(data)
        self.ui.crystalstructure_3d.setModel(crystalstructure_type)

        # input generation
        self.ui.FDFGenerate.clicked.connect(self.fdf_data_to_form)
        self.ui.POSCARgenerate.clicked.connect(self.poscar_data_to_form)
        self.ui.QEgenerate.clicked.connect(self.qe_data_to_form)
        self.ui.crystal_1d_d12_generate.clicked.connect(self.d12_1D_to_form)
        self.ui.crystal_2d_d12_generate.clicked.connect(self.d12_2D_to_form)

        self.ui.data_from_form_to_input_file.clicked.connect(self.data_from_form_to_input_file)
        self.ui.model_rotation_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_rotation_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_x.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_y.valueChanged.connect(self.model_orientation_changed)
        self.ui.camera_pos_z.valueChanged.connect(self.model_orientation_changed)
        self.ui.model_scale.valueChanged.connect(self.model_orientation_changed)

        # 3D data
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
        self.ui.FormActionsPostButSurfaceAdd.clicked.connect(self.add_isosurface_color_to_table)
        self.ui.FormActionsPostButSurfaceDelete.clicked.connect(self.delete_isosurface_color_from_table)

        # colors
        self.ui.ColorBackgroundDialogButton.clicked.connect(self.select_background_color)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.ColorVoronoiDialogButton.clicked.connect(self.select_voronoi_color)
        self.ui.ColorAxesDialogButton.clicked.connect(self.select_axes_color)
        self.ui.ColorContourDialogButton.clicked.connect(self.select_contour_color)
        self.ui.manual_colors_default.clicked.connect(self.set_manual_colors_default)

        self.ui.FormActionsButtonPlotPDOS.clicked.connect(self.plot_pdos)
        self.ui.plot_bands.clicked.connect(self.plot_bands)
        self.ui.parse_bands.clicked.connect(self.parse_bands)
        self.ui.FormActionsButtonPlotPDOSselected.clicked.connect(self.plot_selected_pdos)
        self.ui.FormModifyCellButton.clicked.connect(self.edit_cell)
        self.ui.FormActionsPostButGetBonds.clicked.connect(self.get_bonds)
        self.ui.PropertyAtomAtomDistanceGet.clicked.connect(self.get_bond)
        self.ui.FormStylesFor2DGraph.clicked.connect(self.set_2d_graph_styles)
        self.ui.FormModifyTwist.clicked.connect(self.twist_model)
        self.ui.fit_with.clicked.connect(self.fit_with)

        self.ui.FormSelectPart1File.clicked.connect(self.set_part1_file)
        self.ui.FormSelectPart2File.clicked.connect(self.set_part2_file)
        self.ui.CreateModelFromParts.clicked.connect(self.create_model_from_parts)

        self.ui.FormASERamanAndIRscriptCreate.clicked.connect(self.ase_raman_and_ir_script_create)
        self.ui.FormASERamanAndIRscriptParse.clicked.connect(self.ase_raman_and_ir_parse)
        self.ui.FormASERamanAndIRscriptPlot.clicked.connect(self.ase_raman_and_ir_plot)

        self.ui.changeFragment1StatusByX.clicked.connect(self.change_fragment1_status_by_x)
        self.ui.changeFragment1StatusByY.clicked.connect(self.change_fragment1_status_by_y)
        self.ui.changeFragment1StatusByZ.clicked.connect(self.change_fragment1_status_by_z)
        self.ui.fragment1Clear.clicked.connect(self.fragment1_clear)

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

        self.ui.FormActionsPostButPlusCellParam.clicked.connect(self.add_cell_param)
        self.ui.FormActionsPostButAddRowCellParam.clicked.connect(self.add_cell_param_row)
        self.ui.FormActionsPostButDeleteRowCellParam.clicked.connect(self.delete_cell_param_row)
        self.ui.FormActionsPostButPlusDataCellParam.clicked.connect(self.add_data_cell_param)

        self.ui.FormModifyRotation.clicked.connect(self.model_rotation)
        self.ui.FormModifyGrowX.clicked.connect(self.model_grow_x)
        self.ui.FormModifyGrowY.clicked.connect(self.model_grow_y)
        self.ui.FormModifyGrowZ.clicked.connect(self.model_grow_z)

        self.ui.FormModifyGoPositive.clicked.connect(self.model_go_to_positive)
        self.ui.FormModifyGoToCell.clicked.connect(self.model_go_to_cell)

        self.ui.FormActionsPostButVoronoi.clicked.connect(self.plot_voronoi)
        self.ui.optimize_cell_param.clicked.connect(self.plot_volume_param_energy)

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        mendeley = TPeriodTable()
        atoms_list = mendeley.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))
        self.ui.atoms_list_all.setModel(model)
        self.ui.FormAtomsList1.setModel(model)
        self.ui.FormAtomsList2.setModel(model)
        self.ui.atoms_list_all_cluster.setModel(model)

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
        """Add cell parameter."""
        try:
            f_name = self.get_file_name_from_open_dialog("All files (*.*)")
            if helpers.check_format(f_name) == "SIESTAout":
                self.fill_cell_info(f_name)
            self.plot_volume_param_energy()
        except Exception as e:
            self.show_error(e)

    def add_cell_param_row(self):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)

    def add_data_cell_param(self):
        """Add cell params from file."""
        try:
            f_name = self.get_file_name_from_open_dialog("All files (*.*)")
            self.work_dir = os.path.dirname(f_name)
            row_data = self.read_data_of_cell_params(f_name)
            for data in row_data:
                if len(data) == 5:
                    self.fill_cell_info_row(*data)
        except Exception as e:
            self.show_error(e)

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

    def add_dos_file(self):
        try:
            fname = self.get_file_name_from_open_dialog("All files (*)")
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
        f_name = self.get_file_name_from_open_dialog("All files (*.*)")
        if os.path.exists(f_name):
            self.ui.part1_file.setText(f_name)

    def set_part2_file(self) -> None:
        f_name = self.get_file_name_from_open_dialog("All files (*.*)")
        if os.path.exists(f_name):
            self.ui.part2_file.setText(f_name)

    def create_model_from_parts(self) -> None:
        param = 'all'
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            param = 'opt'
        models1, fdf_data1 = ImporterExporter.import_from_file(self.ui.part1_file.text(), param, False)
        models2, fdf_data2 = ImporterExporter.import_from_file(self.ui.part2_file.text(), param, False)

        combo_model = AtomicModel()
        if len(models1) > 0:
            rot_x1 = self.ui.FormPart1RotX.value()
            rot_y1 = self.ui.FormPart1RotY.value()
            rot_z1 = self.ui.FormPart1RotZ.value()
            cm_x_new1 = self.ui.FormPart1CMx.value()
            cm_y_new1 = self.ui.FormPart1CMy.value()
            cm_z_new1 = self.ui.FormPart1CMz.value()

            part1 = self.model_part_prepare(cm_x_new1, cm_y_new1, cm_z_new1, models1, rot_x1, rot_y1, rot_z1)
            combo_model.add_atomic_model(part1)

        if len(models2) > 0:
            rot_x2 = self.ui.FormPart2RotX.value()
            rot_y2 = self.ui.FormPart2RotY.value()
            rot_z2 = self.ui.FormPart2RotZ.value()
            cm_x_new2 = self.ui.FormPart2CMx.value()
            cm_y_new2 = self.ui.FormPart2CMy.value()
            cm_z_new2 = self.ui.FormPart2CMz.value()

            part2 = self.model_part_prepare(cm_x_new2, cm_y_new2, cm_z_new2, models2, rot_x2, rot_y2, rot_z2)
            combo_model.add_atomic_model(part2)

        self.models.append(combo_model)
        self.plot_last_model()

    @staticmethod
    def model_part_prepare(cm_x_new, cm_y_new, cm_z_new, models, rot_x, rot_y, rot_z):
        part = models[-1]
        cm_old = - part.center_mass()
        part.move(*cm_old)
        part.rotate(rot_x, rot_y, rot_z)
        part.move(cm_x_new, cm_y_new, cm_z_new)
        return part

    def add_left_electrode_file(self):
        f_name = self.get_fdf_file_name()
        if os.path.exists(f_name):
            self.work_dir = os.path.dirname(f_name)
            self.save_active_folder()
            self.ui.FormActionsPreLeftElectrode.setText(f_name)

    def add_right_electrode_file(self):
        f_name = self.get_fdf_file_name()
        if os.path.exists(f_name):
            self.work_dir = os.path.dirname(f_name)
            self.save_active_folder()
            self.ui.FormActionsPreRightElectrode.setText(f_name)

    def add_scat_region_file(self):
        f_name = self.get_fdf_file_name()
        if os.path.exists(f_name):
            self.work_dir = os.path.dirname(f_name)
            self.save_active_folder()
            self.ui.FormActionsPreScatRegion.setText(f_name)

    def atom_add(self):
        if len(self.models) == 0:
            return
        charge, let, position = self.selected_atom_from_form()
        self.models[self.active_model].add_atom(Atom((position[0], position[1], position[2], let, charge)))
        self.model_to_screen(self.active_model)

    def atom_delete(self):
        if len(self.models) == 0:
            return
        if self.ui.openGLWidget.selected_atom < 0:
            return
        self.models[self.active_model].delete_atom(self.ui.openGLWidget.selected_atom)
        self.history_of_atom_selection = []
        self.model_to_screen(self.active_model)

    def atom_modify(self):
        if len(self.models) == 0:
            return
        if self.ui.openGLWidget.selected_atom < 0:
            return
        charge, let, position = self.selected_atom_from_form()
        self.models[self.active_model].atoms[self.ui.openGLWidget.selected_atom] = Atom((position[0], position[1],
                                                                                        position[2], let, charge))
        self.model_to_screen(self.active_model)

    def selected_atom_from_form(self):
        charge = self.ui.atoms_list_all.currentIndex()
        let = self.ui.atoms_list_all.currentText()
        x = self.ui.FormActionsPreSpinAtomsCoordX.value()
        y = self.ui.FormActionsPreSpinAtomsCoordY.value()
        z = self.ui.FormActionsPreSpinAtomsCoordZ.value()
        position = np.array((x, y, z), dtype=float)
        return charge, let, position

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
        if f_name.endswith('vasprun.xml'):
            vasp_data = VaspDataFromXml(f_name)
        dos_file, e_fermy = ImporterExporter.check_dos_file(f_name)
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

            model_left, fdf_left = ImporterExporter.import_from_file(left_file)
            model_scat, fdf_scat = ImporterExporter.import_from_file(scat_file)
            model_righ, fdf_righ = ImporterExporter.import_from_file(righ_file)

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

            model = AtomicModel()
            model.add_atomic_model(model_left)
            model_scat.move(0, 0, -(left_bord - left_elec_max) + left_dist)
            model.add_atomic_model(model_scat)
            right_bord = model.maxZ()
            model_righ.move(0, 0, (right_bord - right_elec_min) + right_dist)
            model.add_atomic_model(model_righ)

            self.models.append(model)
            self.plot_model(-1)
            self.fill_gui("SWNT-model")
        except Exception as e:
            self.show_error(e)

    def colors_of_atoms(self):
        return self.periodic_table.get_all_colors()

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

    def export_volumeric_data_to_xsf(self):
        try:
            f_name = self.get_file_name_from_save_dialog("XSF files (*.XSF)")
            x1 = self.ui.FormVolDataExportX1.value()
            x2 = self.ui.FormVolDataExportX2.value()
            y1 = self.ui.FormVolDataExportY1.value()
            y2 = self.ui.FormVolDataExportY2.value()
            z1 = self.ui.FormVolDataExportZ1.value()
            z2 = self.ui.FormVolDataExportZ2.value()
            self.export_volumeric_data_to_file(f_name, x1, x2, y1, y2, z1, z2)
        except Exception as e:
            self.show_error(e)

    def export_volumeric_data_to_cube(self):
        try:
            f_name = self.get_file_name_from_save_dialog("cube files (*.cube)")
            x1 = self.ui.FormVolDataExportX1.value()
            x2 = self.ui.FormVolDataExportX2.value()
            y1 = self.ui.FormVolDataExportY1.value()
            y2 = self.ui.FormVolDataExportY2.value()
            z1 = self.ui.FormVolDataExportZ1.value()
            z2 = self.ui.FormVolDataExportZ2.value()
            self.export_volumeric_data_to_file(f_name, x1, x2, y1, y2, z1, z2)
        except Exception as e:
            self.show_error(e)

    def export_volumeric_data_to_file(self, fname, x1, x2, y1, y2, z1, z2):
        self.ui.openGLWidget.volumeric_data_to_file(fname, self.volumeric_data, x1, x2, y1, y2, z1, z2)
        self.work_dir = os.path.dirname(fname)
        self.save_active_folder()

    def volumeric_data_to_file(self, f_name, volumeric_data, x1, x2, y1, y2, z1, z2):
        model = self.ui.openGLWidget.get_model()
        if f_name.find("XSF") >= 0:
            f_name = f_name.split(".")[0]
            text = volumeric_data.toXSFfile(model, f_name, x1, x2, y1, y2, z1, z2)

        if f_name.find("cube") >= 0:
            f_name = f_name.split(".")[0]
            text = volumeric_data.toCUBEfile(model, f_name, x1, x2, y1, y2, z1, z2)
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
        self.check_volumeric_data(file_name)

        self.ui.PropertyAtomAtomDistanceAt1.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistanceAt2.setMaximum(self.ui.openGLWidget.main_model.n_atoms())
        self.ui.PropertyAtomAtomDistance.setText("")

        if helpers.check_format(file_name) == "SIESTAout":
            self.check_dos(file_name)
            self.check_pdos(file_name)
            self.check_bands(file_name)
            self.fill_cell_info(file_name)
            self.fill_energies(file_name)

        if helpers.check_format(file_name) == "SIESTAfdf":
            c = np.linalg.norm(self.ui.openGLWidget.main_model.lat_vector3)
            self.ui.FormActionsPreZSizeFillSpace.setValue(c)

    def fill_energies(self, f_name: str) -> None:
        """Plot energies for steps of output."""
        energies = TSIESTA.energies(f_name)
        self.ui.PyqtGraphWidget.set_xticks(None)

        x_title = "Step"
        y_title = "Energy, eV"
        title = "Energies"

        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        self.ui.PyqtGraphWidget.plot([np.arange(0, len(energies))], [energies], [None], title, x_title, y_title)

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
            mendeley = TPeriodTable()
            c1 = mendeley.get_charge_by_letter(bonds_category[0])
            c2 = mendeley.get_charge_by_letter(bonds_category[1])
        return c1, c2

    def fill_cell_info(self, f_name):
        volume = TSIESTA.volume(f_name)
        energy = TSIESTA.energy_tot(f_name)

        models, fdf_data = ImporterExporter.import_from_file(f_name)
        model = models[-1]
        a = np.linalg.norm(model.lat_vector1)
        b = np.linalg.norm(model.lat_vector2)
        c = np.linalg.norm(model.lat_vector3)
        self.fill_cell_info_row(energy, volume, a, b, c)
        self.ui.FormActionsPreZSizeFillSpace.setValue(c)
        self.work_dir = os.path.dirname(f_name)
        self.save_active_folder()

    def fill_cell_info_row(self, energy, volume, a, b, c):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)
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

    def fit_with(self):   # pragma: no cover
        xf, yf, rf = self.models[self.active_model].fit_with_cylinder()
        self.ui.fit_with_textBrowser.setText("x0 = " + str(round(xf, 4)) + " A\ny0 = " +
                                             str(round(yf, 4)) + " A\nR = " + str(round(rf, 4)) + " A")

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

                ImporterExporter.export_to_file(self.models[self.active_model], file_name)
                self.work_dir = os.path.dirname(file_name)
                self.save_active_folder()
            except Exception as e:
                self.show_error(e)

    def menu_open(self, file_name=False):
        if len(self.models) > 0:   # pragma: no cover
            self.action_on_start = 'Open'
            self.save_property(SETTINGS_FormSettingsActionOnStart, self.action_on_start)
            os.execl(sys.executable, sys.executable, *sys.argv)
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

    def model_rotation(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
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
        self.add_model_and_show(model)
        self.model_orientation_to_form()

    def model_go_to_positive(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model.go_to_positive_coordinates_translate()
        self.add_model_and_show(model)

    def model_go_to_cell(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        print("model_go_to_cell")
        model.move_atoms_to_cell()
        self.add_model_and_show(model)

    def add_model_and_show(self, model):  # pragma: no cover
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_x(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_x()
        self.add_model_and_show(model)

    def model_grow_y(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_y()
        self.add_model_and_show(model)

    def model_grow_z(self):
        if self.ui.openGLWidget.main_model.n_atoms() == 0:
            return
        model = self.ui.openGLWidget.main_model
        model = model.grow_z()
        self.add_model_and_show(model)

    def plot_model(self, value):
        if len(self.models) < value:
            return
        if len(self.models[value].atoms) == 0:
            return
        self.active_model = value
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
        self.ui.openGLWidget.set_atomic_structure(self.models[self.active_model], atoms_color, view_atoms,
                                                  view_atom_numbers, view_box, box_color, view_bonds, bonds_color,
                                                  bond_width, color_of_bonds_by_atoms,
                                                  view_axes, axes_color, contour_width)
        self.prepare_form_actions_combo_pdos_species()
        self.prepare_form_actions_combo_pdos_indexes()
        self.ui.AtomsInSelectedFragment.clear()

        self.show_property_enabling()

    def plot_surface(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        self.ui.openGLWidget.is_view_surface = False
        color_map = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv, maxv = self.ui.FormSettingsColorsFixedMin.value, self.ui.FormSettingsColorsFixedMax.value
        else:
            minv, maxv = self.volumeric_data.min, self.volumeric_data.max
        if self.ui.FormActionsPostCheckSurface.isChecked():
            data = []
            for i in range(0, self.ui.IsosurfaceColorsTable.rowCount()):
                value = float(self.ui.IsosurfaceColorsTable.item(i, 0).text())
                verts, faces, normals = self.volumeric_data.isosurface(value)
                transp = float(self.ui.IsosurfaceColorsTable.cellWidget(i, 1).text())
                if __name__ != 'src_gui4dft.qtbased.mainform':
                    color = self.get_color(color_map, minv, maxv, value, color_scale)
                else:
                    if self.is_scaled_colors_for_surface:
                        color = self.get_color(color_map, minv, maxv, value, color_scale)
                    else:
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
            isovalues_log = np.linspace(math.log10(min_v), math.log10(max_v), n_contours + 2)
            isovalues = []
            for i in range(1, len(isovalues_log) - 1):
                item = isovalues_log[i]
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
            atom_index = range(1, self.ui.openGLWidget.main_model.n_atoms() + 1)
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
            species = (self.ui.FormActionsPDOSSpecieces.toPlainText()).split()
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
        x_title = self.ui.bonds_x_label.text()
        y_title = self.ui.bonds_y_label.text()
        title = self.ui.bonds_title.text()
        self.ui.PyqtGraphWidget.add_histogram(b, num_bins, (0, 0, 255, 90), title, x_title, y_title)

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

            x_title = self.ui.pdos_x_label.text()
            y_title = self.ui.pdos_y_label.text()
            title = self.ui.pdos_title.text()

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
            row_title = item.text().split(':')[1]

            energy, spin_up, spin_down = self.PDOSdata[ind][0], self.PDOSdata[ind][1], self.PDOSdata[ind][2]

            if self.ui.FormActionsCheckPDOS_2.isChecked():
                spin_down *= -1

            x.append(energy)
            y.append(spin_up)
            if self.ui.FormActionsCheckPDOS.isChecked():
                labels.append(row_title + "_up")
            else:
                labels.append(row_title)

            if self.ui.FormActionsCheckPDOS.isChecked():
                x.append(energy)
                y.append(spin_down)
                labels.append(row_title + "_down")

        x_title = self.ui.pdos_x_label.text()
        y_title = self.ui.pdos_y_label.text()
        title = self.ui.pdos_title.text()

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

            x_title = self.ui.bands_x_label.text()
            y_title = self.ui.bands_y_label.text()
            title = self.ui.bands_title.text()

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

        is_fermi_level_show = self.ui.dos_efermy_show.isChecked()
        is_invert_spin_down = self.ui.invert_spin_dos.isChecked()
        is_spin_down_needed = self.ui.plot_two_spins_dos.isChecked()

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

        x_title = self.ui.dos_x_label.text()
        y_title = self.ui.dos_y_label.text()
        title = self.ui.dos_title.text()

        self.ui.PyqtGraphWidget.clear()
        self.ui.PyqtGraphWidget.add_legend()
        self.ui.PyqtGraphWidget.enable_auto_range()
        self.ui.PyqtGraphWidget.plot(x, y, labels, title, x_title, y_title)

        if is_fermi_level_show:
            self.ui.PyqtGraphWidget.add_line(0, 90, 2, Qt.DashLine)
        self.ui.PyqtGraphWidget.add_line(0, 0, 2, Qt.SolidLine)

    def plot_voronoi(self):
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.ui.openGLWidget.is_active():
            r = self.state_Color_Of_Voronoi.split()[0]
            g = self.state_Color_Of_Voronoi.split()[1]
            b = self.state_Color_Of_Voronoi.split()[2]
            color = [float(r) / 255, float(g) / 255, float(b) / 255]
            max_dist = float(self.ui.FormActionsPostTextVoronoiMaxDist.value())
            atom_index, volume = self.ui.openGLWidget.add_voronoi(color, max_dist)
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
        prec = 3
        is_shift = self.ui.optimize_cell_param_shift.isChecked()
        method = self.ui.FormActionsPostComboCellParam.currentText()
        xi = self.ui.FormActionsPostComboCellParamX.currentIndex()
        # LabelX = self.ui.FormActionsPostComboCellParamX.currentText()
        yi = 1

        x = []
        y = []

        for index in range(self.ui.FormActionsPostTableCellParam.rowCount()):
            x.append(float(self.ui.FormActionsPostTableCellParam.item(index, xi).text()))
            y.append(float(self.ui.FormActionsPostTableCellParam.item(index, yi).text()))
        x = np.array(x)
        y = np.array(y)

        if is_shift:
            y -= y.min()

        items = np.zeros((len(x), 2), float)
        items[:, 0] = x
        items[:, 1] = y

        if len(items):
            items = sorted(items, key=itemgetter(0))

            xs, ys = [], []
            text0, text1, text2, text3 = "", "", "", ""
            xs2, ys2 = [], []

            for i in range(0, len(items)):
                xs.append(items[i][0])
                ys.append(items[i][1])

            if method == "Murnaghan":
                image_path = str(Path(__file__).parent / 'images' / 'murnaghan.png')  # path to your image file
                if len(items) > 4:
                    aprox, xs2, ys2 = Calculator.approx_murnaghan(items)
                    text0 = "E(V0)=" + str(round(float(aprox[0]), prec))
                    text1 = "B0=" + str(round(float(aprox[1]), prec))
                    text2 = "B0'=" + str(round(float(aprox[2]), prec))
                    text3 = "V0=" + str(round(float(aprox[3]), prec))

            elif method == "BirchMurnaghan":
                image_path = str(Path(__file__).parent / 'images' / 'murnaghanbirch.png')  # path to your image file
                if len(items) > 4:
                    aprox, xs2, ys2 = Calculator.approx_birch_murnaghan(items)
                    text0 = "E(V0)=" + str(round(float(aprox[0]), prec))
                    text1 = "B0=" + str(round(float(aprox[1]), prec))
                    text2 = "B0'=" + str(round(float(aprox[2]), prec))
                    text3 = "V0=" + str(round(float(aprox[3]), prec))

            else:  # method == "Parabola":
                image_path = str(Path(__file__).parent / 'images' / 'parabola.png')
                if len(items) > 2:
                    aprox, xs2, ys2 = Calculator.approx_parabola(items)
                    text0 = "a=" + str(round(float(aprox[2]), prec))
                    text1 = "b=" + str(round(float(aprox[1]), prec))
                    text2 = "c=" + str(round(float(aprox[0]), prec))
                    text3 = "x0=" + str(round(-float(aprox[1]) / float(2 * aprox[2]), prec))

            self.ui.FormActionsPostLabelCellParamOptimExpr.setText(text0)
            self.ui.FormActionsPostLabelCellParamOptimExpr2.setText(text1)
            self.ui.FormActionsPostLabelCellParamOptimExpr3.setText(text2)
            self.ui.FormActionsPostLabelCellParamOptimExpr4.setText(text3)

            self.plot_cell_approx(image_path)
            self.plot_curv_and_points(xs, ys, xs2, ys2)
        self.ui.PyqtGraphWidget.update()

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
        image_profile = image_profile.scaled(320, 54, aspectRatioMode=Qt.KeepAspectRatio,
                                             transformMode=Qt.SmoothTransformation)
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
        self.ui.atoms_list_all.setCurrentIndex(element)
        self.ui.FormActionsPreSpinAtomsCoordX.setValue(position[0])
        self.ui.FormActionsPreSpinAtomsCoordX.update()
        self.ui.FormActionsPreSpinAtomsCoordY.setValue(position[1])
        self.ui.FormActionsPreSpinAtomsCoordY.update()
        self.ui.FormActionsPreSpinAtomsCoordZ.setValue(position[2])
        self.ui.FormActionsPreSpinAtomsCoordZ.update()

    def selected_atom_changed(self, selected):
        selected_atom = selected[0]
        if selected_atom == -1:
            self.history_of_atom_selection = []
        else:
            self.history_of_atom_selection.append(selected_atom)

        text = ""
        if selected_atom >= 0:
            model = self.models[self.active_model]
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
        if len(self.models) == 0:
            return
        try:
            model = self.ui.openGLWidget.get_model()
            text = self.fdf_data.get_all_data(model, self.coord_type, self.units_type, self.lattice_type)
            self.ui.FormActionsPreTextFDF.setText(text)
        except Exception:
            print("There are no atoms in the model")

    def qe_data_to_form(self):
        if len(self.models) == 0:
            return
        print("TODO")

    def poscar_data_to_form(self):
        if len(self.models) == 0:
            return
        try:
            model = self.ui.openGLWidget.get_model()
            text = model_to_vasp_poscar(model)
            self.ui.FormActionsPreTextFDF.setText(text)
        except Exception:
            print("There are no atoms in the model")

    def data_from_form_to_input_file(self):  # pragma: no cover
        try:
            text = self.ui.FormActionsPreTextFDF.toPlainText()
            if len(text) > 0:
                file_mask = "FDF files (*.fdf);;VASP POSCAR file (*.POSCAR)"
                file_mask += ";;Crystal d12 (*.d12)"
                fname = self.get_file_name_from_save_dialog(file_mask)
                if fname is not None:
                    helpers.write_text_to_file(fname, text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_script_create(self):  # pragma: no cover
        if len(self.models) == 0:
            return
        try:
            model2 = deepcopy(self.models[self.active_model])
            text = ase.ase_raman_and_ir_script_create(model2, self.fdf_data)

            if len(text) > 0:
                name = self.get_file_name_from_save_dialog("Python file (*.py)")
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)

    def ase_raman_and_ir_parse(self):
        try:
            fname = self.get_file_name_from_open_dialog("All files (*.*)")
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

    def d12_1D_to_form(self):  # pragma: no cover
        if len(self.models) == 0:
            return
        try:
            model = self.models[self.active_model]
            text = model_1d_to_d12(model)
            if len(text) > 0:
                self.ui.FormActionsPreTextFDF.setText(text)
        except Exception as e:
            self.show_error(e)

    def d12_2D_to_form(self):  # pragma: no cover
        if len(self.models) == 0:
            return
        try:
            model = self.models[self.active_model]
            text = model_2d_to_d12(model)
            if len(text) > 0:
                self.ui.FormActionsPreTextFDF.setText(text)
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

    def parse_volumeric_data(self):
        if len(self.ui.FormActionsPostList3DData.selectedItems()) > 0:
            selected = self.ui.FormActionsPostList3DData.selectedItems()[0].text()
            self.parse_volumeric_data_selected(selected)

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

    def parse_volumeric_data2(self, filename: str = ""):
        try:
            if not filename:  # pragma: no cover
                filename = self.get_file_name_from_open_dialog("All files (*.*)")
            if len(filename) > 0:
                if filename.endswith(".XSF"):
                    self.volumeric_data2 = XSF()
                if filename.endswith(".cube"):
                    self.volumeric_data2 = GaussianCube()
                if self.volumeric_data2.parse(filename):
                    self.fill_volumeric_data(self.volumeric_data2, self.ui.FormActionsPostTreeSurface2)

                self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(True)
                self.ui.FormActionsPosEdit3DData2.setText(filename)
                self.clear_form_isosurface_data2_n()
                self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
                self.ui.CalculateTheVolumericDataSum.setEnabled(False)
                self.ui.ExportTheVolumericDataXSF.setEnabled(False)
                self.ui.ExportTheVolumericDataCube.setEnabled(False)
                self.ui.VolumrricDataGrid2.setTitle("Grid")
        except Exception as e:  # pragma: no cover
            self.show_error(e)

    def set_xsf_x_position(self):
        value = int(self.ui.FormActionsPostSliderContourYZ.value())
        self.ui.FormActionsPostLabelContourYZposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourYZ.maximum()))

    def set_xsf_y_position(self):
        value = int(self.ui.FormActionsPostSliderContourXZ.value())
        self.ui.FormActionsPostLabelContourXZposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourXZ.maximum()))

    def set_xsf_z_position(self):
        value = int(self.ui.FormActionsPostSliderContourXY.value())
        self.ui.FormActionsPostLabelContourXYposition.setText(
            "Slice " + str(value) + " among " + str(self.ui.FormActionsPostSliderContourXY.maximum()))

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

    def create_graphene(self):
        leng, m, n = self.model_2d_parameters()
        model = Graphene(n, m, leng)
        self.models.append(model)
        self.plot_model(-1)
        self.fill_gui("Graphene-model")

    def create_2d_bn(self):
        leng, m, n = self.model_2d_parameters()
        model = BNplane(n, m, leng)
        self.models.append(model)
        self.plot_model(-1)
        self.fill_gui("BN-model")

    def model_2d_parameters(self):
        n = self.ui.FormActionsPreLineGraphene_n.value()
        m = self.ui.FormActionsPreLineGraphene_m.value()
        leng = self.ui.FormActionsPreLineGraphene_len.value()
        return leng, m, n

    def generate_3d_bulk(self):
        """ASE bulk interface"""
        name = self.ui.crystalstructure_3d_name.text()
        crystalstructure = self.ui.crystalstructure_3d.currentText()
        if crystalstructure == "Select":
            crystalstructure = None
        a = None if self.ui.crystalstructure_3d_a_dont_use.isChecked() else self.ui.crystalstructure_3d_a.value()
        b = None if self.ui.crystalstructure_3d_b_dont_use.isChecked() else self.ui.crystalstructure_3d_b.value()
        c = None if self.ui.crystalstructure_3d_c_dont_use.isChecked() else self.ui.crystalstructure_3d_c.value()
        alpha = None if self.ui.crystalstructure_3d_alpha_dont_use.isChecked() else \
            self.ui.crystalstructure_3d_alpha.value()
        covera = None if self.ui.crystalstructure_3d_covera_dont_use.isChecked() else \
            self.ui.crystalstructure_3d_covera.value()
        orthorhombic = self.ui.crystalstructure_3d_orthorhombic.isChecked()
        try:
            atoms = bulk(name, crystalstructure=crystalstructure, a=a, b=b, c=c, alpha=alpha, covera=covera, u=None,
                         orthorhombic=orthorhombic, cubic=not orthorhombic, basis=None)
        except Exception as e:
            print(str(e))

        model = ase.from_ase_atoms_to_atomic_model(atoms)
        self.models.append(model)
        self.plot_model(-1)
        self.fill_gui(name)

    def get_0d_molecula_list(self):
        from ase.collections import g2
        molecules = g2.names
        molecules.append("Be2")
        molecules.append("C7NH5")
        molecules.append("BDA")
        molecules.append("biphenyl")
        molecules.append("C60")
        molecules_db = QStandardItemModel()
        for mol in molecules:
            molecules_db.appendRow(QStandardItem(mol))
        self.ui.molecula_list.setModel(molecules_db)

    def generate_0d_molecula(self):
        name = self.ui.molecula_list.currentText()
        if len(name) == 0:
            return
        atoms = molecule(name)
        model = ase.from_ase_atoms_to_atomic_model(atoms)
        self.models.append(model)
        self.plot_model(-1)
        self.fill_gui(name)

    def generate_0d_cluster(self):
        name = "Cluster"
        surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
        layers = [6, 9, 5]
        lc = 3.61000
        atoms = FaceCenteredCubic('Cu', surfaces, layers, latticeconstant=lc)
        model = ase.from_ase_atoms_to_atomic_model(atoms)
        self.models.append(model)
        self.plot_model(-1)
        self.fill_gui(name)

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
