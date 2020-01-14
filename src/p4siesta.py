# -*- coding: utf-8 -*-

import sys
import os
import math
from copy import deepcopy
import time
from operator import itemgetter


from PyQt5.QtCore import QObject
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QSettings
#from PyQt5.QtCore import QItemSelection
from PyQt5.QtCore import QDir
#from PyQt5.QtCore import QMimeData
#import PyQt5.QtCore as QtCore
from PyQt5 import QtWidgets as qWidget
from PyQt5.QtWidgets import QColorDialog
from PyQt5 import uic
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
from TInterface import Image3Dexporter


class MyFilter(QObject):
    global window
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            window.MainForm.scale(event.angleDelta().y())
        
        if event.type() == QEvent.MouseMove:         
            if event.buttons() == Qt.LeftButton:
                window.MainForm.rotat(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())
                window.MainForm.setXY(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())

            elif event.buttons() == Qt.RightButton:
                if window.MainForm.isAtomSelected():
                    window.MainForm.move_atom(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())
                else:
                    window.MainForm.move(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())
                window.MainForm.setXY(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())

        elif event.type() == QEvent.MouseButtonPress:

            if window.FormSettingsViewCheckAtomSelection.isChecked() and event.buttons() == Qt.LeftButton:
                window.MainForm.CanSearch = True
            window.MainForm.setXY(event.x(), event.y(), window.openGLWidget.width(), window.openGLWidget.height())
        return False

