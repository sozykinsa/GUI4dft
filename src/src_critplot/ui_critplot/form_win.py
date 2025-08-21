# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'critplotform.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QLocale,
                         QMetaObject, QRect,
                         QSize, Qt)
from qtpy.QtGui import (QAction)
from qtpy.QtWidgets import (QCheckBox, QComboBox, QDoubleSpinBox,
                            QFrame, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMenu, QMenuBar, QPushButton,
                            QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
                            QTabWidget, QTableWidget, QTextBrowser,
                            QToolBar, QToolBox, QVBoxLayout, QWidget)

from src_critplot.qtbased.guiopengl_cp import GuiOpenGLCP
from core_atomistic_qt.qt_graph import PyqtGraphWidget
from core_atomistic_qt.qt_image import PyqtGraphWidgetImage

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1121, 925)
        MainWindow.setMinimumSize(QSize(0, 200))
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
        self.FormModelTableProperties.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.FormModelTableProperties)

        self.groupBox_13 = QGroupBox(self.FormTabModel)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_15 = QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_131 = QLabel(self.groupBox_13)
        self.label_131.setObjectName(u"label_131")

        self.horizontalLayout_15.addWidget(self.label_131)

        self.model_rotation_x = QDoubleSpinBox(self.groupBox_13)
        self.model_rotation_x.setObjectName(u"model_rotation_x")
        self.model_rotation_x.setMinimum(-360.000000000000000)
        self.model_rotation_x.setMaximum(360.990000000000009)

        self.horizontalLayout_15.addWidget(self.model_rotation_x)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_3)

        self.label_134 = QLabel(self.groupBox_13)
        self.label_134.setObjectName(u"label_134")

        self.horizontalLayout_15.addWidget(self.label_134)

        self.model_rotation_y = QDoubleSpinBox(self.groupBox_13)
        self.model_rotation_y.setObjectName(u"model_rotation_y")
        self.model_rotation_y.setMinimum(-360.000000000000000)
        self.model_rotation_y.setMaximum(360.990000000000009)

        self.horizontalLayout_15.addWidget(self.model_rotation_y)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_4)

        self.label_135 = QLabel(self.groupBox_13)
        self.label_135.setObjectName(u"label_135")

        self.horizontalLayout_15.addWidget(self.label_135)

        self.model_rotation_z = QDoubleSpinBox(self.groupBox_13)
        self.model_rotation_z.setObjectName(u"model_rotation_z")
        self.model_rotation_z.setMinimum(-360.000000000000000)
        self.model_rotation_z.setMaximum(360.990000000000009)

        self.horizontalLayout_15.addWidget(self.model_rotation_z)


        self.verticalLayout.addWidget(self.groupBox_13)

        self.groupBox_32 = QGroupBox(self.FormTabModel)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_18 = QHBoxLayout(self.groupBox_32)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
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

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_182.addItem(self.horizontalSpacer_6)

        self.label_138 = QLabel(self.frame_167)
        self.label_138.setObjectName(u"label_138")

        self.horizontalLayout_182.addWidget(self.label_138)

        self.camera_pos_y = QDoubleSpinBox(self.frame_167)
        self.camera_pos_y.setObjectName(u"camera_pos_y")
        self.camera_pos_y.setMinimum(-99.000000000000000)

        self.horizontalLayout_182.addWidget(self.camera_pos_y)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_182.addItem(self.horizontalSpacer_19)

        self.label_139 = QLabel(self.frame_167)
        self.label_139.setObjectName(u"label_139")

        self.horizontalLayout_182.addWidget(self.label_139)

        self.camera_pos_z = QDoubleSpinBox(self.frame_167)
        self.camera_pos_z.setObjectName(u"camera_pos_z")
        self.camera_pos_z.setMinimum(-99.000000000000000)

        self.horizontalLayout_182.addWidget(self.camera_pos_z)


        self.horizontalLayout_18.addWidget(self.frame_167)

        self.frame_166 = QFrame(self.groupBox_32)
        self.frame_166.setObjectName(u"frame_166")
        self.frame_166.setFrameShape(QFrame.NoFrame)
        self.frame_166.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_181 = QHBoxLayout(self.frame_166)
        self.horizontalLayout_181.setObjectName(u"horizontalLayout_181")
        self.horizontalLayout_181.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_18.addWidget(self.frame_166)


        self.verticalLayout.addWidget(self.groupBox_32)

        self.groupBox_14 = QGroupBox(self.FormTabModel)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_16 = QHBoxLayout(self.groupBox_14)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.model_scale = QDoubleSpinBox(self.groupBox_14)
        self.model_scale.setObjectName(u"model_scale")
        self.model_scale.setMinimum(0.010000000000000)
        self.model_scale.setSingleStep(0.100000000000000)
        self.model_scale.setValue(1.000000000000000)

        self.horizontalLayout_16.addWidget(self.model_scale)

        self.horizontalSpacer_17 = QSpacerItem(307, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_17)


        self.verticalLayout.addWidget(self.groupBox_14)

        self.tabWidget.addTab(self.FormTabModel, "")
        self.tab_51 = QWidget()
        self.tab_51.setObjectName(u"tab_51")
        self.verticalLayout_12 = QVBoxLayout(self.tab_51)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.add_xyz_critic_data = QPushButton(self.tab_51)
        self.add_xyz_critic_data.setObjectName(u"add_xyz_critic_data")
        self.add_xyz_critic_data.setEnabled(False)

        self.verticalLayout_12.addWidget(self.add_xyz_critic_data)

        self.groupBox_30 = QGroupBox(self.tab_51)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.groupBox_30.setMinimumSize(QSize(0, 0))
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_30)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.frame_110 = QFrame(self.groupBox_30)
        self.frame_110.setObjectName(u"frame_110")
        self.frame_110.setFrameShape(QFrame.Box)
        self.frame_110.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_112 = QHBoxLayout(self.frame_110)
        self.horizontalLayout_112.setObjectName(u"horizontalLayout_112")
        self.horizontalLayout_112.setContentsMargins(-1, 0, -1, 0)
        self.label_82 = QLabel(self.frame_110)
        self.label_82.setObjectName(u"label_82")

        self.horizontalLayout_112.addWidget(self.label_82)

        self.selectedCP = QLabel(self.frame_110)
        self.selectedCP.setObjectName(u"selectedCP")

        self.horizontalLayout_112.addWidget(self.selectedCP)


        self.verticalLayout_16.addWidget(self.frame_110)

        self.frame_2 = QFrame(self.groupBox_30)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_88 = QLabel(self.frame_2)
        self.label_88.setObjectName(u"label_88")

        self.horizontalLayout_5.addWidget(self.label_88)

        self.selected_cp_title = QLabel(self.frame_2)
        self.selected_cp_title.setObjectName(u"selected_cp_title")

        self.horizontalLayout_5.addWidget(self.selected_cp_title)


        self.verticalLayout_16.addWidget(self.frame_2)

        self.frame_87 = QFrame(self.groupBox_30)
        self.frame_87.setObjectName(u"frame_87")
        self.frame_87.setFrameShape(QFrame.Box)
        self.frame_87.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.frame_87)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.horizontalLayout_88.setContentsMargins(-1, 0, -1, 0)
        self.label_107 = QLabel(self.frame_87)
        self.label_107.setObjectName(u"label_107")

        self.horizontalLayout_88.addWidget(self.label_107)

        self.selectedCP_nuclei = QLabel(self.frame_87)
        self.selectedCP_nuclei.setObjectName(u"selectedCP_nuclei")

        self.horizontalLayout_88.addWidget(self.selectedCP_nuclei)


        self.verticalLayout_16.addWidget(self.frame_87)

        self.frame_109 = QFrame(self.groupBox_30)
        self.frame_109.setObjectName(u"frame_109")
        self.frame_109.setFrameShape(QFrame.NoFrame)
        self.frame_109.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_156 = QHBoxLayout(self.frame_109)
        self.horizontalLayout_156.setObjectName(u"horizontalLayout_156")
        self.horizontalLayout_156.setContentsMargins(-1, 0, -1, 0)
        self.label_111 = QLabel(self.frame_109)
        self.label_111.setObjectName(u"label_111")

        self.horizontalLayout_156.addWidget(self.label_111)

        self.selected_cp_bond_len = QLabel(self.frame_109)
        self.selected_cp_bond_len.setObjectName(u"selected_cp_bond_len")

        self.horizontalLayout_156.addWidget(self.selected_cp_bond_len)


        self.verticalLayout_16.addWidget(self.frame_109)

        self.frame_111 = QFrame(self.groupBox_30)
        self.frame_111.setObjectName(u"frame_111")
        self.frame_111.setFrameShape(QFrame.Box)
        self.frame_111.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_113 = QHBoxLayout(self.frame_111)
        self.horizontalLayout_113.setObjectName(u"horizontalLayout_113")
        self.horizontalLayout_113.setContentsMargins(-1, 0, -1, 0)
        self.label_84 = QLabel(self.frame_111)
        self.label_84.setObjectName(u"label_84")

        self.horizontalLayout_113.addWidget(self.label_84)

        self.FormSelectedCP_f = QLabel(self.frame_111)
        self.FormSelectedCP_f.setObjectName(u"FormSelectedCP_f")

        self.horizontalLayout_113.addWidget(self.FormSelectedCP_f)


        self.verticalLayout_16.addWidget(self.frame_111)

        self.frame_112 = QFrame(self.groupBox_30)
        self.frame_112.setObjectName(u"frame_112")
        self.frame_112.setFrameShape(QFrame.NoFrame)
        self.frame_112.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_114 = QHBoxLayout(self.frame_112)
        self.horizontalLayout_114.setObjectName(u"horizontalLayout_114")
        self.horizontalLayout_114.setContentsMargins(-1, 0, -1, 0)
        self.label_85 = QLabel(self.frame_112)
        self.label_85.setObjectName(u"label_85")

        self.horizontalLayout_114.addWidget(self.label_85)

        self.FormSelectedCP_g = QLabel(self.frame_112)
        self.FormSelectedCP_g.setObjectName(u"FormSelectedCP_g")

        self.horizontalLayout_114.addWidget(self.FormSelectedCP_g)


        self.verticalLayout_16.addWidget(self.frame_112)

        self.frame_113 = QFrame(self.groupBox_30)
        self.frame_113.setObjectName(u"frame_113")
        self.frame_113.setFrameShape(QFrame.Box)
        self.frame_113.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_115 = QHBoxLayout(self.frame_113)
        self.horizontalLayout_115.setObjectName(u"horizontalLayout_115")
        self.horizontalLayout_115.setContentsMargins(-1, 0, -1, 0)
        self.label_87 = QLabel(self.frame_113)
        self.label_87.setObjectName(u"label_87")

        self.horizontalLayout_115.addWidget(self.label_87)

        self.FormSelectedCP_lap = QLabel(self.frame_113)
        self.FormSelectedCP_lap.setObjectName(u"FormSelectedCP_lap")
        self.FormSelectedCP_lap.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_115.addWidget(self.FormSelectedCP_lap)


        self.verticalLayout_16.addWidget(self.frame_113)


        self.verticalLayout_12.addWidget(self.groupBox_30)

        self.groupBox_5 = QGroupBox(self.tab_51)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.FormCPlist = QListWidget(self.groupBox_5)
        self.FormCPlist.setObjectName(u"FormCPlist")
        self.FormCPlist.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.FormCPlist)

        self.frame_16 = QFrame(self.groupBox_5)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_16)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.add_cp_to_list = QPushButton(self.frame_16)
        self.add_cp_to_list.setObjectName(u"add_cp_to_list")

        self.verticalLayout_26.addWidget(self.add_cp_to_list)

        self.delete_cp_from_list = QPushButton(self.frame_16)
        self.delete_cp_from_list.setObjectName(u"delete_cp_from_list")

        self.verticalLayout_26.addWidget(self.delete_cp_from_list)

        self.clear_cp_list = QPushButton(self.frame_16)
        self.clear_cp_list.setObjectName(u"clear_cp_list")

        self.verticalLayout_26.addWidget(self.clear_cp_list)

        self.delete_cp_from_model = QPushButton(self.frame_16)
        self.delete_cp_from_model.setObjectName(u"delete_cp_from_model")

        self.verticalLayout_26.addWidget(self.delete_cp_from_model)

        self.leave_cp_in_model = QPushButton(self.frame_16)
        self.leave_cp_in_model.setObjectName(u"leave_cp_in_model")

        self.verticalLayout_26.addWidget(self.leave_cp_in_model)

        self.groupBox_15 = QGroupBox(self.frame_16)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_15 = QTabWidget(self.groupBox_15)
        self.tabWidget_15.setObjectName(u"tabWidget_15")
        self.tabWidget_15.setMinimumSize(QSize(0, 300))
        self.tab_39 = QWidget()
        self.tab_39.setObjectName(u"tab_39")
        self.verticalLayout_20 = QVBoxLayout(self.tab_39)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.frame_58 = QFrame(self.tab_39)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setFrameShape(QFrame.NoFrame)
        self.frame_58.setFrameShadow(QFrame.Raised)
        self.verticalLayout_99 = QVBoxLayout(self.frame_58)
        self.verticalLayout_99.setObjectName(u"verticalLayout_99")
        self.form_critic_list = QRadioButton(self.frame_58)
        self.form_critic_list.setObjectName(u"form_critic_list")
        self.form_critic_list.setChecked(True)

        self.verticalLayout_99.addWidget(self.form_critic_list)

        self.form_critic_all = QRadioButton(self.frame_58)
        self.form_critic_all.setObjectName(u"form_critic_all")

        self.verticalLayout_99.addWidget(self.form_critic_all)


        self.verticalLayout_20.addWidget(self.frame_58)

        self.widget = QWidget(self.tab_39)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_176 = QHBoxLayout(self.widget)
        self.horizontalLayout_176.setObjectName(u"horizontalLayout_176")
        self.horizontalSpacer_57 = QSpacerItem(104, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_176.addItem(self.horizontalSpacer_57)

        self.export_cp_to_csv = QPushButton(self.widget)
        self.export_cp_to_csv.setObjectName(u"export_cp_to_csv")

        self.horizontalLayout_176.addWidget(self.export_cp_to_csv)

        self.horizontalSpacer_123 = QSpacerItem(103, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_176.addItem(self.horizontalSpacer_123)


        self.verticalLayout_20.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 365, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.verticalSpacer)

        self.tabWidget_15.addTab(self.tab_39, "")
        self.tab_53 = QWidget()
        self.tab_53.setObjectName(u"tab_53")
        self.verticalLayout_69 = QVBoxLayout(self.tab_53)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.tabWidget_14 = QTabWidget(self.tab_53)
        self.tabWidget_14.setObjectName(u"tabWidget_14")
        self.tab_48 = QWidget()
        self.tab_48.setObjectName(u"tab_48")
        self.horizontalLayout_162 = QHBoxLayout(self.tab_48)
        self.horizontalLayout_162.setObjectName(u"horizontalLayout_162")
        self.criticalPointImports = QTextBrowser(self.tab_48)
        self.criticalPointImports.setObjectName(u"criticalPointImports")

        self.horizontalLayout_162.addWidget(self.criticalPointImports)

        self.tabWidget_14.addTab(self.tab_48, "")
        self.tab_46 = QWidget()
        self.tab_46.setObjectName(u"tab_46")
        self.verticalLayout_87 = QVBoxLayout(self.tab_46)
        self.verticalLayout_87.setObjectName(u"verticalLayout_87")
        self.frame_140 = QFrame(self.tab_46)
        self.frame_140.setObjectName(u"frame_140")
        self.frame_140.setFrameShape(QFrame.NoFrame)
        self.frame_140.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_143 = QHBoxLayout(self.frame_140)
        self.horizontalLayout_143.setObjectName(u"horizontalLayout_143")
        self.form_critic_all_cp = QCheckBox(self.frame_140)
        self.form_critic_all_cp.setObjectName(u"form_critic_all_cp")

        self.horizontalLayout_143.addWidget(self.form_critic_all_cp)


        self.verticalLayout_87.addWidget(self.frame_140)

        self.frame_134 = QFrame(self.tab_46)
        self.frame_134.setObjectName(u"frame_134")
        self.frame_134.setFrameShape(QFrame.NoFrame)
        self.frame_134.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_137 = QHBoxLayout(self.frame_134)
        self.horizontalLayout_137.setObjectName(u"horizontalLayout_137")
        self.radioButton_9 = QRadioButton(self.frame_134)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.horizontalLayout_137.addWidget(self.radioButton_9)

        self.formCriticBPradio = QRadioButton(self.frame_134)
        self.formCriticBPradio.setObjectName(u"formCriticBPradio")
        self.formCriticBPradio.setChecked(True)

        self.horizontalLayout_137.addWidget(self.formCriticBPradio)

        self.FormExtraPoints = QSpinBox(self.frame_134)
        self.FormExtraPoints.setObjectName(u"FormExtraPoints")

        self.horizontalLayout_137.addWidget(self.FormExtraPoints)

        self.label_86 = QLabel(self.frame_134)
        self.label_86.setObjectName(u"label_86")

        self.horizontalLayout_137.addWidget(self.label_86)


        self.verticalLayout_87.addWidget(self.frame_134)

        self.verticalSpacer_30 = QSpacerItem(20, 342, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_87.addItem(self.verticalSpacer_30)

        self.tabWidget_14.addTab(self.tab_46, "")
        self.tab_47 = QWidget()
        self.tab_47.setObjectName(u"tab_47")
        self.verticalLayout_86 = QVBoxLayout(self.tab_47)
        self.verticalLayout_86.setObjectName(u"verticalLayout_86")
        self.frame_135 = QFrame(self.tab_47)
        self.frame_135.setObjectName(u"frame_135")
        self.frame_135.setFrameShape(QFrame.NoFrame)
        self.frame_135.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_138 = QHBoxLayout(self.frame_135)
        self.horizontalLayout_138.setObjectName(u"horizontalLayout_138")
        self.horizontalLayout_138.setContentsMargins(-1, -1, 0, -1)
        self.form_critic_prop_lag = QCheckBox(self.frame_135)
        self.form_critic_prop_lag.setObjectName(u"form_critic_prop_lag")

        self.horizontalLayout_138.addWidget(self.form_critic_prop_lag)

        self.form_critic_prop_htf_kir = QCheckBox(self.frame_135)
        self.form_critic_prop_htf_kir.setObjectName(u"form_critic_prop_htf_kir")

        self.horizontalLayout_138.addWidget(self.form_critic_prop_htf_kir)

        self.form_critic_prop_htf = QCheckBox(self.frame_135)
        self.form_critic_prop_htf.setObjectName(u"form_critic_prop_htf")

        self.horizontalLayout_138.addWidget(self.form_critic_prop_htf)

        self.form_critic_prop_gtf = QCheckBox(self.frame_135)
        self.form_critic_prop_gtf.setObjectName(u"form_critic_prop_gtf")

        self.horizontalLayout_138.addWidget(self.form_critic_prop_gtf)

        self.form_critic_prop_gtf_kir = QCheckBox(self.frame_135)
        self.form_critic_prop_gtf_kir.setObjectName(u"form_critic_prop_gtf_kir")

        self.horizontalLayout_138.addWidget(self.form_critic_prop_gtf_kir)


        self.verticalLayout_86.addWidget(self.frame_135)

        self.frame_136 = QFrame(self.tab_47)
        self.frame_136.setObjectName(u"frame_136")
        self.frame_136.setMinimumSize(QSize(0, 0))
        self.frame_136.setFrameShape(QFrame.NoFrame)
        self.frame_136.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_86 = QHBoxLayout(self.frame_136)
        self.horizontalLayout_86.setObjectName(u"horizontalLayout_86")
        self.horizontalLayout_86.setContentsMargins(-1, -1, 0, -1)
        self.form_critic_prop_lol_kir = QCheckBox(self.frame_136)
        self.form_critic_prop_lol_kir.setObjectName(u"form_critic_prop_lol_kir")

        self.horizontalLayout_86.addWidget(self.form_critic_prop_lol_kir)

        self.form_critic_prop_rdg = QCheckBox(self.frame_136)
        self.form_critic_prop_rdg.setObjectName(u"form_critic_prop_rdg")

        self.horizontalLayout_86.addWidget(self.form_critic_prop_rdg)

        self.form_critic_prop_vtf = QCheckBox(self.frame_136)
        self.form_critic_prop_vtf.setObjectName(u"form_critic_prop_vtf")

        self.horizontalLayout_86.addWidget(self.form_critic_prop_vtf)

        self.form_critic_prop_vtf_kir = QCheckBox(self.frame_136)
        self.form_critic_prop_vtf_kir.setObjectName(u"form_critic_prop_vtf_kir")

        self.horizontalLayout_86.addWidget(self.form_critic_prop_vtf_kir)


        self.verticalLayout_86.addWidget(self.frame_136)

        self.verticalSpacer_28 = QSpacerItem(20, 344, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_86.addItem(self.verticalSpacer_28)

        self.tabWidget_14.addTab(self.tab_47, "")
        self.tab_49 = QWidget()
        self.tab_49.setObjectName(u"tab_49")
        self.addLinesToCriticFile = QCheckBox(self.tab_49)
        self.addLinesToCriticFile.setObjectName(u"addLinesToCriticFile")
        self.addLinesToCriticFile.setGeometry(QRect(10, 10, 311, 20))
        self.tabWidget_14.addTab(self.tab_49, "")

        self.verticalLayout_69.addWidget(self.tabWidget_14)

        self.frame_115 = QFrame(self.tab_53)
        self.frame_115.setObjectName(u"frame_115")
        self.frame_115.setMinimumSize(QSize(0, 0))
        self.frame_115.setFrameShape(QFrame.NoFrame)
        self.frame_115.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_141 = QHBoxLayout(self.frame_115)
        self.horizontalLayout_141.setObjectName(u"horizontalLayout_141")
        self.horizontalSpacer_77 = QSpacerItem(95, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_141.addItem(self.horizontalSpacer_77)

        self.FormCreateCriFile = QPushButton(self.frame_115)
        self.FormCreateCriFile.setObjectName(u"FormCreateCriFile")

        self.horizontalLayout_141.addWidget(self.FormCreateCriFile)

        self.horizontalSpacer_97 = QSpacerItem(95, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_141.addItem(self.horizontalSpacer_97)


        self.verticalLayout_69.addWidget(self.frame_115)

        self.tabWidget_15.addTab(self.tab_53, "")
        self.tab_52 = QWidget()
        self.tab_52.setObjectName(u"tab_52")
        self.verticalLayout_106 = QVBoxLayout(self.tab_52)
        self.verticalLayout_106.setObjectName(u"verticalLayout_106")
        self.frame_125 = QFrame(self.tab_52)
        self.frame_125.setObjectName(u"frame_125")
        self.frame_125.setMinimumSize(QSize(0, 0))
        self.frame_125.setFrameShape(QFrame.NoFrame)
        self.frame_125.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_130 = QHBoxLayout(self.frame_125)
        self.horizontalLayout_130.setObjectName(u"horizontalLayout_130")
        self.frame_126 = QFrame(self.frame_125)
        self.frame_126.setObjectName(u"frame_126")
        self.frame_126.setMinimumSize(QSize(0, 0))
        self.frame_126.setFrameShape(QFrame.NoFrame)
        self.frame_126.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_129 = QHBoxLayout(self.frame_126)
        self.horizontalLayout_129.setObjectName(u"horizontalLayout_129")
        self.radio_with_cp = QRadioButton(self.frame_126)
        self.radio_with_cp.setObjectName(u"radio_with_cp")
        self.radio_with_cp.setChecked(True)

        self.horizontalLayout_129.addWidget(self.radio_with_cp)

        self.radio_without_cp = QRadioButton(self.frame_126)
        self.radio_without_cp.setObjectName(u"radio_without_cp")

        self.horizontalLayout_129.addWidget(self.radio_without_cp)


        self.horizontalLayout_130.addWidget(self.frame_126)

        self.label_93 = QLabel(self.frame_125)
        self.label_93.setObjectName(u"label_93")

        self.horizontalLayout_130.addWidget(self.label_93)


        self.verticalLayout_106.addWidget(self.frame_125)

        self.frame_139 = QFrame(self.tab_52)
        self.frame_139.setObjectName(u"frame_139")
        self.frame_139.setFrameShape(QFrame.NoFrame)
        self.frame_139.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_142 = QHBoxLayout(self.frame_139)
        self.horizontalLayout_142.setObjectName(u"horizontalLayout_142")
        self.horizontalSpacer_98 = QSpacerItem(93, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_142.addItem(self.horizontalSpacer_98)

        self.FormCreateCriXYZFile = QPushButton(self.frame_139)
        self.FormCreateCriXYZFile.setObjectName(u"FormCreateCriXYZFile")

        self.horizontalLayout_142.addWidget(self.FormCreateCriXYZFile)

        self.horizontalSpacer_99 = QSpacerItem(93, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_142.addItem(self.horizontalSpacer_99)


        self.verticalLayout_106.addWidget(self.frame_139)

        self.frame = QFrame(self.tab_52)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(103, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.save_all_data = QPushButton(self.frame)
        self.save_all_data.setObjectName(u"save_all_data")

        self.horizontalLayout_4.addWidget(self.save_all_data)

        self.horizontalSpacer_2 = QSpacerItem(103, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_106.addWidget(self.frame)

        self.verticalSpacer_31 = QSpacerItem(20, 399, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_106.addItem(self.verticalSpacer_31)

        self.tabWidget_15.addTab(self.tab_52, "")

        self.verticalLayout_11.addWidget(self.tabWidget_15)


        self.verticalLayout_26.addWidget(self.groupBox_15)


        self.horizontalLayout_6.addWidget(self.frame_16)


        self.verticalLayout_12.addWidget(self.groupBox_5)

        self.tabWidget.addTab(self.tab_51, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_25 = QVBoxLayout(self.tab_3)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.groupBox_7 = QGroupBox(self.tab_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.frame_9 = QFrame(self.groupBox_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.min_rho_for_cps = QDoubleSpinBox(self.frame_9)
        self.min_rho_for_cps.setObjectName(u"min_rho_for_cps")
        self.min_rho_for_cps.setDecimals(6)
        self.min_rho_for_cps.setMinimum(0.000000000000000)
        self.min_rho_for_cps.setMaximum(10000.000000000000000)
        self.min_rho_for_cps.setSingleStep(0.000100000000000)
        self.min_rho_for_cps.setValue(0.000100000000000)

        self.horizontalLayout_12.addWidget(self.min_rho_for_cps)

        self.hide_cps_min_rho = QPushButton(self.frame_9)
        self.hide_cps_min_rho.setObjectName(u"hide_cps_min_rho")

        self.horizontalLayout_12.addWidget(self.hide_cps_min_rho)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)


        self.verticalLayout_24.addWidget(self.frame_9)


        self.verticalLayout_25.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_14)

        self.hide_cps_eq_atoms = QPushButton(self.groupBox_8)
        self.hide_cps_eq_atoms.setObjectName(u"hide_cps_eq_atoms")

        self.horizontalLayout_10.addWidget(self.hide_cps_eq_atoms)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_13)


        self.verticalLayout_25.addWidget(self.groupBox_8)

        self.frame_6 = QFrame(self.tab_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 0))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_9 = QSpacerItem(131, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)

        self.cancel_cps_filters = QPushButton(self.frame_6)
        self.cancel_cps_filters.setObjectName(u"cancel_cps_filters")

        self.horizontalLayout_11.addWidget(self.cancel_cps_filters)

        self.horizontalSpacer_12 = QSpacerItem(131, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_12)


        self.verticalLayout_25.addWidget(self.frame_6)

        self.verticalSpacer_3 = QSpacerItem(20, 563, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_10 = QVBoxLayout(self.tab_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.atom_and_cp_properties_text = QTextBrowser(self.tab_4)
        self.atom_and_cp_properties_text.setObjectName(u"atom_and_cp_properties_text")

        self.verticalLayout_10.addWidget(self.atom_and_cp_properties_text)

        self.tabWidget.addTab(self.tab_4, "")
        self.FormTabActions = QWidget()
        self.FormTabActions.setObjectName(u"FormTabActions")
        self.verticalLayout_2 = QVBoxLayout(self.FormTabActions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.FormTabActions)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_22 = QFrame(self.groupBox_2)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 0, -1, 0)
        self.label_8 = QLabel(self.frame_22)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_26.addWidget(self.label_8)

        self.FormActionsPreComboAtomsList = QComboBox(self.frame_22)
        self.FormActionsPreComboAtomsList.setObjectName(u"FormActionsPreComboAtomsList")

        self.horizontalLayout_26.addWidget(self.FormActionsPreComboAtomsList)


        self.verticalLayout_5.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.groupBox_2)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, 0)
        self.label_24 = QLabel(self.frame_23)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_27.addWidget(self.label_24)

        self.FormActionsPreSpinAtomsCoordX = QDoubleSpinBox(self.frame_23)
        self.FormActionsPreSpinAtomsCoordX.setObjectName(u"FormActionsPreSpinAtomsCoordX")
        self.FormActionsPreSpinAtomsCoordX.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordX.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordX.setMaximum(999.990000000000009)

        self.horizontalLayout_27.addWidget(self.FormActionsPreSpinAtomsCoordX)

        self.horizontalSpacer_5 = QSpacerItem(235, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_5)


        self.verticalLayout_5.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.groupBox_2)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, 0, -1, 0)
        self.label_25 = QLabel(self.frame_24)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_29.addWidget(self.label_25)

        self.FormActionsPreSpinAtomsCoordY = QDoubleSpinBox(self.frame_24)
        self.FormActionsPreSpinAtomsCoordY.setObjectName(u"FormActionsPreSpinAtomsCoordY")
        self.FormActionsPreSpinAtomsCoordY.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordY.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordY.setMaximum(999.990000000000009)

        self.horizontalLayout_29.addWidget(self.FormActionsPreSpinAtomsCoordY)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_20)


        self.verticalLayout_5.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.groupBox_2)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, 0, -1, 0)
        self.label_26 = QLabel(self.frame_25)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_28.addWidget(self.label_26)

        self.FormActionsPreSpinAtomsCoordZ = QDoubleSpinBox(self.frame_25)
        self.FormActionsPreSpinAtomsCoordZ.setObjectName(u"FormActionsPreSpinAtomsCoordZ")
        self.FormActionsPreSpinAtomsCoordZ.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordZ.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordZ.setMaximum(999.990000000000009)

        self.horizontalLayout_28.addWidget(self.FormActionsPreSpinAtomsCoordZ)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_21)


        self.verticalLayout_5.addWidget(self.frame_25)

        self.frame_29 = QFrame(self.groupBox_2)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 50))
        self.frame_29.setMaximumSize(QSize(16777215, 50))
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, 0, -1, 0)
        self.FormActionsPreButDeleteAtom = QPushButton(self.frame_29)
        self.FormActionsPreButDeleteAtom.setObjectName(u"FormActionsPreButDeleteAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButDeleteAtom)

        self.FormActionsPreButModifyAtom = QPushButton(self.frame_29)
        self.FormActionsPreButModifyAtom.setObjectName(u"FormActionsPreButModifyAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButModifyAtom)

        self.FormActionsPreButAddAtom = QPushButton(self.frame_29)
        self.FormActionsPreButAddAtom.setObjectName(u"FormActionsPreButAddAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButAddAtom)


        self.verticalLayout_5.addWidget(self.frame_29)

        self.groupBox_18 = QGroupBox(self.groupBox_2)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setMinimumSize(QSize(0, 0))
        self.verticalLayout_28 = QVBoxLayout(self.groupBox_18)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(-1, 0, -1, 0)
        self.frame_19 = QFrame(self.groupBox_18)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 0, -1, 0)
        self.atom_translation_1_plus = QPushButton(self.frame_19)
        self.atom_translation_1_plus.setObjectName(u"atom_translation_1_plus")

        self.horizontalLayout_22.addWidget(self.atom_translation_1_plus)

        self.atom_translation_2_plus = QPushButton(self.frame_19)
        self.atom_translation_2_plus.setObjectName(u"atom_translation_2_plus")

        self.horizontalLayout_22.addWidget(self.atom_translation_2_plus)

        self.atom_translation_3_plus = QPushButton(self.frame_19)
        self.atom_translation_3_plus.setObjectName(u"atom_translation_3_plus")

        self.horizontalLayout_22.addWidget(self.atom_translation_3_plus)


        self.verticalLayout_28.addWidget(self.frame_19)

        self.frame_21 = QFrame(self.groupBox_18)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.atom_translation_1_minus = QPushButton(self.frame_21)
        self.atom_translation_1_minus.setObjectName(u"atom_translation_1_minus")

        self.horizontalLayout_24.addWidget(self.atom_translation_1_minus)

        self.atom_translation_2_minus = QPushButton(self.frame_21)
        self.atom_translation_2_minus.setObjectName(u"atom_translation_2_minus")

        self.horizontalLayout_24.addWidget(self.atom_translation_2_minus)

        self.atom_translation_3_minus = QPushButton(self.frame_21)
        self.atom_translation_3_minus.setObjectName(u"atom_translation_3_minus")

        self.horizontalLayout_24.addWidget(self.atom_translation_3_minus)


        self.verticalLayout_28.addWidget(self.frame_21)


        self.verticalLayout_5.addWidget(self.groupBox_18)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_12 = QGroupBox(self.FormTabActions)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_13 = QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_15 = QSpacerItem(131, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_15)

        self.additional_atoms_delete = QPushButton(self.groupBox_12)
        self.additional_atoms_delete.setObjectName(u"additional_atoms_delete")

        self.horizontalLayout_13.addWidget(self.additional_atoms_delete)

        self.horizontalSpacer_16 = QSpacerItem(131, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_16)


        self.verticalLayout_2.addWidget(self.groupBox_12)

        self.groupBox_3 = QGroupBox(self.FormTabActions)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_57 = QFrame(self.groupBox_3)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_57.setFrameShape(QFrame.NoFrame)
        self.frame_57.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_63 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalLayout_63.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditA1 = QDoubleSpinBox(self.frame_57)
        self.FormModifyCellEditA1.setObjectName(u"FormModifyCellEditA1")
        self.FormModifyCellEditA1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA1.setDecimals(6)
        self.FormModifyCellEditA1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA1.setMaximum(999.000000000000000)

        self.horizontalLayout_63.addWidget(self.FormModifyCellEditA1)

        self.FormModifyCellEditA2 = QDoubleSpinBox(self.frame_57)
        self.FormModifyCellEditA2.setObjectName(u"FormModifyCellEditA2")
        self.FormModifyCellEditA2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA2.setDecimals(6)
        self.FormModifyCellEditA2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA2.setMaximum(999.000000000000000)

        self.horizontalLayout_63.addWidget(self.FormModifyCellEditA2)

        self.FormModifyCellEditA3 = QDoubleSpinBox(self.frame_57)
        self.FormModifyCellEditA3.setObjectName(u"FormModifyCellEditA3")
        self.FormModifyCellEditA3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA3.setDecimals(6)
        self.FormModifyCellEditA3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA3.setMaximum(999.000000000000000)

        self.horizontalLayout_63.addWidget(self.FormModifyCellEditA3)


        self.verticalLayout_6.addWidget(self.frame_57)

        self.frame_55 = QFrame(self.groupBox_3)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_55.setFrameShape(QFrame.NoFrame)
        self.frame_55.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_55)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.horizontalLayout_59.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditB1 = QDoubleSpinBox(self.frame_55)
        self.FormModifyCellEditB1.setObjectName(u"FormModifyCellEditB1")
        self.FormModifyCellEditB1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditB1.setDecimals(6)
        self.FormModifyCellEditB1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB1.setMaximum(999.000000000000000)

        self.horizontalLayout_59.addWidget(self.FormModifyCellEditB1)

        self.FormModifyCellEditB2 = QDoubleSpinBox(self.frame_55)
        self.FormModifyCellEditB2.setObjectName(u"FormModifyCellEditB2")
        self.FormModifyCellEditB2.setDecimals(6)
        self.FormModifyCellEditB2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB2.setMaximum(999.000000000000000)

        self.horizontalLayout_59.addWidget(self.FormModifyCellEditB2)

        self.FormModifyCellEditB3 = QDoubleSpinBox(self.frame_55)
        self.FormModifyCellEditB3.setObjectName(u"FormModifyCellEditB3")
        self.FormModifyCellEditB3.setDecimals(6)
        self.FormModifyCellEditB3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB3.setMaximum(999.000000000000000)

        self.horizontalLayout_59.addWidget(self.FormModifyCellEditB3)


        self.verticalLayout_6.addWidget(self.frame_55)

        self.frame_56 = QFrame(self.groupBox_3)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_56.setFrameShape(QFrame.NoFrame)
        self.frame_56.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.horizontalLayout_61.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditC1 = QDoubleSpinBox(self.frame_56)
        self.FormModifyCellEditC1.setObjectName(u"FormModifyCellEditC1")
        self.FormModifyCellEditC1.setDecimals(6)
        self.FormModifyCellEditC1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC1.setMaximum(999.000000000000000)

        self.horizontalLayout_61.addWidget(self.FormModifyCellEditC1)

        self.FormModifyCellEditC2 = QDoubleSpinBox(self.frame_56)
        self.FormModifyCellEditC2.setObjectName(u"FormModifyCellEditC2")
        self.FormModifyCellEditC2.setDecimals(6)
        self.FormModifyCellEditC2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC2.setMaximum(999.000000000000000)

        self.horizontalLayout_61.addWidget(self.FormModifyCellEditC2)

        self.FormModifyCellEditC3 = QDoubleSpinBox(self.frame_56)
        self.FormModifyCellEditC3.setObjectName(u"FormModifyCellEditC3")
        self.FormModifyCellEditC3.setDecimals(6)
        self.FormModifyCellEditC3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC3.setMaximum(999.000000000000000)

        self.horizontalLayout_61.addWidget(self.FormModifyCellEditC3)


        self.verticalLayout_6.addWidget(self.frame_56)

        self.frame_54 = QFrame(self.groupBox_3)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setFrameShape(QFrame.NoFrame)
        self.frame_54.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_54)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.horizontalSpacer_25 = QSpacerItem(92, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_58.addItem(self.horizontalSpacer_25)

        self.FormModifyCellButton = QPushButton(self.frame_54)
        self.FormModifyCellButton.setObjectName(u"FormModifyCellButton")

        self.horizontalLayout_58.addWidget(self.FormModifyCellButton)

        self.horizontalSpacer_11 = QSpacerItem(91, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_58.addItem(self.horizontalSpacer_11)


        self.verticalLayout_6.addWidget(self.frame_54)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.FormTabActions)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_116 = QFrame(self.groupBox_4)
        self.frame_116.setObjectName(u"frame_116")
        self.frame_116.setMinimumSize(QSize(0, 0))
        self.frame_116.setFrameShape(QFrame.NoFrame)
        self.frame_116.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_116)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.horizontalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.FormModifyGoPositive = QPushButton(self.frame_116)
        self.FormModifyGoPositive.setObjectName(u"FormModifyGoPositive")

        self.horizontalLayout_50.addWidget(self.FormModifyGoPositive)

        self.FormModifyGoToCell = QPushButton(self.frame_116)
        self.FormModifyGoToCell.setObjectName(u"FormModifyGoToCell")

        self.horizontalLayout_50.addWidget(self.FormModifyGoToCell)

        self.modify_center_to_zero = QPushButton(self.frame_116)
        self.modify_center_to_zero.setObjectName(u"modify_center_to_zero")

        self.horizontalLayout_50.addWidget(self.modify_center_to_zero)


        self.verticalLayout_7.addWidget(self.frame_116)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_49 = QGroupBox(self.FormTabActions)
        self.groupBox_49.setObjectName(u"groupBox_49")
        self.groupBox_49.setMinimumSize(QSize(0, 0))
        self.groupBox_49.setSizeIncrement(QSize(0, 0))
        self.verticalLayout_70 = QVBoxLayout(self.groupBox_49)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.frame_117 = QFrame(self.groupBox_49)
        self.frame_117.setObjectName(u"frame_117")
        self.frame_117.setMinimumSize(QSize(0, 0))
        self.frame_117.setFrameShape(QFrame.NoFrame)
        self.frame_117.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_117 = QHBoxLayout(self.frame_117)
        self.horizontalLayout_117.setObjectName(u"horizontalLayout_117")
        self.horizontalLayout_117.setContentsMargins(0, 0, 0, 0)
        self.x_circular_shift_step = QDoubleSpinBox(self.frame_117)
        self.x_circular_shift_step.setObjectName(u"x_circular_shift_step")
        self.x_circular_shift_step.setMinimum(-99.989999999999995)

        self.horizontalLayout_117.addWidget(self.x_circular_shift_step)

        self.x_circular_shift = QPushButton(self.frame_117)
        self.x_circular_shift.setObjectName(u"x_circular_shift")

        self.horizontalLayout_117.addWidget(self.x_circular_shift)

        self.horizontalSpacer_100 = QSpacerItem(157, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_117.addItem(self.horizontalSpacer_100)


        self.verticalLayout_70.addWidget(self.frame_117)

        self.frame_118 = QFrame(self.groupBox_49)
        self.frame_118.setObjectName(u"frame_118")
        self.frame_118.setMinimumSize(QSize(0, 0))
        self.frame_118.setFrameShape(QFrame.NoFrame)
        self.frame_118.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_165 = QHBoxLayout(self.frame_118)
        self.horizontalLayout_165.setObjectName(u"horizontalLayout_165")
        self.horizontalLayout_165.setContentsMargins(0, 0, 0, 0)
        self.y_circular_shift_step = QDoubleSpinBox(self.frame_118)
        self.y_circular_shift_step.setObjectName(u"y_circular_shift_step")
        self.y_circular_shift_step.setMinimum(-99.989999999999995)

        self.horizontalLayout_165.addWidget(self.y_circular_shift_step)

        self.y_circular_shift = QPushButton(self.frame_118)
        self.y_circular_shift.setObjectName(u"y_circular_shift")

        self.horizontalLayout_165.addWidget(self.y_circular_shift)

        self.horizontalSpacer_117 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_165.addItem(self.horizontalSpacer_117)


        self.verticalLayout_70.addWidget(self.frame_118)

        self.frame_170 = QFrame(self.groupBox_49)
        self.frame_170.setObjectName(u"frame_170")
        self.frame_170.setMinimumSize(QSize(0, 0))
        self.frame_170.setFrameShape(QFrame.NoFrame)
        self.frame_170.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_166 = QHBoxLayout(self.frame_170)
        self.horizontalLayout_166.setObjectName(u"horizontalLayout_166")
        self.horizontalLayout_166.setContentsMargins(0, 0, 0, 0)
        self.z_circular_shift_step = QDoubleSpinBox(self.frame_170)
        self.z_circular_shift_step.setObjectName(u"z_circular_shift_step")
        self.z_circular_shift_step.setMinimum(-99.989999999999995)

        self.horizontalLayout_166.addWidget(self.z_circular_shift_step)

        self.z_circular_shift = QPushButton(self.frame_170)
        self.z_circular_shift.setObjectName(u"z_circular_shift")

        self.horizontalLayout_166.addWidget(self.z_circular_shift)

        self.horizontalSpacer_118 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_166.addItem(self.horizontalSpacer_118)


        self.verticalLayout_70.addWidget(self.frame_170)


        self.verticalLayout_2.addWidget(self.groupBox_49)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.FormTabActions, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_8 = QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_60 = QFrame(self.tab_5)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setFrameShape(QFrame.NoFrame)
        self.frame_60.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_22)

        self.FormActionsPostButGetBonds = QPushButton(self.frame_60)
        self.FormActionsPostButGetBonds.setObjectName(u"FormActionsPostButGetBonds")

        self.horizontalLayout_51.addWidget(self.FormActionsPostButGetBonds)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_23)


        self.verticalLayout_8.addWidget(self.frame_60)

        self.FormActionsPosTableBonds = QTableWidget(self.tab_5)
        self.FormActionsPosTableBonds.setObjectName(u"FormActionsPosTableBonds")

        self.verticalLayout_8.addWidget(self.FormActionsPosTableBonds)

        self.frame_8 = QFrame(self.tab_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 80))
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_8)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.FormActionsPostComboBonds = QComboBox(self.frame_8)
        self.FormActionsPostComboBonds.setObjectName(u"FormActionsPostComboBonds")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.FormActionsPostComboBonds.sizePolicy().hasHeightForWidth())
        self.FormActionsPostComboBonds.setSizePolicy(sizePolicy2)

        self.verticalLayout_30.addWidget(self.FormActionsPostComboBonds)

        self.FormActionsPostLabelMeanBond = QLabel(self.frame_8)
        self.FormActionsPostLabelMeanBond.setObjectName(u"FormActionsPostLabelMeanBond")

        self.verticalLayout_30.addWidget(self.FormActionsPostLabelMeanBond)


        self.verticalLayout_8.addWidget(self.frame_8)

        self.groupBox_20 = QGroupBox(self.tab_5)
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


        self.verticalLayout_8.addWidget(self.groupBox_20)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_15 = QVBoxLayout(self.tab)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.ActivateFragmentSelectionModeCheckBox = QCheckBox(self.tab)
        self.ActivateFragmentSelectionModeCheckBox.setObjectName(u"ActivateFragmentSelectionModeCheckBox")

        self.verticalLayout_15.addWidget(self.ActivateFragmentSelectionModeCheckBox)

        self.groupBox_21 = QGroupBox(self.tab)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setMinimumSize(QSize(0, 60))
        self.horizontalLayout_72 = QHBoxLayout(self.groupBox_21)
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.label_52 = QLabel(self.groupBox_21)
        self.label_52.setObjectName(u"label_52")

        self.horizontalLayout_72.addWidget(self.label_52)

        self.ActivateFragmentSelectionTransp = QDoubleSpinBox(self.groupBox_21)
        self.ActivateFragmentSelectionTransp.setObjectName(u"ActivateFragmentSelectionTransp")
        self.ActivateFragmentSelectionTransp.setMaximum(1.000000000000000)
        self.ActivateFragmentSelectionTransp.setSingleStep(0.100000000000000)
        self.ActivateFragmentSelectionTransp.setValue(0.700000000000000)

        self.horizontalLayout_72.addWidget(self.ActivateFragmentSelectionTransp)

        self.horizontalSpacer_47 = QSpacerItem(228, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_72.addItem(self.horizontalSpacer_47)


        self.verticalLayout_15.addWidget(self.groupBox_21)

        self.AtomsInSelectedFragment = QListWidget(self.tab)
        self.AtomsInSelectedFragment.setObjectName(u"AtomsInSelectedFragment")

        self.verticalLayout_15.addWidget(self.AtomsInSelectedFragment)

        self.frame_61 = QFrame(self.tab)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setFrameShape(QFrame.NoFrame)
        self.frame_61.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_53 = QHBoxLayout(self.frame_61)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_55 = QLabel(self.frame_61)
        self.label_55.setObjectName(u"label_55")

        self.horizontalLayout_53.addWidget(self.label_55)

        self.xminborder = QDoubleSpinBox(self.frame_61)
        self.xminborder.setObjectName(u"xminborder")
        self.xminborder.setMinimum(-99.989999999999995)

        self.horizontalLayout_53.addWidget(self.xminborder)

        self.label_57 = QLabel(self.frame_61)
        self.label_57.setObjectName(u"label_57")

        self.horizontalLayout_53.addWidget(self.label_57)

        self.xmaxborder = QDoubleSpinBox(self.frame_61)
        self.xmaxborder.setObjectName(u"xmaxborder")
        self.xmaxborder.setMinimum(-99.989999999999995)
        self.xmaxborder.setValue(2.000000000000000)

        self.horizontalLayout_53.addWidget(self.xmaxborder)

        self.changeFragment1StatusByX = QPushButton(self.frame_61)
        self.changeFragment1StatusByX.setObjectName(u"changeFragment1StatusByX")
        self.changeFragment1StatusByX.setEnabled(False)

        self.horizontalLayout_53.addWidget(self.changeFragment1StatusByX)


        self.verticalLayout_15.addWidget(self.frame_61)

        self.frame_62 = QFrame(self.tab)
        self.frame_62.setObjectName(u"frame_62")
        self.frame_62.setFrameShape(QFrame.NoFrame)
        self.frame_62.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_54 = QHBoxLayout(self.frame_62)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.label_58 = QLabel(self.frame_62)
        self.label_58.setObjectName(u"label_58")

        self.horizontalLayout_54.addWidget(self.label_58)

        self.yminborder = QDoubleSpinBox(self.frame_62)
        self.yminborder.setObjectName(u"yminborder")
        self.yminborder.setMinimum(-99.989999999999995)

        self.horizontalLayout_54.addWidget(self.yminborder)

        self.label_59 = QLabel(self.frame_62)
        self.label_59.setObjectName(u"label_59")

        self.horizontalLayout_54.addWidget(self.label_59)

        self.ymaxborder = QDoubleSpinBox(self.frame_62)
        self.ymaxborder.setObjectName(u"ymaxborder")
        self.ymaxborder.setMinimum(-99.989999999999995)
        self.ymaxborder.setValue(2.000000000000000)

        self.horizontalLayout_54.addWidget(self.ymaxborder)

        self.changeFragment1StatusByY = QPushButton(self.frame_62)
        self.changeFragment1StatusByY.setObjectName(u"changeFragment1StatusByY")
        self.changeFragment1StatusByY.setEnabled(False)

        self.horizontalLayout_54.addWidget(self.changeFragment1StatusByY)


        self.verticalLayout_15.addWidget(self.frame_62)

        self.frame_63 = QFrame(self.tab)
        self.frame_63.setObjectName(u"frame_63")
        self.frame_63.setFrameShape(QFrame.NoFrame)
        self.frame_63.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_63)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.label_60 = QLabel(self.frame_63)
        self.label_60.setObjectName(u"label_60")

        self.horizontalLayout_55.addWidget(self.label_60)

        self.zminborder = QDoubleSpinBox(self.frame_63)
        self.zminborder.setObjectName(u"zminborder")
        self.zminborder.setMinimum(-99.989999999999995)

        self.horizontalLayout_55.addWidget(self.zminborder)

        self.label_61 = QLabel(self.frame_63)
        self.label_61.setObjectName(u"label_61")

        self.horizontalLayout_55.addWidget(self.label_61)

        self.zmaxborder = QDoubleSpinBox(self.frame_63)
        self.zmaxborder.setObjectName(u"zmaxborder")
        self.zmaxborder.setMinimum(-99.989999999999995)
        self.zmaxborder.setValue(2.000000000000000)

        self.horizontalLayout_55.addWidget(self.zmaxborder)

        self.changeFragment1StatusByZ = QPushButton(self.frame_63)
        self.changeFragment1StatusByZ.setObjectName(u"changeFragment1StatusByZ")
        self.changeFragment1StatusByZ.setEnabled(False)

        self.horizontalLayout_55.addWidget(self.changeFragment1StatusByZ)


        self.verticalLayout_15.addWidget(self.frame_63)

        self.frame_64 = QFrame(self.tab)
        self.frame_64.setObjectName(u"frame_64")
        self.frame_64.setMinimumSize(QSize(0, 40))
        self.frame_64.setFrameShape(QFrame.NoFrame)
        self.frame_64.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_64)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_28 = QSpacerItem(107, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_28)

        self.fragment1Clear = QPushButton(self.frame_64)
        self.fragment1Clear.setObjectName(u"fragment1Clear")
        self.fragment1Clear.setEnabled(False)

        self.horizontalLayout_56.addWidget(self.fragment1Clear)

        self.horizontalSpacer_29 = QSpacerItem(106, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_29)


        self.verticalLayout_15.addWidget(self.frame_64)

        self.tabWidget.addTab(self.tab, "")
        self.tab_29 = QWidget()
        self.tab_29.setObjectName(u"tab_29")
        self.verticalLayout_23 = QVBoxLayout(self.tab_29)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.tabWidget_9 = QTabWidget(self.tab_29)
        self.tabWidget_9.setObjectName(u"tabWidget_9")
        self.tab_32 = QWidget()
        self.tab_32.setObjectName(u"tab_32")
        self.verticalLayout_22 = QVBoxLayout(self.tab_32)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.FormSettingsViewCheckShowAtoms = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAtoms.setObjectName(u"FormSettingsViewCheckShowAtoms")
        self.FormSettingsViewCheckShowAtoms.setEnabled(True)

        self.verticalLayout_22.addWidget(self.FormSettingsViewCheckShowAtoms)

        self.FormSettingsViewCheckShowBox = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowBox.setObjectName(u"FormSettingsViewCheckShowBox")
        self.FormSettingsViewCheckShowBox.setStyleSheet(u"")

        self.verticalLayout_22.addWidget(self.FormSettingsViewCheckShowBox)

        self.FormSettingsViewCheckShowAtomNumber = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAtomNumber.setObjectName(u"FormSettingsViewCheckShowAtomNumber")
        self.FormSettingsViewCheckShowAtomNumber.setEnabled(True)

        self.verticalLayout_22.addWidget(self.FormSettingsViewCheckShowAtomNumber)

        self.FormSettingsViewCheckShowAxes = QCheckBox(self.tab_32)
        self.FormSettingsViewCheckShowAxes.setObjectName(u"FormSettingsViewCheckShowAxes")

        self.verticalLayout_22.addWidget(self.FormSettingsViewCheckShowAxes)

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

        self.spin_perspective_angle = QSpinBox(self.frame_131)
        self.spin_perspective_angle.setObjectName(u"spin_perspective_angle")
        self.spin_perspective_angle.setMinimumSize(QSize(120, 24))
        self.spin_perspective_angle.setMaximumSize(QSize(120, 24))
        self.spin_perspective_angle.setMaximum(90)
        self.spin_perspective_angle.setValue(45)

        self.horizontalLayout_100.addWidget(self.spin_perspective_angle)

        self.horizontalSpacer_112 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_100.addItem(self.horizontalSpacer_112)


        self.verticalLayout_22.addWidget(self.frame_131)

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
        self.horizontalLayout_116.setContentsMargins(0, 0, -1, 0)
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
        self.horizontalLayout_110.setContentsMargins(0, 0, 0, 0)
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


        self.verticalLayout_22.addWidget(self.groupBox)

        self.groupBox_6 = QGroupBox(self.tab_32)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 0))
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.frame_3 = QFrame(self.groupBox_6)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, -1, 0, 0)
        self.show_ncp = QCheckBox(self.frame_3)
        self.show_ncp.setObjectName(u"show_ncp")
        self.show_ncp.setChecked(False)

        self.horizontalLayout_7.addWidget(self.show_ncp)

        self.show_bcp = QCheckBox(self.frame_3)
        self.show_bcp.setObjectName(u"show_bcp")
        self.show_bcp.setChecked(True)

        self.horizontalLayout_7.addWidget(self.show_bcp)

        self.show_nnatr = QCheckBox(self.frame_3)
        self.show_nnatr.setObjectName(u"show_nnatr")
        self.show_nnatr.setChecked(False)

        self.horizontalLayout_7.addWidget(self.show_nnatr)

        self.show_rcp = QCheckBox(self.frame_3)
        self.show_rcp.setObjectName(u"show_rcp")
        self.show_rcp.setChecked(False)

        self.horizontalLayout_7.addWidget(self.show_rcp)

        self.show_ccp = QCheckBox(self.frame_3)
        self.show_ccp.setObjectName(u"show_ccp")
        self.show_ccp.setChecked(False)

        self.horizontalLayout_7.addWidget(self.show_ccp)


        self.verticalLayout_9.addWidget(self.frame_3)


        self.verticalLayout_22.addWidget(self.groupBox_6)

        self.groupBox_11 = QGroupBox(self.tab_32)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.frame_4 = QFrame(self.groupBox_11)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.show_bond_path = QCheckBox(self.frame_4)
        self.show_bond_path.setObjectName(u"show_bond_path")
        self.show_bond_path.setChecked(True)

        self.horizontalLayout_8.addWidget(self.show_bond_path)

        self.show_bp_if_avail = QRadioButton(self.frame_4)
        self.show_bp_if_avail.setObjectName(u"show_bp_if_avail")
        self.show_bp_if_avail.setChecked(True)

        self.horizontalLayout_8.addWidget(self.show_bp_if_avail)

        self.horizontalSpacer_7 = QSpacerItem(281, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.radioButton_2 = QRadioButton(self.frame_4)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_8.addWidget(self.radioButton_2)


        self.verticalLayout_18.addWidget(self.frame_4)

        self.frame_69 = QFrame(self.groupBox_11)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setMinimumSize(QSize(200, 0))
        self.frame_69.setFrameShape(QFrame.NoFrame)
        self.frame_69.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_69)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.frame_69)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_62.addWidget(self.label_23)

        self.bond_path_width = QSpinBox(self.frame_69)
        self.bond_path_width.setObjectName(u"bond_path_width")
        self.bond_path_width.setMinimumSize(QSize(120, 24))
        self.bond_path_width.setMaximumSize(QSize(120, 24))
        self.bond_path_width.setValue(20)

        self.horizontalLayout_62.addWidget(self.bond_path_width)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_31)


        self.verticalLayout_18.addWidget(self.frame_69)

        self.frame_160 = QFrame(self.groupBox_11)
        self.frame_160.setObjectName(u"frame_160")
        self.frame_160.setFrameShape(QFrame.NoFrame)
        self.frame_160.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_178 = QHBoxLayout(self.frame_160)
        self.horizontalLayout_178.setObjectName(u"horizontalLayout_178")
        self.horizontalLayout_178.setContentsMargins(0, 0, 0, 0)
        self.show_bcp_text = QCheckBox(self.frame_160)
        self.show_bcp_text.setObjectName(u"show_bcp_text")

        self.horizontalLayout_178.addWidget(self.show_bcp_text)

        self.PropertyForBCPtext = QComboBox(self.frame_160)
        self.PropertyForBCPtext.setObjectName(u"PropertyForBCPtext")

        self.horizontalLayout_178.addWidget(self.PropertyForBCPtext)


        self.verticalLayout_18.addWidget(self.frame_160)


        self.verticalLayout_22.addWidget(self.groupBox_11)

        self.groupBox_34 = QGroupBox(self.tab_32)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_163 = QHBoxLayout(self.groupBox_34)
        self.horizontalLayout_163.setObjectName(u"horizontalLayout_163")
        self.OpenGL_GL_CULL_FACE = QCheckBox(self.groupBox_34)
        self.OpenGL_GL_CULL_FACE.setObjectName(u"OpenGL_GL_CULL_FACE")
        self.OpenGL_GL_CULL_FACE.setEnabled(True)

        self.horizontalLayout_163.addWidget(self.OpenGL_GL_CULL_FACE)


        self.verticalLayout_22.addWidget(self.groupBox_34)

        self.groupBox_29 = QGroupBox(self.tab_32)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(0, 0))
        self.verticalLayout_107 = QVBoxLayout(self.groupBox_29)
        self.verticalLayout_107.setObjectName(u"verticalLayout_107")
        self.frame_165 = QFrame(self.groupBox_29)
        self.frame_165.setObjectName(u"frame_165")
        self.frame_165.setFrameShape(QFrame.StyledPanel)
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

        self.label_81 = QLabel(self.frame_164)
        self.label_81.setObjectName(u"label_81")

        self.horizontalLayout_180.addWidget(self.label_81)

        self.property_precision = QSpinBox(self.frame_164)
        self.property_precision.setObjectName(u"property_precision")
        self.property_precision.setValue(5)

        self.horizontalLayout_180.addWidget(self.property_precision)


        self.verticalLayout_107.addWidget(self.frame_164)


        self.verticalLayout_22.addWidget(self.groupBox_29)

        self.verticalSpacer_9 = QSpacerItem(20, 374, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_9)

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
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_38)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
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
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
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
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
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
        self.frame_121.setFrameShape(QFrame.StyledPanel)
        self.frame_121.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_126 = QHBoxLayout(self.frame_121)
        self.horizontalLayout_126.setObjectName(u"horizontalLayout_126")
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
        self.frame_120.setFrameShape(QFrame.StyledPanel)
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
        self.verticalLayout_17 = QVBoxLayout(self.tab_41)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
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


        self.verticalLayout_17.addWidget(self.frame_144)

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


        self.verticalLayout_17.addWidget(self.frame_77)

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


        self.verticalLayout_17.addWidget(self.frame_78)

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


        self.verticalLayout_17.addWidget(self.frame_79)

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

        self.color_bond_cp = QFrame(self.frame_10)
        self.color_bond_cp.setObjectName(u"color_bond_cp")
        self.color_bond_cp.setFrameShape(QFrame.StyledPanel)
        self.color_bond_cp.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_83.addWidget(self.color_bond_cp)

        self.color_bond_cp_button = QPushButton(self.frame_10)
        self.color_bond_cp_button.setObjectName(u"color_bond_cp_button")
        self.color_bond_cp_button.setCheckable(False)
        self.color_bond_cp_button.setChecked(False)

        self.horizontalLayout_83.addWidget(self.color_bond_cp_button)


        self.verticalLayout_17.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.tab_41)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 0))
        self.frame_11.setMaximumSize(QSize(16777215, 16777215))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.horizontalLayout_87.setContentsMargins(0, 0, 0, 0)
        self.label_33 = QLabel(self.frame_11)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_87.addWidget(self.label_33)

        self.color_ring_cp = QFrame(self.frame_11)
        self.color_ring_cp.setObjectName(u"color_ring_cp")
        self.color_ring_cp.setFrameShape(QFrame.StyledPanel)
        self.color_ring_cp.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_87.addWidget(self.color_ring_cp)

        self.color_ring_cp_button = QPushButton(self.frame_11)
        self.color_ring_cp_button.setObjectName(u"color_ring_cp_button")
        self.color_ring_cp_button.setCheckable(False)
        self.color_ring_cp_button.setChecked(False)

        self.horizontalLayout_87.addWidget(self.color_ring_cp_button)


        self.verticalLayout_17.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.tab_41)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 0))
        self.frame_12.setMaximumSize(QSize(16777215, 16777215))
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_91 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_91.setObjectName(u"horizontalLayout_91")
        self.horizontalLayout_91.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.frame_12)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_91.addWidget(self.label_35)

        self.color_cage_cp = QFrame(self.frame_12)
        self.color_cage_cp.setObjectName(u"color_cage_cp")
        self.color_cage_cp.setFrameShape(QFrame.StyledPanel)
        self.color_cage_cp.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_91.addWidget(self.color_cage_cp)

        self.color_cage_cp_button = QPushButton(self.frame_12)
        self.color_cage_cp_button.setObjectName(u"color_cage_cp_button")
        self.color_cage_cp_button.setCheckable(False)
        self.color_cage_cp_button.setChecked(False)

        self.horizontalLayout_91.addWidget(self.color_cage_cp_button)


        self.verticalLayout_17.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.tab_41)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 0))
        self.frame_13.setMaximumSize(QSize(16777215, 16777215))
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_92 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_92.setObjectName(u"horizontalLayout_92")
        self.horizontalLayout_92.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.frame_13)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_92.addWidget(self.label_36)

        self.color_bond_path = QFrame(self.frame_13)
        self.color_bond_path.setObjectName(u"color_bond_path")
        self.color_bond_path.setFrameShape(QFrame.StyledPanel)
        self.color_bond_path.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_92.addWidget(self.color_bond_path)

        self.color_bond_path_button = QPushButton(self.frame_13)
        self.color_bond_path_button.setObjectName(u"color_bond_path_button")
        self.color_bond_path_button.setCheckable(False)
        self.color_bond_path_button.setChecked(False)

        self.horizontalLayout_92.addWidget(self.color_bond_path_button)


        self.verticalLayout_17.addWidget(self.frame_13)

        self.frame_76 = QFrame(self.tab_41)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setMaximumSize(QSize(16777215, 16777215))
        self.frame_76.setFrameShape(QFrame.NoFrame)
        self.frame_76.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_77 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.horizontalLayout_77.setContentsMargins(0, -1, -1, -1)
        self.label_29 = QLabel(self.frame_76)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_77.addWidget(self.label_29)

        self.FormSettingsColorsScale = QComboBox(self.frame_76)
        self.FormSettingsColorsScale.setObjectName(u"FormSettingsColorsScale")
        self.FormSettingsColorsScale.setMinimumSize(QSize(150, 0))
        self.FormSettingsColorsScale.setEditable(False)

        self.horizontalLayout_77.addWidget(self.FormSettingsColorsScale)


        self.verticalLayout_17.addWidget(self.frame_76)

        self.ColorRow = PyqtGraphWidgetImage(self.tab_41)
        self.ColorRow.setObjectName(u"ColorRow")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ColorRow.sizePolicy().hasHeightForWidth())
        self.ColorRow.setSizePolicy(sizePolicy3)
        self.ColorRow.setMinimumSize(QSize(0, 40))
        self.ColorRow.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_17.addWidget(self.ColorRow)

        self.frame_102 = QFrame(self.tab_41)
        self.frame_102.setObjectName(u"frame_102")
        self.frame_102.setFrameShape(QFrame.NoFrame)
        self.frame_102.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_106 = QHBoxLayout(self.frame_102)
        self.horizontalLayout_106.setObjectName(u"horizontalLayout_106")
        self.horizontalLayout_106.setContentsMargins(0, -1, -1, -1)
        self.label_14 = QLabel(self.frame_102)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_106.addWidget(self.label_14)

        self.FormSettingsColorsScaleType = QComboBox(self.frame_102)
        self.FormSettingsColorsScaleType.setObjectName(u"FormSettingsColorsScaleType")
        self.FormSettingsColorsScaleType.setMinimumSize(QSize(250, 0))
        self.FormSettingsColorsScaleType.setEditable(False)

        self.horizontalLayout_106.addWidget(self.FormSettingsColorsScaleType)


        self.verticalLayout_17.addWidget(self.frame_102)

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


        self.verticalLayout_17.addWidget(self.frame_72)

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


        self.verticalLayout_17.addWidget(self.frame_5)

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


        self.verticalLayout_17.addWidget(self.frame_89)

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


        self.verticalLayout_17.addWidget(self.frame_90)

        self.verticalSpacer_19 = QSpacerItem(20, 215, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_19)

        self.tabWidget_12.addTab(self.tab_41, "")

        self.verticalLayout_14.addWidget(self.tabWidget_12)

        self.tabWidget_9.addTab(self.tab_37, "")

        self.verticalLayout_23.addWidget(self.tabWidget_9)

        self.tabWidget.addTab(self.tab_29, "")
        self.FormTabSettings = QWidget()
        self.FormTabSettings.setObjectName(u"FormTabSettings")
        self.verticalLayout_3 = QVBoxLayout(self.FormTabSettings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
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

        self.frame_85 = QFrame(self.FormTabSettings)
        self.frame_85.setObjectName(u"frame_85")
        self.frame_85.setFrameShape(QFrame.NoFrame)
        self.frame_85.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_85)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.horizontalLayout_85.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_85)

        self.frame_80 = QFrame(self.FormTabSettings)
        self.frame_80.setObjectName(u"frame_80")
        self.frame_80.setFrameShape(QFrame.NoFrame)
        self.frame_80.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_84 = QHBoxLayout(self.frame_80)
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.horizontalLayout_84.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_80)

        self.is_add_translated_atoms = QCheckBox(self.FormTabSettings)
        self.is_add_translated_atoms.setObjectName(u"is_add_translated_atoms")

        self.verticalLayout_3.addWidget(self.is_add_translated_atoms)

        self.is_show_props_for_cp_list = QCheckBox(self.FormTabSettings)
        self.is_show_props_for_cp_list.setObjectName(u"is_show_props_for_cp_list")

        self.verticalLayout_3.addWidget(self.is_show_props_for_cp_list)

        self.verticalSpacer_18 = QSpacerItem(20, 568, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_18)

        self.tabWidget.addTab(self.FormTabSettings, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.Form3Dand2DTabs = QToolBox(self.centralwidget)
        self.Form3Dand2DTabs.setObjectName(u"Form3Dand2DTabs")
        sizePolicy3.setHeightForWidth(self.Form3Dand2DTabs.sizePolicy().hasHeightForWidth())
        self.Form3Dand2DTabs.setSizePolicy(sizePolicy3)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.page_7.setGeometry(QRect(0, 0, 642, 765))
        self.horizontalLayout_3 = QHBoxLayout(self.page_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.openGLWidget = GuiOpenGLCP(self.page_7)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(3)
        sizePolicy4.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.openGLWidget)

        self.Form3Dand2DTabs.addItem(self.page_7, u"3D View")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.page_8.setGeometry(QRect(0, 0, 642, 765))
        self.verticalLayout_21 = QVBoxLayout(self.page_8)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.cps_rule = QLabel(self.page_8)
        self.cps_rule.setObjectName(u"cps_rule")
        self.cps_rule.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_21.addWidget(self.cps_rule)

        self.frame_15 = QFrame(self.page_8)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_15)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.label = QLabel(self.frame_15)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.bcp_for_figure = QComboBox(self.frame_15)
        self.bcp_for_figure.setObjectName(u"bcp_for_figure")

        self.horizontalLayout.addWidget(self.bcp_for_figure)

        self.horizontalSpacer_8 = QSpacerItem(391, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_8)


        self.verticalLayout_21.addWidget(self.frame_15)

        self.tabWidget_2 = QTabWidget(self.page_8)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_19 = QVBoxLayout(self.tab_6)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.PyqtGraphWidget = PyqtGraphWidget(self.tab_6)
        self.PyqtGraphWidget.setObjectName(u"PyqtGraphWidget")
        sizePolicy3.setHeightForWidth(self.PyqtGraphWidget.sizePolicy().hasHeightForWidth())
        self.PyqtGraphWidget.setSizePolicy(sizePolicy3)
        self.PyqtGraphWidget.setMinimumSize(QSize(0, 100))

        self.verticalLayout_19.addWidget(self.PyqtGraphWidget)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.frame_14 = QFrame(self.tab_7)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setGeometry(QRect(10, 20, 620, 30))
        self.frame_14.setMaximumSize(QSize(16777215, 30))
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.bcp_table = QRadioButton(self.frame_14)
        self.bcp_table.setObjectName(u"bcp_table")
        self.bcp_table.setChecked(True)

        self.horizontalLayout_9.addWidget(self.bcp_table)

        self.natr_table = QRadioButton(self.frame_14)
        self.natr_table.setObjectName(u"natr_table")

        self.horizontalLayout_9.addWidget(self.natr_table)

        self.rcp_table = QRadioButton(self.frame_14)
        self.rcp_table.setObjectName(u"rcp_table")

        self.horizontalLayout_9.addWidget(self.rcp_table)

        self.ccp_table = QRadioButton(self.frame_14)
        self.ccp_table.setObjectName(u"ccp_table")

        self.horizontalLayout_9.addWidget(self.ccp_table)

        self.cps_table = QTableWidget(self.tab_7)
        self.cps_table.setObjectName(u"cps_table")
        self.cps_table.setGeometry(QRect(20, 70, 620, 712))
        sizePolicy1.setHeightForWidth(self.cps_table.sizePolicy().hasHeightForWidth())
        self.cps_table.setSizePolicy(sizePolicy1)
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_4 = QVBoxLayout(self.tab_8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_18 = QFrame(self.tab_8)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, -1, 0, -1)
        self.groupBox_16 = QGroupBox(self.frame_18)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.verticalLayout_27 = QVBoxLayout(self.groupBox_16)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.bp_len_histogram = QRadioButton(self.groupBox_16)
        self.bp_len_histogram.setObjectName(u"bp_len_histogram")

        self.verticalLayout_27.addWidget(self.bp_len_histogram)

        self.bcp_rho_histogram = QRadioButton(self.groupBox_16)
        self.bcp_rho_histogram.setObjectName(u"bcp_rho_histogram")

        self.verticalLayout_27.addWidget(self.bcp_rho_histogram)

        self.bonds_histogram = QRadioButton(self.groupBox_16)
        self.bonds_histogram.setObjectName(u"bonds_histogram")
        self.bonds_histogram.setCheckable(False)

        self.verticalLayout_27.addWidget(self.bonds_histogram)


        self.horizontalLayout_19.addWidget(self.groupBox_16)

        self.groupBox_52 = QGroupBox(self.frame_18)
        self.groupBox_52.setObjectName(u"groupBox_52")
        self.groupBox_52.setMinimumSize(QSize(0, 0))
        self.verticalLayout_101 = QVBoxLayout(self.groupBox_52)
        self.verticalLayout_101.setObjectName(u"verticalLayout_101")
        self.frame_153 = QFrame(self.groupBox_52)
        self.frame_153.setObjectName(u"frame_153")
        self.frame_153.setFrameShape(QFrame.NoFrame)
        self.frame_153.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_168 = QHBoxLayout(self.frame_153)
        self.horizontalLayout_168.setObjectName(u"horizontalLayout_168")
        self.horizontalLayout_168.setContentsMargins(-1, 0, -1, 0)
        self.label_125 = QLabel(self.frame_153)
        self.label_125.setObjectName(u"label_125")

        self.horizontalLayout_168.addWidget(self.label_125)

        self.histogram_title = QLineEdit(self.frame_153)
        self.histogram_title.setObjectName(u"histogram_title")

        self.horizontalLayout_168.addWidget(self.histogram_title)


        self.verticalLayout_101.addWidget(self.frame_153)

        self.frame_154 = QFrame(self.groupBox_52)
        self.frame_154.setObjectName(u"frame_154")
        self.frame_154.setFrameShape(QFrame.NoFrame)
        self.frame_154.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_169 = QHBoxLayout(self.frame_154)
        self.horizontalLayout_169.setObjectName(u"horizontalLayout_169")
        self.horizontalLayout_169.setContentsMargins(-1, 0, -1, 0)
        self.label_126 = QLabel(self.frame_154)
        self.label_126.setObjectName(u"label_126")

        self.horizontalLayout_169.addWidget(self.label_126)

        self.histogram_x_label = QLineEdit(self.frame_154)
        self.histogram_x_label.setObjectName(u"histogram_x_label")

        self.horizontalLayout_169.addWidget(self.histogram_x_label)


        self.verticalLayout_101.addWidget(self.frame_154)

        self.frame_155 = QFrame(self.groupBox_52)
        self.frame_155.setObjectName(u"frame_155")
        self.frame_155.setFrameShape(QFrame.NoFrame)
        self.frame_155.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_170 = QHBoxLayout(self.frame_155)
        self.horizontalLayout_170.setObjectName(u"horizontalLayout_170")
        self.horizontalLayout_170.setContentsMargins(-1, 0, -1, 0)
        self.label_127 = QLabel(self.frame_155)
        self.label_127.setObjectName(u"label_127")

        self.horizontalLayout_170.addWidget(self.label_127)

        self.histogram_y_label = QLineEdit(self.frame_155)
        self.histogram_y_label.setObjectName(u"histogram_y_label")

        self.horizontalLayout_170.addWidget(self.histogram_y_label)


        self.verticalLayout_101.addWidget(self.frame_155)

        self.frame_7 = QFrame(self.groupBox_52)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 40))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.frame_7.setLineWidth(0)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_27)

        self.FormActionsPostPlotBondsHistogramN = QSpinBox(self.frame_7)
        self.FormActionsPostPlotBondsHistogramN.setObjectName(u"FormActionsPostPlotBondsHistogramN")
        self.FormActionsPostPlotBondsHistogramN.setMinimum(1)
        self.FormActionsPostPlotBondsHistogramN.setValue(5)

        self.horizontalLayout_32.addWidget(self.FormActionsPostPlotBondsHistogramN)

        self.plot_histogram = QPushButton(self.frame_7)
        self.plot_histogram.setObjectName(u"plot_histogram")
        self.plot_histogram.setEnabled(False)

        self.horizontalLayout_32.addWidget(self.plot_histogram)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_26)


        self.verticalLayout_101.addWidget(self.frame_7)


        self.horizontalLayout_19.addWidget(self.groupBox_52)


        self.verticalLayout_4.addWidget(self.frame_18)

        self.pyqt_hist_widget = PyqtGraphWidget(self.tab_8)
        self.pyqt_hist_widget.setObjectName(u"pyqt_hist_widget")
        sizePolicy3.setHeightForWidth(self.pyqt_hist_widget.sizePolicy().hasHeightForWidth())
        self.pyqt_hist_widget.setSizePolicy(sizePolicy3)
        self.pyqt_hist_widget.setMinimumSize(QSize(0, 100))

        self.verticalLayout_4.addWidget(self.pyqt_hist_widget)

        self.tabWidget_2.addTab(self.tab_8, "")

        self.verticalLayout_21.addWidget(self.tabWidget_2)

        self.Form3Dand2DTabs.addItem(self.page_8, u"CPs statistics")

        self.horizontalLayout_2.addWidget(self.Form3Dand2DTabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1121, 26))
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
        self.tabWidget_15.setCurrentIndex(0)
        self.tabWidget_14.setCurrentIndex(0)
        self.tabWidget_9.setCurrentIndex(0)
        self.tabWidget_12.setCurrentIndex(0)
        self.Form3Dand2DTabs.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CritPlot - Open interfece to the TOPOND and Critic2 programms", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionOrtho.setText(QCoreApplication.translate("MainWindow", u"Ortho", None))
        self.actionPerspective.setText(QCoreApplication.translate("MainWindow", u"Perspective", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionShowBox.setText(QCoreApplication.translate("MainWindow", u"Show Box", None))
        self.actionHideBox.setText(QCoreApplication.translate("MainWindow", u"Hide Box", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_131.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_134.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.label_135.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Camera position", None))
        self.label_137.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_138.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.label_139.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabModel), QCoreApplication.translate("MainWindow", u"Model", None))
        self.add_xyz_critic_data.setText(QCoreApplication.translate("MainWindow", u"Add data from *.xyz file (for opened *.cro file)", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Selected CP", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.selectedCP.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.selected_cp_title.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_107.setText(QCoreApplication.translate("MainWindow", u"Nuclei:", None))
        self.selectedCP_nuclei.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_111.setText(QCoreApplication.translate("MainWindow", u"Bond length, A:", None))
        self.selected_cp_bond_len.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"RHO:", None))
        self.FormSelectedCP_f.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"|grad|:", None))
        self.FormSelectedCP_g.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"Lap:", None))
        self.FormSelectedCP_lap.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"List of CP", None))
        self.add_cp_to_list.setText(QCoreApplication.translate("MainWindow", u"Add to List", None))
        self.delete_cp_from_list.setText(QCoreApplication.translate("MainWindow", u"Delete selected from List", None))
        self.clear_cp_list.setText(QCoreApplication.translate("MainWindow", u"Clear List", None))
        self.delete_cp_from_model.setText(QCoreApplication.translate("MainWindow", u"Exclude CPs (list) from model", None))
        self.leave_cp_in_model.setText(QCoreApplication.translate("MainWindow", u"Limit to CPs (list) in model", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.form_critic_list.setText(QCoreApplication.translate("MainWindow", u"From list", None))
        self.form_critic_all.setText(QCoreApplication.translate("MainWindow", u"All CP", None))
        self.export_cp_to_csv.setText(QCoreApplication.translate("MainWindow", u"Export to *.csv", None))
        self.tabWidget_15.setTabText(self.tabWidget_15.indexOf(self.tab_39), QCoreApplication.translate("MainWindow", u"*.csv", None))
        self.tabWidget_14.setTabText(self.tabWidget_14.indexOf(self.tab_48), QCoreApplication.translate("MainWindow", u"Imports", None))
        self.form_critic_all_cp.setText(QCoreApplication.translate("MainWindow", u"All CP", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"CP only", None))
        self.formCriticBPradio.setText(QCoreApplication.translate("MainWindow", u"BP with", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"extra points", None))
        self.tabWidget_14.setTabText(self.tabWidget_14.indexOf(self.tab_46), QCoreApplication.translate("MainWindow", u"CP", None))
        self.form_critic_prop_lag.setText(QCoreApplication.translate("MainWindow", u"lag", None))
        self.form_critic_prop_htf_kir.setText(QCoreApplication.translate("MainWindow", u"htf_kir", None))
        self.form_critic_prop_htf.setText(QCoreApplication.translate("MainWindow", u"htf", None))
        self.form_critic_prop_gtf.setText(QCoreApplication.translate("MainWindow", u"gtf", None))
        self.form_critic_prop_gtf_kir.setText(QCoreApplication.translate("MainWindow", u"gtf_kir", None))
        self.form_critic_prop_lol_kir.setText(QCoreApplication.translate("MainWindow", u"lol_kir", None))
        self.form_critic_prop_rdg.setText(QCoreApplication.translate("MainWindow", u"rdg", None))
        self.form_critic_prop_vtf.setText(QCoreApplication.translate("MainWindow", u"vtf", None))
        self.form_critic_prop_vtf_kir.setText(QCoreApplication.translate("MainWindow", u"vtf_kir", None))
        self.tabWidget_14.setTabText(self.tabWidget_14.indexOf(self.tab_47), QCoreApplication.translate("MainWindow", u"Properties", None))
        self.addLinesToCriticFile.setText(QCoreApplication.translate("MainWindow", u"add lines to *.cri file", None))
        self.tabWidget_14.setTabText(self.tabWidget_14.indexOf(self.tab_49), QCoreApplication.translate("MainWindow", u"Lines", None))
        self.FormCreateCriFile.setText(QCoreApplication.translate("MainWindow", u"Create *.cri file", None))
        self.tabWidget_15.setTabText(self.tabWidget_15.indexOf(self.tab_53), QCoreApplication.translate("MainWindow", u"*.cri", None))
        self.radio_with_cp.setText(QCoreApplication.translate("MainWindow", u"with", None))
        self.radio_without_cp.setText(QCoreApplication.translate("MainWindow", u"without", None))
        self.label_93.setText(QCoreApplication.translate("MainWindow", u"selected CP", None))
        self.FormCreateCriXYZFile.setText(QCoreApplication.translate("MainWindow", u"Create *.xyz file", None))
        self.save_all_data.setText(QCoreApplication.translate("MainWindow", u"SaveAllData", None))
        self.tabWidget_15.setTabText(self.tabWidget_15.indexOf(self.tab_52), QCoreApplication.translate("MainWindow", u"*.xyz", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_51), QCoreApplication.translate("MainWindow", u"CPs", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"RHO", None))
        self.hide_cps_min_rho.setText(QCoreApplication.translate("MainWindow", u"Hide cp with smaller RHO", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Nuclei", None))
        self.hide_cps_eq_atoms.setText(QCoreApplication.translate("MainWindow", u"Hide cp with eq atoms", None))
        self.cancel_cps_filters.setText(QCoreApplication.translate("MainWindow", u"\u0421ancel filters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Filter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Selection", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Add or Modify Atom", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Element", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.FormActionsPreButDeleteAtom.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.FormActionsPreButModifyAtom.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.FormActionsPreButAddAtom.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Translation", None))
        self.atom_translation_1_plus.setText(QCoreApplication.translate("MainWindow", u"+ Translation 1", None))
        self.atom_translation_2_plus.setText(QCoreApplication.translate("MainWindow", u"+ Translation 2", None))
        self.atom_translation_3_plus.setText(QCoreApplication.translate("MainWindow", u"+ Translation 3", None))
        self.atom_translation_1_minus.setText(QCoreApplication.translate("MainWindow", u"- Translation 1", None))
        self.atom_translation_2_minus.setText(QCoreApplication.translate("MainWindow", u"- Translation 2", None))
        self.atom_translation_3_minus.setText(QCoreApplication.translate("MainWindow", u"- Translation 3", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Additional atoms", None))
        self.additional_atoms_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Cell", None))
        self.FormModifyCellButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Transforms", None))
        self.FormModifyGoPositive.setText(QCoreApplication.translate("MainWindow", u"To positive", None))
        self.FormModifyGoToCell.setText(QCoreApplication.translate("MainWindow", u"To cell", None))
        self.modify_center_to_zero.setText(QCoreApplication.translate("MainWindow", u"Center to zero", None))
        self.groupBox_49.setTitle(QCoreApplication.translate("MainWindow", u"Circular shift", None))
        self.x_circular_shift.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.y_circular_shift.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.z_circular_shift.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabActions), QCoreApplication.translate("MainWindow", u"Modify", None))
        self.FormActionsPostButGetBonds.setText(QCoreApplication.translate("MainWindow", u"Get bonds", None))
        self.FormActionsPostLabelMeanBond.setText("")
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Atom - atom distance", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.PropertyAtomAtomDistanceGet.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Bonds", None))
        self.ActivateFragmentSelectionModeCheckBox.setText(QCoreApplication.translate("MainWindow", u"Activate fragment selection mode", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Visual effect for selected fragment", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Transparency", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"x from", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"to", None))
        self.changeFragment1StatusByX.setText(QCoreApplication.translate("MainWindow", u"change status", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"y from", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"to", None))
        self.changeFragment1StatusByY.setText(QCoreApplication.translate("MainWindow", u"change status", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"z from", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"to", None))
        self.changeFragment1StatusByZ.setText(QCoreApplication.translate("MainWindow", u"change status", None))
        self.fragment1Clear.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Coloring", None))
        self.FormSettingsViewCheckShowAtoms.setText(QCoreApplication.translate("MainWindow", u"Show atoms", None))
        self.FormSettingsViewCheckShowBox.setText(QCoreApplication.translate("MainWindow", u"Show box", None))
        self.FormSettingsViewCheckShowAtomNumber.setText(QCoreApplication.translate("MainWindow", u"Show atom number", None))
        self.FormSettingsViewCheckShowAxes.setText(QCoreApplication.translate("MainWindow", u"Show axes", None))
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
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Critical points", None))
        self.show_ncp.setText(QCoreApplication.translate("MainWindow", u"NCP", None))
        self.show_bcp.setText(QCoreApplication.translate("MainWindow", u"BCP", None))
        self.show_nnatr.setText(QCoreApplication.translate("MainWindow", u"NATTR", None))
        self.show_rcp.setText(QCoreApplication.translate("MainWindow", u"RCP", None))
        self.show_ccp.setText(QCoreApplication.translate("MainWindow", u"CCP", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Bond path", None))
        self.show_bond_path.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.show_bp_if_avail.setText(QCoreApplication.translate("MainWindow", u"bond path (if available)", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"only lines", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.show_bcp_text.setText(QCoreApplication.translate("MainWindow", u"BCP property", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"OpenGl", None))
        self.OpenGL_GL_CULL_FACE.setText(QCoreApplication.translate("MainWindow", u"GL_CULL_FACE", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Text", None))
        self.label_132.setText(QCoreApplication.translate("MainWindow", u"Position: X", None))
        self.label_133.setText(QCoreApplication.translate("MainWindow", u", Y", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"Font size", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"Figures in property", None))
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
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Bond CP color", None))
        self.color_bond_cp_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Ring CP color", None))
        self.color_ring_cp_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Cage CP color", None))
        self.color_cage_cp_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Bond Path color", None))
        self.color_bond_path_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
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
        self.FormSettingsViewCheckAtomSelection.setText(QCoreApplication.translate("MainWindow", u"Allow atom selection", None))
        self.FormSettingsViewCheckModelMove.setText(QCoreApplication.translate("MainWindow", u"Allow model move", None))
        self.is_add_translated_atoms.setText(QCoreApplication.translate("MainWindow", u"Add translated atoms", None))
        self.is_show_props_for_cp_list.setText(QCoreApplication.translate("MainWindow", u"Show properties only for CPs from list", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabSettings), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Form3Dand2DTabs.setItemText(self.Form3Dand2DTabs.indexOf(self.page_7), QCoreApplication.translate("MainWindow", u"3D View", None))
        self.cps_rule.setText(QCoreApplication.translate("MainWindow", u"Poincare-Hoff rule ...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Bond ritical points filter", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"RHO(r)", None))
        self.bcp_table.setText(QCoreApplication.translate("MainWindow", u"bcp", None))
        self.natr_table.setText(QCoreApplication.translate("MainWindow", u"natr", None))
        self.rcp_table.setText(QCoreApplication.translate("MainWindow", u"rcp", None))
        self.ccp_table.setText(QCoreApplication.translate("MainWindow", u"ccp", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Properties table", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Source", None))
        self.bp_len_histogram.setText(QCoreApplication.translate("MainWindow", u"BP len", None))
        self.bcp_rho_histogram.setText(QCoreApplication.translate("MainWindow", u"BCP rho", None))
        self.bonds_histogram.setText(QCoreApplication.translate("MainWindow", u"Bonds", None))
        self.groupBox_52.setTitle(QCoreApplication.translate("MainWindow", u"Plot details", None))
        self.label_125.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.histogram_title.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_126.setText(QCoreApplication.translate("MainWindow", u"X label", None))
        self.histogram_x_label.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_127.setText(QCoreApplication.translate("MainWindow", u"Y label", None))
        self.histogram_y_label.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.plot_histogram.setText(QCoreApplication.translate("MainWindow", u"Plot histogram", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Histogram", None))
        self.Form3Dand2DTabs.setItemText(self.Form3Dand2DTabs.indexOf(self.page_8), QCoreApplication.translate("MainWindow", u"CPs statistics", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuOrtho_Perspective.setTitle(QCoreApplication.translate("MainWindow", u"Ortho / Perspective", None))
        self.menuBox.setTitle(QCoreApplication.translate("MainWindow", u"Box", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

