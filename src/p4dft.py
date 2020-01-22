# -*- coding: utf-8 -*-

import sys
import os
import math
from copy import deepcopy
#import time
from operator import itemgetter

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QVariant
#from PyQt5.QtCore import QItemSelection

#from PyQt5.QtCore import QMimeData
#import PyQt5.QtCore as QtCore
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
#from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QImage

#from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor


#from AdvancedTools import TAtom as Atom
from AdvancedTools import TFDFFile
from AdvancedTools import TPeriodTable
from AdvancedTools import TSWNT
from AdvancedTools import TAtomicModel
from AdvancedTools import TSIESTA
from AdvancedTools import Helpers
from TGui import GuiOpenGL
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
#import matplotlib.cm as cm
import matplotlib.pyplot as plt

from TInterface import Importer
from TInterface import Calculator
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
        selected_atom_info = [self.ui.FormActionsPreComboAtomsList, self.ui.FormActionsPreSpinAtomsCoordX, self.ui.FormActionsPreSpinAtomsCoordY, self.ui.FormActionsPreSpinAtomsCoordZ]
        self.MainForm = GuiOpenGL(self.ui.openGLWidget, self.ui.FormSettingsViewCheckAtomSelection, selected_atom_info)
        self.FDFData = TFDFFile()
        self.VolumericData = TVolumericData()
        self.filename = ""
        self.colors_cash = {}

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
        
        #buttons
        self.ui.FileBrouserOpenFile.clicked.connect(self.menu_open)
        self.ui.FormActionsPostButCreateBonds.clicked.connect(self.fill_bonds)
        self.ui.FormActionsPostButPlotBondsHistogram.clicked.connect(self.plot_bonds_histogram)
        self.ui.FormActionsPreButFDFGenerate.clicked.connect(self.fdf_data_to_form)
        self.ui.FormActionsPreButFDFToFile.clicked.connect(self.fdf_data_from_form_to_file)
        self.ui.FormActionsPreButFillSpace.clicked.connect(self.fill_space)
        self.ui.FormActionsPreButSWNTGenerate.clicked.connect(self.swnt_create)
        self.ui.FormActionsPostButSurface.clicked.connect(self.plot_surface)
        self.ui.FormActionsPostButSurfaceParse.clicked.connect(self.parse_volumeric_data)
        self.ui.FormActionsPostButSurfaceLoadData.clicked.connect(self.volumeric_data_load)
        self.ui.FormActionsPostButContour.clicked.connect(self.plot_contour)
        self.ui.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ui.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ui.ColorAtomDialogButton.clicked.connect(self.select_atom_color)
        self.ui.ColorVoronoiDialogButton.clicked.connect(self.select_voronoi_color)
        self.ui.ColorAxesDialogButton.clicked.connect(self.select_axes_color)
        self.ui.FormActionsPostButSurfaceAdd.clicked.connect(self.add_isosurface_color_to_table)
        self.ui.FormActionsPostButSurfaceDelete.clicked.connect(self.delete_isosurface_color_from_table)
        self.ui.FormActionsButtonPlotPDOS.clicked.connect(self.plot_pdos)
        self.ui.FormActionsButtonPlotBANDS.clicked.connect(self.plot_bands)

        self.ui.FormActionsPreButDeleteAtom.clicked.connect(self.atom_delete)
        self.ui.FormActionsPreButModifyAtom.clicked.connect(self.atom_modify)
        self.ui.FormActionsPreButAddAtom.clicked.connect(self.atom_add)
                
        self.ui.FormActionsButtonAddDOSFile.clicked.connect(self.add_dos_file)
        self.ui.FormActionsButtonPlotDOS.clicked.connect(self.plot_dos)
        self.ui.FormActionsButtonClearDOS.clicked.connect(self.clear_dos)

        self.ui.FormActionsPostButPlusCellParam.clicked.connect(self.add_cell_param)
        self.ui.FormActionsPostButAddRowCellParam.clicked.connect(self.add_cell_param_row)
        self.ui.FormActionsPostButDeleteRowCellParam.clicked.connect(self.delete_cell_param_row)
        self.ui.FormActionsPostButPlusDataCellParam.clicked.connect(self.add_data_cell_param)

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

        table_header_stylesheet = "::section{Background-color:rgb(194,169,226)}"

        
        self.ui.FormModelTableAtoms.setColumnCount(4)
        self.ui.FormModelTableAtoms.setHorizontalHeaderLabels(["Atom", "x", "y","z"])
        self.ui.FormModelTableAtoms.setColumnWidth(0, 40)
        self.ui.FormModelTableAtoms.setColumnWidth(1, 80)
        self.ui.FormModelTableAtoms.setColumnWidth(2, 80)
        self.ui.FormModelTableAtoms.setColumnWidth(3, 80)
        self.ui.FormModelTableAtoms.horizontalHeader().setStyleSheet(table_header_stylesheet)
        self.ui.FormModelTableAtoms.verticalHeader().setStyleSheet(table_header_stylesheet)


        self.ui.FormModelTableProperties.setColumnCount(2)
        self.ui.FormModelTableProperties.setHorizontalHeaderLabels(["Property", "Value"])
        self.ui.FormModelTableProperties.setColumnWidth(0, 85)
        self.ui.FormModelTableProperties.setColumnWidth(1, 240)
        self.ui.FormModelTableProperties.horizontalHeader().setStyleSheet(table_header_stylesheet)
        self.ui.FormModelTableProperties.verticalHeader().setStyleSheet(table_header_stylesheet)
        
        
        self.ui.FormActionsTabeDOSProperty.setColumnCount(3)
        self.ui.FormActionsTabeDOSProperty.setHorizontalHeaderLabels(["sp", "EFermy","S11 (M11)"])
        self.ui.FormActionsTabeDOSProperty.setColumnWidth(0, 40)
        self.ui.FormActionsTabeDOSProperty.setColumnWidth(1, 80)
        self.ui.FormActionsTabeDOSProperty.setColumnWidth(2, 80)


        self.ui.IsosurfaceColorsTable.setColumnCount(2)
        self.ui.IsosurfaceColorsTable.setHorizontalHeaderLabels(["Value","Transparancy"])
        self.ui.IsosurfaceColorsTable.setColumnWidth(0, 120)
        self.ui.IsosurfaceColorsTable.setColumnWidth(1, 150)

        CellPredictionType = QStandardItemModel()
        CellPredictionType.appendRow(QStandardItem("Murnaghan"))
        CellPredictionType.appendRow(QStandardItem("BirchMurnaghan"))
        CellPredictionType.appendRow(QStandardItem("Parabola"))
        self.ui.FormActionsPostComboCellParam.setModel(CellPredictionType)

        FillSpaceModel = QStandardItemModel()
        FillSpaceModel.appendRow(QStandardItem("cylinder"))
        #FillSpaceModel.appendRow(QStandardItem("parallelepiped"))
        self.ui.FormActionsPreComboFillSpace.setModel(FillSpaceModel)

        self.prepare_FormActionsComboPDOSIndexes()
        self.prepare_FormActionsComboPDOSspecies()

        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSn, 0, 8)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSl, 0, 7)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSm, -7, 7)
        self.prepare_q_numbers_combo(self.ui.FormActionsComboPDOSz, -1, 1)

        ColorType = QStandardItemModel()
        ColorTypes = [ 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
        # Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Gr
        # eys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu,
        # RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrB
        # r_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r,
        # flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gn
        # uplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, r
        # ainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r,
        #  viridis, viridis_r, winter, winter_r
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

        
        argsCell = QStandardItemModel()
        argsCell.appendRow(QStandardItem("V"))
        argsCell.appendRow(QStandardItem("E"))
        argsCell.appendRow(QStandardItem("a"))
        argsCell.appendRow(QStandardItem("b"))
        argsCell.appendRow(QStandardItem("c")) 
        self.ui.FormActionsPostComboCellParamX.setModel(argsCell)


        self.ui.FormActionsPosTableBonds.setColumnCount(2)
        self.ui.FormActionsPosTableBonds.setHorizontalHeaderLabels(["Bond", "Lenght"])
        self.ui.FormActionsPosTableBonds.setColumnWidth(0, 70)
        self.ui.FormActionsPosTableBonds.setColumnWidth(1, 180)

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

    def create_checkable_item(self, QuantumNumbersList, value):
        item = QStandardItem(value)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
        QuantumNumbersList.appendRow(item)

    def load_settings(self):
        # The SETTINGS
        settings = QSettings()
        state_FormSettingsOpeningCheckOnlyOptimal = settings.value(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, False, type=bool)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.setChecked(state_FormSettingsOpeningCheckOnlyOptimal)
        self.ui.FormSettingsOpeningCheckOnlyOptimal.clicked.connect(self.save_state_FormSettingsOpeningCheckOnlyOptimal)
        state_FormSettingsViewCheckShowAxes = settings.value(SETTINGS_FormSettingsViewCheckShowAxes, False, type=bool)
        self.ui.FormSettingsViewCheckShowAxes.setChecked(state_FormSettingsViewCheckShowAxes)
        self.ui.FormSettingsViewCheckShowAxes.clicked.connect(self.save_state_FormSettingsViewCheckShowAxes)
        state_FormSettingsViewCheckAtomSelection = settings.value(SETTINGS_FormSettingsViewCheckAtomSelection, False, type=bool)
        self.ui.FormSettingsViewCheckAtomSelection.setChecked(state_FormSettingsViewCheckAtomSelection)
        self.ui.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_FormSettingsViewCheckAtomSelection)
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
        self.ui.ColorsOfAtomsTable.setColumnCount(1)
        self.ui.ColorsOfAtomsTable.setHorizontalHeaderLabels(["Values"])
        self.ui.ColorsOfAtomsTable.setColumnWidth(0, 120)
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

    def color_to_ui(self, ColorUi, state_Color):
        r = state_Color.split()[0]
        g = state_Color.split()[1]
        b = state_Color.split()[2]
        ColorUi.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

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


    def colors_of_atoms(self):
        atomscolor = [ self.ui.ColorsOfAtomsTable.item(0, 0).background().color().getRgbF()]
        for i in range(0, self.ui.ColorsOfAtomsTable.rowCount()):
            col = self.ui.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
        return atomscolor

    def get_color_from_SETTING(self, strcolor):
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor

    def menu_export(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File', self.WorkDir, "FDF files (*.fdf);;XYZ files (*.xyz)")[0]
        self.MainForm.atomic_structure_to_file(fname)
        self.WorkDir = os.path.dirname(fname)
        self.save_active_Folder()
        
    def menu_open(self):
        """ menu Open"""
        self.ui.Form3Dand2DTabs.setCurrentIndex(0)
        if self.ui.FileBrouserUseCheckBox.isChecked():
            fname = self.ui.FileBrouserTree.model().filePath(self.ui.IndexOfFileToOpen)
        else:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        if os.path.exists(fname):
            self.filename = fname
            self.WorkDir = os.path.dirname(fname)
            if self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked():
                self.models, self.FDFData = Importer.Import(fname, 'opt')
            else:
                self.models, self.FDFData = Importer.Import(fname)

            problemAtoms = []
            for structure in self.models:
                for at in structure:
                    if at.charge >=200:
                        problemAtoms.append(at.charge)
            problemAtoms = set(problemAtoms)

            if len(problemAtoms)>0:
                self.atomDialog = AtomsIdentifier(problemAtoms)
                self.atomDialog.exec()
                ansv = self.atomDialog.ansv

                for structure in self.models:
                    structure.ModifyAtomsTypes(ansv)

            if len(self.models)>0:
                if len(self.models[-1].atoms) > 0:
                    self.plot_model(-1)
                    self.fill_gui()
                    self.save_active_Folder()


    def model_to_screen(self, value):
        """print("combobox changed", value)"""
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()

    def plot_model(self, value):
        ViewBox = self.ui.FormSettingsViewCheckShowBox.isChecked()
        ViewBonds = self.ui.FormSettingsViewCheckShowBonds.isChecked()
        bondWidth = 0.005*self.ui.FormSettingsViewSpinBondWidth.value()
        bondscolor = self.get_color_from_SETTING(self.state_Color_Of_Bonds)
        axescolor = self.get_color_from_SETTING(self.state_Color_Of_Axes)
        ViewAxes = self.ui.FormSettingsViewCheckShowAxes.isChecked()
        boxcolor = self.get_color_from_SETTING(self.state_Color_Of_Box)
        atomscolor = self.colors_of_atoms()
        self.MainForm.set_atomic_structure(self.models[value], atomscolor, ViewBox, boxcolor, ViewBonds, bondscolor, bondWidth, ViewAxes, axescolor)
        self.prepare_FormActionsComboPDOSIndexes()
        self.prepare_FormActionsComboPDOSspecies()

    def menu_ortho(self):
        """ menu Ortho"""
        self.MainForm.ViewOrtho = True
        self.ui.openGLWidget.update()


    def menu_perspective(self):
        """ menu Perspective"""
        self.MainForm.ViewOrtho = False
        self.ui.openGLWidget.update()

    def menu_show_box(self):
        """  """
        self.ui.FormSettingsViewCheckShowBox.isChecked(True)
        self.MainForm.ViewBox = True
        self.ui.openGLWidget.update()

    def menu_hide_box(self):
        """  """
        self.ui.FormSettingsViewCheckShowBox.isChecked(False)
        self.MainForm.ViewBox = False
        self.ui.openGLWidget.update()


    def menu_about(self):
        """ menu About """        
        dialogWin = QDialog(self)
        dialogWin.ui = Ui_about()
        dialogWin.ui.setupUi(self)
        dialogWin.setFixedSize(QSize(532,149))
        dialogWin.show()

    def volumeric_data_range(self):
        getSelected = self.ui.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                data = self.VolumericData.blocks
                for dat in data:
                    for da in dat:
                        if da.title.find(getChildNode) > -1:
                            return da.min, da.max

    def volumeric_data_load(self):
        getSelected = self.ui.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                atoms = self.VolumericData.load_data(getChildNode)
                model = TAtomicModel()
                atoms1 = TAtomicModel(atoms)
                for at in atoms1:
                    model.add_atom(at)
                self.models = []
                self.models.append(model)
                self.plot_model(-1)
                self.ui.FormActionsPostButSurfaceAdd.setEnabled(True)
                self.ui.FormActionsPostButContour.setEnabled(True)

                minv, maxv = self.volumeric_data_range()
                self.ui.FormActionsPostLabelSurfaceMax.setText("Max: " + str(maxv))
                self.ui.FormActionsPostLabelSurfaceMin.setText("Min: " + str(minv))
                self.ui.FormActionsPostLabelSurfaceValue.setRange(minv,maxv)
                self.ui.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))

                self.ui.FormActionsPostSliderContourXY.setMaximum(self.VolumericData.Nz)
                self.ui.FormActionsPostSliderContourXZ.setMaximum(self.VolumericData.Ny)
                self.ui.FormActionsPostSliderContourYZ.setMaximum(self.VolumericData.Nx)

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

    def plot_contour(self):
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

            if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                conts = self.VolumericData.contours(isovalues, plane, slice)
                params.append([isovalues, conts, colors])

            if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
                #params_fill.append([self.XSFfile.contours_fill(isovalues_xy, "xy", slice_xy), colors_xy])
                points = self.VolumericData.plane(plane,slice)
                colors = self.get_color_of_plane(minv, maxv, points, cmap, color_scale)
                params_colored_plane.append([points, colors])

        if self.ui.FormActionsPostRadioContour.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_contour(params)

        if self.ui.FormActionsPostRadioColorPlane.isChecked() or self.ui.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_colored_plane(params_colored_plane)
        
    def fill_file_name(self, fname):
        self.ui.Form3Dand2DTabs.setItemText(0, "3D View: "+fname)
        self.ui.Form3Dand2DTabs.update()
        
    def fill_models_list(self):
        model = QStandardItemModel()
        if len(self.models) == 1:
            model.appendRow(QStandardItem("single model"))
        else:
            for i in range(0,len(self.models)):
                model.appendRow(QStandardItem("model "+str(i)))
  
        self.ui.FormModelComboModels.setModel(model)
        self.ui.FormModelComboModels.setCurrentIndex(len(self.models)-1)
        
    def fill_atoms_table(self):
        model = self.MainForm.get_model().atoms
        self.ui.FormModelTableAtoms.setRowCount(len(model))        # и одну строку в таблице
                
        for i in range(0, len(model)):
            self.ui.FormModelTableAtoms.setItem(i, 0, QTableWidgetItem(model[i].let))
            self.ui.FormModelTableAtoms.setItem(i, 1, QTableWidgetItem(str(round(model[i].x,5))))
            self.ui.FormModelTableAtoms.setItem(i, 2, QTableWidgetItem(str(round(model[i].y,5))))
            self.ui.FormModelTableAtoms.setItem(i, 3, QTableWidgetItem(str(round(model[i].z,5))))
 
        # делаем ресайз колонок по содержимому
        #self.ui.FormModelTableAtoms.resizeColumnsToContents()
  
  
    def fill_properties_table(self):
        properties = []
                
        model = self.MainForm.get_model()
        properties.append(["Natoms",str(len(model.atoms))])
        properties.append(["LatVect1", str(model.LatVect1)])
        properties.append(["LatVect2", str(model.LatVect2)])
        properties.append(["LatVect3", str(model.LatVect3)])

        self.ui.FormModelTableProperties.setRowCount(len(properties))        # и одну строку в таблице
        
        for i in range(0, len(properties)):
            self.ui.FormModelTableProperties.setItem(i, 0, QTableWidgetItem(properties[i][0]))
            self.ui.FormModelTableProperties.setItem(i, 1, QTableWidgetItem(properties[i][1]))

        #self.ui.FormModelTableAtoms.resizeColumnsToContents()

    def check_pdos(self, fname):
        PDOSfile = Importer.CheckPDOSfile(fname)
        if PDOSfile != False:
            self.ui.FormActionsLinePDOSfile.setText(PDOSfile)
            self.ui.FormActionsButtonPlotPDOS.setEnabled(True)

    def check_bands(self, fname):
        BANDSfile = Importer.CheckBANDSfile(fname)
        if BANDSfile != False:
            self.ui.FormActionsLineBANDSfile.setText(BANDSfile)
            self.ui.FormActionsButtonPlotBANDS.setEnabled(True)

        
    def check_dos(self, fname):
        DOSfile = Importer.CheckDOSfile(fname)
        if DOSfile != False:
            self.ui.FormActionsListDOSfile.addItems([DOSfile])
            self.ui.FormActionsListDOSfile.update()
            
            eFermy = Importer.EFermySIESTA(fname)            
            DOS = Importer.DOSSIESTA(DOSfile,eFermy)
            M11S11 = str(Calculator.M11S11(DOS))
            
            i = self.ui.FormActionsTabeDOSProperty.rowCount()+1
            
            self.ui.FormActionsTabeDOSProperty.setRowCount(i)
            
            self.ui.FormActionsTabeDOSProperty.setItem(i-1, 0, QTableWidgetItem(str("?")))
            self.ui.FormActionsTabeDOSProperty.setItem(i-1, 1, QTableWidgetItem(str(eFermy)))
            self.ui.FormActionsTabeDOSProperty.setItem(i-1, 2, QTableWidgetItem(M11S11))
            
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
                if len(F)>1:
                    F = F[1]
                    if F.startswith(label) and F.endswith(".cube"):
                        files.append(Dir + "/" + F)

            files.append(Dir + "/" + label + ".XSF")
        for file in files:
            if os.path.exists(file):
                self.ui.FormActionsPostList3DData.addItems([file])
            self.ui.FormActionsPostList3DData.update()

    def clearQTreeWidget(self, tree):
        iterator = QTreeWidgetItemIterator(tree, QTreeWidgetItemIterator.All)
        while iterator.value():
            iterator.value().takeChildren()
            iterator += 1
        i = tree.topLevelItemCount()
        while i > -1:
            tree.takeTopLevelItem(i)
            i -= 1

    def fill_volumeric_data(self, data):
        type = data.type
        data = data.blocks
        self.clearQTreeWidget(self.ui.FormActionsPostTreeSurface)

        if type == "TXSF":
            for dat in data:
                text = ((dat[0].title).split('_')[3]).split(':')[0]
                parent = QTreeWidgetItem(self.ui.FormActionsPostTreeSurface)
                parent.setText(0, "{}".format(text) + "3D")
                for da in dat:
                    ch = text + ':' + (da.title).split(':')[1]
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(ch))

        if type == "TGaussianCube":
            for dat in data:
                text = dat[0].title.split(".cube")[0]
                parent = QTreeWidgetItem(self.ui.FormActionsPostTreeSurface)
                parent.setText(0, "{}".format(text))
                for da in dat:
                    ch = text
                    child = QTreeWidgetItem(parent)
                    child.setText(0, "{}".format(ch))
        self.ui.FormActionsPostTreeSurface.show()

    def fill_bonds(self):
        bonds = self.MainForm.MainModel.Bonds()
        self.ui.FormActionsPosTableBonds.setRowCount(len(bonds))  # и одну строку в таблице

        BondsType = QStandardItemModel()
        BondsType.appendRow(QStandardItem("All"))
        self.ui.FormActionsPostComboBonds.setModel(BondsType)

        mean = 0
        n = 0

        for i in range(0, len(bonds)):
            s = str(bonds[i][3])+str(bonds[i][4])+"-"+str(bonds[i][5])+str(bonds[i][6])
            self.ui.FormActionsPosTableBonds.setItem(i, 0, QTableWidgetItem(s))
            self.ui.FormActionsPosTableBonds.setItem(i, 1, QTableWidgetItem(str(bonds[i][2])))
            mean+=bonds[i][2]
            n+=1
        if n>0:
            self.ui.FormActionsPostLabelMeanBond.setText("Mean value: "+str(mean/n))


    def fill_cell_info(self, fname):
        Volume = Importer.volume(fname)
        Energy = Importer.Energy(fname)
        a = self.MainForm.MainModel.get_LatVect1_norm()
        b = self.MainForm.MainModel.get_LatVect2_norm()
        c = self.MainForm.MainModel.get_LatVect3_norm()
        self.fill_cell_info_row(Energy, Volume, a, b, c)
        self.ui.FormActionsPreZSizeFillSpace.setText(str(c))

    def fill_cell_info_row(self, Energy, Volume, a, b, c):
        i = self.ui.FormActionsPostTableCellParam.rowCount() + 1
        self.ui.FormActionsPostTableCellParam.setRowCount(i)  # и одну строку в таблице
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 0, QTableWidgetItem(str(Volume)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 1, QTableWidgetItem(str(Energy)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 2, QTableWidgetItem(str(a)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 3, QTableWidgetItem(str(b)))
        self.ui.FormActionsPostTableCellParam.setItem(i - 1, 4, QTableWidgetItem(str(c)))


    def delete_cell_param_row(self):
        row = self.ui.FormActionsPostTableCellParam.currentRow()
        self.ui.FormActionsPostTableCellParam.removeRow(row)

    def delete_isosurface_color_from_table(self):
        row = self.ui.IsosurfaceColorsTable.currentRow()
        self.ui.IsosurfaceColorsTable.removeRow(row)


        
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
            self.ui.FormActionsPreZSizeFillSpace.setText(str(c))


    def plot_bonds_histogram(self):
        bonds = self.MainForm.MainModel.Bonds()
        self.ui.MplWidget.canvas.axes.clear()
        b = []
        for bond in bonds:
            b.append(bond[2])

        num_bins = 5
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

            print(atom_index)

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

            print(species)

            number_n = [0, 1, 2, 3]
            number_l = [0, 1, 2, 3]
            number_m = [0, 1, 2, 3]
            number_z = [0, 1, 2, 3]

            pdos, energy = TSIESTA.calc_pdos(root, atom_index, species, number_l, number_m, number_n, number_z)
            EF = TSIESTA.FermiEnergy(self.filename)
            energy -=EF

            self.ui.MplWidget.canvas.axes.clear()

            xs = energy
            ys = pdos[0]
            sign = 1
            if self.ui.FormActionsCheckPDOS_2.isChecked():
                sign = -1
            ys2 = sign*pdos[1]

            self.ui.MplWidget.canvas.axes.plot(xs, ys)
            if self.ui.FormActionsCheckPDOS.isChecked():
                self.ui.MplWidget.canvas.axes.plot(xs, ys2)

            self.ui.MplWidget.canvas.axes.set_xlabel("Energy, eV")
            self.ui.MplWidget.canvas.axes.set_ylabel("PDOS, states/eV")

            self.ui.MplWidget.canvas.draw()

    def list_of_selected_items_in_combo(self, atom_index, combo):
        model = combo.model()
        maxi = combo.count()
        for i in range(0, maxi):
            if model.itemFromIndex(model.index(i, 0)).checkState() == Qt.Checked:
                atom_index.append(model.itemFromIndex(model.index(i, 0)).text())

    def plot_bands(self):
        file = self.ui.FormActionsLineBANDSfile.text()
        if os.path.exists(file):
            f = open(file)
            eF = float(f.readline())
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_float(str1)
            kmin = str1[0]
            kmax = str1[1]
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_float(str1)
            emin = str1[0]
            emax = str1[1]
            str1 = f.readline().split()
            str1 = Helpers.list_str_to_int(str1)
            kmesh = np.zeros((str1[2]))
            bands = np.zeros((str1[0],str1[2]))
            for i in range(0,str1[2]):
                str2 = f.readline().split()
                str2 = Helpers.list_str_to_float(str2)
                kmesh[i] = str2[0]
                for j in range(1,len(str2)):
                    bands[j-1][i] = str2[j]
                kol = len(str2)-1
                while kol < str1[0]:
                    str2 = f.readline().split()
                    str2 = Helpers.list_str_to_float(str2)
                    for j in range(0, len(str2)):
                        bands[kol + j][i] = str2[j]
                    kol += len(str2)
            nsticks = int(f.readline())
            xticks = []
            xticklabels = []
            for i in range(0,nsticks):
                str3 = f.readline().split()
                xticks.append(float(str3[0]))
                xticklabels.append(str3[1])
            f.close()
            #print(bands)
            #print(xticks)
            self.ui.MplWidget.canvas.axes.clear()
            for band in bands:
                self.ui.MplWidget.canvas.axes.plot(kmesh, band)
            self.ui.MplWidget.canvas.axes.set_xticks(xticks)
            self.ui.MplWidget.canvas.axes.set_xticklabels(xticklabels)
            self.ui.MplWidget.canvas.axes.set_xlabel("k")
            self.ui.MplWidget.canvas.axes.set_ylabel("Energy, eV")

            self.ui.MplWidget.canvas.draw()
           
    def plot_dos(self):
        items = []
        for index in range(self.ui.FormActionsListDOSfile.count()):
            eF = float(self.ui.FormActionsTabeDOSProperty.item(index,1).text())
            items.append([self.ui.FormActionsListDOSfile.item(index).text(),eF])
        
        self.ui.MplWidget.canvas.axes.clear()
        
        for file in items:
            if os.path.exists(file[0]):
                DOS = Importer.DOSSIESTA(file[0],file[1])
            
                xs = []
                ys = []
                ys2= []
                sign = 1
                if self.ui.FormActionsCheckDOS_2.isChecked():
                    sign = -1
                for row in DOS:
                    xs.append(row[0])
                    ys.append(row[1])
                    ys2.append(sign*float(row[2]))

                self.ui.MplWidget.canvas.axes.plot(xs, ys)
                if self.ui.FormActionsCheckDOS.isChecked():
                        self.ui.MplWidget.canvas.axes.plot(xs, ys2)
                
        self.ui.MplWidget.canvas.axes.set_xlabel("Energy, eV")
        self.ui.MplWidget.canvas.axes.set_ylabel("DOS, states/eV")

        self.ui.MplWidget.canvas.draw()

    def clear_dos(self):
        self.ui.FormActionsListDOSfile.clear()  #      addItems([DOSfile])
        self.ui.FormActionsListDOSfile.update()

        self.ui.FormActionsTabeDOSProperty.setRowCount(0)
        self.ui.FormActionsTabeDOSProperty.update()


    def plot_volume_param_energy(self):
        items = []
        method = self.ui.FormActionsPostComboCellParam.currentText()
        xi = self.ui.FormActionsPostComboCellParamX.currentIndex()
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

            #self.MplWidget.canvas.axes.plot(xs, ys)
            self.ui.MplWidget.canvas.axes.scatter(xs, ys, color='orange', s=40, marker='o')

            if method == "Parabola":
                aprox, xs2, ys2 = Calculator.ApproxParabola(items)
                image_path = '.\images\parabola.png' #path to your image file
                self.ui.FormActionsPostLabelCellParamOptimExpr.setText("E(x0)="+str(round(float(aprox[0]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr2.setText("a="+str(round(float(aprox[1]),2)))
                self.ui.FormActionsPostLabelCellParamOptimExpr3.setText("b="+str(round(float(aprox[2]),2)))

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

            self.ui.MplWidget.canvas.axes.plot(xs2, ys2)
                
            self.ui.MplWidget.canvas.axes.set_xlabel("volume, A^3")
            self.ui.MplWidget.canvas.axes.set_ylabel("Energy, eV")

            self.ui.MplWidget.canvas.draw()

            image_profile = QImage(image_path)
            print(image_profile)
            image_profile = image_profile.scaled(320,320, aspectRatioMode=QKeepAspectRatio, transformMode=Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration
            self.ui.FormActionsPostLabelCellParamFig.setPixmap(QPixmap.fromImage(image_profile))
            
            
    def add_dos_file(self):
        """ menu Open"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        self.WorkDir = os.path.dirname(fname)
        self.check_dos(fname)
            
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
        #print(DATA)
        
    def save_image_to_file(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File', self.WorkDir, "PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp)")[0]
        newWindow = Image3Dexporter(5*self.ui.openGLWidget.width(), 5*self.ui.openGLWidget.height())
        newWindow.MainForm.copy_state(self.MainForm)
        newWindow.MainForm.image3D_to_file(fname)
        self.WorkDir = os.path.dirname(fname)
        self.save_active_Folder()

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


    def file_brouser_selection(self, selected, deselected):
        self.IndexOfFileToOpen = selected.indexes()[0]
        text = str(self.ui.FileBrouserTree.model().filePath(self.IndexOfFileToOpen))
        self.ui.FileBrouserOpenLine.setText(text)
        self.ui.FileBrouserOpenLine.update()

    def save_active_Folder(self):
        self.save_property(SETTINGS_Folder, self.WorkDir)

    def save_state_FormSettingsOpeningCheckOnlyOptimal(self):
        self.save_property(SETTINGS_FormSettingsOpeningCheckOnlyOptimal,
                           self.ui.FormSettingsOpeningCheckOnlyOptimal.isChecked())

    def save_state_FormSettingsViewCheckShowAxes(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowAxes,
                           self.ui.FormSettingsViewCheckShowAxes.isChecked())
        self.MainForm.set_axes_visible(self.ui.FormSettingsViewCheckShowAxes.isChecked())

    def save_state_FormSettingsViewCheckAtomSelection(self):
        self.save_property(SETTINGS_FormSettingsViewCheckAtomSelection,
                           self.ui.FormSettingsViewCheckAtomSelection.isChecked())

    def save_state_FormSettingsViewCheckShowBox(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBox, self.ui.FormSettingsViewCheckShowBox.isChecked())
        self.MainForm.set_box_visible(self.ui.FormSettingsViewCheckShowBox.isChecked())

    def save_state_FormSettingsViewCheckShowBonds(self):
        self.save_property(SETTINGS_FormSettingsViewCheckShowBonds, self.ui.FormSettingsViewCheckShowBonds.isChecked())
        self.MainForm.set_bonds_visible(self.ui.FormSettingsViewCheckShowBonds.isChecked())

    def save_state_FormSettingsColorsFixed(self):
        self.save_property(SETTINGS_FormSettingsColorsFixed, self.ui.FormSettingsColorsFixed.isChecked())

    def save_state_FormSettingsColorsFixedMin(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMin, self.ui.FormSettingsColorsFixedMin.text())

    def save_state_FormSettingsViewSpinBondWidth(self):
        self.save_property(SETTINGS_FormSettingsViewSpinBondWidth, self.ui.FormSettingsViewSpinBondWidth.text())

    def save_state_FormSettingsColorsFixedMax(self):
        self.save_property(SETTINGS_FormSettingsColorsFixedMax, self.ui.FormSettingsColorsFixedMax.text())

    def save_state_FormSettingsColorsScale(self):
        self.save_property(SETTINGS_FormSettingsColorsScale, self.ui.FormSettingsColorsScale.currentText())
        self.colors_cash = {}

    def save_state_FormSettingsColorsScaleType(self):
        self.save_property(SETTINGS_FormSettingsColorsScaleType, self.ui.FormSettingsColorsScaleType.currentText())
        self.colors_cash = {}

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
        text = self.FDFData.get_all_data(model.atoms)
        self.ui.FormActionsPreTextFDF.setText(text)

    def fdf_data_from_form_to_file(self):
        text = self.ui.FormActionsPreTextFDF.toPlainText()

        name = QFileDialog.getSaveFileName(self, 'Save File')[0]
        with open(name, 'w') as f:
            f.write(text)

    def fill_space(self):
        Mendeley = TPeriodTable()
        nAtoms = int(self.ui.FormActionsPreNAtomsFillSpace.text())
        charge = int(self.ui.FormActionsPreAtomChargeFillSpace.text())
        radAtom = Mendeley.get_rad(charge)
        #print(radAtom)
        let = Mendeley.get_let(charge)
        delta = float(self.ui.FormActionsPreDeltaFillSpace.text())
        nPrompts = int(self.ui.FormActionsPreNPromptsFillSpace.text())
        radTube = float(self.ui.FormActionsPreRadiusFillSpace.text())
        length = float(self.ui.FormActionsPreZSizeFillSpace.text())
        models = Calculator.FillTube(radTube, length, nAtoms, 0.01*radAtom, delta, nPrompts, let, charge)
        #print(len(models))

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
        Selected = self.ui.FormActionsPostList3DData.selectedItems()[0].text()
        if Selected.endswith(".XSF"):
            self.VolumericData = TXSF()
        if Selected.endswith(".cube"):
            self.VolumericData = TGaussianCube()
        if self.VolumericData.parse(Selected):
            data = self.VolumericData.blocks
            self.fill_volumeric_data(self.VolumericData)

        self.ui.FormActionsPostButSurfaceLoadData.setEnabled(True)

    def set_xsf_z_position(self):
        value = int(self.ui.FormActionsPostSliderContourXY.value())
        self.ui.FormActionsPostLabelContourXYposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourXY.maximum()))

    def set_xsf_y_position(self):
        value = int(self.ui.FormActionsPostSliderContourXZ.value())
        self.ui.FormActionsPostLabelContourXZposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourXZ.maximum()))

    def set_xsf_x_position(self):
        value = int(self.ui.FormActionsPostSliderContourYZ.value())
        self.ui.FormActionsPostLabelContourYZposition.setText("Slice "+str(value)+" among "+str(self.ui.FormActionsPostSliderContourYZ.maximum()))

    def swnt_create(self):
        n = int(self.ui.FormActionsPreLineSWNTn.text())
        m = int(self.ui.FormActionsPreLineSWNTm.text())
        if self.ui.FormActionsPreRadioSWNTuselen.isChecked():
            leng = float(self.ui.FormActionsPreLineSWNTlen.text())
            cells = 1
        else:
            leng = 0
            cells = float(self.ui.FormActionsPreLineSWNTcells.text())

        model = TSWNT(n,m,leng,cells)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("SWNT-model")


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

    def change_color(self, colorUi, property):
        color = QColorDialog.getColor()
        colorUi.setStyleSheet(
            "background-color:rgb(" + str(color.getRgb()[0]) + "," + str(color.getRgb()[1]) + "," + str(
                color.getRgb()[2]) + ")")
        newcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        self.save_property(property,
                           str(color.getRgb()[0]) + " " + str(color.getRgb()[1]) + " " + str(color.getRgb()[2]))
        return newcolor

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
        self.ui.IsosurfaceColorsTable.setCellWidget(i - 1, 1, transp_cell)
        minv, maxv = self.volumeric_data_range()
        color = self.get_color(cmap, minv, maxv, float(value), color_scale)
        self.ui.IsosurfaceColorsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], color[3]))

        self.ui.FormActionsPostButSurface.setEnabled(True)
        self.ui.FormActionsPostButSurfaceDelete.setEnabled(True)

    def atom_delete(self):
        self.MainForm.delete_selected_atom()

    def atom_modify(self):
        self.MainForm.modify_selected_atom()

    def atom_add(self):
        self.MainForm.add_new_atom()


ORGANIZATION_NAME = 'Sozykin'
ORGANIZATION_DOMAIN = 'example.com'
APPLICATION_NAME = 'p4dft'

SETTINGS_Folder = '\home'
SETTINGS_FormSettingsColorsScale = 'colors/ColorsScale'
SETTINGS_FormSettingsColorsFixed = 'colors/ColorsFixed'
SETTINGS_FormSettingsColorsFixedMin = 'colors/ColorsFixedMin'
SETTINGS_FormSettingsColorsFixedMax = 'colors/ColorsFixedMin'
SETTINGS_FormSettingsColorsScaleType = 'colors/ColorsFixedMin'
SETTINGS_FormSettingsOpeningCheckOnlyOptimal = 'open/CheckOnlyOptimal'
SETTINGS_FormSettingsViewCheckAtomSelection = 'view/CheckAtomSelection'
SETTINGS_FormSettingsViewCheckShowBox = 'view/CheckShowBox'
SETTINGS_FormSettingsViewCheckShowAxes = 'view/CheckShowAxes'
SETTINGS_FormSettingsViewCheckShowBonds = 'view/CheckShowBonds'
SETTINGS_FormSettingsViewSpinBondWidth = 'view/SpinBondWidth'

SETTINGS_Color_Of_Atoms = 'colors/atoms'
SETTINGS_Color_Of_Bonds = 'colors/bonds'
SETTINGS_Color_Of_Box = 'colors/box'
SETTINGS_Color_Of_Voronoi = 'colors/voronoi'
SETTINGS_Color_Of_Axes = 'colors/axes'

QCoreApplication.setApplicationName(ORGANIZATION_NAME)
QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
QCoreApplication.setApplicationName(APPLICATION_NAME)

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)
window = mainWindow()
window.setupUI()
window.show()

sys.exit(app.exec_())