class mainWindow(qWidget.QMainWindow):  
    def __init__(self, *args):
        super(mainWindow, self).__init__(*args)
        ui = os.path.join(os.path.dirname(__file__), 'form.ui')
        uic.loadUi(ui, self)

        self.models = []
        self.MainForm = GuiOpenGL(self.openGLWidget)
        self.FDFData = TFDFFile()
        self.XSFfile = TXSF()
        self.filename = ""
        self.colors_cash = {}

    def setupUI(self):
        print("\033[1;101m SETU6P UI \033[0m")
        self.openGLWidget.initializeGL()
        self.openGLWidget.paintGL = self.MainForm.paintGL
        self.openGLWidget.initializeGL = self.MainForm.initializeGL
        self.openGLWidget.setMouseTracking(True)        
        self.filter = MyFilter()      
        self.openGLWidget.installEventFilter(self.filter)

        # The SETTINGS
        settings = QSettings()
        state_FormSettingsOpeningCheckOnlyOptimal = settings.value(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, False,
                                                                   type=bool)
        self.FormSettingsOpeningCheckOnlyOptimal.setChecked(state_FormSettingsOpeningCheckOnlyOptimal)
        self.FormSettingsOpeningCheckOnlyOptimal.clicked.connect(self.save_state_FormSettingsOpeningCheckOnlyOptimal)

        state_FormSettingsViewCheckAtomSelection = settings.value(SETTINGS_FormSettingsViewCheckAtomSelection, False,
                                                                  type=bool)
        self.FormSettingsViewCheckAtomSelection.setChecked(state_FormSettingsViewCheckAtomSelection)
        self.FormSettingsViewCheckAtomSelection.clicked.connect(self.save_state_FormSettingsViewCheckAtomSelection)

        state_FormSettingsViewCheckShowBox = settings.value(SETTINGS_FormSettingsViewCheckShowBox, False, type=bool)
        self.FormSettingsViewCheckShowBox.setChecked(state_FormSettingsViewCheckShowBox)
        self.FormSettingsViewCheckShowBox.clicked.connect(self.save_state_FormSettingsViewCheckShowBox)

        state_FormSettingsViewCheckShowBonds = settings.value(SETTINGS_FormSettingsViewCheckShowBonds, False, type=bool)
        self.FormSettingsViewCheckShowBonds.setChecked(state_FormSettingsViewCheckShowBonds)
        self.FormSettingsViewCheckShowBonds.clicked.connect(self.save_state_FormSettingsViewCheckShowBonds)

        self.WorkDir = str(settings.value(SETTINGS_Folder, "/home"))

        self.ColorType = str(settings.value(SETTINGS_FormSettingsColorsScale, 'rainbow'))
        self.FormSettingsColorsScale.currentIndexChanged.connect(self.save_state_FormSettingsColorsScale)
        self.FormSettingsColorsScale.currentTextChanged.connect(self.state_changed_FormSettingsColorsScale)

        self.ColorTypeScale = str(settings.value(SETTINGS_FormSettingsColorsScaleType, 'Log'))
        self.FormSettingsColorsScaleType.currentIndexChanged.connect(self.save_state_FormSettingsColorsScaleType)

        state_FormSettingsColorsFixed = settings.value(SETTINGS_FormSettingsColorsFixed, False, type=bool)
        self.FormSettingsColorsFixed.setChecked(state_FormSettingsColorsFixed)
        self.FormSettingsColorsFixed.clicked.connect(self.save_state_FormSettingsColorsFixed)

        state_FormSettingsColorsFixedMin = settings.value(SETTINGS_FormSettingsColorsFixedMin, '0.0')
        self.FormSettingsColorsFixedMin.setText(state_FormSettingsColorsFixedMin)
        self.FormSettingsColorsFixedMin.textChanged.connect(self.save_state_FormSettingsColorsFixedMin)

        state_FormSettingsColorsFixedMax = settings.value(SETTINGS_FormSettingsColorsFixedMax, '0.2')
        self.FormSettingsColorsFixedMax.setText(state_FormSettingsColorsFixedMax)
        self.FormSettingsColorsFixedMax.textChanged.connect(self.save_state_FormSettingsColorsFixedMax)

        self.ColorsOfAtomsTable.setColumnCount(1)
        self.ColorsOfAtomsTable.setHorizontalHeaderLabels(["Values"])
        self.ColorsOfAtomsTable.setColumnWidth(0, 120)
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
        for i in range(1, len(lets)-1):
            self.ColorsOfAtomsTable.setRowCount(i)  # и одну строку в таблице
            self.ColorsOfAtomsTable.setItem(i - 1, 0, qWidget.QTableWidgetItem(lets[i]))
            color = colors[i]
            self.ColorsOfAtomsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], 1))

        self.state_Color_Of_Bonds = str(settings.value(SETTINGS_Color_Of_Bonds, '0 0 255'))
        r = self.state_Color_Of_Bonds.split()[0]
        g = self.state_Color_Of_Bonds.split()[1]
        b = self.state_Color_Of_Bonds.split()[2]
        self.ColorBond.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

        self.state_Color_Of_Box = str(settings.value(SETTINGS_Color_Of_Box, '0 0 0'))
        r = self.state_Color_Of_Box.split()[0]
        g = self.state_Color_Of_Box.split()[1]
        b = self.state_Color_Of_Box.split()[2]
        self.ColorBox.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

        self.state_Color_Of_Voronoi = str(settings.value(SETTINGS_Color_Of_Voronoi, '255 0 0'))
        r = self.state_Color_Of_Voronoi.split()[0]
        g = self.state_Color_Of_Voronoi.split()[1]
        b = self.state_Color_Of_Voronoi.split()[2]
        self.ColorVoronoi.setStyleSheet("background-color:rgb(" + r + "," + g + "," + b + ")")

        self.actionOpen.triggered.connect(self.menu_open)
        self.actionOrtho.triggered.connect(self.menu_ortho)
        self.actionPerspective.triggered.connect(self.menu_perspective)
        self.actionShowBox.triggered.connect(self.menu_show_box)
        self.actionHideBox.triggered.connect(self.menu_hide_box)
        
        self.actionAbout.triggered.connect(self.menu_about)

        self.FormModelComboModels.currentIndexChanged.connect(self.model_to_screen)
        self.FormActionsPostTreeSurface.itemSelectionChanged.connect(self.type_of_surface)
        
        #buttons
        self.FileBrouserOpenFile.clicked.connect(self.menu_open)
        self.FormActionsPostButCreateBonds.clicked.connect(self.fill_bonds)
        self.FormActionsPostButPlotBondsHistogram.clicked.connect(self.plot_bonds_histogram)
        self.FormActionsPreButFDFGenerate.clicked.connect(self.fdf_data_to_form)
        self.FormActionsPreButFDFToFile.clicked.connect(self.fdf_data_from_form_to_file)
        self.FormActionsPreButFillSpace.clicked.connect(self.fill_space)
        self.FormActionsPreButSWNTGenerate.clicked.connect(self.swnt_create)
        self.FormActionsPostButSurface.clicked.connect(self.plot_surface)
        self.FormActionsPostButSurfaceParse.clicked.connect(self.parse_xsf)
        self.FormActionsPostButSurfaceLoadData.clicked.connect(self.load_xsf_data)
        self.FormActionsPostButContour.clicked.connect(self.plot_contour)
        self.ColorBondDialogButton.clicked.connect(self.select_bond_color)
        self.ColorBoxDialogButton.clicked.connect(self.select_box_color)
        self.ColorAtomDialogButton.clicked.connect(self.select_atom_color)
        self.ColorVoronoiDialogButton.clicked.connect(self.select_voronoi_color)
        self.FormActionsPostButSurfaceAdd.clicked.connect(self.add_isosurface_color_to_table)
        self.FormActionsPostButSurfaceDelete.clicked.connect(self.delete_isosurface_color_from_table)
                
        self.FormActionsButtonAddDOSFile.clicked.connect(self.add_dos_file)
        self.FormActionsButtonPlotDOS.clicked.connect(self.plot_dos)
        self.FormActionsButtonClearDOS.clicked.connect(self.clear_dos)

        self.FormActionsPostButPlusCellParam.clicked.connect(self.add_cell_param)
        self.FormActionsPostButAddRowCellParam.clicked.connect(self.add_cell_param_row)
        self.FormActionsPostButDeleteRowCellParam.clicked.connect(self.delete_cell_param_row)
        self.FormActionsPostButPlusDataCellParam.clicked.connect(self.add_data_cell_param)

        self.FormActionsPostButVoronoi.clicked.connect(self.plot_voronoi)
        
        self.FormActionsPostButOptimizeCellParam.clicked.connect(self.plot_volume_param_energy)
        
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        # sliders
        self.FormActionsPostSliderContourXY.valueChanged.connect(self.set_xsf_z_position)
        self.FormActionsPostSliderContourXZ.valueChanged.connect(self.set_xsf_y_position)
        self.FormActionsPostSliderContourYZ.valueChanged.connect(self.set_xsf_x_position)

        
        self.FormModelTableAtoms.setColumnCount(4)     # Устанавливаем 4 колонки
        # Устанавливаем заголовки таблицы
        self.FormModelTableAtoms.setHorizontalHeaderLabels(["Atom", "x", "y","z"])
        self.FormModelTableAtoms.setColumnWidth(0, 40)
        
        self.FormModelTableProperties.setColumnCount(2)     # Устанавливаем 2 колонки
        # Устанавливаем заголовки таблицы
        self.FormModelTableProperties.setHorizontalHeaderLabels(["Property", "Value"])
        self.FormModelTableProperties.setColumnWidth(0, 90)
        self.FormModelTableProperties.setColumnWidth(1, 90)
        
        
        self.FormActionsTabeDOSProperty.setColumnCount(3)     # Устанавливаем три колонки
        # Устанавливаем заголовки таблицы
        self.FormActionsTabeDOSProperty.setHorizontalHeaderLabels(["sp", "EFermy","S11 (M11)"])
        self.FormActionsTabeDOSProperty.setColumnWidth(0, 40)
        self.FormActionsTabeDOSProperty.setColumnWidth(1, 80)
        self.FormActionsTabeDOSProperty.setColumnWidth(2, 80)


        self.IsosurfaceColorsTable.setColumnCount(2)
        self.IsosurfaceColorsTable.setHorizontalHeaderLabels(["Value","Transparancy"])
        self.IsosurfaceColorsTable.setColumnWidth(0, 120)
        self.IsosurfaceColorsTable.setColumnWidth(1, 150)

        CellPredictionType = QStandardItemModel()
        CellPredictionType.appendRow(QStandardItem("Murnaghan"))
        CellPredictionType.appendRow(QStandardItem("BirchMurnaghan"))
        CellPredictionType.appendRow(QStandardItem("Parabola"))
        self.FormActionsPostComboCellParam.setModel(CellPredictionType)


        FillSpaceModel = QStandardItemModel()
        FillSpaceModel.appendRow(QStandardItem("cylinder"))
        FillSpaceModel.appendRow(QStandardItem("parallelepiped"))
        self.FormActionsPreComboFillSpace.setModel(FillSpaceModel)


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

        self.FormSettingsColorsScale.setModel(ColorType)
        #self.FormSettingsColorsScale.setCurrentIndex(ColorType.indexFromItem(QStandardItem(self.ColorType)).row())
        self.FormSettingsColorsScale.setCurrentText(self.ColorType)


        ColorTypeScale = QStandardItemModel()
        ColorTypeScale.appendRow(QStandardItem("Linear"))
        ColorTypeScale.appendRow(QStandardItem("Log"))
        self.FormSettingsColorsScaleType.setModel(ColorTypeScale)
        self.FormSettingsColorsScaleType.setCurrentText(self.ColorTypeScale)


        self.FormActionsPostTableCellParam.setColumnCount(5)     # Устанавливаем три колонки
        # Устанавливаем заголовки таблицы
        self.FormActionsPostTableCellParam.setHorizontalHeaderLabels(["Volume", "Energy","a","b","c"])
        self.FormActionsPostTableCellParam.setColumnWidth(0, 60)
        self.FormActionsPostTableCellParam.setColumnWidth(1, 60)
        self.FormActionsPostTableCellParam.setColumnWidth(2, 50)
        self.FormActionsPostTableCellParam.setColumnWidth(3, 50)
        self.FormActionsPostTableCellParam.setColumnWidth(4, 50)

        
        argsCell = QStandardItemModel()
        argsCell.appendRow(QStandardItem("V"))
        argsCell.appendRow(QStandardItem("E"))
        argsCell.appendRow(QStandardItem("a"))
        argsCell.appendRow(QStandardItem("b"))
        argsCell.appendRow(QStandardItem("c")) 
        self.FormActionsPostComboCellParamX.setModel(argsCell)


        self.FormActionsPosTableBonds.setColumnCount(2)
        self.FormActionsPosTableBonds.setHorizontalHeaderLabels(["Bond", "Lenght"])
        self.FormActionsPosTableBonds.setColumnWidth(0, 70)
        self.FormActionsPosTableBonds.setColumnWidth(1, 180)

        openAction = qWidget.QAction(QIcon('./images/Open.jpg'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.menu_open)
        self.toolBar.addAction(openAction)

        modelFile = qWidget.QFileSystemModel()
        modelFile.setRootPath((QDir.rootPath()))
        self.FileBrouserTree.setModel(modelFile)
        self.FileBrouserTree.selectionModel().selectionChanged.connect(self.file_brouser_selection)

        # xRot = qWidget.QAction('Xrot', self)
        # self.toolBar.addAction(xRot)

        # yRot = qWidget.QAction('Yrot', self)
        # self.toolBar.addAction(yRot)

        # zRot = qWidget.QAction('Zrot', self)
        # self.toolBar.addAction(zRot)

        SaveImageToFileAction = qWidget.QAction(QIcon('./images/Save3D.jpg'), 'SaveFigure3D', self)
        SaveImageToFileAction.triggered.connect(self.save_image_to_file)
        self.toolBar.addAction(SaveImageToFileAction)

        Save2DImageToFileAction = qWidget.QAction(QIcon('./images/Save2D.jpg'), 'SaveDataFromFigure', self)
        Save2DImageToFileAction.triggered.connect(self.save_data_from_figure2d)
        self.toolBar.addAction(Save2DImageToFileAction)


    def add_cell_param(self):
        """ add cell params"""
        fname = qWidget.QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        if Importer.checkFormat(fname) == "SIESTAout":
            self.fill_cell_info(fname)

    def add_cell_param_row(self):
        i = self.FormActionsPostTableCellParam.rowCount()+1
        self.FormActionsPostTableCellParam.setRowCount(i)

    def add_data_cell_param(self):
        """ add cell params from file"""
        fname = qWidget.QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
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
        atomscolor = [ self.ColorsOfAtomsTable.item(0, 0).background().color().getRgbF()]
        for i in range(0, self.ColorsOfAtomsTable.rowCount()):
            col = self.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
        return atomscolor

    def get_color_from_SETTING(self, strcolor):
        r = strcolor.split()[0]
        g = strcolor.split()[1]
        b = strcolor.split()[2]
        bondscolor = [float(r) / 255, float(g) / 255, float(b) / 255]
        return bondscolor
        
    def menu_open(self):
        """ menu Open"""
        self.Form3Dand2DTabs.setCurrentIndex(0)
        if self.FileBrouserUseCheckBox.isChecked():
            fname = self.FileBrouserTree.model().filePath(self.IndexOfFileToOpen)
        else:
            fname = qWidget.QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        if os.path.exists(fname):
            self.filename = fname
            self.WorkDir = os.path.dirname(fname)
            if self.FormSettingsOpeningCheckOnlyOptimal.isChecked():
                self.models, self.FDFData = Importer.Import(fname, 'opt')
            else:
                self.models, self.FDFData = Importer.Import(fname)
            if len(self.models)>0:
                if len(self.models[-1].atoms) > 0:
                    value = -1
                    self.plot_model(value)
                    self.fill_gui()
                    self.save_active_Folder()


    def model_to_screen(self, value):
        """print("combobox changed", value)"""
        self.plot_model(value)
        self.fill_atoms_table()
        self.fill_properties_table()

    def plot_model(self, value):
        ViewBox = self.FormSettingsViewCheckShowBox.isChecked()
        ViewBonds = self.FormSettingsViewCheckShowBonds.isChecked()
        bondscolor = self.get_color_from_SETTING(self.state_Color_Of_Bonds)
        boxcolor = self.get_color_from_SETTING(self.state_Color_Of_Box)
        atomscolor = self.colors_of_atoms()
        self.MainForm.set_atomic_structure(self.models[value], atomscolor, ViewBox, boxcolor, ViewBonds, bondscolor)

    def menu_ortho(self):
        """ menu Ortho"""
        self.MainForm.ViewOrtho = True
        window.openGLWidget.update() 


    def menu_perspective(self):
        """ menu Perspective"""
        self.MainForm.ViewOrtho = False
        window.openGLWidget.update()

    def menu_show_box(self):
        """  """
        self.FormSettingsViewCheckShowBox.isChecked(True)
        self.MainForm.ViewBox = True
        window.openGLWidget.update()

    def menu_hide_box(self):
        """  """
        self.FormSettingsViewCheckShowBox.isChecked(False)
        self.MainForm.ViewBox = False
        window.openGLWidget.update()


    def menu_about(self):
        """ menu About """        
        dialogWin = qWidget.QDialog(self)
        ui = os.path.join(os.path.dirname(__file__), 'about.ui')
        uic.loadUi(ui, dialogWin)
        dialogWin.setFixedSize(QSize(532,149))
        dialogWin.show()

    def xsf_data_range(self):
        getSelected = self.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                data = self.XSFfile.blocks
                for dat in data:
                    for da in dat:
                        if da.title.find(getChildNode) > -1:
                            return da.min, da.max

    def load_xsf_data(self):
        getSelected = self.FormActionsPostTreeSurface.selectedItems()
        if getSelected:
            if getSelected[0].parent() != None:
                getChildNode = getSelected[0].text(0)
                atoms, box = self.XSFfile.load_data(getChildNode)
                model = TAtomicModel()
                model.box = box
                atoms1 = TAtomicModel(atoms)
                for at in atoms1:
                    model.AddAtom(at)
                self.models = []
                self.models.append(model)
                self.MainForm.MainModel = self.models[-1]
                self.FormActionsPostButSurfaceAdd.setEnabled(True)
                self.FormActionsPostButContour.setEnabled(True)

                minv, maxv = self.xsf_data_range()
                self.FormActionsPostLabelSurfaceMax.setText("Max: " + str(maxv))
                self.FormActionsPostLabelSurfaceMin.setText("Min: " + str(minv))
                self.FormActionsPostLabelSurfaceValue.setRange(minv,maxv)
                self.FormActionsPostLabelSurfaceValue.setValue(round(0.5 * (maxv + minv), 5))

                self.FormActionsPostSliderContourXY.setMaximum(self.XSFfile.Nz)
                self.FormActionsPostSliderContourXZ.setMaximum(self.XSFfile.Ny)
                self.FormActionsPostSliderContourYZ.setMaximum(self.XSFfile.Nx)

    def plot_surface(self):
        self.MainForm.ViewSurface = False
        cmap = plt.get_cmap(self.FormSettingsColorsScale.currentText())
        color_scale = self.FormSettingsColorsScaleType.currentText()
        if self.FormSettingsColorsFixed.isChecked():
            minv = float(self.FormSettingsColorsFixedMin.text())
            maxv = float(self.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.xsf_data_range()
        if self.FormActionsPostCheckSurface.isChecked():
            data = []
            for i in range(0, self.IsosurfaceColorsTable.rowCount()):
                value = float(self.IsosurfaceColorsTable.item(i, 0).text())
                verts, faces = self.XSFfile.isosurface(value)
                transp = float(self.IsosurfaceColorsTable.cellWidget(i, 1).text())
                color = self.get_color(cmap, minv, maxv, value, color_scale)
                color = (color[0], color[1], color[2], transp)
                data.append([verts, faces, color])
            self.MainForm.add_surface(data)

    def plot_contous_isovalues(self, n_contours, scale = "Log"):
        minv, maxv = self.xsf_data_range()
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
        cmap = plt.get_cmap(self.FormSettingsColorsScale.currentText())
        color_scale = self.FormSettingsColorsScaleType.currentText()
        if self.FormSettingsColorsFixed.isChecked():
            minv = float(self.FormSettingsColorsFixedMin.text())
            maxv = float(self.FormSettingsColorsFixedMax.text())
        else:
            minv, maxv = self.xsf_data_range()
        params = []
        params_colored_plane = []

        planes = []
        if self.FormActionsPostCheckContourXY.isChecked():
            planes.append("xy")
        if self.FormActionsPostCheckContourXZ.isChecked():
            planes.append("xz")
        if self.FormActionsPostCheckContourYZ.isChecked():
            planes.append("yz")

        for plane in planes:
            if plane == "xy":
                n_contours = int(self.FormActionsPostLabelSurfaceNcontoursXY.text())
                slice = int(self.FormActionsPostSliderContourXY.value())
            if plane == "xz":
                n_contours = int(self.FormActionsPostLabelSurfaceNcontoursXZ.text())
                slice = int(self.FormActionsPostSliderContourXZ.value())
            if plane == "yz":
                n_contours = int(self.FormActionsPostLabelSurfaceNcontoursYZ.text())
                slice = int(self.FormActionsPostSliderContourYZ.value())

            isovalues = self.plot_contous_isovalues(n_contours, color_scale)

            if self.FormActionsPostRadioColorPlaneContours.isChecked():
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, 'black')
            else:
                colors = self.get_colors_list(minv, maxv, isovalues, cmap, color_scale)

            if self.FormActionsPostRadioContour.isChecked() or self.FormActionsPostRadioColorPlaneContours.isChecked():
                conts = self.XSFfile.contours(isovalues, plane, slice)
                params.append([isovalues, conts, colors])

            if self.FormActionsPostRadioColorPlane.isChecked() or self.FormActionsPostRadioColorPlaneContours.isChecked():
                #params_fill.append([self.XSFfile.contours_fill(isovalues_xy, "xy", slice_xy), colors_xy])
                points = self.XSFfile.plane(plane,slice)
                colors = self.get_color_of_plane(minv, maxv, points, cmap, color_scale)
                params_colored_plane.append([points, colors])

        if self.FormActionsPostRadioContour.isChecked() or self.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_contour(params)

        if self.FormActionsPostRadioColorPlane.isChecked()  or self.FormActionsPostRadioColorPlaneContours.isChecked():
            self.MainForm.add_colored_plane(params_colored_plane)
            #self.MainForm.add_contour_fill(params_fill)
        #self.openGLWidget.update()
        
    def fill_file_name(self, fname):
        self.Form3Dand2DTabs.setItemText(0, "3D View: "+fname)        
        self.Form3Dand2DTabs.update()
        
    def fill_models_list(self):
        model = QStandardItemModel()
        if len(self.models) == 1:
            model.appendRow(QStandardItem("single model"))
        else:
            for i in range(0,len(self.models)):
                model.appendRow(QStandardItem("model "+str(i)))
  
        self.FormModelComboModels.setModel(model)
        self.FormModelComboModels.setCurrentIndex(len(self.models)-1)
        
    def fill_atoms_table(self):
        model = self.MainForm.MainModel.atoms        
        self.FormModelTableAtoms.setRowCount(len(model))        # и одну строку в таблице 
                
        for i in range(0, len(model)):
            self.FormModelTableAtoms.setItem(i, 0, qWidget.QTableWidgetItem(model[i].let))
            self.FormModelTableAtoms.setItem(i, 1, qWidget.QTableWidgetItem(str(model[i].x)))
            self.FormModelTableAtoms.setItem(i, 2, qWidget.QTableWidgetItem(str(model[i].y))) 
            self.FormModelTableAtoms.setItem(i, 3, qWidget.QTableWidgetItem(str(model[i].z)))
 
        # делаем ресайз колонок по содержимому
        self.FormModelTableAtoms.resizeColumnsToContents()
  
  
    def fill_properties_table(self):
        properties = []
                
        model = self.MainForm.MainModel.atoms          
        properties.append(["Natoms",str(len(model))])      
        self.FormModelTableProperties.setRowCount(len(properties))        # и одну строку в таблице 
        
        for i in range(0, len(properties)):
            self.FormModelTableProperties.setItem(i, 0, qWidget.QTableWidgetItem(properties[i][0]))
            self.FormModelTableProperties.setItem(i, 1, qWidget.QTableWidgetItem(properties[i][1]))

        self.FormModelTableAtoms.resizeColumnsToContents()  
        
    def check_dos(self, fname):
        DOSfile = Importer.CheckDOSfile(fname)
        if DOSfile != False:
            self.FormActionsListDOSfile.addItems([DOSfile])            
            self.FormActionsListDOSfile.update()
            
            eFermy = Importer.EFermySIESTA(fname)            
            DOS = Importer.DOSSIESTA(DOSfile,eFermy)
            M11S11 = str(Calculator.M11S11(DOS))
            
            i = self.FormActionsTabeDOSProperty.rowCount()+1
            
            self.FormActionsTabeDOSProperty.setRowCount(i)                
            
            self.FormActionsTabeDOSProperty.setItem(i-1, 0, qWidget.QTableWidgetItem(str("?")))
            self.FormActionsTabeDOSProperty.setItem(i-1, 1, qWidget.QTableWidgetItem(str(eFermy)))
            self.FormActionsTabeDOSProperty.setItem(i-1, 2, qWidget.QTableWidgetItem(M11S11))
            
            self.FormActionsTabeDOSProperty.update()

    def check_xsf(self, fname):
        if fname.endswith(".XSF"):
            xsf_file = fname
        else:
            xsf_file = os.path.dirname(fname) + "/" + str(TSIESTA.SystemLabel(fname)) + ".XSF"
        if os.path.exists(xsf_file):
            self.FormActionsPostTreeSurface.setHeaderLabels([xsf_file])
            self.FormActionsPostEditSurface.setText(xsf_file)

    def fill_xsf(self, data):
        for dat in data:
            text = ((dat[0].title).split('_')[3]).split(':')[0]
            parent = qWidget.QTreeWidgetItem(self.FormActionsPostTreeSurface)
            parent.setText(0, "{}".format(text) + "3D")
            # parent.setFlags(parent.flags() | qt.ItemIsTristate | qt.ItemIsUserCheckable)
            for da in dat:
                ch = text + ':' + (da.title).split(':')[1]
                child = qWidget.QTreeWidgetItem(parent)
                # child.setFlags(child.flags() | qt.ItemIsUserCheckable)
                child.setText(0, "{}".format(ch))
                # child.setCheckState(0, qt.Unchecked)
        self.FormActionsPostTreeSurface.show()

    def fill_bonds(self):
        bonds = self.MainForm.MainModel.Bonds()
        self.FormActionsPosTableBonds.setRowCount(len(bonds))  # и одну строку в таблице

        BondsType = QStandardItemModel()
        BondsType.appendRow(QStandardItem("All"))
        self.FormActionsPostComboBonds.setModel(BondsType)

        mean = 0
        n = 0

        for i in range(0, len(bonds)):
            s = str(bonds[i][3])+str(bonds[i][4])+"-"+str(bonds[i][5])+str(bonds[i][6])
            self.FormActionsPosTableBonds.setItem(i, 0, qWidget.QTableWidgetItem(s))
            self.FormActionsPosTableBonds.setItem(i, 1, qWidget.QTableWidgetItem(str(bonds[i][2])))
            mean+=bonds[i][2]
            n+=1
        if n>0:
            self.FormActionsPostLabelMeanBond.setText("Mean value: "+str(mean/n))


    def fill_cell_info(self, fname):
        Volume = Importer.Volume(fname)
        Energy = Importer.Energy(fname)
        self.MainForm.MainModel.LatVect1
        a = self.MainForm.MainModel.get_LatVect1_norm()
        b = self.MainForm.MainModel.get_LatVect2_norm()
        c = self.MainForm.MainModel.get_LatVect3_norm()
        self.fill_cell_info_row(Energy, Volume, a, b, c)
        self.FormActionsPreZSizeFillSpace.setText(str(c))

    def fill_cell_info_row(self, Energy, Volume, a, b, c):
        i = self.FormActionsPostTableCellParam.rowCount() + 1
        self.FormActionsPostTableCellParam.setRowCount(i)  # и одну строку в таблице
        self.FormActionsPostTableCellParam.setItem(i - 1, 0, qWidget.QTableWidgetItem(str(Volume)))
        self.FormActionsPostTableCellParam.setItem(i - 1, 1, qWidget.QTableWidgetItem(str(Energy)))
        self.FormActionsPostTableCellParam.setItem(i - 1, 2, qWidget.QTableWidgetItem(str(a)))
        self.FormActionsPostTableCellParam.setItem(i - 1, 3, qWidget.QTableWidgetItem(str(b)))
        self.FormActionsPostTableCellParam.setItem(i - 1, 4, qWidget.QTableWidgetItem(str(c)))


    def delete_cell_param_row(self):
        row = self.FormActionsPostTableCellParam.currentRow()
        self.FormActionsPostTableCellParam.removeRow(row)

    def delete_isosurface_color_from_table(self):
        row = self.IsosurfaceColorsTable.currentRow()
        self.IsosurfaceColorsTable.removeRow(row)


        
    def fill_gui(self, title = "" ):
        fname = self.filename
        if title == "":
            self.fill_file_name(fname)
        else:
            self.fill_file_name(title)
        self.fill_models_list()
        self.fill_atoms_table()
        self.fill_properties_table()
        self.check_xsf(fname)
        if Importer.checkFormat(fname) == "SIESTAout":
            self.check_dos(fname)
            self.fill_cell_info(fname)

        if Importer.checkFormat(fname) == "SIESTAfdf":
            c = self.MainForm.MainModel.get_LatVect3_norm()
            self.FormActionsPreZSizeFillSpace.setText(str(c))


    def plot_bonds_histogram(self):
        bonds = self.MainForm.MainModel.Bonds()
        self.MplWidget.canvas.axes.clear()
        b = []
        for bond in bonds:
            b.append(bond[2])

        num_bins = 5
        n, bins, patches = self.MplWidget.canvas.axes.hist(b, num_bins, facecolor='blue', alpha=0.5)
        self.MplWidget.canvas.axes.set_xlabel("Bond lenght")
        self.MplWidget.canvas.axes.set_ylabel("Number of bonds")
        self.MplWidget.canvas.draw()
        
           
    def plot_dos(self):
        items = []
        for index in range(self.FormActionsListDOSfile.count()):
            eF = float(self.FormActionsTabeDOSProperty.item(index,1).text())
            items.append([self.FormActionsListDOSfile.item(index).text(),eF])
        
        self.MplWidget.canvas.axes.clear()
        
        for file in items:
            if os.path.exists(file[0]):
                DOS = Importer.DOSSIESTA(file[0],file[1])
            
                xs = []
                ys = []
                ys2= []
                sign = 1
                if self.FormActionsCheckDOS_2.isChecked():
                    sign = -1
                for row in DOS:
                    xs.append(row[0])
                    ys.append(row[1])
                    ys2.append(sign*float(row[2]))

                self.MplWidget.canvas.axes.plot(xs, ys)
                if self.FormActionsCheckDOS.isChecked():
                        self.MplWidget.canvas.axes.plot(xs, ys2)
                
        self.MplWidget.canvas.axes.set_xlabel("Energy, eV")
        self.MplWidget.canvas.axes.set_ylabel("DOS, states/eV")

        self.MplWidget.canvas.draw()

    def clear_dos(self):
        self.FormActionsListDOSfile.clear()  #      addItems([DOSfile])
        self.FormActionsListDOSfile.update()

        self.FormActionsTabeDOSProperty.setRowCount(0)
        self.FormActionsTabeDOSProperty.update()


    def plot_volume_param_energy(self):
        items = []
        method = self.FormActionsPostComboCellParam.currentText()
        xi = self.FormActionsPostComboCellParamX.currentIndex()
        yi = 1


        for index in range(self.FormActionsPostTableCellParam.rowCount()):
            x = self.FormActionsPostTableCellParam.item(index, xi).text()
            y = self.FormActionsPostTableCellParam.item(index, yi).text()
            items.append([float(x),float(y)])

        if len(items):

            items = sorted(items, key=itemgetter(0))
        
            self.MplWidget.canvas.axes.clear()

            xs = []
            ys = []
        
            for i in range(0, len(items)):           
                xs.append(items[i][0])
                ys.append(items[i][1])

            #self.MplWidget.canvas.axes.plot(xs, ys)
            self.MplWidget.canvas.axes.scatter(xs, ys, color='orange', s=40, marker='o')

            if method == "Parabola":
                aprox, xs2, ys2 = Calculator.ApproxParabola(items)
                image_path = '.\images\parabola.png' #path to your image file
                self.FormActionsPostLabelCellParamOptimExpr.setText("E(x0)="+str(round(float(aprox[0]),2)))
                self.FormActionsPostLabelCellParamOptimExpr2.setText("a="+str(round(float(aprox[1]),2)))
                self.FormActionsPostLabelCellParamOptimExpr3.setText("b="+str(round(float(aprox[2]),2)))

            if method == "Murnaghan":
                aprox, xs2, ys2 = Calculator.ApproxMurnaghan(items)
                image_path = '.\images\murnaghan.png' #path to your image file
                self.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)="+str(round(float(aprox[0]),2)))
                self.FormActionsPostLabelCellParamOptimExpr2.setText("B0="+str(round(float(aprox[1]),2)))
                self.FormActionsPostLabelCellParamOptimExpr3.setText("B0'="+str(round(float(aprox[2]),2)))
                self.FormActionsPostLabelCellParamOptimExpr4.setText("V0="+str(round(float(aprox[3]),2)))

            if method == "BirchMurnaghan":
                aprox, xs2, ys2 = Calculator.ApproxBirchMurnaghan(items)
                image_path = '.\images\murnaghanbirch.png'  # path to your image file
                self.FormActionsPostLabelCellParamOptimExpr.setText("E(V0)="+str(round(float(aprox[0]),2)))
                self.FormActionsPostLabelCellParamOptimExpr2.setText("B0="+str(round(float(aprox[1]),2)))
                self.FormActionsPostLabelCellParamOptimExpr3.setText("B0'="+str(round(float(aprox[2]),2)))
                self.FormActionsPostLabelCellParamOptimExpr4.setText("V0="+str(round(float(aprox[3]),2)))

            self.MplWidget.canvas.axes.plot(xs2, ys2)
                
            self.MplWidget.canvas.axes.set_xlabel("Volume, A^3")
            self.MplWidget.canvas.axes.set_ylabel("Energy, eV")

            self.MplWidget.canvas.draw()

            image_profile = QImage(image_path)
            print(image_profile)
            image_profile = image_profile.scaled(320,320, aspectRatioMode=QKeepAspectRatio, transformMode=Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration
            self.FormActionsPostLabelCellParamFig.setPixmap(QPixmap.fromImage(image_profile)) 
            
            
    def add_dos_file(self):
        """ menu Open"""
        fname = qWidget.QFileDialog.getOpenFileName(self, 'Open file', self.WorkDir)[0]
        self.WorkDir = os.path.dirname(fname)
        self.check_dos(fname)
            
    def save_data_from_figure2d(self):
        DATA = []
        lines = self.MplWidget.canvas.axes.lines

        for line in lines:
            DATA.append(line.get_xydata())

        if len(DATA)>0:
            name = qWidget.QFileDialog.getSaveFileName(self, 'Save File')[0]

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
        newWindow = Image3Dexporter(5*self.openGLWidget.width(), 5*self.openGLWidget.height())

        ViewBox = self.FormSettingsViewCheckShowBox.isChecked()
        ViewBonds = self.FormSettingsViewCheckShowBonds.isChecked()
        bondscolor = self.get_color_from_SETTING(self.state_Color_Of_Bonds)
        boxcolor = self.get_color_from_SETTING(self.state_Color_Of_Box)
        atomscolor = self.colors_of_atoms()

        newWindow.MainForm.copy_state(self.MainForm)
        newWindow.MainForm.save_to_file("image1.png") #  openGLWidget.grab().save("image1.png")

        self.MainForm.save_to_file("image.png")    #openGLWidget.grab().save("image.png")

    def plot_voronoi(self):
        if self.MainForm.isActive():
            r = self.state_Color_Of_Voronoi.split()[0]
            g = self.state_Color_Of_Voronoi.split()[1]
            b = self.state_Color_Of_Voronoi.split()[2]
            color = [float(r)/255, float(g)/255, float(b)/255]
            maxDist = float(self.FormActionsPostTextVoronoiMaxDist.value())
            atom_index, volume = self.MainForm.add_voronoi(color, maxDist)
            if atom_index >=0:
                self.FormActionsPostLabelVoronoiAtom.setText("Atom: " + str(atom_index))
                self.FormActionsPostLabelVoronoiVolume.setText("Volume: "+str(volume))
            else:
                self.FormActionsPostLabelVoronoiAtom.setText("Atom: ")
                self.FormActionsPostLabelVoronoiVolume.setText("Volume: ")


    def file_brouser_selection(self, selected, deselected):
        self.IndexOfFileToOpen = selected.indexes()[0]
        text = str(self.FileBrouserTree.model().filePath(self.IndexOfFileToOpen))

        #self.FileBrouserOpenLine.text
        self.FileBrouserOpenLine.setText(text)
        self.FileBrouserOpenLine.update()

    def save_active_Folder(self):
        settings = QSettings()
        settings.setValue(SETTINGS_Folder, self.WorkDir)
        settings.sync()

    def save_state_FormSettingsOpeningCheckOnlyOptimal(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsOpeningCheckOnlyOptimal, self.FormSettingsOpeningCheckOnlyOptimal.isChecked())
        settings.sync()

    def save_state_FormSettingsViewCheckAtomSelection(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsViewCheckAtomSelection, self.FormSettingsViewCheckAtomSelection.isChecked())
        settings.sync()

    def save_state_FormSettingsViewCheckShowBox(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsViewCheckShowBox, self.FormSettingsViewCheckShowBox.isChecked())
        settings.sync()
        self.MainForm.set_box_visible(self.FormSettingsViewCheckShowBox.isChecked())
        #window.openGLWidget.update()

    def save_state_FormSettingsViewCheckShowBonds(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsViewCheckShowBonds, self.FormSettingsViewCheckShowBonds.isChecked())
        settings.sync()
        self.MainForm.set_bonds_visible(self.FormSettingsViewCheckShowBonds.isChecked())
        #window.openGLWidget.update()


    def save_state_FormSettingsColorsFixed(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsColorsFixed, self.FormSettingsColorsFixed.isChecked())
        settings.sync()

    def save_state_FormSettingsColorsFixedMin(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsColorsFixedMin, self.FormSettingsColorsFixedMin.text())
        settings.sync()

    def save_state_FormSettingsColorsFixedMax(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsColorsFixedMax, self.FormSettingsColorsFixedMax.text())
        settings.sync()


    def save_state_FormSettingsColorsScale(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsColorsScale, self.FormSettingsColorsScale.currentText())
        settings.sync()
        self.colors_cash = {}

    def save_state_FormSettingsColorsScaleType(self):
        settings = QSettings()
        settings.setValue(SETTINGS_FormSettingsColorsScaleType, self.FormSettingsColorsScaleType.currentText())
        settings.sync()
        self.colors_cash = {}

    def state_changed_FormSettingsColorsScale(self):
        if self.FormSettingsColorsScale.currentText() =="":
            self.ColorRow.canvas.axes.clear()
        else:
            gradient = np.linspace(0, 1, 256)
            gradient = np.vstack((gradient, gradient))
            self.ColorRow.canvas.axes.imshow(gradient, aspect='auto',
                                         cmap=plt.get_cmap(self.FormSettingsColorsScale.currentText()))
            self.ColorRow.canvas.axes.set_axis_off()
            self.ColorRow.canvas.draw()

    def type_of_surface(self):
        self.FormActionsPostLabelSurfaceMin.setText("")
        self.FormActionsPostLabelSurfaceMax.setText("")
        self.FormActionsPostLabelSurfaceValue.setValue(0)
        self.FormActionsPostButSurface.setEnabled(False)
        self.FormActionsPostButContour.setEnabled(False)

    def fdf_data_to_form(self):
        text = self.FDFData.get_all_data(self.MainForm.MainModel.atoms)
        self.FormActionsPreTextFDF.setText(text)

    def fdf_data_from_form_to_file(self):
        text = self.FormActionsPreTextFDF.toPlainText()

        name = qWidget.QFileDialog.getSaveFileName(self, 'Save File')[0]
        with open(name, 'w') as f:
            f.write(text)

    def fill_space(self):
        Mendeley = TPeriodTable()
        nAtoms = int(self.FormActionsPreNAtomsFillSpace.text())
        charge = int(self.FormActionsPreAtomChargeFillSpace.text())
        radAtom = Mendeley.get_rad(charge)
        #print(radAtom)
        let = Mendeley.get_let(charge)
        delta = float(self.FormActionsPreDeltaFillSpace.text())
        nPrompts = int(self.FormActionsPreNPromptsFillSpace.text())
        radTube = float(self.FormActionsPreRadiusFillSpace.text())
        length = float(self.FormActionsPreZSizeFillSpace.text())
        models = Calculator.FillTube(radTube, length, nAtoms, 0.01*radAtom, delta, nPrompts, let, charge)
        #print(len(models))

        filename = "."
        if self.FormActionsPreSaveToFileFillSpace.isChecked():
            filename = qWidget.QFileDialog.getSaveFileName(self, 'Save File')[0]
            filename = filename.split(".fdf")[0]

        iter = 0
        for model in models:
            secondModel = deepcopy(self.MainForm.MainModel)
            for at in model:
                secondModel.AddAtom(at)
            self.models.append(secondModel)
            if self.FormActionsPreSaveToFileFillSpace.isChecked():
                text = self.FDFData.get_all_data(secondModel.atoms)
                with open(filename + str(iter) + '.fdf', 'w') as f:
                    f.write(text)
            iter += 1
        self.fill_models_list()

    def parse_xsf(self):
        xsf_file = self.FormActionsPostEditSurface.text()
        if self.XSFfile.parse(xsf_file):
            data = self.XSFfile.blocks
            self.fill_xsf(data)
            self.FormActionsPostButSurfaceLoadData.setEnabled(True)

    def set_xsf_z_position(self):
        value = int(self.FormActionsPostSliderContourXY.value())
        self.FormActionsPostLabelContourXYposition.setText("Slice "+str(value)+" among "+str(self.FormActionsPostSliderContourXY.maximum()))

    def set_xsf_y_position(self):
        value = int(self.FormActionsPostSliderContourXZ.value())
        self.FormActionsPostLabelContourXZposition.setText("Slice "+str(value)+" among "+str(self.FormActionsPostSliderContourXZ.maximum()))

    def set_xsf_x_position(self):
        value = int(self.FormActionsPostSliderContourYZ.value())
        self.FormActionsPostLabelContourYZposition.setText("Slice "+str(value)+" among "+str(self.FormActionsPostSliderContourYZ.maximum()))

    def swnt_create(self):
        n = int(self.FormActionsPreLineSWNTn.text())
        m = int(self.FormActionsPreLineSWNTm.text())
        if self.FormActionsPreRadioSWNTuselen.isChecked():
            leng = float(self.FormActionsPreLineSWNTlen.text())
            cells = 1
        else:
            leng = 0
            cells = float(self.FormActionsPreLineSWNTcells.text())

        model = TSWNT(n,m,leng,cells)

        self.models.append(model)
        self.plot_model(-1)
        self.MainForm.add_atoms()
        self.fill_gui("SWNT-model")

    def select_bond_color(self):
        color = QColorDialog.getColor()
        self.ColorBond.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        bondscolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]

        settings = QSettings()
        settings.setValue(SETTINGS_Color_Of_Bonds, str(color.getRgb()[0])+" "+str(color.getRgb()[1])+" "+str(color.getRgb()[2]))
        settings.sync()
        self.MainForm.set_color_of_bonds(bondscolor)

    def select_atom_color(self):
        color = QColorDialog.getColor()
        atomcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]
        i = self.ColorsOfAtomsTable.selectedIndexes()[0].row()
        self.ColorsOfAtomsTable.item(i, 0).setBackground(QColor.fromRgbF(atomcolor[0], atomcolor[1], atomcolor[2], 1))

        text_color = ""
        atomscolor = []
        col = self.ColorsOfAtomsTable.item(0, 0).background().color().getRgbF()
        atomscolor.append(col)
        text_color += str(col[0]) + " " + str(col[1]) + " " + str(col[2]) + "|"
        for i in range(0, self.ColorsOfAtomsTable.rowCount() ):
            col = self.ColorsOfAtomsTable.item(i, 0).background().color().getRgbF()
            atomscolor.append(col)
            text_color+=str(col[0])+" "+str(col[1])+" "+str(col[2])+"|"

        settings = QSettings()
        settings.setValue(SETTINGS_Color_Of_Atoms, text_color)
        settings.sync()
        #print("!")
        self.MainForm.set_color_of_atoms(atomscolor)

    def select_box_color(self):
        color = QColorDialog.getColor()
        self.ColorBox.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        boxcolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]

        settings = QSettings()
        settings.setValue(SETTINGS_Color_Of_Box, str(color.getRgb()[0])+" "+str(color.getRgb()[1])+" "+str(color.getRgb()[2]))
        settings.sync()
        self.MainForm.set_color_of_box(boxcolor)

    def select_voronoi_color(self):
        color = QColorDialog.getColor()
        self.ColorVoronoi.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        voronoicolor = [color.getRgbF()[0], color.getRgbF()[1], color.getRgbF()[2]]

        settings = QSettings()
        settings.setValue(SETTINGS_Color_Of_Voronoi, str(color.getRgb()[0])+" "+str(color.getRgb()[1])+" "+str(color.getRgb()[2]))
        settings.sync()
        self.MainForm.set_color_of_voronoi(voronoicolor)

    def add_isosurface_color_to_table(self):
        cmap = plt.get_cmap(self.FormSettingsColorsScale.currentText())
        color_scale = self.FormSettingsColorsScaleType.currentText()
        i = self.IsosurfaceColorsTable.rowCount() + 1
        value = self.FormActionsPostLabelSurfaceValue.text()
        self.IsosurfaceColorsTable.setRowCount(i)  # и одну строку в таблице
        color_cell = qWidget.QTableWidgetItem(value)
        color_cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        self.IsosurfaceColorsTable.setItem(i - 1, 0, color_cell)
        transp_cell = qWidget.QDoubleSpinBox()
        transp_cell.setRange(0,1)
        transp_cell.setValue(1)
        transp_cell.setSingleStep(0.1)
        transp_cell.setDecimals(2)
        #transp_cell.show()
        self.IsosurfaceColorsTable.setCellWidget(i - 1, 1, transp_cell)
        minv, maxv = self.xsf_data_range()
        color = self.get_color(cmap, minv, maxv, float(value), color_scale)
        #print(color)
        self.IsosurfaceColorsTable.item(i - 1, 0).setBackground(QColor.fromRgbF(color[0], color[1], color[2], color[3]))

        self.FormActionsPostButSurface.setEnabled(True)
        self.FormActionsPostButSurfaceDelete.setEnabled(True)


