# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form-hexagons.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextBrowser, QToolBar, QToolBox,
    QVBoxLayout, QWidget)

from qtbased.guiopengl import GuiOpenGL
from core_atomistic_qt.qt_graph import PyqtGraphWidget
from core_atomistic_qt.qt_image import PyqtGraphWidgetImage

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1144, 925)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOrtho = QAction(MainWindow)
        self.actionOrtho.setObjectName(u"actionOrtho")
        self.actionPerspective = QAction(MainWindow)
        self.actionPerspective.setObjectName(u"actionPerspective")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionShowBox = QAction(MainWindow)
        self.actionShowBox.setObjectName(u"actionShowBox")
        self.actionHideBox = QAction(MainWindow)
        self.actionHideBox.setObjectName(u"actionHideBox")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionManual = QAction(MainWindow)
        self.actionManual.setObjectName(u"actionManual")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(450, 500))
        self.tabWidget.setMaximumSize(QSize(450, 16777215))
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.FormTabModel = QWidget()
        self.FormTabModel.setObjectName(u"FormTabModel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FormTabModel.sizePolicy().hasHeightForWidth())
        self.FormTabModel.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.FormTabModel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.FormModelComboModels = QComboBox(self.FormTabModel)
        self.FormModelComboModels.setObjectName(u"FormModelComboModels")

        self.verticalLayout.addWidget(self.FormModelComboModels)

        self.FormModelTableAtoms = QTableWidget(self.FormTabModel)
        self.FormModelTableAtoms.setObjectName(u"FormModelTableAtoms")

        self.verticalLayout.addWidget(self.FormModelTableAtoms)

        self.FormModelTableProperties = QTableWidget(self.FormTabModel)
        self.FormModelTableProperties.setObjectName(u"FormModelTableProperties")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.FormModelTableProperties.sizePolicy().hasHeightForWidth())
        self.FormModelTableProperties.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.FormModelTableProperties)

        self.groupBox_58 = QGroupBox(self.FormTabModel)
        self.groupBox_58.setObjectName(u"groupBox_58")
        self.groupBox_58.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_17 = QHBoxLayout(self.groupBox_58)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, -1, 0, 0)
        self.label_131 = QLabel(self.groupBox_58)
        self.label_131.setObjectName(u"label_131")

        self.horizontalLayout_17.addWidget(self.label_131)

        self.model_rotation_x = QDoubleSpinBox(self.groupBox_58)
        self.model_rotation_x.setObjectName(u"model_rotation_x")
        self.model_rotation_x.setMinimum(-360.000000000000000)
        self.model_rotation_x.setMaximum(360.990000000000009)

        self.horizontalLayout_17.addWidget(self.model_rotation_x)

        self.horizontalSpacer_129 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_129)

        self.label_134 = QLabel(self.groupBox_58)
        self.label_134.setObjectName(u"label_134")

        self.horizontalLayout_17.addWidget(self.label_134)

        self.model_rotation_y = QDoubleSpinBox(self.groupBox_58)
        self.model_rotation_y.setObjectName(u"model_rotation_y")
        self.model_rotation_y.setMinimum(-360.000000000000000)
        self.model_rotation_y.setMaximum(360.990000000000009)

        self.horizontalLayout_17.addWidget(self.model_rotation_y)

        self.horizontalSpacer_127 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_127)

        self.label_135 = QLabel(self.groupBox_58)
        self.label_135.setObjectName(u"label_135")

        self.horizontalLayout_17.addWidget(self.label_135)

        self.model_rotation_z = QDoubleSpinBox(self.groupBox_58)
        self.model_rotation_z.setObjectName(u"model_rotation_z")
        self.model_rotation_z.setMinimum(-360.000000000000000)
        self.model_rotation_z.setMaximum(360.990000000000009)

        self.horizontalLayout_17.addWidget(self.model_rotation_z)


        self.verticalLayout.addWidget(self.groupBox_58)

        self.groupBox_32 = QGroupBox(self.FormTabModel)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setMinimumSize(QSize(0, 0))
        self.verticalLayout_108 = QVBoxLayout(self.groupBox_32)
        self.verticalLayout_108.setObjectName(u"verticalLayout_108")
        self.verticalLayout_108.setContentsMargins(0, -1, 0, 3)
        self.frame_167 = QFrame(self.groupBox_32)
        self.frame_167.setObjectName(u"frame_167")
        self.frame_167.setFrameShape(QFrame.NoFrame)
        self.frame_167.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_182 = QHBoxLayout(self.frame_167)
        self.horizontalLayout_182.setObjectName(u"horizontalLayout_182")
        self.horizontalLayout_182.setContentsMargins(0, 0, 0, 0)
        self.label_137 = QLabel(self.frame_167)
        self.label_137.setObjectName(u"label_137")

        self.horizontalLayout_182.addWidget(self.label_137)

        self.camera_pos_x = QDoubleSpinBox(self.frame_167)
        self.camera_pos_x.setObjectName(u"camera_pos_x")
        self.camera_pos_x.setMinimum(-99.000000000000000)

        self.horizontalLayout_182.addWidget(self.camera_pos_x)

        self.horizontalSpacer_130 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_182.addItem(self.horizontalSpacer_130)

        self.label_138 = QLabel(self.frame_167)
        self.label_138.setObjectName(u"label_138")

        self.horizontalLayout_182.addWidget(self.label_138)

        self.camera_pos_y = QDoubleSpinBox(self.frame_167)
        self.camera_pos_y.setObjectName(u"camera_pos_y")
        self.camera_pos_y.setMinimum(-99.000000000000000)

        self.horizontalLayout_182.addWidget(self.camera_pos_y)

        self.horizontalSpacer_156 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_182.addItem(self.horizontalSpacer_156)

        self.label_139 = QLabel(self.frame_167)
        self.label_139.setObjectName(u"label_139")

        self.horizontalLayout_182.addWidget(self.label_139)

        self.camera_pos_z = QDoubleSpinBox(self.frame_167)
        self.camera_pos_z.setObjectName(u"camera_pos_z")
        self.camera_pos_z.setMinimum(-99.000000000000000)

        self.horizontalLayout_182.addWidget(self.camera_pos_z)


        self.verticalLayout_108.addWidget(self.frame_167)


        self.verticalLayout.addWidget(self.groupBox_32)

        self.frame_168 = QFrame(self.FormTabModel)
        self.frame_168.setObjectName(u"frame_168")
        self.frame_168.setFrameShape(QFrame.NoFrame)
        self.frame_168.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_183 = QHBoxLayout(self.frame_168)
        self.horizontalLayout_183.setObjectName(u"horizontalLayout_183")
        self.horizontalLayout_183.setContentsMargins(0, 0, 0, 0)
        self.label_136 = QLabel(self.frame_168)
        self.label_136.setObjectName(u"label_136")

        self.horizontalLayout_183.addWidget(self.label_136)

        self.model_scale = QDoubleSpinBox(self.frame_168)
        self.model_scale.setObjectName(u"model_scale")

        self.horizontalLayout_183.addWidget(self.model_scale)

        self.horizontalSpacer_126 = QSpacerItem(289, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_183.addItem(self.horizontalSpacer_126)


        self.verticalLayout.addWidget(self.frame_168)

        self.tabWidget.addTab(self.FormTabModel, "")
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.verticalLayout_89 = QVBoxLayout(self.tab_20)
        self.verticalLayout_89.setObjectName(u"verticalLayout_89")
        self.AtomPropertiesText = QTextBrowser(self.tab_20)
        self.AtomPropertiesText.setObjectName(u"AtomPropertiesText")

        self.verticalLayout_89.addWidget(self.AtomPropertiesText)

        self.groupBox_20 = QGroupBox(self.tab_20)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setMinimumSize(QSize(0, 60))
        self.horizontalLayout_66 = QHBoxLayout(self.groupBox_20)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.PropertyAtomAtomDistanceAt1 = QSpinBox(self.groupBox_20)
        self.PropertyAtomAtomDistanceAt1.setObjectName(u"PropertyAtomAtomDistanceAt1")
        self.PropertyAtomAtomDistanceAt1.setMinimumSize(QSize(50, 0))
        self.PropertyAtomAtomDistanceAt1.setMinimum(1)
        self.PropertyAtomAtomDistanceAt1.setMaximum(100)

        self.horizontalLayout_66.addWidget(self.PropertyAtomAtomDistanceAt1)

        self.label_56 = QLabel(self.groupBox_20)
        self.label_56.setObjectName(u"label_56")

        self.horizontalLayout_66.addWidget(self.label_56)

        self.PropertyAtomAtomDistanceAt2 = QSpinBox(self.groupBox_20)
        self.PropertyAtomAtomDistanceAt2.setObjectName(u"PropertyAtomAtomDistanceAt2")
        self.PropertyAtomAtomDistanceAt2.setMinimumSize(QSize(50, 0))
        self.PropertyAtomAtomDistanceAt2.setMinimum(1)
        self.PropertyAtomAtomDistanceAt2.setValue(2)

        self.horizontalLayout_66.addWidget(self.PropertyAtomAtomDistanceAt2)

        self.label_62 = QLabel(self.groupBox_20)
        self.label_62.setObjectName(u"label_62")

        self.horizontalLayout_66.addWidget(self.label_62)

        self.PropertyAtomAtomDistance = QLineEdit(self.groupBox_20)
        self.PropertyAtomAtomDistance.setObjectName(u"PropertyAtomAtomDistance")

        self.horizontalLayout_66.addWidget(self.PropertyAtomAtomDistance)

        self.PropertyAtomAtomDistanceGet = QPushButton(self.groupBox_20)
        self.PropertyAtomAtomDistanceGet.setObjectName(u"PropertyAtomAtomDistanceGet")
        self.PropertyAtomAtomDistanceGet.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_66.addWidget(self.PropertyAtomAtomDistanceGet)


        self.verticalLayout_89.addWidget(self.groupBox_20)

        self.tabWidget.addTab(self.tab_20, "")
        self.FormTabActions = QWidget()
        self.FormTabActions.setObjectName(u"FormTabActions")
        self.verticalLayout_2 = QVBoxLayout(self.FormTabActions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_24 = QGroupBox(self.FormTabActions)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMinimumSize(QSize(0, 0))
        self.verticalLayout_74 = QVBoxLayout(self.groupBox_24)
        self.verticalLayout_74.setObjectName(u"verticalLayout_74")
        self.label = QLabel(self.groupBox_24)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)

        self.verticalLayout_74.addWidget(self.label)

        self.FormActionsPreComboFillSpace = QComboBox(self.groupBox_24)
        self.FormActionsPreComboFillSpace.setObjectName(u"FormActionsPreComboFillSpace")

        self.verticalLayout_74.addWidget(self.FormActionsPreComboFillSpace)

        self.frame_83 = QFrame(self.groupBox_24)
        self.frame_83.setObjectName(u"frame_83")
        self.frame_83.setFrameShape(QFrame.NoFrame)
        self.frame_83.setFrameShadow(QFrame.Raised)
        self.frame_83.setLineWidth(0)
        self.horizontalLayout_96 = QHBoxLayout(self.frame_83)
        self.horizontalLayout_96.setObjectName(u"horizontalLayout_96")
        self.horizontalLayout_96.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_83)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_96.addWidget(self.label_3)

        self.FormActionsPreNAtomsFillSpace = QSpinBox(self.frame_83)
        self.FormActionsPreNAtomsFillSpace.setObjectName(u"FormActionsPreNAtomsFillSpace")
        self.FormActionsPreNAtomsFillSpace.setMaximum(200)
        self.FormActionsPreNAtomsFillSpace.setValue(5)

        self.horizontalLayout_96.addWidget(self.FormActionsPreNAtomsFillSpace)

        self.label_6 = QLabel(self.frame_83)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_96.addWidget(self.label_6)

        self.FormActionsPreAtomChargeFillSpace = QSpinBox(self.frame_83)
        self.FormActionsPreAtomChargeFillSpace.setObjectName(u"FormActionsPreAtomChargeFillSpace")
        self.FormActionsPreAtomChargeFillSpace.setValue(3)

        self.horizontalLayout_96.addWidget(self.FormActionsPreAtomChargeFillSpace)


        self.verticalLayout_74.addWidget(self.frame_83)

        self.frame_95 = QFrame(self.groupBox_24)
        self.frame_95.setObjectName(u"frame_95")
        self.frame_95.setFrameShape(QFrame.NoFrame)
        self.frame_95.setFrameShadow(QFrame.Raised)
        self.frame_95.setLineWidth(0)
        self.horizontalLayout_97 = QHBoxLayout(self.frame_95)
        self.horizontalLayout_97.setObjectName(u"horizontalLayout_97")
        self.horizontalLayout_97.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_95)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_97.addWidget(self.label_5)

        self.FormActionsPreDeltaFillSpace = QDoubleSpinBox(self.frame_95)
        self.FormActionsPreDeltaFillSpace.setObjectName(u"FormActionsPreDeltaFillSpace")
        self.FormActionsPreDeltaFillSpace.setMaximum(20.000000000000000)
        self.FormActionsPreDeltaFillSpace.setSingleStep(0.100000000000000)
        self.FormActionsPreDeltaFillSpace.setValue(2.500000000000000)

        self.horizontalLayout_97.addWidget(self.FormActionsPreDeltaFillSpace)

        self.label_4 = QLabel(self.frame_95)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_97.addWidget(self.label_4)

        self.FormActionsPreNPromptsFillSpace = QSpinBox(self.frame_95)
        self.FormActionsPreNPromptsFillSpace.setObjectName(u"FormActionsPreNPromptsFillSpace")
        self.FormActionsPreNPromptsFillSpace.setMaximum(1000)
        self.FormActionsPreNPromptsFillSpace.setValue(200)

        self.horizontalLayout_97.addWidget(self.FormActionsPreNPromptsFillSpace)


        self.verticalLayout_74.addWidget(self.frame_95)

        self.frame_96 = QFrame(self.groupBox_24)
        self.frame_96.setObjectName(u"frame_96")
        self.frame_96.setFrameShape(QFrame.NoFrame)
        self.frame_96.setFrameShadow(QFrame.Raised)
        self.frame_96.setLineWidth(0)
        self.horizontalLayout_98 = QHBoxLayout(self.frame_96)
        self.horizontalLayout_98.setObjectName(u"horizontalLayout_98")
        self.horizontalLayout_98.setContentsMargins(0, 0, 0, 0)
        self.cylinder = QLabel(self.frame_96)
        self.cylinder.setObjectName(u"cylinder")

        self.horizontalLayout_98.addWidget(self.cylinder)

        self.FormActionsPreRadiusFillSpace = QDoubleSpinBox(self.frame_96)
        self.FormActionsPreRadiusFillSpace.setObjectName(u"FormActionsPreRadiusFillSpace")
        self.FormActionsPreRadiusFillSpace.setSingleStep(0.100000000000000)
        self.FormActionsPreRadiusFillSpace.setValue(4.200000000000000)

        self.horizontalLayout_98.addWidget(self.FormActionsPreRadiusFillSpace)


        self.verticalLayout_74.addWidget(self.frame_96)

        self.frame_11 = QFrame(self.groupBox_24)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 0))
        self.frame_11.setMaximumSize(QSize(16777215, 16777215))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.frame_11.setLineWidth(0)
        self.horizontalLayout_99 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_99.setObjectName(u"horizontalLayout_99")
        self.horizontalLayout_99.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.frame_11)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_99.addWidget(self.label_7)

        self.FormActionsPreZSizeFillSpace = QDoubleSpinBox(self.frame_11)
        self.FormActionsPreZSizeFillSpace.setObjectName(u"FormActionsPreZSizeFillSpace")
        self.FormActionsPreZSizeFillSpace.setMaximum(1000.000000000000000)
        self.FormActionsPreZSizeFillSpace.setSingleStep(0.100000000000000)
        self.FormActionsPreZSizeFillSpace.setValue(10.100000000000000)

        self.horizontalLayout_99.addWidget(self.FormActionsPreZSizeFillSpace)


        self.verticalLayout_74.addWidget(self.frame_11)

        self.frame_82 = QFrame(self.groupBox_24)
        self.frame_82.setObjectName(u"frame_82")
        self.frame_82.setFrameShape(QFrame.NoFrame)
        self.frame_82.setFrameShadow(QFrame.Raised)
        self.frame_82.setLineWidth(0)
        self.horizontalLayout_95 = QHBoxLayout(self.frame_82)
        self.horizontalLayout_95.setObjectName(u"horizontalLayout_95")
        self.horizontalLayout_95.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_72 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_95.addItem(self.horizontalSpacer_72)

        self.fill_space = QPushButton(self.frame_82)
        self.fill_space.setObjectName(u"fill_space")

        self.horizontalLayout_95.addWidget(self.fill_space)

        self.horizontalSpacer_71 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_95.addItem(self.horizontalSpacer_71)


        self.verticalLayout_74.addWidget(self.frame_82)


        self.verticalLayout_2.addWidget(self.groupBox_24)

        self.groupBox_60 = QGroupBox(self.FormTabActions)
        self.groupBox_60.setObjectName(u"groupBox_60")
        self.groupBox_60.setMinimumSize(QSize(0, 0))
        self.verticalLayout_75 = QVBoxLayout(self.groupBox_60)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.frame_187 = QFrame(self.groupBox_60)
        self.frame_187.setObjectName(u"frame_187")
        self.frame_187.setFrameShape(QFrame.StyledPanel)
        self.frame_187.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_205 = QHBoxLayout(self.frame_187)
        self.horizontalLayout_205.setObjectName(u"horizontalLayout_205")
        self.label_8 = QLabel(self.frame_187)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_205.addWidget(self.label_8)

        self.number_of_atoms_to_add = QSpinBox(self.frame_187)
        self.number_of_atoms_to_add.setObjectName(u"number_of_atoms_to_add")

        self.horizontalLayout_205.addWidget(self.number_of_atoms_to_add)

        self.label_84 = QLabel(self.frame_187)
        self.label_84.setObjectName(u"label_84")

        self.horizontalLayout_205.addWidget(self.label_84)

        self.horizontalSpacer_159 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_205.addItem(self.horizontalSpacer_159)


        self.verticalLayout_75.addWidget(self.frame_187)

        self.frame_185 = QFrame(self.groupBox_60)
        self.frame_185.setObjectName(u"frame_185")
        self.frame_185.setFrameShape(QFrame.StyledPanel)
        self.frame_185.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_202 = QHBoxLayout(self.frame_185)
        self.horizontalLayout_202.setObjectName(u"horizontalLayout_202")
        self.horizontalSpacer_131 = QSpacerItem(84, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_202.addItem(self.horizontalSpacer_131)

        self.add_atoms_to_hexagons = QPushButton(self.frame_185)
        self.add_atoms_to_hexagons.setObjectName(u"add_atoms_to_hexagons")

        self.horizontalLayout_202.addWidget(self.add_atoms_to_hexagons)

        self.horizontalSpacer_132 = QSpacerItem(83, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_202.addItem(self.horizontalSpacer_132)


        self.verticalLayout_75.addWidget(self.frame_185)


        self.verticalLayout_2.addWidget(self.groupBox_60)

        self.FormActionsPreSaveToFileFillSpace = QCheckBox(self.FormTabActions)
        self.FormActionsPreSaveToFileFillSpace.setObjectName(u"FormActionsPreSaveToFileFillSpace")

        self.verticalLayout_2.addWidget(self.FormActionsPreSaveToFileFillSpace)

        self.groupBox_61 = QGroupBox(self.FormTabActions)
        self.groupBox_61.setObjectName(u"groupBox_61")
        self.groupBox_61.setMinimumSize(QSize(0, 200))
        self.horizontalLayout_204 = QHBoxLayout(self.groupBox_61)
        self.horizontalLayout_204.setObjectName(u"horizontalLayout_204")
        self.frame_186 = QFrame(self.groupBox_61)
        self.frame_186.setObjectName(u"frame_186")
        self.frame_186.setFrameShape(QFrame.StyledPanel)
        self.frame_186.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_203 = QHBoxLayout(self.frame_186)
        self.horizontalLayout_203.setObjectName(u"horizontalLayout_203")
        self.horizontalSpacer_157 = QSpacerItem(84, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_203.addItem(self.horizontalSpacer_157)

        self.hops_analis = QPushButton(self.frame_186)
        self.hops_analis.setObjectName(u"hops_analis")

        self.horizontalLayout_203.addWidget(self.hops_analis)

        self.horizontalSpacer_158 = QSpacerItem(83, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_203.addItem(self.horizontalSpacer_158)


        self.horizontalLayout_204.addWidget(self.frame_186)


        self.verticalLayout_2.addWidget(self.groupBox_61)

        self.tabWidget.addTab(self.FormTabActions, "")
        self.tab_29 = QWidget()
        self.tab_29.setObjectName(u"tab_29")
        self.verticalLayout_23 = QVBoxLayout(self.tab_29)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.tabWidget_9 = QTabWidget(self.tab_29)
        self.tabWidget_9.setObjectName(u"tabWidget_9")
        self.tab_32 = QWidget()
        self.tab_32.setObjectName(u"tab_32")
        self.verticalLayout_31 = QVBoxLayout(self.tab_32)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.FormSettingsViewCheckShowAtoms = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAtoms.setObjectName(u"FormSettingsViewCheckShowAtoms")
        self.FormSettingsViewCheckShowAtoms.setEnabled(True)

        self.verticalLayout_31.addWidget(self.FormSettingsViewCheckShowAtoms)

        self.FormSettingsViewCheckShowBox = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowBox.setObjectName(u"FormSettingsViewCheckShowBox")
        self.FormSettingsViewCheckShowBox.setStyleSheet(u"")

        self.verticalLayout_31.addWidget(self.FormSettingsViewCheckShowBox)

        self.FormSettingsViewCheckShowAtomNumber = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAtomNumber.setObjectName(u"FormSettingsViewCheckShowAtomNumber")
        self.FormSettingsViewCheckShowAtomNumber.setEnabled(True)

        self.verticalLayout_31.addWidget(self.FormSettingsViewCheckShowAtomNumber)

        self.FormSettingsViewCheckShowAxes = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAxes.setObjectName(u"FormSettingsViewCheckShowAxes")

        self.verticalLayout_31.addWidget(self.FormSettingsViewCheckShowAxes)

        self.frame_70 = QFrame(self.tab_32)
        self.frame_70.setObjectName(u"frame_70")
        self.frame_70.setMinimumSize(QSize(0, 40))
        self.frame_70.setFrameShape(QFrame.NoFrame)
        self.frame_70.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_70)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(0, 0, 0, 0)
        self.label_43 = QLabel(self.frame_70)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_62.addWidget(self.label_43)

        self.horizontalSpacer_55 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_55)

        self.FormSettingsViewSpinContourWidth = QSpinBox(self.frame_70)
        self.FormSettingsViewSpinContourWidth.setObjectName(u"FormSettingsViewSpinContourWidth")
        self.FormSettingsViewSpinContourWidth.setMinimumSize(QSize(120, 24))
        self.FormSettingsViewSpinContourWidth.setMaximumSize(QSize(120, 24))
        self.FormSettingsViewSpinContourWidth.setValue(20)

        self.horizontalLayout_62.addWidget(self.FormSettingsViewSpinContourWidth)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_31)


        self.verticalLayout_31.addWidget(self.frame_70)

        self.frame_131 = QFrame(self.tab_32)
        self.frame_131.setObjectName(u"frame_131")
        self.frame_131.setMinimumSize(QSize(0, 0))
        self.frame_131.setFrameShape(QFrame.NoFrame)
        self.frame_131.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_100 = QHBoxLayout(self.frame_131)
        self.horizontalLayout_100.setObjectName(u"horizontalLayout_100")
        self.horizontalLayout_100.setContentsMargins(0, 0, 0, 0)
        self.label_105 = QLabel(self.frame_131)
        self.label_105.setObjectName(u"label_105")

        self.horizontalLayout_100.addWidget(self.label_105)

        self.horizontalSpacer_113 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_100.addItem(self.horizontalSpacer_113)

        self.spin_perspective_angle = QSpinBox(self.frame_131)
        self.spin_perspective_angle.setObjectName(u"spin_perspective_angle")
        self.spin_perspective_angle.setMinimumSize(QSize(120, 24))
        self.spin_perspective_angle.setMaximumSize(QSize(120, 24))
        self.spin_perspective_angle.setMaximum(90)
        self.spin_perspective_angle.setValue(45)

        self.horizontalLayout_100.addWidget(self.spin_perspective_angle)

        self.horizontalSpacer_112 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_100.addItem(self.horizontalSpacer_112)


        self.verticalLayout_31.addWidget(self.frame_131)

        self.groupBox = QGroupBox(self.tab_32)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.verticalLayout_68 = QVBoxLayout(self.groupBox)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.FormSettingsViewCheckShowBonds = QCheckBox(self.groupBox)
        self.FormSettingsViewCheckShowBonds.setObjectName(u"FormSettingsViewCheckShowBonds")

        self.verticalLayout_68.addWidget(self.FormSettingsViewCheckShowBonds)

        self.frame_68 = QFrame(self.groupBox)
        self.frame_68.setObjectName(u"frame_68")
        self.frame_68.setMinimumSize(QSize(200, 0))
        self.frame_68.setFrameShape(QFrame.NoFrame)
        self.frame_68.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_68)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.horizontalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.label_22 = QLabel(self.frame_68)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_60.addWidget(self.label_22)

        self.horizontalSpacer_54 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_60.addItem(self.horizontalSpacer_54)

        self.FormSettingsViewSpinBondWidth = QSpinBox(self.frame_68)
        self.FormSettingsViewSpinBondWidth.setObjectName(u"FormSettingsViewSpinBondWidth")
        self.FormSettingsViewSpinBondWidth.setMinimumSize(QSize(120, 24))
        self.FormSettingsViewSpinBondWidth.setMaximumSize(QSize(120, 24))
        self.FormSettingsViewSpinBondWidth.setValue(20)

        self.horizontalLayout_60.addWidget(self.FormSettingsViewSpinBondWidth)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_60.addItem(self.horizontalSpacer_30)


        self.verticalLayout_68.addWidget(self.frame_68)

        self.frame_114 = QFrame(self.groupBox)
        self.frame_114.setObjectName(u"frame_114")
        self.frame_114.setMinimumSize(QSize(0, 50))
        self.frame_114.setFrameShape(QFrame.NoFrame)
        self.frame_114.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_116 = QHBoxLayout(self.frame_114)
        self.horizontalLayout_116.setObjectName(u"horizontalLayout_116")
        self.horizontalLayout_116.setContentsMargins(0, -1, -1, -1)
        self.label_83 = QLabel(self.frame_114)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_116.addWidget(self.label_83)

        self.FormSettingsViewRadioColorBondsManual = QRadioButton(self.frame_114)
        self.FormSettingsViewRadioColorBondsManual.setObjectName(u"FormSettingsViewRadioColorBondsManual")
        self.FormSettingsViewRadioColorBondsManual.setChecked(True)

        self.horizontalLayout_116.addWidget(self.FormSettingsViewRadioColorBondsManual)

        self.FormSettingsViewRadioColorBondsByAtoms = QRadioButton(self.frame_114)
        self.FormSettingsViewRadioColorBondsByAtoms.setObjectName(u"FormSettingsViewRadioColorBondsByAtoms")

        self.horizontalLayout_116.addWidget(self.FormSettingsViewRadioColorBondsByAtoms)


        self.verticalLayout_68.addWidget(self.frame_114)

        self.frame_106 = QFrame(self.groupBox)
        self.frame_106.setObjectName(u"frame_106")
        self.frame_106.setFrameShape(QFrame.NoFrame)
        self.frame_106.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_110 = QHBoxLayout(self.frame_106)
        self.horizontalLayout_110.setObjectName(u"horizontalLayout_110")
        self.horizontalLayout_110.setContentsMargins(0, -1, 0, -1)
        self.label_2 = QLabel(self.frame_106)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_110.addWidget(self.label_2)

        self.FormAtomsList1 = QComboBox(self.frame_106)
        self.FormAtomsList1.setObjectName(u"FormAtomsList1")

        self.horizontalLayout_110.addWidget(self.FormAtomsList1)

        self.label_31 = QLabel(self.frame_106)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_110.addWidget(self.label_31)

        self.FormAtomsList2 = QComboBox(self.frame_106)
        self.FormAtomsList2.setObjectName(u"FormAtomsList2")

        self.horizontalLayout_110.addWidget(self.FormAtomsList2)

        self.horizontalSpacer_76 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_110.addItem(self.horizontalSpacer_76)

        self.FormBondLenSpinBox = QDoubleSpinBox(self.frame_106)
        self.FormBondLenSpinBox.setObjectName(u"FormBondLenSpinBox")
        self.FormBondLenSpinBox.setReadOnly(False)
        self.FormBondLenSpinBox.setSingleStep(0.100000000000000)

        self.horizontalLayout_110.addWidget(self.FormBondLenSpinBox)

        self.label_30 = QLabel(self.frame_106)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_110.addWidget(self.label_30)


        self.verticalLayout_68.addWidget(self.frame_106)


        self.verticalLayout_31.addWidget(self.groupBox)

        self.groupBox_29 = QGroupBox(self.tab_32)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(0, 0))
        self.verticalLayout_107 = QVBoxLayout(self.groupBox_29)
        self.verticalLayout_107.setObjectName(u"verticalLayout_107")
        self.frame_165 = QFrame(self.groupBox_29)
        self.frame_165.setObjectName(u"frame_165")
        self.frame_165.setFrameShape(QFrame.NoFrame)
        self.frame_165.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_179 = QHBoxLayout(self.frame_165)
        self.horizontalLayout_179.setObjectName(u"horizontalLayout_179")
        self.horizontalLayout_179.setContentsMargins(-1, 0, -1, 0)
        self.label_132 = QLabel(self.frame_165)
        self.label_132.setObjectName(u"label_132")

        self.horizontalLayout_179.addWidget(self.label_132)

        self.property_shift_x = QSpinBox(self.frame_165)
        self.property_shift_x.setObjectName(u"property_shift_x")
        self.property_shift_x.setMinimum(-99)

        self.horizontalLayout_179.addWidget(self.property_shift_x)

        self.label_133 = QLabel(self.frame_165)
        self.label_133.setObjectName(u"label_133")

        self.horizontalLayout_179.addWidget(self.label_133)

        self.property_shift_y = QSpinBox(self.frame_165)
        self.property_shift_y.setObjectName(u"property_shift_y")
        self.property_shift_y.setMinimum(-99)

        self.horizontalLayout_179.addWidget(self.property_shift_y)

        self.horizontalSpacer_125 = QSpacerItem(126, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_179.addItem(self.horizontalSpacer_125)


        self.verticalLayout_107.addWidget(self.frame_165)

        self.frame_164 = QFrame(self.groupBox_29)
        self.frame_164.setObjectName(u"frame_164")
        self.frame_164.setMinimumSize(QSize(0, 0))
        self.frame_164.setFrameShape(QFrame.NoFrame)
        self.frame_164.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_180 = QHBoxLayout(self.frame_164)
        self.horizontalLayout_180.setObjectName(u"horizontalLayout_180")
        self.horizontalLayout_180.setContentsMargins(-1, 0, -1, 0)
        self.label_90 = QLabel(self.frame_164)
        self.label_90.setObjectName(u"label_90")

        self.horizontalLayout_180.addWidget(self.label_90)

        self.font_size_3d = QSpinBox(self.frame_164)
        self.font_size_3d.setObjectName(u"font_size_3d")
        self.font_size_3d.setValue(8)

        self.horizontalLayout_180.addWidget(self.font_size_3d)

        self.horizontalSpacer_83 = QSpacerItem(239, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_180.addItem(self.horizontalSpacer_83)


        self.verticalLayout_107.addWidget(self.frame_164)

        self.frame_119 = QFrame(self.groupBox_29)
        self.frame_119.setObjectName(u"frame_119")
        self.frame_119.setFrameShape(QFrame.NoFrame)
        self.frame_119.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_122 = QHBoxLayout(self.frame_119)
        self.horizontalLayout_122.setObjectName(u"horizontalLayout_122")
        self.horizontalLayout_122.setContentsMargins(-1, 0, -1, 0)
        self.label_81 = QLabel(self.frame_119)
        self.label_81.setObjectName(u"label_81")

        self.horizontalLayout_122.addWidget(self.label_81)

        self.property_precision = QSpinBox(self.frame_119)
        self.property_precision.setObjectName(u"property_precision")
        self.property_precision.setValue(5)

        self.horizontalLayout_122.addWidget(self.property_precision)

        self.horizontalSpacer_99 = QSpacerItem(182, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_122.addItem(self.horizontalSpacer_99)


        self.verticalLayout_107.addWidget(self.frame_119)


        self.verticalLayout_31.addWidget(self.groupBox_29)

        self.groupBox_34 = QGroupBox(self.tab_32)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_163 = QHBoxLayout(self.groupBox_34)
        self.horizontalLayout_163.setObjectName(u"horizontalLayout_163")
        self.OpenGL_GL_CULL_FACE = QCheckBox(self.groupBox_34)
        self.OpenGL_GL_CULL_FACE.setObjectName(u"OpenGL_GL_CULL_FACE")
        self.OpenGL_GL_CULL_FACE.setEnabled(True)

        self.horizontalLayout_163.addWidget(self.OpenGL_GL_CULL_FACE)


        self.verticalLayout_31.addWidget(self.groupBox_34)

        self.frame_36 = QFrame(self.tab_32)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.NoFrame)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_112 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_112.setObjectName(u"horizontalLayout_112")
        self.horizontalLayout_112.setContentsMargins(0, 0, 0, 0)
        self.ColorAtomsProperty = QCheckBox(self.frame_36)
        self.ColorAtomsProperty.setObjectName(u"ColorAtomsProperty")

        self.horizontalLayout_112.addWidget(self.ColorAtomsProperty)

        self.PropertyForColorOfAtom = QComboBox(self.frame_36)
        self.PropertyForColorOfAtom.setObjectName(u"PropertyForColorOfAtom")

        self.horizontalLayout_112.addWidget(self.PropertyForColorOfAtom)

        self.show_property_text = QCheckBox(self.frame_36)
        self.show_property_text.setObjectName(u"show_property_text")

        self.horizontalLayout_112.addWidget(self.show_property_text)


        self.verticalLayout_31.addWidget(self.frame_36)

        self.verticalSpacer_9 = QSpacerItem(20, 374, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_9)

        self.tabWidget_9.addTab(self.tab_32, "")
        self.tab_33 = QWidget()
        self.tab_33.setObjectName(u"tab_33")
        self.verticalLayout_58 = QVBoxLayout(self.tab_33)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.groupBox_9 = QGroupBox(self.tab_33)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setEnabled(True)
        self.groupBox_9.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_125 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_125.setObjectName(u"horizontalLayout_125")
        self.label_32 = QLabel(self.groupBox_9)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_125.addWidget(self.label_32)

        self.Form2DFontColorR = QSpinBox(self.groupBox_9)
        self.Form2DFontColorR.setObjectName(u"Form2DFontColorR")
        self.Form2DFontColorR.setMaximum(255)

        self.horizontalLayout_125.addWidget(self.Form2DFontColorR)

        self.Form2DFontColorG = QSpinBox(self.groupBox_9)
        self.Form2DFontColorG.setObjectName(u"Form2DFontColorG")
        self.Form2DFontColorG.setMaximum(255)

        self.horizontalLayout_125.addWidget(self.Form2DFontColorG)

        self.Form2DFontColorB = QSpinBox(self.groupBox_9)
        self.Form2DFontColorB.setObjectName(u"Form2DFontColorB")
        self.Form2DFontColorB.setMaximum(255)

        self.horizontalLayout_125.addWidget(self.Form2DFontColorB)


        self.verticalLayout_58.addWidget(self.groupBox_9)

        self.groupBox_10 = QGroupBox(self.tab_33)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setEnabled(True)
        self.groupBox_10.setMinimumSize(QSize(0, 0))
        self.verticalLayout_45 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.frame_38 = QFrame(self.groupBox_10)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.NoFrame)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_38)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 0, -1, 0)
        self.label_91 = QLabel(self.frame_38)
        self.label_91.setObjectName(u"label_91")

        self.horizontalLayout_20.addWidget(self.label_91)

        self.FormTitleFontSize = QSpinBox(self.frame_38)
        self.FormTitleFontSize.setObjectName(u"FormTitleFontSize")
        self.FormTitleFontSize.setMinimum(1)
        self.FormTitleFontSize.setValue(20)

        self.horizontalLayout_20.addWidget(self.FormTitleFontSize)

        self.horizontalSpacer_73 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_73)


        self.verticalLayout_45.addWidget(self.frame_38)

        self.frame_32 = QFrame(self.groupBox_10)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.label_34 = QLabel(self.frame_32)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_21.addWidget(self.label_34)

        self.FormAxesFontSize = QSpinBox(self.frame_32)
        self.FormAxesFontSize.setObjectName(u"FormAxesFontSize")
        self.FormAxesFontSize.setMinimum(1)
        self.FormAxesFontSize.setValue(20)

        self.horizontalLayout_21.addWidget(self.FormAxesFontSize)

        self.horizontalSpacer_18 = QSpacerItem(187, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_18)


        self.verticalLayout_45.addWidget(self.frame_32)

        self.frame_33 = QFrame(self.groupBox_10)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, 0)
        self.label_40 = QLabel(self.frame_33)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_25.addWidget(self.label_40)

        self.FormLabelFontSize = QSpinBox(self.frame_33)
        self.FormLabelFontSize.setObjectName(u"FormLabelFontSize")
        self.FormLabelFontSize.setMinimum(1)
        self.FormLabelFontSize.setValue(20)

        self.horizontalLayout_25.addWidget(self.FormLabelFontSize)

        self.horizontalSpacer_67 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_67)


        self.verticalLayout_45.addWidget(self.frame_33)


        self.verticalLayout_58.addWidget(self.groupBox_10)

        self.groupBox_17 = QGroupBox(self.tab_33)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setMinimumSize(QSize(0, 0))
        self.verticalLayout_76 = QVBoxLayout(self.groupBox_17)
        self.verticalLayout_76.setObjectName(u"verticalLayout_76")
        self.frame_121 = QFrame(self.groupBox_17)
        self.frame_121.setObjectName(u"frame_121")
        self.frame_121.setFrameShape(QFrame.NoFrame)
        self.frame_121.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_126 = QHBoxLayout(self.frame_121)
        self.horizontalLayout_126.setObjectName(u"horizontalLayout_126")
        self.horizontalLayout_126.setContentsMargins(-1, 0, -1, 0)
        self.label_28 = QLabel(self.frame_121)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_126.addWidget(self.label_28)

        self.Form2DLineWidth = QSpinBox(self.frame_121)
        self.Form2DLineWidth.setObjectName(u"Form2DLineWidth")
        self.Form2DLineWidth.setMinimum(2)

        self.horizontalLayout_126.addWidget(self.Form2DLineWidth)

        self.horizontalSpacer_88 = QSpacerItem(208, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_126.addItem(self.horizontalSpacer_88)


        self.verticalLayout_76.addWidget(self.frame_121)


        self.verticalLayout_58.addWidget(self.groupBox_17)

        self.frame_120 = QFrame(self.tab_33)
        self.frame_120.setObjectName(u"frame_120")
        self.frame_120.setFrameShape(QFrame.NoFrame)
        self.frame_120.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_120)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalSpacer_86 = QSpacerItem(117, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_86)

        self.FormStylesFor2DGraph = QPushButton(self.frame_120)
        self.FormStylesFor2DGraph.setObjectName(u"FormStylesFor2DGraph")

        self.horizontalLayout_34.addWidget(self.FormStylesFor2DGraph)

        self.horizontalSpacer_87 = QSpacerItem(117, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_87)


        self.verticalLayout_58.addWidget(self.frame_120)

        self.verticalSpacer_27 = QSpacerItem(20, 531, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_58.addItem(self.verticalSpacer_27)

        self.tabWidget_9.addTab(self.tab_33, "")
        self.tab_37 = QWidget()
        self.tab_37.setObjectName(u"tab_37")
        self.verticalLayout_14 = QVBoxLayout(self.tab_37)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tabWidget_12 = QTabWidget(self.tab_37)
        self.tabWidget_12.setObjectName(u"tabWidget_12")
        self.tab_40 = QWidget()
        self.tab_40.setObjectName(u"tab_40")
        self.verticalLayout_13 = QVBoxLayout(self.tab_40)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame_142 = QFrame(self.tab_40)
        self.frame_142.setObjectName(u"frame_142")
        self.frame_142.setMinimumSize(QSize(0, 50))
        self.frame_142.setFrameShape(QFrame.NoFrame)
        self.frame_142.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_154 = QHBoxLayout(self.frame_142)
        self.horizontalLayout_154.setObjectName(u"horizontalLayout_154")
        self.cpk_radio = QRadioButton(self.frame_142)
        self.cpk_radio.setObjectName(u"cpk_radio")
        self.cpk_radio.setChecked(True)

        self.horizontalLayout_154.addWidget(self.cpk_radio)

        self.jmol_radio = QRadioButton(self.frame_142)
        self.jmol_radio.setObjectName(u"jmol_radio")

        self.horizontalLayout_154.addWidget(self.jmol_radio)

        self.manual_colors_radio = QRadioButton(self.frame_142)
        self.manual_colors_radio.setObjectName(u"manual_colors_radio")

        self.horizontalLayout_154.addWidget(self.manual_colors_radio)

        self.manual_colors_default = QPushButton(self.frame_142)
        self.manual_colors_default.setObjectName(u"manual_colors_default")

        self.horizontalLayout_154.addWidget(self.manual_colors_default)


        self.verticalLayout_13.addWidget(self.frame_142)

        self.ColorsOfAtomsTable = QTableWidget(self.tab_40)
        self.ColorsOfAtomsTable.setObjectName(u"ColorsOfAtomsTable")
        self.ColorsOfAtomsTable.setMinimumSize(QSize(0, 30))

        self.verticalLayout_13.addWidget(self.ColorsOfAtomsTable)

        self.tabWidget_12.addTab(self.tab_40, "")
        self.tab_41 = QWidget()
        self.tab_41.setObjectName(u"tab_41")
        self.verticalLayout_20 = QVBoxLayout(self.tab_41)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.frame_144 = QFrame(self.tab_41)
        self.frame_144.setObjectName(u"frame_144")
        self.frame_144.setMinimumSize(QSize(0, 0))
        self.frame_144.setFrameShape(QFrame.NoFrame)
        self.frame_144.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_101 = QHBoxLayout(self.frame_144)
        self.horizontalLayout_101.setObjectName(u"horizontalLayout_101")
        self.horizontalLayout_101.setContentsMargins(0, 0, 0, 0)
        self.label_106 = QLabel(self.frame_144)
        self.label_106.setObjectName(u"label_106")

        self.horizontalLayout_101.addWidget(self.label_106)

        self.ColorBackground = QFrame(self.frame_144)
        self.ColorBackground.setObjectName(u"ColorBackground")
        self.ColorBackground.setFrameShape(QFrame.StyledPanel)
        self.ColorBackground.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_101.addWidget(self.ColorBackground)

        self.ColorBackgroundDialogButton = QPushButton(self.frame_144)
        self.ColorBackgroundDialogButton.setObjectName(u"ColorBackgroundDialogButton")
        self.ColorBackgroundDialogButton.setCheckable(False)
        self.ColorBackgroundDialogButton.setChecked(False)

        self.horizontalLayout_101.addWidget(self.ColorBackgroundDialogButton)


        self.verticalLayout_20.addWidget(self.frame_144)

        self.frame_77 = QFrame(self.tab_41)
        self.frame_77.setObjectName(u"frame_77")
        self.frame_77.setMinimumSize(QSize(0, 0))
        self.frame_77.setFrameShape(QFrame.NoFrame)
        self.frame_77.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_80 = QHBoxLayout(self.frame_77)
        self.horizontalLayout_80.setObjectName(u"horizontalLayout_80")
        self.horizontalLayout_80.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.frame_77)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_80.addWidget(self.label_17)

        self.ColorBond = QFrame(self.frame_77)
        self.ColorBond.setObjectName(u"ColorBond")
        self.ColorBond.setFrameShape(QFrame.StyledPanel)
        self.ColorBond.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_80.addWidget(self.ColorBond)

        self.ColorBondDialogButton = QPushButton(self.frame_77)
        self.ColorBondDialogButton.setObjectName(u"ColorBondDialogButton")
        self.ColorBondDialogButton.setCheckable(False)
        self.ColorBondDialogButton.setChecked(False)

        self.horizontalLayout_80.addWidget(self.ColorBondDialogButton)


        self.verticalLayout_20.addWidget(self.frame_77)

        self.frame_78 = QFrame(self.tab_41)
        self.frame_78.setObjectName(u"frame_78")
        self.frame_78.setMinimumSize(QSize(0, 0))
        self.frame_78.setFrameShape(QFrame.NoFrame)
        self.frame_78.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_81 = QHBoxLayout(self.frame_78)
        self.horizontalLayout_81.setObjectName(u"horizontalLayout_81")
        self.horizontalLayout_81.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.frame_78)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_81.addWidget(self.label_19)

        self.ColorBox = QFrame(self.frame_78)
        self.ColorBox.setObjectName(u"ColorBox")
        self.ColorBox.setFrameShape(QFrame.StyledPanel)
        self.ColorBox.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_81.addWidget(self.ColorBox)

        self.ColorBoxDialogButton = QPushButton(self.frame_78)
        self.ColorBoxDialogButton.setObjectName(u"ColorBoxDialogButton")
        self.ColorBoxDialogButton.setCheckable(False)
        self.ColorBoxDialogButton.setChecked(False)

        self.horizontalLayout_81.addWidget(self.ColorBoxDialogButton)


        self.verticalLayout_20.addWidget(self.frame_78)

        self.frame_79 = QFrame(self.tab_41)
        self.frame_79.setObjectName(u"frame_79")
        self.frame_79.setMinimumSize(QSize(0, 0))
        self.frame_79.setFrameShape(QFrame.NoFrame)
        self.frame_79.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_82 = QHBoxLayout(self.frame_79)
        self.horizontalLayout_82.setObjectName(u"horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.frame_79)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_82.addWidget(self.label_18)

        self.ColorAxes = QFrame(self.frame_79)
        self.ColorAxes.setObjectName(u"ColorAxes")
        self.ColorAxes.setFrameShape(QFrame.StyledPanel)
        self.ColorAxes.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_82.addWidget(self.ColorAxes)

        self.ColorAxesDialogButton = QPushButton(self.frame_79)
        self.ColorAxesDialogButton.setObjectName(u"ColorAxesDialogButton")
        self.ColorAxesDialogButton.setCheckable(False)
        self.ColorAxesDialogButton.setChecked(False)

        self.horizontalLayout_82.addWidget(self.ColorAxesDialogButton)


        self.verticalLayout_20.addWidget(self.frame_79)

        self.frame_10 = QFrame(self.tab_41)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 0))
        self.frame_10.setMaximumSize(QSize(16777215, 16777215))
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_83 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_83.setObjectName(u"horizontalLayout_83")
        self.horizontalLayout_83.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.frame_10)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_83.addWidget(self.label_27)

        self.ColorVoronoi = QFrame(self.frame_10)
        self.ColorVoronoi.setObjectName(u"ColorVoronoi")
        self.ColorVoronoi.setFrameShape(QFrame.StyledPanel)
        self.ColorVoronoi.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_83.addWidget(self.ColorVoronoi)

        self.ColorVoronoiDialogButton = QPushButton(self.frame_10)
        self.ColorVoronoiDialogButton.setObjectName(u"ColorVoronoiDialogButton")
        self.ColorVoronoiDialogButton.setCheckable(False)
        self.ColorVoronoiDialogButton.setChecked(False)

        self.horizontalLayout_83.addWidget(self.ColorVoronoiDialogButton)


        self.verticalLayout_20.addWidget(self.frame_10)

        self.frame_76 = QFrame(self.tab_41)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setMaximumSize(QSize(16777215, 16777215))
        self.frame_76.setFrameShape(QFrame.NoFrame)
        self.frame_76.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_77 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.label_29 = QLabel(self.frame_76)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_77.addWidget(self.label_29)

        self.FormSettingsColorsScale = QComboBox(self.frame_76)
        self.FormSettingsColorsScale.setObjectName(u"FormSettingsColorsScale")
        self.FormSettingsColorsScale.setMinimumSize(QSize(250, 0))
        self.FormSettingsColorsScale.setEditable(False)

        self.horizontalLayout_77.addWidget(self.FormSettingsColorsScale)


        self.verticalLayout_20.addWidget(self.frame_76)

        self.ColorRow = PyqtGraphWidgetImage(self.tab_41)
        self.ColorRow.setObjectName(u"ColorRow")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ColorRow.sizePolicy().hasHeightForWidth())
        self.ColorRow.setSizePolicy(sizePolicy2)
        self.ColorRow.setMinimumSize(QSize(0, 40))
        self.ColorRow.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_20.addWidget(self.ColorRow)

        self.frame_102 = QFrame(self.tab_41)
        self.frame_102.setObjectName(u"frame_102")
        self.frame_102.setFrameShape(QFrame.NoFrame)
        self.frame_102.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_106 = QHBoxLayout(self.frame_102)
        self.horizontalLayout_106.setObjectName(u"horizontalLayout_106")
        self.label_14 = QLabel(self.frame_102)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_106.addWidget(self.label_14)

        self.FormSettingsColorsScaleType = QComboBox(self.frame_102)
        self.FormSettingsColorsScaleType.setObjectName(u"FormSettingsColorsScaleType")
        self.FormSettingsColorsScaleType.setMinimumSize(QSize(250, 0))
        self.FormSettingsColorsScaleType.setEditable(False)

        self.horizontalLayout_106.addWidget(self.FormSettingsColorsScaleType)


        self.verticalLayout_20.addWidget(self.frame_102)

        self.frame_72 = QFrame(self.tab_41)
        self.frame_72.setObjectName(u"frame_72")
        self.frame_72.setMinimumSize(QSize(0, 0))
        self.frame_72.setMaximumSize(QSize(16777215, 16777215))
        self.frame_72.setFrameShape(QFrame.NoFrame)
        self.frame_72.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_78 = QHBoxLayout(self.frame_72)
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.horizontalLayout_78.setContentsMargins(0, -1, 0, -1)
        self.FormSettingsContourColorFixed = QCheckBox(self.frame_72)
        self.FormSettingsContourColorFixed.setObjectName(u"FormSettingsContourColorFixed")

        self.horizontalLayout_78.addWidget(self.FormSettingsContourColorFixed)

        self.ColorContour = QFrame(self.frame_72)
        self.ColorContour.setObjectName(u"ColorContour")
        self.ColorContour.setFrameShape(QFrame.StyledPanel)
        self.ColorContour.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_78.addWidget(self.ColorContour)

        self.ColorContourDialogButton = QPushButton(self.frame_72)
        self.ColorContourDialogButton.setObjectName(u"ColorContourDialogButton")
        self.ColorContourDialogButton.setCheckable(False)
        self.ColorContourDialogButton.setChecked(False)

        self.horizontalLayout_78.addWidget(self.ColorContourDialogButton)


        self.verticalLayout_20.addWidget(self.frame_72)

        self.frame_5 = QFrame(self.tab_41)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_57 = QVBoxLayout(self.frame_5)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_57.setContentsMargins(0, -1, 0, 0)
        self.FormSettingsColorsFixed = QCheckBox(self.frame_5)
        self.FormSettingsColorsFixed.setObjectName(u"FormSettingsColorsFixed")

        self.verticalLayout_57.addWidget(self.FormSettingsColorsFixed)


        self.verticalLayout_20.addWidget(self.frame_5)

        self.frame_89 = QFrame(self.tab_41)
        self.frame_89.setObjectName(u"frame_89")
        self.frame_89.setFrameShape(QFrame.NoFrame)
        self.frame_89.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_90 = QHBoxLayout(self.frame_89)
        self.horizontalLayout_90.setObjectName(u"horizontalLayout_90")
        self.horizontalLayout_90.setContentsMargins(60, 0, -1, 0)
        self.label_15 = QLabel(self.frame_89)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_90.addWidget(self.label_15)

        self.FormSettingsColorsFixedMin = QDoubleSpinBox(self.frame_89)
        self.FormSettingsColorsFixedMin.setObjectName(u"FormSettingsColorsFixedMin")
        self.FormSettingsColorsFixedMin.setDecimals(4)
        self.FormSettingsColorsFixedMin.setMinimum(-100.000000000000000)
        self.FormSettingsColorsFixedMin.setMaximum(100.000000000000000)
        self.FormSettingsColorsFixedMin.setSingleStep(0.100000000000000)

        self.horizontalLayout_90.addWidget(self.FormSettingsColorsFixedMin)

        self.horizontalSpacer_50 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_90.addItem(self.horizontalSpacer_50)


        self.verticalLayout_20.addWidget(self.frame_89)

        self.frame_90 = QFrame(self.tab_41)
        self.frame_90.setObjectName(u"frame_90")
        self.frame_90.setFrameShape(QFrame.NoFrame)
        self.frame_90.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_89 = QHBoxLayout(self.frame_90)
        self.horizontalLayout_89.setObjectName(u"horizontalLayout_89")
        self.horizontalLayout_89.setContentsMargins(60, 0, -1, 0)
        self.label_16 = QLabel(self.frame_90)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_89.addWidget(self.label_16)

        self.FormSettingsColorsFixedMax = QDoubleSpinBox(self.frame_90)
        self.FormSettingsColorsFixedMax.setObjectName(u"FormSettingsColorsFixedMax")
        self.FormSettingsColorsFixedMax.setDecimals(4)
        self.FormSettingsColorsFixedMax.setMinimum(-100.000000000000000)
        self.FormSettingsColorsFixedMax.setMaximum(100.000000000000000)
        self.FormSettingsColorsFixedMax.setSingleStep(0.100000000000000)

        self.horizontalLayout_89.addWidget(self.FormSettingsColorsFixedMax)

        self.horizontalSpacer_52 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_89.addItem(self.horizontalSpacer_52)


        self.verticalLayout_20.addWidget(self.frame_90)

        self.verticalSpacer_19 = QSpacerItem(20, 215, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.verticalSpacer_19)

        self.tabWidget_12.addTab(self.tab_41, "")

        self.verticalLayout_14.addWidget(self.tabWidget_12)

        self.tabWidget_9.addTab(self.tab_37, "")

        self.verticalLayout_23.addWidget(self.tabWidget_9)

        self.tabWidget.addTab(self.tab_29, "")
        self.FormTabSettings = QWidget()
        self.FormTabSettings.setObjectName(u"FormTabSettings")
        self.verticalLayout_3 = QVBoxLayout(self.FormTabSettings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.FormSettingsOpeningCheckOnlyOptimal = QCheckBox(self.FormTabSettings)
        self.FormSettingsOpeningCheckOnlyOptimal.setObjectName(u"FormSettingsOpeningCheckOnlyOptimal")
        self.FormSettingsOpeningCheckOnlyOptimal.setFocusPolicy(Qt.StrongFocus)

        self.verticalLayout_3.addWidget(self.FormSettingsOpeningCheckOnlyOptimal)

        self.FormSettingsParseAtomicProperties = QCheckBox(self.FormTabSettings)
        self.FormSettingsParseAtomicProperties.setObjectName(u"FormSettingsParseAtomicProperties")

        self.verticalLayout_3.addWidget(self.FormSettingsParseAtomicProperties)

        self.frame_108 = QFrame(self.FormTabSettings)
        self.frame_108.setObjectName(u"frame_108")
        self.frame_108.setEnabled(True)
        self.frame_108.setMinimumSize(QSize(0, 0))
        self.frame_108.setFrameShape(QFrame.NoFrame)
        self.frame_108.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_111 = QHBoxLayout(self.frame_108)
        self.horizontalLayout_111.setObjectName(u"horizontalLayout_111")
        self.horizontalLayout_111.setContentsMargins(0, -1, -1, -1)
        self.FormSettingsViewCheckAtomSelection = QRadioButton(self.frame_108)
        self.FormSettingsViewCheckAtomSelection.setObjectName(u"FormSettingsViewCheckAtomSelection")
        self.FormSettingsViewCheckAtomSelection.setEnabled(True)

        self.horizontalLayout_111.addWidget(self.FormSettingsViewCheckAtomSelection)

        self.FormSettingsViewCheckModelMove = QRadioButton(self.frame_108)
        self.FormSettingsViewCheckModelMove.setObjectName(u"FormSettingsViewCheckModelMove")

        self.horizontalLayout_111.addWidget(self.FormSettingsViewCheckModelMove)


        self.verticalLayout_3.addWidget(self.frame_108)

        self.frame_122 = QFrame(self.FormTabSettings)
        self.frame_122.setObjectName(u"frame_122")
        self.frame_122.setFrameShape(QFrame.NoFrame)
        self.frame_122.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_127 = QHBoxLayout(self.frame_122)
        self.horizontalLayout_127.setObjectName(u"horizontalLayout_127")
        self.horizontalLayout_127.setContentsMargins(0, 11, 0, 0)
        self.label_92 = QLabel(self.frame_122)
        self.label_92.setObjectName(u"label_92")

        self.horizontalLayout_127.addWidget(self.label_92)

        self.FormSettingsPreferredUnits = QComboBox(self.frame_122)
        self.FormSettingsPreferredUnits.setObjectName(u"FormSettingsPreferredUnits")
        self.FormSettingsPreferredUnits.setEditable(False)

        self.horizontalLayout_127.addWidget(self.FormSettingsPreferredUnits)


        self.verticalLayout_3.addWidget(self.frame_122)

        self.frame_151 = QFrame(self.FormTabSettings)
        self.frame_151.setObjectName(u"frame_151")
        self.frame_151.setFrameShape(QFrame.NoFrame)
        self.frame_151.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_164 = QHBoxLayout(self.frame_151)
        self.horizontalLayout_164.setObjectName(u"horizontalLayout_164")
        self.horizontalLayout_164.setContentsMargins(0, -1, 0, -1)
        self.label_49 = QLabel(self.frame_151)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_164.addWidget(self.label_49)

        self.FormSettingsPreferredCoordinates = QComboBox(self.frame_151)
        self.FormSettingsPreferredCoordinates.setObjectName(u"FormSettingsPreferredCoordinates")
        self.FormSettingsPreferredCoordinates.setEditable(False)

        self.horizontalLayout_164.addWidget(self.FormSettingsPreferredCoordinates)


        self.verticalLayout_3.addWidget(self.frame_151)

        self.frame_85 = QFrame(self.FormTabSettings)
        self.frame_85.setObjectName(u"frame_85")
        self.frame_85.setFrameShape(QFrame.NoFrame)
        self.frame_85.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_85)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.horizontalLayout_85.setContentsMargins(0, 0, 0, 0)
        self.label_50 = QLabel(self.frame_85)
        self.label_50.setObjectName(u"label_50")

        self.horizontalLayout_85.addWidget(self.label_50)

        self.FormSettingsPreferredLattice = QComboBox(self.frame_85)
        self.FormSettingsPreferredLattice.setObjectName(u"FormSettingsPreferredLattice")
        self.FormSettingsPreferredLattice.setEditable(False)

        self.horizontalLayout_85.addWidget(self.FormSettingsPreferredLattice)


        self.verticalLayout_3.addWidget(self.frame_85)

        self.frame_80 = QFrame(self.FormTabSettings)
        self.frame_80.setObjectName(u"frame_80")
        self.frame_80.setFrameShape(QFrame.NoFrame)
        self.frame_80.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_84 = QHBoxLayout(self.frame_80)
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.horizontalLayout_84.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_80)

        self.verticalSpacer_18 = QSpacerItem(20, 568, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_18)

        self.tabWidget.addTab(self.FormTabSettings, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.Form3Dand2DTabs = QToolBox(self.centralwidget)
        self.Form3Dand2DTabs.setObjectName(u"Form3Dand2DTabs")
        sizePolicy2.setHeightForWidth(self.Form3Dand2DTabs.sizePolicy().hasHeightForWidth())
        self.Form3Dand2DTabs.setSizePolicy(sizePolicy2)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.page_7.setGeometry(QRect(0, 0, 665, 765))
        self.horizontalLayout_3 = QHBoxLayout(self.page_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.openGLWidget = GuiOpenGL(self.page_7)
        self.openGLWidget.setObjectName(u"openGLWidget")

        self.horizontalLayout_3.addWidget(self.openGLWidget)

        self.Form3Dand2DTabs.addItem(self.page_7, u"3D View")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.page_8.setGeometry(QRect(0, 0, 79, 100))
        self.horizontalLayout = QHBoxLayout(self.page_8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.PyqtGraphWidget = PyqtGraphWidget(self.page_8)
        self.PyqtGraphWidget.setObjectName(u"PyqtGraphWidget")
        sizePolicy2.setHeightForWidth(self.PyqtGraphWidget.sizePolicy().hasHeightForWidth())
        self.PyqtGraphWidget.setSizePolicy(sizePolicy2)
        self.PyqtGraphWidget.setMinimumSize(QSize(0, 100))

        self.horizontalLayout.addWidget(self.PyqtGraphWidget)

        self.Form3Dand2DTabs.addItem(self.page_8, u"2D Figure")

        self.horizontalLayout_2.addWidget(self.Form3Dand2DTabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1144, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuOrtho_Perspective = QMenu(self.menuView)
        self.menuOrtho_Perspective.setObjectName(u"menuOrtho_Perspective")
        self.menuBox = QMenu(self.menuView)
        self.menuBox.setObjectName(u"menuBox")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(30, 50))
        self.toolBar.setMaximumSize(QSize(16777215, 50))
        self.toolBar.setOrientation(Qt.Horizontal)
        self.toolBar.setFloatable(True)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionClose)
        self.menuView.addAction(self.menuOrtho_Perspective.menuAction())
        self.menuView.addAction(self.menuBox.menuAction())
        self.menuOrtho_Perspective.addAction(self.actionOrtho)
        self.menuOrtho_Perspective.addAction(self.actionPerspective)
        self.menuBox.addAction(self.actionShowBox)
        self.menuBox.addAction(self.actionHideBox)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionManual)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_9.setCurrentIndex(0)
        self.tabWidget_12.setCurrentIndex(1)
        self.Form3Dand2DTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GUI4dft, the SIESTA Visualization Tool", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionOrtho.setText(QCoreApplication.translate("MainWindow", u"Ortho", None))
        self.actionPerspective.setText(QCoreApplication.translate("MainWindow", u"Perspective", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionShowBox.setText(QCoreApplication.translate("MainWindow", u"Show Box", None))
        self.actionHideBox.setText(QCoreApplication.translate("MainWindow", u"Hide Box", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.groupBox_58.setTitle(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_131.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_134.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.label_135.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Camera position", None))
        self.label_137.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_138.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.label_139.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.label_136.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabModel), QCoreApplication.translate("MainWindow", u"Model", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Atom - atom distance", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.PropertyAtomAtomDistanceGet.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_20), QCoreApplication.translate("MainWindow", u"Selection", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Fill Space", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This tab is designed to search for various configurations of a given number of atoms within a given cylindrical volume.</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"nAtoms", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"charge of atoms", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"delta", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"nPrompts", None))
        self.cylinder.setText(QCoreApplication.translate("MainWindow", u"radius of cylinder (center in the origin)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"height of cylinder (Z direction)", None))
        self.fill_space.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.groupBox_60.setTitle(QCoreApplication.translate("MainWindow", u"Add Li to hexagons", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"Li atoms", None))
        self.add_atoms_to_hexagons.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.FormActionsPreSaveToFileFillSpace.setText(QCoreApplication.translate("MainWindow", u"Save to files", None))
        self.groupBox_61.setTitle(QCoreApplication.translate("MainWindow", u"Hops", None))
        self.hops_analis.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabActions), QCoreApplication.translate("MainWindow", u"Hexagons", None))
        self.FormSettingsViewCheckShowAtoms.setText(QCoreApplication.translate("MainWindow", u"Show atoms", None))
        self.FormSettingsViewCheckShowBox.setText(QCoreApplication.translate("MainWindow", u"Show box", None))
        self.FormSettingsViewCheckShowAtomNumber.setText(QCoreApplication.translate("MainWindow", u"Show atom number", None))
        self.FormSettingsViewCheckShowAxes.setText(QCoreApplication.translate("MainWindow", u"Show axes", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Contours width", None))
        self.label_105.setText(QCoreApplication.translate("MainWindow", u"Perspective angle", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Bonds", None))
        self.FormSettingsViewCheckShowBonds.setText(QCoreApplication.translate("MainWindow", u"Show bonds", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Bonds width", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.FormSettingsViewRadioColorBondsManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.FormSettingsViewRadioColorBondsByAtoms.setText(QCoreApplication.translate("MainWindow", u"By atoms color", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Bond parameter", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Text", None))
        self.label_132.setText(QCoreApplication.translate("MainWindow", u"Position: X", None))
        self.label_133.setText(QCoreApplication.translate("MainWindow", u", Y", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"Font size", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"Figures in property", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"OpenGl", None))
        self.OpenGL_GL_CULL_FACE.setText(QCoreApplication.translate("MainWindow", u"GL_CULL_FACE", None))
        self.ColorAtomsProperty.setText(QCoreApplication.translate("MainWindow", u"Color atoms with property", None))
        self.show_property_text.setText(QCoreApplication.translate("MainWindow", u"Show property", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_32), QCoreApplication.translate("MainWindow", u"View 3D", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Colors", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Font color", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Font size", None))
        self.label_91.setText(QCoreApplication.translate("MainWindow", u"Title font size", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Axes font size", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Label font size", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Line width", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Line width", None))
        self.FormStylesFor2DGraph.setText(QCoreApplication.translate("MainWindow", u"Apply style", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_33), QCoreApplication.translate("MainWindow", u"View 2D", None))
        self.cpk_radio.setText(QCoreApplication.translate("MainWindow", u"cpk", None))
        self.jmol_radio.setText(QCoreApplication.translate("MainWindow", u"jmol", None))
        self.manual_colors_radio.setText(QCoreApplication.translate("MainWindow", u"manual", None))
        self.manual_colors_default.setText(QCoreApplication.translate("MainWindow", u"default", None))
        self.tabWidget_12.setTabText(self.tabWidget_12.indexOf(self.tab_40), QCoreApplication.translate("MainWindow", u"Atoms", None))
        self.label_106.setText(QCoreApplication.translate("MainWindow", u"Background color", None))
        self.ColorBackgroundDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Bonds color", None))
        self.ColorBondDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Box color", None))
        self.ColorBoxDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Axes color", None))
        self.ColorAxesDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Voronoi color", None))
        self.ColorVoronoiDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Color scheme", None))
        self.FormSettingsColorsScale.setCurrentText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.FormSettingsColorsScaleType.setCurrentText("")
        self.FormSettingsContourColorFixed.setText(QCoreApplication.translate("MainWindow", u"Contour color", None))
        self.ColorContourDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.FormSettingsColorsFixed.setText(QCoreApplication.translate("MainWindow", u"Use fixed colors range", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Min value", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Max value", None))
        self.tabWidget_12.setTabText(self.tabWidget_12.indexOf(self.tab_41), QCoreApplication.translate("MainWindow", u"Other Colors", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_37), QCoreApplication.translate("MainWindow", u"Colors", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_29), QCoreApplication.translate("MainWindow", u"View", None))
        self.FormSettingsOpeningCheckOnlyOptimal.setText(QCoreApplication.translate("MainWindow", u"Get only optimal structures", None))
        self.FormSettingsParseAtomicProperties.setText(QCoreApplication.translate("MainWindow", u"Parse atomic properties", None))
        self.FormSettingsViewCheckAtomSelection.setText(QCoreApplication.translate("MainWindow", u"Allow atom selection", None))
        self.FormSettingsViewCheckModelMove.setText(QCoreApplication.translate("MainWindow", u"Allow model move", None))
        self.label_92.setText(QCoreApplication.translate("MainWindow", u"Preferred units", None))
        self.FormSettingsPreferredUnits.setCurrentText("")
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Preferred coordinates", None))
        self.FormSettingsPreferredCoordinates.setCurrentText("")
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Preferred lattice", None))
        self.FormSettingsPreferredLattice.setCurrentText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabSettings), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Form3Dand2DTabs.setItemText(self.Form3Dand2DTabs.indexOf(self.page_7), QCoreApplication.translate("MainWindow", u"3D View", None))
        self.Form3Dand2DTabs.setItemText(self.Form3Dand2DTabs.indexOf(self.page_8), QCoreApplication.translate("MainWindow", u"2D Figure", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuOrtho_Perspective.setTitle(QCoreApplication.translate("MainWindow", u"Ortho / Perspective", None))
        self.menuBox.setTitle(QCoreApplication.translate("MainWindow", u"Box", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

