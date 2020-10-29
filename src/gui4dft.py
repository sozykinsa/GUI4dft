# -*- coding: utf-8 -*-
import sys
import os
import math
from copy import deepcopy
from operator import itemgetter
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QTreeWidgetItemIterator
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
from AdvancedTools import TFDFFile
from AdvancedTools import TPeriodTable
from AdvancedTools import TSWNT
from AdvancedTools import TCapedSWNT
from AdvancedTools import TGraphene
from AdvancedTools import TAtomicModel
from AdvancedTools import TSIESTA
from AdvancedTools import Helpers
from AdvancedTools import TCalculators as Calculator
from TGui import GuiOpenGL
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import myfigureoptions
import numpy as np
import matplotlib.pyplot as plt
from TInterface import Importer
from TInterface import TXSF
from TInterface import TVolumericData
from TInterface import TGaussianCube
from TInterface import Image3Dexporter
from TInterface import AtomsIdentifier
from form import Ui_MainWindow as Ui_form
from about import Ui_DialogAbout as Ui_about
import xml.etree.ElementTree as ET

class mainWindow(QMainWindow):
    def __init__(self, *args):
        super(mainWindow, self).__init__(*args)
        self.ui = Ui_form()
        self.ui.setupUi(self)
        self.models = []
        selected_atom_info = [self.ui.FormActionsPreComboAtomsList, self.ui.FormActionsPreSpinAtomsCoordX, self.ui.FormActionsPreSpinAtomsCoordY, self.ui.FormActionsPreSpinAtomsCoordZ, self.ui.AtomPropertiesText]
        self.MainForm = GuiOpenGL(self.ui.openGLWidget, self.ui.FormSettingsViewCheckAtomSelection, selected_atom_info, 1)
        self.FDFData = TFDFFile()
        self.VolumericData = TVolumericData()
        self.VolumericData2 = TVolumericData()  # only for volumeric data difference
        self.PDOSdata = []
        self.filename = ""
        self.colors_cash = {}
        self.table_header_stylesheet = "::section{Background-color:rgb(194,169,226)}"

    def setupUI(self):
        self.load_settings()
        self.ui.actionOpen.triggered.connect(self.menu_open)
        self.ui.actionExport.triggered.connect(self.menu_export)
        self.ui.actionOrtho.triggered.connect(self.menu_ortho)
        self.ui.actionPerspective.triggered.connect(self.menu_perspective)
        self.ui.actionShowBox.triggered.connect(self.menu_show_box)
        self.ui.actionHideBox.triggered.connect(self.menu_hide_box)
        self.ui.actionAbout.triggered.connect(self.menu_about)

        self.ui.FormModelComboModels.currentIndexChanged.connect(self.model_to_screen)
        self.ui.FormActionsPostTreeSurface.itemSelectionChanged.connect(self.type_of_surface)
        self.ui.PropertyForColorOfAtoms.currentIndexChanged.connect(self.color_atoms_with_property)
        self.ui.ColorAtomsWithProperty.stateChanged.connect(self.color_atoms_with_property)

        self.ui.FormActionsPreRadioSWNT.toggled.connect(self.swnt_type1_selected)
        self.ui.FormActionsPreRadioSWNTcap.toggled.connect(self.swnt_type2_selected)
        self.ui.FormActionsPreRadioSWNTcap_2.toggled.connect(self.swnt_type2_selected)

        self.ui.ActivateFragmentSelectionModeCheckBox.toggled.connect(self.activate_fragment_selection_mode)
        self.ui.ActivateFragmentSelectionTransp.valueChanged.connect(self.activate_fragment_selection_mode)
        
        #buttons
        self.ui.FileBrouserOpenFile.clicked.connect(self.menu_open)
        self.ui.FormActionsPostButPlotBondsHistogram.clicked.connect(self.plot_bonds_histogram)
        self.ui.FormActionsPreButFDFGenerate.clicked.connect(self.fdf_data_to_form)
        self.ui.FormActionsPreButFDFToFile.clicked.connect(self.fdf_data_from_form_to_file)
        self.ui.FormActionsPreButFillSpace.clicked.connect(self.fill_space)
        self.ui.FormActionsPreButSWNTGenerate.clicked.connect(self.create_swnt)
        self.ui.FormActionsPreButGrapheneGenerate.clicked.connect(self.create_graphene)
        self.ui.FormActionsPostButSurface.clicked.connect(self.plot_surface)
        self.ui.FormActionsPostButSurfaceParse.clicked.connect(self.parse_volumeric_data)
        self.ui.FormActionsPostButSurfaceParse2.clicked.connect(self.parse_volumeric_data2)
        self.ui.FormActionsPostButSurfaceLoadData.clicked.connect(self.volumeric_data_load)
        self.ui.FormActionsPostButSurfaceLoadData2.clicked.connect(self.volumeric_data_load2)
        self.ui.CalculateTheVolumericDataDifference.clicked.connect(self.volumeric_data_difference)
        self.ui.ExportTheVolumericDataDifference.clicked.connect(self.export_volumeric_data_difference)
        self.ui.FormActionsPostButContour.clicked.connect(self.plot_contour)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.ColorAtomDialogButton.clicked.connect(self.select_atom_color)
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

        self.ui.changeFragment1StatusByX.clicked.connect(self.change_fragment1_status_by_X)
        self.ui.changeFragment1StatusByY.clicked.connect(self.change_fragment1_status_by_Y)
        self.ui.changeFragment1StatusByZ.clicked.connect(self.change_fragment1_status_by_Z)
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

        self.ui.FormActionsPostButVoronoi.clicked.connect(self.plot_voronoi)
        
        self.ui.FormActionsPostButOptimizeCellParam.clicked.connect(self.plot_volume_param_energy)
        
        self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self))

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        Mendeley = TPeriodTable()
        atoms_list = Mendeley.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))
        self.ui.FormActionsPreComboAtomsList.setModel(model)

        # sliders
        self.ui.FormActionsPostSliderContourXY.valueChanged.connect(self.set_xsf_z_position)
        self.ui.FormActionsPostSliderContourXZ.valueChanged.connect(self.set_xsf_y_position)
        self.ui.FormActionsPostSliderContourYZ.valueChanged.connect(self.set_xsf_x_position)

        self.ui.FormModelTableAtoms.setColumnCount(4)
        self.ui.FormModelTableAtoms.setHorizontalHeaderLabels(["Atom", "x", "y","z"])
        self.ui.FormModelTableAtoms.setColumnWidth(0, 40)
        self.ui.FormModelTableAtoms.setColumnWidth(1, 80)
        self.ui.FormModelTableAtoms.setColumnWidth(2, 80)
        self.ui.FormModelTableAtoms.setColumnWidth(3, 80)
        self.ui.FormModelTableAtoms.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormModelTableAtoms.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.ui.FormModelTableProperties.setColumnCount(2)
        self.ui.FormModelTableProperties.setHorizontalHeaderLabels(["Property", "Value"])
        self.ui.FormModelTableProperties.setColumnWidth(0, 85)
        self.ui.FormModelTableProperties.setColumnWidth(1, 240)
        self.ui.FormModelTableProperties.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormModelTableProperties.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        self.ui.IsosurfaceColorsTable.setColumnCount(2)
        self.ui.IsosurfaceColorsTable.setHorizontalHeaderLabels(["Value","Transparancy"])
        self.ui.IsosurfaceColorsTable.setColumnWidth(0, 120)
        self.ui.IsosurfaceColorsTable.setColumnWidth(1, 150)
        self.ui.IsosurfaceColorsTable.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.IsosurfaceColorsTable.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        CellPredictionType = QStandardItemModel()
        CellPredictionType.appendRow(QStandardItem("Murnaghan"))
        CellPredictionType.appendRow(QStandardItem("BirchMurnaghan"))
        CellPredictionType.appendRow(QStandardItem("Parabola"))
        self.ui.FormActionsPostComboCellParam.setModel(CellPredictionType)

        FormSettingsPreferredCoordinatesType = QStandardItemModel()
        FormSettingsPreferredCoordinatesType.appendRow(QStandardItem("Zmatrix Cartesian"))
        FormSettingsPreferredCoordinatesType.appendRow(QStandardItem("Fractional"))
        self.ui.FormSettingsPreferredCoordinates.setModel(FormSettingsPreferredCoordinatesType)
        self.ui.FormSettingsPreferredCoordinates.setCurrentText(self.CoordType)
        self.ui.FormSettingsPreferredCoordinates.currentIndexChanged.connect(self.save_state_FormSettingsPreferredCoordinates)

        FormSettingsPreferredLatticeType = QStandardItemModel()
        FormSettingsPreferredLatticeType.appendRow(QStandardItem("LatticeParameters"))
        FormSettingsPreferredLatticeType.appendRow(QStandardItem("LatticeVectors"))
        self.ui.FormSettingsPreferredLattice.setModel(FormSettingsPreferredLatticeType)
        self.ui.FormSettingsPreferredLattice.setCurrentText(self.LatticeType)
        self.ui.FormSettingsPreferredLattice.currentIndexChanged.connect(self.save_state_FormSettingsPreferredLattice)

        self.ui.FormActionsPostComboBonds.currentIndexChanged.connect(self.fill_bonds)

        EnergyUnitsType = QStandardItemModel()
        EnergyUnitsType.appendRow(QStandardItem("eV"))
        #EnergyUnitsType.appendRow(QStandardItem("Ry"))
        self.ui.FormActionsPostComboCellParamEnergy.setModel(EnergyUnitsType)

        LengUnitsType = QStandardItemModel()
        LengUnitsType.appendRow(QStandardItem("A"))
        #LengUnitsType.appendRow(QStandardItem("Bohr"))
        #LengUnitsType.appendRow(QStandardItem("nm"))
        self.ui.FormActionsPostComboCellParamLen.setModel(LengUnitsType)

        SWNTindType = QStandardItemModel()
        SWNTindType.appendRow(QStandardItem("(6,6)"))
        SWNTindType.appendRow(QStandardItem("(10,0)"))
        self.ui.FormActionsPreComboSWNTind.setModel(SWNTindType)

        FillSpaceModel = QStandardItemModel()
        FillSpaceModel.appendRow(QStandardItem("cylinder"))
        #FillSpaceModel.appendRow(QStandardItem("parallelepiped"))
        self.ui.FormActionsPreComboFillSpace.setModel(FillSpaceModel)

        self.prepare_FormActionsComboPDOSIndexes()
        self.prepare_FormActionsComboPDOSspecies()

        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSn, 0, 8)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSl, 0, 7)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSm, -7, 7)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSz, 1, 5)

        ColorType = QStandardItemModel()
        ColorTypes = [ 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for t in ColorTypes:
            ColorType.appendRow(QStandardItem(t))

        self.ui.FormSettingsColorsScale.setModel(ColorType)
        self.ui.FormSettingsColorsScale.setCurrentText(self.ColorType)

        ColorTypeScale = QStandardItemModel()
        ColorTypeScale.appendRow(QStandardItem("Linear"))
        ColorTypeScale.appendRow(QStandardItem("Log"))
        self.ui.FormSettingsColorsScaleType.setModel(ColorTypeScale)
        self.ui.FormSettingsColorsScaleType.setCurrentText(self.ColorTypeScale)

        self.ui.FormActionsPostTableCellParam.setColumnCount(5)
        self.ui.FormActionsPostTableCellParam.setHorizontalHeaderLabels(["volume", "Energy","a","b","c"])
        self.ui.FormActionsPostTableCellParam.setColumnWidth(0, 60)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(1, 60)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(2, 50)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(3, 50)
        self.ui.FormActionsPostTableCellParam.setColumnWidth(4, 50)
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
        self.ui.FormActionsPosTableBonds.setColumnWidth(0, 100)
        self.ui.FormActionsPosTableBonds.setColumnWidth(1, 150)
        self.ui.FormActionsPosTableBonds.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.FormActionsPosTableBonds.verticalHeader().setStyleSheet(self.table_header_stylesheet)

        openAction = QAction(QIcon('./images/Open.jpg'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.menu_open)
        self.ui.toolBar.addAction(openAction)

        modelFile = QFileSystemModel()
        modelFile.setRootPath((QDir.rootPath()))
        self.ui.FileBrouserTree.setModel(modelFile)
        self.ui.FileBrouserTree.selectionModel().selectionChanged.connect(self.file_brouser_selection)

        SaveImageToFileAction = QAction(QIcon('./images/Save3D.jpg'), 'SaveFigure3D', self)
        SaveImageToFileAction.triggered.connect(self.save_image_to_file)
        self.ui.toolBar.addAction(SaveImageToFileAction)

        Save2DImageToFileAction = QAction(QIcon('./images/Save2D.jpg'), 'SaveDataFromFigure', self)
        Save2DImageToFileAction.triggered.connect(self.save_data_from_figure2d)
        self.ui.toolBar.addAction(Save2DImageToFileAction)

    def activate_fragment_selection_mode(self):
        if self.ui.ActivateFragmentSelectionModeCheckBox.isChecked() == True:
            self.MainForm.setSelectedFragmentMode(self.ui.AtomsInSelectedFragment, self.ui.ActivateFragmentSelectionTransp.value())
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
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        if Importer.checkFormat(fname) == "SIESTAout":
            self.fill_cell_info(fname)

    def add_cell_param_row(self):
        i = self.ui.FormActionsPostTableCellParam.rowCount()+1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)

    def add_data_cell_param(self):
        """ add cell params from file"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        self.WorkDir = os.path.dirname(fname)

        if os.path.exists(fname):
            f = open(fname)
            rows = f.readlines()

            for i in range(2,len(rows)):
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

    def add_dos_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        self.WorkDir = os.path.dirname(fname)
        self.check_dos(fname)


    def add_isosurface_color_to_table(self):
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        i = self.ui.IsosurfaceColorsTable.rowCount() + 1
        value = self.ui.FormActionsPostLabelSurfaceValue.text()
        self.ui.IsosurfaceColorsTable.setRowCount(i)  # и одну строку в таблице
        color_cell = QTableWidgetItem(value)
        color_cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        self.ui.IsosurfaceColorsTable.setItem(i - 1, 0, color_cell)
        transp_cell = QDoubleSpinBox()
        transp_cell.setRange(0,1)
        transp_cell.setValue(1)
        transp_cell.setSingleStep(0.1)
        transp_cell.setDecimals(2)
        transp_cell.setLocale(QLocale(QLocale.English))
        transp_cell.setMaximumWidth(145)
        self.ui.IsosurfaceColorsTable.setCellWidget(i - 1, 1, transp_cell)
        minv, maxv = self.volumeric_data_range()
        color = self.get_color(cmap, minv, maxv, float(value), color_scale)
        self.ui.IsosurfaceColorsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], color[3]))

        self.ui.FormActionsPostButSurface.setEnabled(True)
        self.ui.FormActionsPostButSurfaceDelete.setEnabled(True)


    def add_left_electrode_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.WorkDir = os.path.dirname(fname)
            self.save_active_Folder()
            self.ui.FormActionsPreLeftElectrode.setText(fname)

    def add_right_electrode_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.WorkDir = os.path.dirname(fname)
            self.save_active_Folder()
            self.ui.FormActionsPreRightElectrode.setText(fname)

    def add_scat_region_file(self):
        fname = self.get_fdf_file_name()
        if os.path.exists(fname):
            self.WorkDir = os.path.dirname(fname)
            self.save_active_Folder()
            self.ui.FormActionsPreScatRegion.setText(fname)


    def atom_add(self):
        self.MainForm.add_new_atom()

    def atom_delete(self):
        self.MainForm.delete_selected_atom()

    def atom_modify(self):
        self.MainForm.modify_selected_atom()
        self.models.append(self.MainForm.MainModel)
        self.model_to_screen(-1)

    def clear_form(self):
        self.clear_form_postprocessing()
        self.clear_form_isosurface()

    def clear_form_postprocessing(self):
        self.ui.FormActionsPostTableCellParam.setRowCount(0)
        self.ui.FormActionsPosTableBonds.setRowCount(0)
        self.ui.FormActionsTabeDOSProperty.setRowCount(0)
        self.ui.FormActionsListPDOS.clear()
        self.ui.FormActionsButtonPlotBANDS.setEnabled(False)
        self.ui.FormActionsPreTextFDF.setText("")

    def clear_form_isosurface(self):
        self.clear_form_isosurface_data1()
        self.clear_form_isosurface_data2()
        self.clear_form_isosurface_isosurface()

    def clear_form_isosurface_data1(self):
        self.ui.FormActionsPostList3DData.clear()
        self.ui.FormActionsPostTreeSurface.clear()
        self.ui.FormActionsPostLabelSurfaceMin.setText("")
        self.ui.FormActionsPostLabelSurfaceMax.setText("")

    def clear_form_isosurface_data2(self):
        self.clear_form_isosurface_data2_N()

    def clear_form_isosurface_data2_N(self):
        self.ui.FormActionsPostLabelSurfaceNx.setText("")
        self.ui.FormActionsPostLabelSurfaceNy.setText("")
        self.ui.FormActionsPostLabelSurfaceNz.setText("")

    def clear_form_isosurface_isosurface(self):
        self.ui.IsosurfaceColorsTable.setRowCount(0)


    def check_pdos(self, fname):
        PDOSfile = Importer.CheckPDOSfile(fname)
        if PDOSfile != False:
            self.ui.FormActionsLinePDOSfile.setText(PDOSfile)
            self.ui.FormActionsButtonPlotPDOS.setEnabled(True)

    def check_bands(self, fname):
        BANDSfile = Importer.CheckBANDSfile(fname)
        if BANDSfile != False:
            self.ui.FormActionsLineBANDSfile.setText(BANDSfile)
            self.ui.FormActionsButtonParseBANDS.setEnabled(True)

    def check_dos(self, fname):
        DOSfile = Importer.CheckDOSfile(fname)
        if DOSfile != False:
            eFermy = TSIESTA.FermiEnergy(fname)
            self.ui.FormActionsEditPDOSefermi.setText(str(eFermy))

            i = self.ui.FormActionsTabeDOSProperty.rowCount() + 1

            self.ui.FormActionsTabeDOSProperty.setRowCount(i)

            line = "..." + str(DOSfile)[-15:]
            QTabWidg = QTableWidgetItem(line)
            QTabWidg.setToolTip(DOSfile)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 0, QTabWidg)
            self.ui.FormActionsTabeDOSProperty.setItem(i - 1, 1, QTableWidgetItem(str(eFermy)))
            self.ui.FormActionsTabeDOSProperty.update()

    def check_volumeric_data(self, fname):
        files = []
        if fname.endswith(".XSF"):
            files.append(fname)
        if fname.endswith(".cube"):
            files.append(fname)

        if fname.endswith(".out") or fname.endswith(".OUT"):
            label = TSIESTA.SystemLabel(fname)
            Dir = os.path.dirname(fname)
            dirs, content = Helpers.getsubs(Dir)
            for posFile in content:
                F = posFile.split("\\")
                if len(F) > 1:
                    F = F[1]
                    if F.startswith(label) and F.endswith(".cube"):
                        files.append(Dir + "/" + F)

            files.append(Dir + "/" + label + ".XSF")
        for file in files:
            if os.path.exists(file):
                self.ui.FormActionsPostList3DData.addItems([file])
                self.ui.FormActionsPostButSurfaceParse.setEnabled(True)
            self.ui.FormActionsPostList3DData.update()

    def change_fragment1_status_by_X(self):
        xmin = self.ui.xminborder.value()
        xmax = self.ui.xmaxborder.value()
        for at in self.MainForm.MainModel.atoms:
            if (at.x >= xmin) and (at.x <= xmax):
                at.fragment1 = True
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def change_fragment1_status_by_Y(self):
        ymin = self.ui.yminborder.value()
        ymax = self.ui.ymaxborder.value()
        for at in self.MainForm.MainModel.atoms:
            if (at.y >= ymin) and (at.y <= ymax):
                at.fragment1 = True
        self.MainForm.atoms_of_selected_fragment_to_form()
        self.MainForm.update_view()

    def change_fragment1_status_by_Z(self):
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
        left_file = self.ui.FormActionsPreLeftElectrode.text()
        scat_file = self.ui.FormActionsPreScatRegion.text()
        righ_file = self.ui.FormActionsPreRightElectrode.text()

        model_left, fdf_left = Importer.Import(left_file)
        model_scat, fdf_scat = Importer.Import(scat_file)
        model_righ, fdf_righ = Importer.Import(righ_file)

        model_left = model_left[0]
        model_scat = model_scat[0]
        model_righ = model_righ[0]

        left_elec_max = model_left.maxZ()
        left_bord = model_scat.minZ()

        right_elec_min = model_righ.minZ()

        left_dist = self.ui.FormActionsPreSpinLeftElectrodeDist.value()
        righ_dist = self.ui.FormActionsPreSpinRightElectrodeDist.value()

        scat_rotation = self.ui.FormActionsPreSpinScatRotation.value()

        model = TAtomicModel()
        """model_left.move(0,0,0)"""
        model.add_atomic_model(model_left)
        model_scat.rotateZ(scat_rotation)
        model_scat.move(0, 0, -(left_bord - left_elec_max) + left_dist)
        model.add_atomic_model(model_scat)
        righ_bord = model.maxZ()
        model_righ.move(0, 0, (righ_bord - right_elec_min) + righ_dist)
        model.add_atomic_model(model_righ)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("SWNT-model")

    def colors_of_atoms(self):
        atomscolor = [ self.ui.ColorsOfAtomsTable.item(0, 0).background().color().getRgbF()]
        for i in range(0, self.ui.ColorsOfAtomsTable.rowCount()):
            col = self.ui.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
        return atomscolor


    def create_checkable_item(self, QuantumNumbersList, value):
        item = QStandardItem(value)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
        QuantumNumbersList.appendRow(item)


    def delete_cell_param_row(self):
        row = self.ui.FormActionsPostTableCellParam.currentRow()
        self.ui.FormActionsPostTableCellParam.removeRow(row)

    def delete_isosurface_color_from_table(self):
        row = self.ui.IsosurfaceColorsTable.currentRow()
        self.ui.IsosurfaceColorsTable.removeRow(row)

    def edit_cell(self):
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


    def export_volumeric_data_difference(self):
        """ not implemented """
        fname = QFileDialog.getSaveFileName(self, 'Save File', self.WorkDir,"XSF files (*.XSF)")[0]
        self.MainForm.volumeric_data_to_file(fname, self.VolumericData)
        self.WorkDir = os.path.dirname(fname)
        self.save_active_Folder()

    def fill_gui(self, title = "" ):
        fname = self.filename
        if title == "":
            self.fill_file_name(fname)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()
        self.check_volumeric_data(fname)
        if Importer.checkFormat(fname) == "SIESTAout":
            self.check_dos(fname)
            self.check_pdos(fname)
            self.check_bands(fname)
            self.fill_cell_info(fname)

        if Importer.checkFormat(fname) == "SIESTAfdf":
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
        self.ui.FormModelTableAtoms.setRowCount(len(model))  # и одну строку в таблице

        for i in range(0, len(model)):
            self.ui.FormModelTableAtoms.setItem(i, 0, QTableWidgetItem(model[i].let))
            self.ui.FormModelTableAtoms.setItem(i, 1, QTableWidgetItem(str(round(model[i].x, 5))))
            self.ui.FormModelTableAtoms.setItem(i, 2, QTableWidgetItem(str(round(model[i].y, 5))))
            self.ui.FormModelTableAtoms.setItem(i, 3, QTableWidgetItem(str(round(model[i].z, 5))))

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

        self.ui.FormModifyCellEditA1.setText(str(model.LatVect1[0]))
        self.ui.FormModifyCellEditA2.setText(str(model.LatVect1[1]))
        self.ui.FormModifyCellEditA3.setText(str(model.LatVect1[2]))
        self.ui.FormModifyCellEditB1.setText(str(model.LatVect2[0]))
        self.ui.FormModifyCellEditB2.setText(str(model.LatVect2[1]))
        self.ui.FormModifyCellEditB3.setText(str(model.LatVect2[2]))
        self.ui.FormModifyCellEditC1.setText(str(model.LatVect3[0]))
        self.ui.FormModifyCellEditC2.setText(str(model.LatVect3[1]))
        self.ui.FormModifyCellEditC3.setText(str(model.LatVect3[2]))

    def file_brouser_selection(self, selected, deselected):
        self.IndexOfFileToOpen = selected.indexes()[0]
        text = str(self.ui.FileBrouserTree.model().filePath(self.IndexOfFileToOpen))
        self.ui.FileBrouserOpenLine.setText(text)
        self.ui.FileBrouserOpenLine.update()

    def fill_volumeric_data(self, data, tree = " "):
        if tree == " ":
            tree = self.ui.FormActionsPostTreeSurface
        type = data.type
        data = data.blocks
        self.clearQTreeWidget(tree)

        if type == "TXSF":
            for dat in data:
                text = ((dat[0].title).split('_')[3]).split(':')[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text) + "3D")
                for da in dat:
                    ch = text + ':' + (da.title).split(':')[1]
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(ch))

        if type == "TGaussianCube":
            for dat in data:
                text = dat[0].title.split(".cube")[0]
                parent = QTreeWidgetItem(tree)
                parent.setText(0, "{}".format(text))
                for da in dat:
                    ch = text
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(ch))
        tree.show()

    def fill_bonds(self):
        c1, c2 = self.fill_bonds_charges()
        bonds = self.MainForm.MainModel.Bonds()
        self.ui.FormActionsPosTableBonds.setRowCount(0)

        mean = 0
        n = 0

        for bond in bonds:
            if ((c1 == 0) or (c2 == 0)) or ((c1 == bond[0]) and (c2 == bond[1])) or ((c1 == bond[1]) and (c2 == bond[2])):
                self.ui.FormActionsPosTableBonds.setRowCount(self.ui.FormActionsPosTableBonds.rowCount()+1)
                s = str(bond[3]) + str(bond[4]) + "-" + str(bond[5]) + str(bond[6])
                self.ui.FormActionsPosTableBonds.setItem(n, 0, QTableWidgetItem(s))
                self.ui.FormActionsPosTableBonds.setItem(n, 1, QTableWidgetItem(str(bond[2])))
                mean += bond[2]
                n += 1
        if n > 0:
            self.ui.FormActionsPostLabelMeanBond.setText("Mean value: " + str(round(mean / n,5)))

    def fill_bonds_charges(self):
        bonds_category = self.ui.FormActionsPostComboBonds.currentText()
        if bonds_category == "All":
            c1 = 0
            c2 = 0
        else:
            bonds_category = bonds_category.split('-')
            Mendeley = TPeriodTable()
            c1 = Mendeley.get_charge_by_letter(bonds_category[0])
            c2 = Mendeley.get_charge_by_letter(bonds_category[1])
        return c1, c2

    def fill_cell_info(self, fname):
        Volume = TSIESTA.volume(fname)
        Energy = TSIESTA.Etot(fname)

        """model, FDFData = Importer.Import(fname)"""
        model = self.models[-1]
        a = model.get_LatVect1_norm()
        b = model.get_LatVect2_norm()
        c = model.get_LatVect3_norm()
        self.fill_cell_info_row(Energy, Volume, a, b, c)
        self.ui.FormActionsPreZSizeFillSpace.setValue(c)
        self.WorkDir = os.path.dirname(fname)
        self.save_active_Folder()

    def fill_cell_info_row(self, Energy, Volume, a, b, c):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)  # и одну строку в таблице
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 0, QTableWidgetItem(str(Volume)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 1, QTableWidgetItem(str(Energy)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 2, QTableWidgetItem(str(a)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 3, QTableWidgetItem(str(b)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 4, QTableWidgetItem(str(c)))

    def get_bonds(self):
        BondsType = QStandardItemModel()
        BondsType.appendRow(QStandardItem("All"))
        bonds = self.MainForm.MainModel.Bonds()
        items = []
        for bond in bonds:
            st1 = bond[3] + "-" + bond[5]
            st2 = bond[5] + "-" + bond[3]
            if (st1 not in items) and (st2 not in items):
                items.append(st1)
        items.sort()
        for item in items:
            BondsType.appendRow(QStandardItem(item))

        self.ui.FormActionsPostComboBonds.currentIndexChanged.disconnect()
        self.ui.FormActionsPostComboBonds.setModel(BondsType)
        self.ui.FormActionsPostComboBonds.currentIndexChanged.connect(self.fill_bonds)

        self.fill_bonds()
        self.ui.FormActionsPostButPlotBondsHistogram.setEnabled(True)

    def get_colors_list(self, minv, maxv, values, cmap, color_scale):
        n = len(values)
        colors = []
        for i in range(0,n):
            value = values[i]
            colors.append(self.get_color(cmap, minv, maxv,  value, color_scale))
        return colors

    def get_color_of_plane(self, minv, maxv, points, cmap, color_scale):
        Nx = len(points)
        Ny = len(points[0])
        minv = float(minv)
        maxv = float(maxv)
        colors = []
        for i in range(0, Nx):
            row = []
            for j in range(0, Ny):
                value = float(points[i][j][3])
                prev = self.colors_cash.get(value)
                if prev == None:
                    color = self.get_color(cmap, minv, maxv,  value, color_scale)
                    self.colors_cash[value] = [color[0], color[1], color[2]]
                    row.append([color[0], color[1], color[2]])
                else:
                    row.append(prev)
            colors.append(row)
        return colors

    def get_color(self, cmap, minv, maxv, value, scale):
        if scale == "black":
            return QColor.fromRgb(0,0,0,1).getRgbF()
        if scale == "Linear":
            part = (value - minv) / (maxv - minv)
        if scale == "Log":
            if minv < 1e-8:
                minv = 1e-8
            if value < 1e-8:
                value = 1e-8
            part = (math.log10(value) - math.log10(minv)) / (math.log10(maxv) - math.log10(minv))
        color = cmap(part)
        return color


    def get_fdf_file_name(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir, "FDF files (*.fdf)")[0]
        if not fname.endswith(".fdf"):
            fname += ".fdf"
        return fname


    def get_color_from_SETTING(self, strcolor):
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor


    def load_settings(self):
        # The SETTINGS
        settings = QSettings()
        state_FormSettingsOpeningCheckOnlyOptimal = settings.value(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, False, type=bool)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.setChecked(state_FormSettingsOpeningCheckOnlyOptimal)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.clicked.connect(self.save_state_FormSettingsOpeningCheckOnlyOptimal)
        state_FormSettingsParseAtomicProperties = settings.value(SETTINGS_FormSettingsParseAtomicProperties, False, type=bool)
        self.ui.FormSettingsParseAtomicProperties.setChecked(state_FormSettingsParseAtomicProperties)
        self.ui.FormSettingsParseAtomicProperties.clicked.connect(self.save_state_FormSettingsParseAtomicProperties)
        state_FormSettingsViewCheckShowAxes = settings.value(SETTINGS_FormSettingsViewCheckShowAxes, False, type=bool)
        self.ui.FormSettingsViewCheckShowAxes.setChecked(state_FormSettingsViewCheckShowAxes)
        self.ui.FormSettingsViewCheckShowAxes.clicked.connect(self.save_state_FormSettingsViewCheckShowAxes)
        state_FormSettingsViewCheckAtomSelection = settings.value(SETTINGS_FormSettingsViewCheckAtomSelection, False, type=bool)
        self.ui.FormSettingsViewCheckAtomSelection.setChecked(state_FormSettingsViewCheckAtomSelection)
        self.ui.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_FormSettingsViewCheckAtomSelection)

        state_FormSettingsViewCheckShowAtoms = settings.value(SETTINGS_FormSettingsViewCheckShowAtoms, True, type=bool)
        self.ui.FormSettingsViewCheckShowAtoms.setChecked(state_FormSettingsViewCheckShowAtoms)
        self.ui.FormSettingsViewCheckShowAtoms.clicked.connect(self.save_state_FormSettingsViewCheckShowAtoms)

        state_FormSettingsViewCheckShowBox = settings.value(SETTINGS_FormSettingsViewCheckShowBox, False, type=bool)
        self.ui.FormSettingsViewCheckShowBox.setChecked(state_FormSettingsViewCheckShowBox)
        self.ui.FormSettingsViewCheckShowBox.clicked.connect(self.save_state_FormSettingsViewCheckShowBox)

        state_FormSettingsViewCheckShowBonds = settings.value(SETTINGS_FormSettingsViewCheckShowBonds, True, type=bool)
        self.ui.FormSettingsViewCheckShowBonds.setChecked(state_FormSettingsViewCheckShowBonds)
        self.ui.FormSettingsViewCheckShowBonds.clicked.connect(self.save_state_FormSettingsViewCheckShowBonds)

        self.WorkDir = str(settings.value(SETTINGS_Folder, "/home"))
        self.ColorType = str(settings.value(SETTINGS_FormSettingsColorsScale, 'rainbow'))
        self.ui.FormSettingsColorsScale.currentIndexChanged.connect(self.save_state_FormSettingsColorsScale)
        self.ui.FormSettingsColorsScale.currentTextChanged.connect(self.state_changed_FormSettingsColorsScale)
        self.ColorTypeScale = str(settings.value(SETTINGS_FormSettingsColorsScaleType, 'Log'))
        self.ui.FormSettingsColorsScaleType.currentIndexChanged.connect(self.save_state_FormSettingsColorsScaleType)
        state_FormSettingsColorsFixed = settings.value(SETTINGS_FormSettingsColorsFixed, False, type=bool)
        self.ui.FormSettingsColorsFixed.setChecked(state_FormSettingsColorsFixed)
        self.ui.FormSettingsColorsFixed.clicked.connect(self.save_state_FormSettingsColorsFixed)
        state_FormSettingsColorsFixedMin = settings.value(SETTINGS_FormSettingsColorsFixedMin, '0.0')
        self.ui.FormSettingsColorsFixedMin.setText(state_FormSettingsColorsFixedMin)
        self.ui.FormSettingsColorsFixedMin.textChanged.connect(self.save_state_FormSettingsColorsFixedMin)
        state_FormSettingsColorsFixedMax = settings.value(SETTINGS_FormSettingsColorsFixedMax, '0.2')
        self.ui.FormSettingsColorsFixedMax.setText(state_FormSettingsColorsFixedMax)
        self.ui.FormSettingsColorsFixedMax.textChanged.connect(self.save_state_FormSettingsColorsFixedMax)
        state_FormSettingsViewSpinBondWidth = int(settings.value(SETTINGS_FormSettingsViewSpinBondWidth, '20'))
        self.ui.FormSettingsViewSpinBondWidth.setValue(state_FormSettingsViewSpinBondWidth)
        self.ui.FormSettingsViewSpinBondWidth.valueChanged.connect(self.save_state_FormSettingsViewSpinBondWidth)
        state_FormSettingsViewSpinContourWidth = int(settings.value(SETTINGS_FormSettingsViewSpinContourWidth, '20'))
        self.ui.FormSettingsViewSpinContourWidth.setValue(state_FormSettingsViewSpinContourWidth)
        self.ui.FormSettingsViewSpinContourWidth.valueChanged.connect(self.save_state_FormSettingsViewSpinContourWidth)
        self.ui.ColorsOfAtomsTable.setColumnCount(1)
        self.ui.ColorsOfAtomsTable.setHorizontalHeaderLabels(["Values"])
        self.ui.ColorsOfAtomsTable.setColumnWidth(0, 120)
        self.ui.ColorsOfAtomsTable.horizontalHeader().setStyleSheet(self.table_header_stylesheet)
        self.ui.ColorsOfAtomsTable.verticalHeader().setStyleSheet(self.table_header_stylesheet)
        Mendeley = TPeriodTable()
        self.state_Color_Of_Atoms = str(settings.value(SETTINGS_Color_Of_Atoms, ''))
        if (self.state_Color_Of_Atoms == 'None') or (self.state_Color_Of_Atoms == ''):
            colors = Mendeley.get_all_colors()
        else:
            colors = []
            col = self.state_Color_Of_Atoms.split('|')
            for item in col:
                it = Helpers.list_str_to_float(item.split())
                colors.append(it)
        lets = Mendeley.get_all_letters()
        for i in range(1, len(lets) - 1):
            self.ui.ColorsOfAtomsTable.setRowCount(i)  # и одну строку в таблице
            self.ui.ColorsOfAtomsTable.setItem(i - 1, 0, QTableWidgetItem(lets[i]))
            color = colors[i]
            self.ui.ColorsOfAtomsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], 1))

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

        self.CoordType = str(settings.value(SETTINGS_FormSettingsPreferredCoordinates, 'Zmatrix Cartesian'))

        self.LatticeType = str(settings.value(SETTINGS_FormSettingsPreferredLattice, 'LatticeParameters'))

    def menu_export(self):
        if self.MainForm.MainModel.nAtoms()>0:
            fname = QFileDialog.getSaveFileName(self, 'Save File', self.WorkDir, "All files (*);;FDF files (*.fdf);;XYZ files (*.xyz)")[0]
            self.MainForm.atomic_structure_to_file(fname)
            self.WorkDir = os.path.dirname(fname)
            self.save_active_Folder()


    def menu_open(self):
        self.clear_form()
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.ui.FileBrouserUseCheckBox.isChecked():
            fname = self.ui.FileBrouserTree.model().filePath(self.ui.IndexOfFileToOpen)
        else:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        if os.path.exists(fname):
            self.filename = fname
            self.WorkDir = os.path.dirname(fname)
            self.get_TAtomicModel_and_FDF(fname)

            problemAtoms = []
            for structure in self.models:
                for at in structure:
                    if at.charge >= 200:
                        problemAtoms.append(at.charge)
            problemAtoms = set(problemAtoms)

            if len(problemAtoms) > 0:
                self.atomDialog = AtomsIdentifier(problemAtoms)
                self.atomDialog.show()
                ansv = self.atomDialog.ansv

                for structure in self.models:
                    structure.ModifyAtomsTypes(ansv)

            self.plot_last_model()

    def get_TAtomicModel_and_FDF(self, fname):
        parse_properies = self.ui.FormSettingsParseAtomicProperties.isChecked()
        if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
            self.models, self.FDFData = Importer.Import(fname, 'opt', parse_properies)
        else:
            self.models, self.FDFData = Importer.Import(fname, 'all', parse_properies)

    def plot_last_model(self):
        if len(self.models) > 0:
            if len(self.models[-1].atoms) > 0:
                self.plot_model(-1)
                self.fill_gui()
                self.save_active_Folder()

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
        dialogWin = QDialog(self)
        dialogWin.ui = Ui_about()
        dialogWin.ui.setupUi(dialogWin)
        dialogWin.setFixedSize(QSize(532,149))
        dialogWin.show()


    def model_to_screen(self, value):
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()
        self.MainForm.selected_atom_properties.setText("select")

        self.color_with_property_enabling()

    def color_with_property_enabling(self):
        if self.MainForm.MainModel.nAtoms() > 0:
            atom = self.MainForm.MainModel.atoms[0]
            AtomPropType = QStandardItemModel()
            for key in atom.properties:
                AtomPropType.appendRow(QStandardItem(str(key)))
            self.ui.PropertyForColorOfAtoms.setModel(AtomPropType)

    def color_atoms_with_property(self):
        if self.ui.ColorAtomsWithProperty.isChecked():
            prop = self.ui.PropertyForColorOfAtoms.currentText()
            if len(prop)>0:
                self.MainForm.color_atoms_with_property(prop)
            else:
                self.MainForm.color_atoms_with_charge()
        else:
            self.MainForm.color_atoms_with_charge()
        self.MainForm.update()

    def model_rotation(self):
        angle = self.ui.FormModifyRotationAngle.value()
        model = self.MainForm.MainModel

        if self.ui.FormModifyRotationCenter.isChecked():
            center = model.centr_mass()
            model.move(center[0],center[1],center[2])

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
        model = self.MainForm.MainModel
        model = model.growX()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_y(self):
        model = self.MainForm.MainModel
        model = model.growY()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def model_grow_z(self):
        model = self.MainForm.MainModel
        model = model.growZ()
        self.models.append(model)
        self.fill_models_list()
        self.model_to_screen(-1)

    def plot_model(self, value):
        ViewAtoms = self.ui.FormSettingsViewCheckShowAtoms.isChecked()
        ViewBox = self.ui.FormSettingsViewCheckShowBox.isChecked()
        ViewBonds = self.ui.FormSettingsViewCheckShowBonds.isChecked()
        bondWidth = 0.005*self.ui.FormSettingsViewSpinBondWidth.value()
        bondscolor = self.get_color_from_SETTING(self.state_Color_Of_Bonds)
        axescolor = self.get_color_from_SETTING(self.state_Color_Of_Axes)
        ViewAxes = self.ui.FormSettingsViewCheckShowAxes.isChecked()
        boxcolor = self.get_color_from_SETTING(self.state_Color_Of_Box)
        atomscolor = self.colors_of_atoms()
        contour_width = (self.ui.FormSettingsViewSpinContourWidth.value())/1000.0
        self.MainForm.set_atomic_structure(self.models[value], atomscolor, ViewAtoms, ViewBox, boxcolor, ViewBonds, bondscolor, bondWidth, ViewAxes, axescolor, contour_width)
        self.prepare_FormActionsComboPDOSIndexes()
        self.prepare_FormActionsComboPDOSspecies()
        self.color_with_property_enabling()


    def plot_surface(self):
        self.MainForm.ViewSurface = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.volumeric_data_range()
        if self.ui.FormActionsPostCheckSurface.isChecked():
            data = []
            for i in range(0, self.ui.IsosurfaceColorsTable.rowCount()):
                value = float(self.ui.IsosurfaceColorsTable.item(i, 0).text())
                verts, faces = self.VolumericData.isosurface(value)
                transp = float(self.ui.IsosurfaceColorsTable.cellWidget(i, 1).text())
                color = self.get_color(cmap, minv, maxv, value, color_scale)
                color = (color[0], color[1], color[2], transp)
                data.append([verts, faces, color])
            self.MainForm.add_surface(data)
        else:
            self.MainForm.update()

    def plot_contous_isovalues(self, n_contours, scale = "Log"):
        minv, maxv = self.volumeric_data_range()
        if scale =="Linear":
            isovalues = np.linspace(minv, maxv, n_contours + 2)
        if scale == "Log":
            zero = 1e-8
            if minv<zero:
                minv = zero
            isovalueslog = np.linspace( math.log10(minv), math.log10(maxv), n_contours+2 )
            isovalues = []
            for i in range(1,len(isovalueslog)-1):
                item = isovalueslog[i]
                isovalues.append( math.exp( math.log(10)*item ))
        return isovalues

    def plot_contour(self):
        if self.VolumericData.Nx == None:
            return
        self.MainForm.ViewContour = False
        self.MainForm.ViewContourFill = False
        cmap = plt.get_cmap(self.ui.FormSettingsColorsScale.currentText())
        color_scale = self.ui.FormSettingsColorsScaleType.currentText()
        if self.ui.FormSettingsColorsFixed.isChecked():
            minv = float(self.ui.FormSettingsColorsFixedMin.text())
            maxv = float(self.ui.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.volumeric_data_range()
        params = []
        params_colored_plane = []

        planes = []
        if self.ui.FormActionsPostCheckContourXY.isChecked():
            planes.append("xy")
        if self.ui.FormActionsPostCheckContourXZ.isChecked():
            planes.append("xz")
        if self.ui.FormActionsPostCheckContourYZ.isChecked():
            planes.append("yz")

        for plane in planes:
            if plane == "xy":
                n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursXY.text())
                slice = int(self.ui.FormActionsPostSliderContourXY.value())
            if plane == "xz":
                n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursXZ.text())
                slice = int(self.ui.FormActionsPostSliderContourXZ.value())
            if plane == "yz":
                n_contours = int(self.ui.FormActionsPostLabelSurfaceNcontoursYZ.text())
                slice = int(self.ui.FormActionsPostSliderContourYZ.value())

            isovalues = self.plot_contous_isovalues(n_contours, color_scale)

            if self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, 'black')
            else:
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, color_scale)

            if self.ui.FormSettingsContourColorFixed.isChecked():
                color = self.get_color_from_SETTING(self.state_Color_Of_Contour)
                for i in range(0,len(colors)):
                    colors[i] = color

            if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                conts = self.VolumericData.contours(isovalues, plane, slice)
                params.append([isovalues, conts, colors])

            if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                points = self.VolumericData.plane(plane,slice)
                colors = self.get_color_of_plane(minv, maxv, points, cmap, color_scale)
                params_colored_plane.append([points, colors])

        if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_contour(params)

        if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_colored_plane(params_colored_plane)


    def prepare_FormActionsComboPDOSIndexes(self):
        model = QStandardItemModel()
        model.appendRow(QStandardItem("All"))
        model.appendRow(QStandardItem("Selected atom (3D View)"))
        model.appendRow(QStandardItem("Selected in list below"))
        for i in range(1, self.MainForm.MainModel.nAtoms() + 1):
            self.create_checkable_item(model, str(i))
        self.ui.FormActionsComboPDOSIndexes.setModel(model)

    def prepare_FormActionsComboPDOSspecies(self):
        Mendeley = TPeriodTable()
        atoms_list = Mendeley.get_all_letters()
        model = QStandardItemModel()
        model.appendRow(QStandardItem("All"))
        model.appendRow(QStandardItem("Selected atom (3D View)"))
        model.appendRow(QStandardItem("Selected in list below"))
        typesOfAtoms = self.MainForm.MainModel.typesOfAtoms()
        for i in range(0, len(typesOfAtoms)):
            self.create_checkable_item(model, str(atoms_list[typesOfAtoms[i][0]]))
        self.ui.FormActionsComboPDOSspecies.setModel(model)

    def prepare_q_numbers_combo(self, FormActionsComboPDOSn, start, stop):
        QuantumNumbersList = QStandardItemModel()
        QuantumNumbersList.appendRow(QStandardItem("All"))
        QuantumNumbersList.appendRow(QStandardItem("Selected"))
        for i in range(start, stop+1):
            self.create_checkable_item(QuantumNumbersList, str(i))
        FormActionsComboPDOSn.setModel(QuantumNumbersList)


    def plot_bonds_histogram(self):
        c1, c2 = self.fill_bonds_charges()
        bonds = self.MainForm.MainModel.Bonds()
        self.ui.MplWidget.canvas.axes.clear()
        b = []
        for bond in bonds:
            if ((c1 == 0) or (c2 == 0)) or ((c1 == bond[0]) and (c2 == bond[1])) or ((c1 == bond[1]) and (c2 == bond[2])):
                b.append(bond[2])

        num_bins = self.ui.FormActionsPostPlotBondsHistogramN.value()
        n, bins, patches = self.ui.MplWidget.canvas.axes.hist(b, num_bins, facecolor='blue', alpha=0.5)
        self.ui.MplWidget.canvas.axes.set_xlabel("Bond lenght")
        self.ui.MplWidget.canvas.axes.set_ylabel("Number of bonds")
        self.ui.MplWidget.canvas.draw()

    def plot_pdos(self):
        file = self.ui.FormActionsLinePDOSfile.text()
        if os.path.exists(file):
            tree = ET.parse(file)
            root = tree.getroot()

            atom_index = []
            if self.ui.FormActionsComboPDOSIndexes.currentText() == 'All':
                atom_index = range(1, self.MainForm.MainModel.nAtoms()+1)
            if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected atom (3D View)':
                atom_index = [self.MainForm.MainModel.selected_atom+1]
            if self.ui.FormActionsComboPDOSIndexes.currentText() == 'Selected in list below':
                self.list_of_selected_items_in_combo(atom_index, self.ui.FormActionsComboPDOSIndexes)

            species = []
            if self.ui.FormActionsComboPDOSspecies.currentText() == 'All':
                Mendeley = TPeriodTable()
                atoms_list = Mendeley.get_all_letters()
                typesOfAtoms = self.MainForm.MainModel.typesOfAtoms()
                for i in range(0, len(typesOfAtoms)):
                    species.append(str(atoms_list[typesOfAtoms[i][0]]))
            if self.ui.FormActionsComboPDOSspecies.currentText() == 'Selected atom (3D View)':
                species = [self.MainForm.MainModel.atoms[self.MainForm.MainModel.selected_atom].let]
            if self.ui.FormActionsComboPDOSspecies.currentText() == 'Selected in list below':
                self.list_of_selected_items_in_combo(species, self.ui.FormActionsComboPDOSspecies)

            number_n = []
            if self.ui.FormActionsComboPDOSn.currentText() == 'All':
                number_n = range(0, 9)
            if self.ui.FormActionsComboPDOSn.currentText() == 'Selected':
                self.list_of_selected_items_in_combo(number_n, self.ui.FormActionsComboPDOSn)
            number_l = []
            if self.ui.FormActionsComboPDOSl.currentText() == 'All':
                number_l = range(0, 8)
            if self.ui.FormActionsComboPDOSl.currentText() == 'Selected':
                self.list_of_selected_items_in_combo(number_l, self.ui.FormActionsComboPDOSl)
            print(number_l)

            number_m = []
            if self.ui.FormActionsComboPDOSm.currentText() == 'All':
                number_m = range(-7, 8)
            if self.ui.FormActionsComboPDOSm.currentText() == 'Selected':
                self.list_of_selected_items_in_combo(number_m, self.ui.FormActionsComboPDOSm)
            number_z = []
            if self.ui.FormActionsComboPDOSz.currentText() == 'All':
                number_z = range(1, 8)
            if self.ui.FormActionsComboPDOSz.currentText() == 'Selected':
                self.list_of_selected_items_in_combo(number_z, self.ui.FormActionsComboPDOSz)

            pdos, energy = TSIESTA.calc_pdos(root, atom_index, species, number_l, number_m, number_n, number_z)
            EF = TSIESTA.FermiEnergy(self.filename)
            shift = 0
            if self.ui.FormActionsCheckBANDSfermyShift_2.isChecked():
                shift = EF
                energy -=EF

            self.ui.MplWidget.canvas.axes.clear()

            ys = pdos[0]
            sign = 1
            if self.ui.FormActionsCheckPDOS_2.isChecked():
                sign = -1
            if len(pdos)>1:
                ys2 = sign*pdos[1]
            else:
                ys2 = np.zeros((len(pdos[0])))

            self.ui.MplWidget.canvas.axes.plot(energy, ys)
            if self.ui.FormActionsCheckPDOS.isChecked():
                self.ui.MplWidget.canvas.axes.plot(energy, ys2)

            self.ui.MplWidget.canvas.axes.set_xlabel("Energy, eV")
            self.ui.MplWidget.canvas.axes.set_ylabel("PDOS, states/eV")
            if self.ui.FormActionsCheckBANDSfermyShow_2.isChecked():
                self.ui.MplWidget.canvas.axes.axvline(x=EF - shift, linestyle="--")
            self.ui.MplWidget.canvas.axes.axhline(y=0, linestyle="-.")

            self.ui.MplWidget.canvas.draw()
            if len(pdos) > 1:
                self.PDOSdata.append([energy, pdos[0], pdos[1]])
            else:
                self.PDOSdata.append([energy, pdos[0], np.zeros((len(pdos[0])))])

            self.ui.FormActionsListPDOS.addItems([str(len(self.PDOSdata))+": "+str(self.ui.FormActionsComboPDOSIndexes.currentText())+";  "+str(self.ui.FormActionsComboPDOSspecies.currentText())+" : "+ self.ui.FormActionsEditPDOSLabel.text()])
            self.ui.FormActionsButtonPlotPDOSselected.setEnabled(True)

    def plot_selected_pdos(self):
        EF = TSIESTA.FermiEnergy(self.filename)
        shift = 0
        labels = []
        if self.ui.FormActionsCheckBANDSfermyShift_2.isChecked():
            shift = EF
            #energy -= EF

        selected = self.ui.FormActionsListPDOS.selectedItems()
        self.ui.MplWidget.canvas.axes.clear()
        for item in selected:
            ind = int(item.text().split(':')[0])-1
            labels.append(item.text())

            energy = self.PDOSdata[ind][0]
            spinUp = self.PDOSdata[ind][1]
            spinDown = self.PDOSdata[ind][2]

            if self.ui.FormActionsCheckPDOS_2.isChecked():
                spinDown *=-1

            self.ui.MplWidget.canvas.axes.plot(energy, spinUp)
            if self.ui.FormActionsCheckPDOS.isChecked():
                self.ui.MplWidget.canvas.axes.plot(energy, spinDown)

        self.ui.MplWidget.canvas.axes.set_xlabel("Energy, eV")
        self.ui.MplWidget.canvas.axes.set_ylabel("PDOS, states/eV")
        if self.ui.FormActionsCheckBANDSfermyShow_2.isChecked():
                self.ui.MplWidget.canvas.axes.axvline(x=EF - shift, linestyle="--")
        self.ui.MplWidget.canvas.axes.axhline(y=0, linestyle="-.")

        self.ui.MplWidget.canvas.axes.legend(labels)

        self.ui.MplWidget.canvas.draw()

    def list_of_selected_items_in_combo(self, atom_index, combo):
        model = combo.model()
        maxi = combo.count()
        for i in range(0, maxi):
            if model.itemFromIndex(model.index(i, 0)).checkState() == Qt.Checked:
                atom_index.append(int(model.itemFromIndex(model.index(i, 0)).text()))

    def parse_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        if os.path.exists(file):
            f = open(file)
            eF = float(f.readline())
            self.ui.FormActionsEditBANDSefermi.setText(str(eF))
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_float(str1)
            kmin = float(str1[0])
            kmax = float(str1[1])
            self.ui.FormActionsSpinBANDSxmin.setRange(kmin,kmax)
            self.ui.FormActionsSpinBANDSxmin.setValue(kmin)
            self.ui.FormActionsSpinBANDSxmax.setRange(kmin, kmax)
            self.ui.FormActionsSpinBANDSxmax.setValue(kmax)

            str1 = f.readline().split()
            str1 = Helpers.list_str_to_float(str1)
            emin = float(str1[0])
            emax = float(str1[1])
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_int(str1)
            nspins = float(str1[1])
            if nspins == 2:
                self.ui.FormActionsGrBoxBANDSspin.setEnabled(True)
            else:
                self.ui.FormActionsGrBoxBANDSspin.setEnabled(False)
            self.ui.FormActionsSpinBANDSemin.setRange(emin, emax)
            self.ui.FormActionsSpinBANDSemin.setValue(emin)
            self.ui.FormActionsSpinBANDSemax.setRange(emin, emax)
            self.ui.FormActionsSpinBANDSemax.setValue(emax)
            f.close()
            self.ui.FormActionsButtonPlotBANDS.setEnabled(True)

    def plot_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        if os.path.exists(file):
            f = open(file)
            eF = float(f.readline())
            shift = 0
            if self.ui.FormActionsCheckBANDSfermyShift.isChecked():
                shift = eF
            str1 = f.readline().split()
            kmin = self.ui.FormActionsSpinBANDSxmin.value()
            kmax = self.ui.FormActionsSpinBANDSxmax.value()
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_float(str1)
            eminf = float(str1[0])
            emaxf = float(str1[1])
            emin = self.ui.FormActionsSpinBANDSemin.value()
            emax = self.ui.FormActionsSpinBANDSemax.value()
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_int(str1)
            nbands = int(str1[0])
            nspins = int(str1[1])
            kmesh = np.zeros((str1[2]))
            HOMO = eminf*np.ones((str1[2]))
            LUMO = emaxf*np.ones((str1[2]))
            bands = np.zeros((nbands*nspins, str1[2]))
            for i in range(0, str1[2]):
                str2 = f.readline().split()
                str2 = Helpers.list_str_to_float(str2)
                kmesh[i] = str2[0]
                for j in range(1, len(str2)):
                    bands[j-1][i] = float(str2[j]) - shift
                kol = len(str2)-1
                while kol < nbands*nspins:
                    str2 = f.readline().split()
                    str2 = Helpers.list_str_to_float(str2)
                    for j in range(0, len(str2)):
                        bands[kol + j][i] = float(str2[j]) - shift
                    kol += len(str2)

            if self.ui.FormActionsCheckBANDSspinUp.isChecked():
                bands = bands[:nbands]
            else:
                bands = bands[nbands:]

            for i in range(0,nbands):
                for j in range(0,len(bands[0])):
                    tm = float(bands[i][j]) - eF + shift
                    if (tm > HOMO[j]) and (tm <= 0):
                        HOMO[j] = tm
                    if (tm < LUMO[j]) and (tm > 0):
                        LUMO[j] = tm

            nsticks = int(f.readline())
            xticks = []
            xticklabels = []
            for i in range(0, nsticks):
                str3 = f.readline().split()
                value = float(str3[0])
                if (round(value,2)>=kmin) and (round(value,2)<=kmax):
                    xticks.append(value)
                    letter = self.utf8_letter(str3[1][1:-1])
                    xticklabels.append(letter)
            f.close()
            self.ui.MplWidget.canvas.axes.clear()
            gap = emaxf - eminf
            #print(gap)
            for band in bands:
                self.ui.MplWidget.canvas.axes.plot(kmesh, band, linestyle = "-", color = "black")
                for i in range(0, len(band)-1):
                    if (band[i]-eF + shift) * (band[i+1]-eF + shift) <=0:
                        gap = 0
            mini = 0
            if gap > 0:
                for i in range(0, len(bands[0])):
                    if (LUMO[i]-HOMO[i] < gap):
                        gap = LUMO[i]-HOMO[i]
                        mini = i
            #print(gap)

            HOMOind = 0
            HOMOmax = HOMO[0]
            LUMOind = 0
            LUMOmin = LUMO[0]
            for i in range(0, len(bands[0])):
                if HOMO[i] > HOMOmax:
                    HOMOmax = HOMO[i]
                    HOMOind = i
                if LUMO[i] < LUMOmin:
                    LUMOmin = LUMO[i]
                    LUMOind = i
            gapIND = LUMOmin - HOMOmax
            #print(gapIND)
            self.ui.FormActionsLabelBANDSgap.setText("Band gap = "+str(round(gap,3))+"  "+ "Indirect gap = "+str(round(gapIND,3)))
            #self.ui.MplWidget.canvas.axes.plot(kmesh, HOMO, linestyle="-", color="blue")
            #self.ui.MplWidget.canvas.axes.plot(kmesh, LUMO, linestyle="-", color="red")
            self.ui.MplWidget.canvas.axes.set_xlim(kmin, kmax)
            self.ui.MplWidget.canvas.axes.set_ylim(emin, emax)
            self.ui.MplWidget.canvas.axes.set_xticks(xticks)
            for tick in xticks:
                self.ui.MplWidget.canvas.axes.axvline(x=tick, linestyle = "--")
            if self.ui.FormActionsCheckBANDSfermyShow.isChecked():
                self.ui.MplWidget.canvas.axes.axhline(y=eF - shift, linestyle="-.")
            self.ui.MplWidget.canvas.axes.set_xticklabels(xticklabels)
            self.ui.MplWidget.canvas.axes.set_xlabel("k")
            self.ui.MplWidget.canvas.axes.set_ylabel("Energy, eV")

            self.ui.MplWidget.canvas.draw()

    def plot_voronoi(self):
        if self.MainForm.isActive():
            r = self.state_Color_Of_Voronoi.split()[0]
            g = self.state_Color_Of_Voronoi.split()[1]
            b = self.state_Color_Of_Voronoi.split()[2]
            color = [float(r)/255, float(g)/255, float(b)/255]
            maxDist = float(self.ui.FormActionsPostTextVoronoiMaxDist.value())
            atom_index, volume = self.MainForm.add_voronoi(color, maxDist)
            if atom_index >=0:
                self.ui.FormActionsPostLabelVoronoiAtom.setText("Atom: " + str(atom_index))
                self.ui.FormActionsPostLabelVoronoiVolume.setText("volume: "+str(volume))
            else:
                self.ui.FormActionsPostLabelVoronoiAtom.setText("Atom: ")
                self.ui.FormActionsPostLabelVoronoiVolume.setText("volume: ")

    def plot_dos(self):
        self.ui.MplWidget.canvas.axes.clear()
        for index in range(self.ui.FormActionsTabeDOSProperty.rowCount()):
            path = self.ui.FormActionsTabeDOSProperty.item(index,0).toolTip()
            eF = float(self.ui.FormActionsTabeDOSProperty.item(index,1).text())

            if os.path.exists(path):
                spinUp, spinDown, energy = TSIESTA.DOSsiesta(path)
                shift = 0
                if self.ui.FormActionsCheckBANDSfermyShift_3.isChecked():
                    shift = eF
                    energy-=shift
                if self.ui.FormActionsCheckDOS_2.isChecked():
                    spinDown *=-1
                self.ui.MplWidget.canvas.axes.plot(energy, spinUp)
                if self.ui.FormActionsCheckDOS.isChecked():
                    self.ui.MplWidget.canvas.axes.plot(energy, spinDown)
                
        self.ui.MplWidget.canvas.axes.set_xlabel("Energy, eV")
        self.ui.MplWidget.canvas.axes.set_ylabel("DOS, states/eV")
        if self.ui.FormActionsCheckBANDSfermyShow_3.isChecked():
            self.ui.MplWidget.canvas.axes.axvline(x=eF-shift, linestyle="--")
        self.ui.MplWidget.canvas.axes.axhline(y=0, linestyle="-.")

        self.ui.MplWidget.canvas.draw()

    def clear_dos(self):
        self.ui.FormActionsTabeDOSProperty.setRowCount(0)
        self.ui.FormActionsTabeDOSProperty.update()


    def plot_volume_param_energy(self):
        items = []
        method = self.ui.FormActionsPostComboCellParam.currentText()
        xi = self.ui.FormActionsPostComboCellParamX.currentIndex()
        LabelX = self.ui.FormActionsPostComboCellParamX.currentText()
        yi = 1

        for index in range(self.ui.FormActionsPostTableCellParam.rowCount()):
            x = self.ui.FormActionsPostTableCellParam.item(index, xi).text()
            y = self.ui.FormActionsPostTableCellParam.item(index, yi).text()
            items.append([float(x),float(y)])

        if len(items):
            items = sorted(items, key=itemgetter(0))
            self.ui.MplWidget.canvas.axes.clear()

            xs = []
            ys = []
        
            for i in range(0, len(items)):           
                xs.append(items[i][0])
                ys.append(items[i][1])
            self.ui.MplWidget.canvas.axes.scatter(xs, ys, color='orange', s=40, marker='o')

            if method == "Murnaghan":
                aprox, xs2, ys2 = Calculator.ApproxMurnaghan(items)
                image_path = '.\images\murnaghan.png' #path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)="+str(round(float(aprox[0]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0="+str(round(float(aprox[1]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'="+str(round(float(aprox[2]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0="+str(round(float(aprox[3]),2)))

            if method == "BirchMurnaghan":
                aprox, xs2, ys2 = Calculator.ApproxBirchMurnaghan(items)
                image_path = '.\images\murnaghanbirch.png'  # path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)="+str(round(float(aprox[0]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("B0="+str(round(float(aprox[1]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("B0'="+str(round(float(aprox[2]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("V0="+str(round(float(aprox[3]),2)))

            if method == "Parabola":
                aprox, xs2, ys2 = Calculator.ApproxParabola(items)
                image_path = '.\images\parabola.png' #path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("a=" + str(round(float(aprox[2]), 2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("b="+str(round(float(aprox[1]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("x0="+str(round(-float(aprox[1])/float(2*aprox[2]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr4.setText("c="+str(round(float(aprox[0]),2)))

            self.ui.MplWidget.canvas.axes.plot(xs2, ys2)

            self.ui.MplWidget.canvas.axes.set_ylabel("Energy, "+self.ui.FormActionsPostComboCellParamEnergy.currentText())
            if LabelX == "V":
                self.ui.MplWidget.canvas.axes.set_xlabel(LabelX+", "+self.ui.FormActionsPostComboCellParamLen.currentText()+"^3")
            else:
                self.ui.MplWidget.canvas.axes.set_xlabel(LabelX + ", " + self.ui.FormActionsPostComboCellParamLen.currentText())

            self.ui.MplWidget.canvas.draw()

            image_profile = QImage(image_path)
            #print(image_profile)
            image_profile = image_profile.scaled(320,320, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration
            self.ui.FormActionsPostLabelCellParamFig.setPixmap(QPixmap.fromImage(image_profile))


    def save_data_from_figure2d(self):
        DATA = []
        lines = self.ui.MplWidget.canvas.axes.lines

        for line in lines:
            DATA.append(line.get_xydata())

        if len(DATA)>0:
            name = QFileDialog.getSaveFileName(self, 'Save File')[0]

            iter = 0
            for line in DATA:
                if len(DATA)>1:
                    iter+=1
                    prefix = "line_"+str(iter)+"_in_"
                file = open(name, 'w')
                for row in line:
                    s = ""
                    for number in row:
                        s+=str(number)+" "
                    file.write(s+"\n")
                file.close()
        
    def save_image_to_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', self.WorkDir, "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)")
        fname = name[0]
        if name[1] == "PNG files (*.png)":
            ext = "png"
        if name[1] == "JPG files (*.jpg)":
            ext = "jpg"
        if name[1] == "BMP files (*.bmp)":
            ext = "bmp"
        if not fname.endswith(ext):
            fname +="."+ext

        newWindow = Image3Dexporter(5*self.ui.openGLWidget.width(), 5*self.ui.openGLWidget.height(),5)
        newWindow.MainForm.copy_state(self.MainForm)

        newWindow.MainForm.image3D_to_file(fname)
        #self.MainForm.image3D_to_file("copy.png")
        self.WorkDir = os.path.dirname(fname)
        self.save_active_Folder()

    def save_active_Folder(self):
        self.save_property(SETTINGS_Folder, self.WorkDir)

    def save_state_FormSettingsOpeningCheckOnlyOptimal(self):
        self.save_property(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked())

    def save_state_FormSettingsParseAtomicProperties(self):
        self.save_property(SETTINGS_FormSettingsParseAtomicProperties, self.ui.FormSettingsParseAtomicProperties.isChecked())

    def save_state_FormSettingsViewCheckShowAxes(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAxes,
                           self.ui.FormSettingsViewCheckShowAxes.isChecked())
        self.MainForm.set_axes_visible(self.ui.FormSettingsViewCheckShowAxes.isChecked())

    def save_state_FormSettingsViewCheckAtomSelection(self):
        self.save_property(SETTINGS_FormSettingsViewCheckAtomSelection,
                           self.ui.FormSettingsViewCheckAtomSelection.isChecked())

    def save_state_FormSettingsViewCheckShowAtoms(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAtoms, self.ui.FormSettingsViewCheckShowAtoms.isChecked())
        self.MainForm.set_atoms_visible(self.ui.FormSettingsViewCheckShowAtoms.isChecked())

    def save_state_FormSettingsViewCheckShowBox(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.MainForm.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_FormSettingsViewCheckShowBonds(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.MainForm.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

    def save_state_FormSettingsColorsFixed(self):
        self.save_property(SETTINGS_FormSettingsColorsFixed, self.ui.FormSettingsColorsFixed.isChecked())

    def save_state_FormSettingsViewSpinContourWidth(self):
        self.save_property(SETTINGS_FormSettingsViewSpinContourWidth, self.ui.FormSettingsViewSpinContourWidth.text())
        self.MainForm.set_contour_width(self.ui.FormSettingsViewSpinContourWidth.value() / 1000)
        self.plot_contour()

    def save_state_FormSettingsColorsFixedMin(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMin, self.ui.FormSettingsColorsFixedMin.text())

    def save_state_FormSettingsViewSpinBondWidth(self):
        self.save_property(SETTINGS_FormSettingsViewSpinBondWidth, self.ui.FormSettingsViewSpinBondWidth.text())
        self.MainForm.set_bond_width(self.ui.FormSettingsViewSpinBondWidth.value()*0.005)

    def save_state_FormSettingsColorsFixedMax(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMax, self.ui.FormSettingsColorsFixedMax.text())

    def save_state_FormSettingsColorsScale(self):
        self.save_property(SETTINGS_FormSettingsColorsScale, self.ui.FormSettingsColorsScale.currentText())
        self.colors_cash = {}

    def save_state_FormSettingsColorsScaleType(self):
        self.save_property(SETTINGS_FormSettingsColorsScaleType, self.ui.FormSettingsColorsScaleType.currentText())
        self.colors_cash = {}

    def save_state_FormSettingsPreferredCoordinates(self):
        self.save_property(SETTINGS_FormSettingsPreferredCoordinates, self.ui.FormSettingsPreferredCoordinates.currentText())
        self.CoordType = self.ui.FormSettingsPreferredCoordinates.currentText()

    def save_state_FormSettingsPreferredLattice(self):
        self.save_property(SETTINGS_FormSettingsPreferredLattice, self.ui.FormSettingsPreferredLattice.currentText())
        self.LatticeType = self.ui.FormSettingsPreferredLattice.currentText()


    def save_property(self, property, value):
        settings = QSettings()
        settings.setValue(property, value)
        settings.sync()

    def state_changed_FormSettingsColorsScale(self):
        if self.ui.FormSettingsColorsScale.currentText() =="":
            self.ui.ColorRow.canvas.axes.clear()
        else:
            gradient = np.linspace(0, 1, 256)
            gradient = np.vstack((gradient, gradient))
            self.ui.ColorRow.canvas.axes.imshow(gradient, aspect='auto',
                                         cmap=plt.get_cmap(self.ui.FormSettingsColorsScale.currentText()))
            self.ui.ColorRow.canvas.axes.set_axis_off()
            self.ui.ColorRow.canvas.draw()

    def type_of_surface(self):
        self.ui.FormActionsPostLabelSurfaceMin.setText("")
        self.ui.FormActionsPostLabelSurfaceMax.setText("")
        self.ui.FormActionsPostLabelSurfaceValue.setValue(0)
        self.ui.FormActionsPostButSurface.setEnabled(False)
        self.ui.FormActionsPostButContour.setEnabled(False)

    def fdf_data_to_form(self):
        model = self.MainForm.get_model()
        text = self.FDFData.get_all_data(model, self.CoordType, self.LatticeType)
        self.ui.FormActionsPreTextFDF.setText(text)

    def fdf_data_from_form_to_file(self):
        text = self.ui.FormActionsPreTextFDF.toPlainText()

        name = QFileDialog.getSaveFileName(self, 'Save File')[0]
        if len(name)>0:
            with open(name, 'w') as f:
                f.write(text)

    def fill_space(self):
        Mendeley = TPeriodTable()
        nAtoms = int(self.ui.FormActionsPreNAtomsFillSpace.value())
        charge = int(self.ui.FormActionsPreAtomChargeFillSpace.value())
        radAtom = Mendeley.get_rad(charge)
        let = Mendeley.get_let(charge)
        delta = float(self.ui.FormActionsPreDeltaFillSpace.value())
        nPrompts = int(self.ui.FormActionsPreNPromptsFillSpace.value())
        radTube = float(self.ui.FormActionsPreRadiusFillSpace.value())
        length = float(self.ui.FormActionsPreZSizeFillSpace.value())
        models = Calculator.FillTube(radTube, length, nAtoms, 0.01*radAtom, delta, nPrompts, let, charge)

        filename = "."
        if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
            filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
            filename = filename.split(".fdf")[0]

        iter = 0
        for model in models:
            secondModel = deepcopy(self.MainForm.get_model())
            for at in model:
                secondModel.add_atom(at)
            self.models.append(secondModel)
            if self.ui.FormActionsPreSaveToFileFillSpace.isChecked():
                text = self.FDFData.get_all_data(secondModel.atoms)
                with open(filename + str(iter) + '.fdf', 'w') as f:
                    f.write(text)
            iter += 1
        self.fill_models_list()

    def parse_volumeric_data(self):
        if len(self.ui.FormActionsPostList3DData.selectedItems())>0:
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
            self.clear_form_isosurface_data2_N()
            self.ui.VolumrricDataGridCorrect.setEnabled(False)
            self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)

    def parse_volumeric_data2(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)
        if len(fname)>0:
            fname = fname[0]
            if fname.endswith(".XSF"):
                self.VolumericData2 = TXSF()
            if fname.endswith(".cube"):
                self.VolumericData2 = TGaussianCube()
            if self.VolumericData2.parse(fname):
                #data = self.VolumericData.blocks
                self.fill_volumeric_data(self.VolumericData2, self.ui.FormActionsPostTreeSurface2)

            self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(True)
            self.ui.CalculateTheVolumericDataDifference.setEnabled(True)
            self.ui.FormActionsPosEdit3DData2.setText(fname)
            self.clear_form_isosurface_data2_N()
            self.ui.VolumrricDataGridCorrect.setEnabled(False)
            self.ui.CalculateTheVolumericDataDifference.setEnabled(False)

    def set_xsf_z_position(self):
        value = int(self.ui.FormActionsPostSliderContourXY.value())
        self.ui.FormActionsPostLabelContourXYposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourXY.maximum()))

    def set_xsf_y_position(self):
        value = int(self.ui.FormActionsPostSliderContourXZ.value())
        self.ui.FormActionsPostLabelContourXZposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourXZ.maximum()))

    def set_xsf_x_position(self):
        value = int(self.ui.FormActionsPostSliderContourYZ.value())
        self.ui.FormActionsPostLabelContourYZposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourYZ.maximum()))

    def select_atom_color(self):
        color = QColorDialog.getColor()
        atomcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        i = self.ui.ColorsOfAtomsTable.selectedIndexes()[0].row()
        self.ui.ColorsOfAtomsTable.item(i, 0).setBackground(QColor.fromRgbF(atomcolor[0], atomcolor[1], atomcolor[2], 1))

        text_color = ""
        atomscolor = []
        col = self.ui.ColorsOfAtomsTable.item(0, 0).background().color().getRgbF()
        atomscolor.append(col)
        text_color += str(col[0]) + " " + str(col[1]) + " " + str(col[2]) + "|"
        for i in range(0, self.ui.ColorsOfAtomsTable.rowCount() ):
            col = self.ui.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
            text_color+=str(col[0])+" "+str(col[1])+" "+str(col[2])+"|"

        self.save_property(SETTINGS_Color_Of_Atoms, text_color)
        self.MainForm.set_color_of_atoms(atomscolor)

    def select_box_color(self):
        boxcolor = self.change_color(self.ui.ColorBox, SETTINGS_Color_Of_Box)
        self.MainForm.set_color_of_box(boxcolor)

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
        n=0
        m=0
        type = 0
        if self.ui.FormActionsPreRadioSWNT.isChecked():
            n = self.ui.FormActionsPreLineSWNTn.value()
            m = self.ui.FormActionsPreLineSWNTm.value()
        if self.ui.FormActionsPreRadioSWNTcap.isChecked() or self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            nm = self.ui.FormActionsPreComboSWNTind.currentText().split(",")
            n = int( nm[0].split("(")[1] )
            m = int( nm[1].split(")")[0] )
        if self.ui.FormActionsPreRadioSWNTcap.isChecked():
            type = 1
        if self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            type = 2
        if self.ui.FormActionsPreRadioSWNTuselen.isChecked():
            leng = float(self.ui.FormActionsPreLineSWNTlen.text())
            cells = 1
        else:
            leng = 0
            cells = float(self.ui.FormActionsPreLineSWNTcells.text())

        if type == 0:
            model = TSWNT(n, m, leng, cells)

        if type == 1 or type == 2:
            dist1 = float(self.ui.FormCreateSpinFirstCapDist.value())
            angle1 = float(self.ui.FormCreateSpinFirstCapAngle.value())
            dist2 = float(self.ui.FormCreateSpinSecondCapDist.value())
            angle2 = float(self.ui.FormCreateSpinSecondCapAngle.value())
            model = TCapedSWNT(n, m, leng, cells, type, dist1, angle1, dist2, angle2)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("SWNT-model")

    def swnt_type1_selected(self):
        self.ui.FormActionsPreLineSWNTn.setEnabled(True)
        self.ui.FormActionsPreLineSWNTm.setEnabled(True)
        self.ui.FormActionsPreComboSWNTind.setEnabled(False)
        self.ui.FormCreateGroupFirstCap.setEnabled(False)
        self.ui.FormCreateGroupSecondCap.setEnabled(False)

    def swnt_type2_selected(self):
        self.ui.FormActionsPreLineSWNTn.setEnabled(False)
        self.ui.FormActionsPreLineSWNTm.setEnabled(False)
        self.ui.FormActionsPreComboSWNTind.setEnabled(True)
        self.ui.FormCreateGroupFirstCap.setEnabled(True)
        if self.ui.FormActionsPreRadioSWNTcap_2.isChecked():
            self.ui.FormCreateGroupSecondCap.setEnabled(True)
        else:
            self.ui.FormCreateGroupSecondCap.setEnabled(False)

    def change_color(self, colorUi, property):
        color = QColorDialog.getColor()
        colorUi.setStyleSheet(
            "background-color:rgb(" + str(color.getRgb()[0]) + "," + str(color.getRgb()[1]) + "," + str(
                color.getRgb()[2]) + ")")
        newcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        self.save_property(property,
                           str(color.getRgb()[0]) + " " + str(color.getRgb()[1]) + " " + str(color.getRgb()[2]))
        return newcolor

    def volumeric_data_range(self):
        getSelected = self.ui.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                return self.VolumericData.min, self.VolumericData.max

    def volumeric_data_load(self):
        getSelected = self.ui.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                self.get_TAtomicModel_and_FDF(self.VolumericData.filename)
                self.VolumericData.load_data(getChildNode)

                self.clear_form_postprocessing()
                self.ui.FormActionsPostList3DData.clear()
                self.plot_last_model()

                self.ui.FormActionsPostButSurfaceAdd.setEnabled(True)
                self.ui.FormActionsPostButContour.setEnabled(True)
                self.ui.FormActionsPostButSurfaceParse2.setEnabled(True)

                minv, maxv = self.volumeric_data_range()
                self.ui.FormActionsPostLabelSurfaceMax.setText("Max: " + str(round(maxv,5)))
                self.ui.FormActionsPostLabelSurfaceMin.setText("Min: " + str(round(minv,5)))
                self.ui.FormActionsPostLabelSurfaceValue.setRange(minv,maxv)
                self.ui.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))

                self.ui.FormActionsPostSliderContourXY.setMaximum(self.VolumericData.Nz)
                self.ui.FormActionsPostSliderContourXZ.setMaximum(self.VolumericData.Ny)
                self.ui.FormActionsPostSliderContourYZ.setMaximum(self.VolumericData.Nx)

    def volumeric_data_load2(self):
        getSelected = self.ui.FormActionsPostTreeSurface2.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                atoms = self.VolumericData2.load_data(getChildNode)

                self.ui.FormActionsPostLabelSurfaceNx.setText("Nx: " + str(self.VolumericData2.Nx))
                self.ui.FormActionsPostLabelSurfaceNy.setText("Ny: " + str(self.VolumericData2.Ny))
                self.ui.FormActionsPostLabelSurfaceNz.setText("Nz: " + str(self.VolumericData2.Nz))

                if (self.VolumericData2.Nx == self.VolumericData.Nx) and (self.VolumericData2.Ny == self.VolumericData.Ny) and (self.VolumericData2.Nz == self.VolumericData.Nz):
                    self.ui.VolumrricDataGridCorrect.setEnabled(True)
                    self.ui.CalculateTheVolumericDataDifference.setEnabled(True)

    def volumeric_data_difference(self):
        self.ui.CalculateTheVolumericDataDifference.setEnabled(False)
        self.ui.FormActionsPostButSurfaceLoadData2.setEnabled(False)
        self.VolumericData.difference(self.VolumericData2)
        minv, maxv = self.volumeric_data_range()
        self.ui.FormActionsPostLabelSurfaceMax.setText("Max: " + str(round(maxv,5)))
        self.ui.FormActionsPostLabelSurfaceMin.setText("Min: " + str(round(minv,5)))
        self.ui.FormActionsPostLabelSurfaceValue.setRange(minv, maxv)
        self.ui.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))
        self.ui.CalculateTheVolumericDataDifference.setEnabled(True)

    def utf8_letter(self, let):
        if let == '\Gamma':
            return '\u0393'
        if let == '\Delta':
            return '\u0394'
        if let == '\Lambda':
            return '\u039B'
        if let == '\Pi':
            return '\u03A0'
        if let == '\Sigma':
            return '\u03A3'
        if let == '\Omega':
            return '\u03A9'
        return let

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
SETTINGS_FormSettingsViewCheckShowAtoms = 'view/CheckShowAtoms'
SETTINGS_FormSettingsViewCheckShowBox = 'view/CheckShowBox'
SETTINGS_FormSettingsViewCheckShowAxes = 'view/CheckShowAxes'
SETTINGS_FormSettingsViewCheckShowBonds = 'view/CheckShowBonds'
SETTINGS_FormSettingsViewSpinBondWidth = 'view/SpinBondWidth'
SETTINGS_FormSettingsViewSpinContourWidth = 'view/SpinContourWidth'

SETTINGS_FormSettingsPreferredCoordinates = 'model/FormSettingsPreferredCoordinates'
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
window.setupUI()
window.setWindowIcon(QIcon('./images/ico.png'))
window.show()

sys.exit(app.exec_())