ORGANIZATION_NAME = 'Sozykin'
ORGANIZATION_DOMAIN = 'example.com'
APPLICATION_NAME = 'p4siesta'
SETTINGS_Folder = '\home'
SETTINGS_FormSettingsColorsScale = 'rainbow'
SETTINGS_FormSettingsColorsFixed = 'False'
SETTINGS_FormSettingsColorsFixedMin = '1e-8'
SETTINGS_FormSettingsColorsFixedMax = '0.15'
SETTINGS_FormSettingsColorsScaleType = 'Log'
SETTINGS_FormSettingsOpeningCheckOnlyOptimal = 'False'
SETTINGS_FormSettingsViewCheckAtomSelection = 'False'
SETTINGS_FormSettingsViewCheckShowBox = 'False'
SETTINGS_FormSettingsViewCheckShowBonds = 'True'

SETTINGS_Color_Of_Atoms = "|1.0 0.6666666666666666 0.0|0.5000076295109483 0.0 1.0|1.0 1.0 0.14999618524452582|0.30000762951094834 1.0 1.0|0.6 0.30000762951094834 0.0|0.2 0.2 0.8|0.4500038147554742 0.30000762951094834 0.6|1.0 0.0 0.500007629\
5109483|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0\
.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.\
0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6\
 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6\
0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0\
.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|0.6 0.6 1.0|"
SETTINGS_Color_Of_Bonds = '25 36 157'
SETTINGS_Color_Of_Box = '0 0 0'
SETTINGS_Color_Of_Voronoi = '255 0 0'

# Для того, чтобы каждый раз при вызове QSettings не вводить данные вашего приложения
# по которым будут находиться настройки, можно
# установить их глобально для всего приложения
QCoreApplication.setApplicationName(ORGANIZATION_NAME)
QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
QCoreApplication.setApplicationName(APPLICATION_NAME)

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = qWidget.QApplication(sys.argv)
window = mainWindow()
window.setupUI()
window.show()

sys.exit(app.exec_())