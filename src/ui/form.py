# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form-v1.x.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraphwidget import PyqtGraphWidget
from pyqtgraphwidgetimage import PyqtGraphWidgetImage


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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(450, 500))
        self.tabWidget.setMaximumSize(QSize(450, 16777215))
        self.tabWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.FormTabModel = QWidget()
        self.FormTabModel.setObjectName(u"FormTabModel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.FormModelTableProperties.sizePolicy().hasHeightForWidth())
        self.FormModelTableProperties.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.FormModelTableProperties)

        self.tabWidget.addTab(self.FormTabModel, "")
        self.FormTabActions = QWidget()
        self.FormTabActions.setObjectName(u"FormTabActions")
        self.verticalLayout_2 = QVBoxLayout(self.FormTabActions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget_3 = QTabWidget(self.FormTabActions)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tabWidget_3.setEnabled(True)
        self.tabWidget_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_17 = QVBoxLayout(self.tab_5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.toolBox = QToolBox(self.tab_5)
        self.toolBox.setObjectName(u"toolBox")
        self.page_17 = QWidget()
        self.page_17.setObjectName(u"page_17")
        self.page_17.setGeometry(QRect(0, 0, 371, 624))
        self.verticalLayout_52 = QVBoxLayout(self.page_17)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.frame_81 = QFrame(self.page_17)
        self.frame_81.setObjectName(u"frame_81")
        self.frame_81.setFrameShape(QFrame.NoFrame)
        self.frame_81.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_76 = QHBoxLayout(self.frame_81)
        self.horizontalLayout_76.setObjectName(u"horizontalLayout_76")
        self.label_75 = QLabel(self.frame_81)
        self.label_75.setObjectName(u"label_75")

        self.horizontalLayout_76.addWidget(self.label_75)

        self.FormActionsPreLineGraphene_n = QSpinBox(self.frame_81)
        self.FormActionsPreLineGraphene_n.setObjectName(u"FormActionsPreLineGraphene_n")
        self.FormActionsPreLineGraphene_n.setValue(7)

        self.horizontalLayout_76.addWidget(self.FormActionsPreLineGraphene_n)

        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_76.addItem(self.horizontalSpacer_39)

        self.label_76 = QLabel(self.frame_81)
        self.label_76.setObjectName(u"label_76")

        self.horizontalLayout_76.addWidget(self.label_76)

        self.FormActionsPreLineGraphene_m = QSpinBox(self.frame_81)
        self.FormActionsPreLineGraphene_m.setObjectName(u"FormActionsPreLineGraphene_m")
        self.FormActionsPreLineGraphene_m.setValue(7)

        self.horizontalLayout_76.addWidget(self.FormActionsPreLineGraphene_m)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_76.addItem(self.horizontalSpacer_40)

        self.label_77 = QLabel(self.frame_81)
        self.label_77.setObjectName(u"label_77")

        self.horizontalLayout_76.addWidget(self.label_77)

        self.FormActionsPreLineGraphene_len = QDoubleSpinBox(self.frame_81)
        self.FormActionsPreLineGraphene_len.setObjectName(u"FormActionsPreLineGraphene_len")
        self.FormActionsPreLineGraphene_len.setMinimumSize(QSize(0, 24))
        self.FormActionsPreLineGraphene_len.setMaximumSize(QSize(16777215, 16777215))
        self.FormActionsPreLineGraphene_len.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreLineGraphene_len.setSingleStep(0.500000000000000)
        self.FormActionsPreLineGraphene_len.setValue(9.800000000000001)

        self.horizontalLayout_76.addWidget(self.FormActionsPreLineGraphene_len)


        self.verticalLayout_52.addWidget(self.frame_81)

        self.frame_84 = QFrame(self.page_17)
        self.frame_84.setObjectName(u"frame_84")
        self.frame_84.setFrameShape(QFrame.NoFrame)
        self.frame_84.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_75 = QHBoxLayout(self.frame_84)
        self.horizontalLayout_75.setObjectName(u"horizontalLayout_75")
        self.horizontalSpacer_42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_75.addItem(self.horizontalSpacer_42)

        self.FormActionsPreButGrapheneGenerate = QPushButton(self.frame_84)
        self.FormActionsPreButGrapheneGenerate.setObjectName(u"FormActionsPreButGrapheneGenerate")

        self.horizontalLayout_75.addWidget(self.FormActionsPreButGrapheneGenerate)

        self.horizontalSpacer_43 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_75.addItem(self.horizontalSpacer_43)


        self.verticalLayout_52.addWidget(self.frame_84)

        self.verticalSpacer_14 = QSpacerItem(20, 387, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_52.addItem(self.verticalSpacer_14)

        self.toolBox.addItem(self.page_17, u"Graphene")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_95 = QVBoxLayout(self.page_4)
        self.verticalLayout_95.setObjectName(u"verticalLayout_95")
        self.tabWidget_11 = QTabWidget(self.page_4)
        self.tabWidget_11.setObjectName(u"tabWidget_11")
        self.tab_36 = QWidget()
        self.tab_36.setObjectName(u"tab_36")
        self.verticalLayout_94 = QVBoxLayout(self.tab_36)
        self.verticalLayout_94.setObjectName(u"verticalLayout_94")
        self.groupBox_3 = QGroupBox(self.tab_36)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.groupBox_3.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_43 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.groupBox_3)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_13)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.FormActionsPreRadioSWNT = QRadioButton(self.frame_13)
        self.FormActionsPreRadioSWNT.setObjectName(u"FormActionsPreRadioSWNT")
        self.FormActionsPreRadioSWNT.setChecked(True)

        self.verticalLayout_19.addWidget(self.FormActionsPreRadioSWNT)

        self.FormActionsPreRadioSWNTcap = QRadioButton(self.frame_13)
        self.FormActionsPreRadioSWNTcap.setObjectName(u"FormActionsPreRadioSWNTcap")

        self.verticalLayout_19.addWidget(self.FormActionsPreRadioSWNTcap)

        self.FormActionsPreRadioSWNTcap_2 = QRadioButton(self.frame_13)
        self.FormActionsPreRadioSWNTcap_2.setObjectName(u"FormActionsPreRadioSWNTcap_2")

        self.verticalLayout_19.addWidget(self.FormActionsPreRadioSWNTcap_2)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_5)


        self.horizontalLayout_43.addWidget(self.frame_13)

        self.frame_24 = QFrame(self.groupBox_3)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.frame_24)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.FormCreateGroupFirstCap = QGroupBox(self.frame_24)
        self.FormCreateGroupFirstCap.setObjectName(u"FormCreateGroupFirstCap")
        self.FormCreateGroupFirstCap.setEnabled(False)
        self.FormCreateGroupFirstCap.setMinimumSize(QSize(0, 0))
        self.verticalLayout_66 = QVBoxLayout(self.FormCreateGroupFirstCap)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.frame_98 = QFrame(self.FormCreateGroupFirstCap)
        self.frame_98.setObjectName(u"frame_98")
        self.frame_98.setFrameShape(QFrame.NoFrame)
        self.frame_98.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_102 = QHBoxLayout(self.frame_98)
        self.horizontalLayout_102.setObjectName(u"horizontalLayout_102")
        self.horizontalLayout_102.setContentsMargins(0, 0, 0, 0)
        self.label_45 = QLabel(self.frame_98)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_102.addWidget(self.label_45)

        self.FormCreateSpinFirstCapDist = QDoubleSpinBox(self.frame_98)
        self.FormCreateSpinFirstCapDist.setObjectName(u"FormCreateSpinFirstCapDist")
        self.FormCreateSpinFirstCapDist.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.horizontalLayout_102.addWidget(self.FormCreateSpinFirstCapDist)


        self.verticalLayout_66.addWidget(self.frame_98)

        self.frame_99 = QFrame(self.FormCreateGroupFirstCap)
        self.frame_99.setObjectName(u"frame_99")
        self.frame_99.setFrameShape(QFrame.NoFrame)
        self.frame_99.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_103 = QHBoxLayout(self.frame_99)
        self.horizontalLayout_103.setObjectName(u"horizontalLayout_103")
        self.horizontalLayout_103.setContentsMargins(0, 0, 0, 0)
        self.label_46 = QLabel(self.frame_99)
        self.label_46.setObjectName(u"label_46")

        self.horizontalLayout_103.addWidget(self.label_46)

        self.FormCreateSpinFirstCapAngle = QDoubleSpinBox(self.frame_99)
        self.FormCreateSpinFirstCapAngle.setObjectName(u"FormCreateSpinFirstCapAngle")
        self.FormCreateSpinFirstCapAngle.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.horizontalLayout_103.addWidget(self.FormCreateSpinFirstCapAngle)


        self.verticalLayout_66.addWidget(self.frame_99)


        self.verticalLayout_64.addWidget(self.FormCreateGroupFirstCap)

        self.FormCreateGroupSecondCap = QGroupBox(self.frame_24)
        self.FormCreateGroupSecondCap.setObjectName(u"FormCreateGroupSecondCap")
        self.FormCreateGroupSecondCap.setEnabled(False)
        self.FormCreateGroupSecondCap.setMinimumSize(QSize(0, 0))
        self.verticalLayout_67 = QVBoxLayout(self.FormCreateGroupSecondCap)
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.frame_100 = QFrame(self.FormCreateGroupSecondCap)
        self.frame_100.setObjectName(u"frame_100")
        self.frame_100.setFrameShape(QFrame.NoFrame)
        self.frame_100.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_105 = QHBoxLayout(self.frame_100)
        self.horizontalLayout_105.setObjectName(u"horizontalLayout_105")
        self.horizontalLayout_105.setContentsMargins(0, 0, 0, 0)
        self.label_47 = QLabel(self.frame_100)
        self.label_47.setObjectName(u"label_47")

        self.horizontalLayout_105.addWidget(self.label_47)

        self.FormCreateSpinSecondCapDist = QDoubleSpinBox(self.frame_100)
        self.FormCreateSpinSecondCapDist.setObjectName(u"FormCreateSpinSecondCapDist")
        self.FormCreateSpinSecondCapDist.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.horizontalLayout_105.addWidget(self.FormCreateSpinSecondCapDist)


        self.verticalLayout_67.addWidget(self.frame_100)

        self.frame_101 = QFrame(self.FormCreateGroupSecondCap)
        self.frame_101.setObjectName(u"frame_101")
        self.frame_101.setFrameShape(QFrame.NoFrame)
        self.frame_101.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_104 = QHBoxLayout(self.frame_101)
        self.horizontalLayout_104.setObjectName(u"horizontalLayout_104")
        self.horizontalLayout_104.setContentsMargins(0, 0, 0, 0)
        self.label_48 = QLabel(self.frame_101)
        self.label_48.setObjectName(u"label_48")

        self.horizontalLayout_104.addWidget(self.label_48)

        self.FormCreateSpinSecondCapAngle = QDoubleSpinBox(self.frame_101)
        self.FormCreateSpinSecondCapAngle.setObjectName(u"FormCreateSpinSecondCapAngle")
        self.FormCreateSpinSecondCapAngle.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.horizontalLayout_104.addWidget(self.FormCreateSpinSecondCapAngle)


        self.verticalLayout_67.addWidget(self.frame_101)


        self.verticalLayout_64.addWidget(self.FormCreateGroupSecondCap)


        self.horizontalLayout_43.addWidget(self.frame_24)


        self.verticalLayout_94.addWidget(self.groupBox_3)

        self.groupBox_8 = QGroupBox(self.tab_36)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(0, 0))
        self.groupBox_8.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_30 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_9 = QLabel(self.groupBox_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.label_9)

        self.FormActionsPreLineSWNTn = QSpinBox(self.groupBox_8)
        self.FormActionsPreLineSWNTn.setObjectName(u"FormActionsPreLineSWNTn")
        self.FormActionsPreLineSWNTn.setValue(7)

        self.horizontalLayout_30.addWidget(self.FormActionsPreLineSWNTn)

        self.label_23 = QLabel(self.groupBox_8)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(10, 16777215))
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.label_23)

        self.FormActionsPreLineSWNTm = QSpinBox(self.groupBox_8)
        self.FormActionsPreLineSWNTm.setObjectName(u"FormActionsPreLineSWNTm")
        self.FormActionsPreLineSWNTm.setValue(7)

        self.horizontalLayout_30.addWidget(self.FormActionsPreLineSWNTm)

        self.label_44 = QLabel(self.groupBox_8)
        self.label_44.setObjectName(u"label_44")

        self.horizontalLayout_30.addWidget(self.label_44)

        self.FormActionsPreComboSWNTind = QComboBox(self.groupBox_8)
        self.FormActionsPreComboSWNTind.setObjectName(u"FormActionsPreComboSWNTind")
        self.FormActionsPreComboSWNTind.setEnabled(False)

        self.horizontalLayout_30.addWidget(self.FormActionsPreComboSWNTind)


        self.verticalLayout_94.addWidget(self.groupBox_8)

        self.groupBox_2 = QGroupBox(self.tab_36)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_65 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.frame_12 = QFrame(self.groupBox_2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_100 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_100.setObjectName(u"horizontalLayout_100")
        self.FormActionsPreRadioSWNTuselen = QRadioButton(self.frame_12)
        self.FormActionsPreRadioSWNTuselen.setObjectName(u"FormActionsPreRadioSWNTuselen")
        self.FormActionsPreRadioSWNTuselen.setChecked(True)

        self.horizontalLayout_100.addWidget(self.FormActionsPreRadioSWNTuselen)

        self.FormActionsPreLineSWNTlen = QDoubleSpinBox(self.frame_12)
        self.FormActionsPreLineSWNTlen.setObjectName(u"FormActionsPreLineSWNTlen")
        self.FormActionsPreLineSWNTlen.setMinimumSize(QSize(0, 24))
        self.FormActionsPreLineSWNTlen.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPreLineSWNTlen.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreLineSWNTlen.setSingleStep(0.500000000000000)
        self.FormActionsPreLineSWNTlen.setValue(9.800000000000001)

        self.horizontalLayout_100.addWidget(self.FormActionsPreLineSWNTlen)


        self.verticalLayout_65.addWidget(self.frame_12)

        self.frame_97 = QFrame(self.groupBox_2)
        self.frame_97.setObjectName(u"frame_97")
        self.frame_97.setFrameShape(QFrame.NoFrame)
        self.frame_97.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_101 = QHBoxLayout(self.frame_97)
        self.horizontalLayout_101.setObjectName(u"horizontalLayout_101")
        self.radioButton_2 = QRadioButton(self.frame_97)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_101.addWidget(self.radioButton_2)

        self.FormActionsPreLineSWNTcells = QSpinBox(self.frame_97)
        self.FormActionsPreLineSWNTcells.setObjectName(u"FormActionsPreLineSWNTcells")
        self.FormActionsPreLineSWNTcells.setMinimumSize(QSize(0, 24))
        self.FormActionsPreLineSWNTcells.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPreLineSWNTcells.setValue(1)

        self.horizontalLayout_101.addWidget(self.FormActionsPreLineSWNTcells)


        self.verticalLayout_65.addWidget(self.frame_97)


        self.verticalLayout_94.addWidget(self.groupBox_2)

        self.frame_23 = QFrame(self.tab_36)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(0, 0))
        self.frame_23.setMaximumSize(QSize(16777215, 16777215))
        self.frame_23.setFrameShape(QFrame.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_15 = QSpacerItem(115, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_15)

        self.FormActionsPreButSWNTGenerate = QPushButton(self.frame_23)
        self.FormActionsPreButSWNTGenerate.setObjectName(u"FormActionsPreButSWNTGenerate")

        self.horizontalLayout_13.addWidget(self.FormActionsPreButSWNTGenerate)

        self.horizontalSpacer_16 = QSpacerItem(115, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_16)


        self.verticalLayout_94.addWidget(self.frame_23)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_94.addItem(self.verticalSpacer_4)

        self.tabWidget_11.addTab(self.tab_36, "")
        self.tab_37 = QWidget()
        self.tab_37.setObjectName(u"tab_37")
        self.tabWidget_11.addTab(self.tab_37, "")
        self.tab_38 = QWidget()
        self.tab_38.setObjectName(u"tab_38")
        self.verticalLayout_96 = QVBoxLayout(self.tab_38)
        self.verticalLayout_96.setObjectName(u"verticalLayout_96")
        self.frame_116 = QFrame(self.tab_38)
        self.frame_116.setObjectName(u"frame_116")
        self.frame_116.setFrameShape(QFrame.StyledPanel)
        self.frame_116.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_118 = QHBoxLayout(self.frame_116)
        self.horizontalLayout_118.setObjectName(u"horizontalLayout_118")
        self.label_88 = QLabel(self.frame_116)
        self.label_88.setObjectName(u"label_88")

        self.horizontalLayout_118.addWidget(self.label_88)

        self.FormNanotypeTypeSelector = QComboBox(self.frame_116)
        self.FormNanotypeTypeSelector.setObjectName(u"FormNanotypeTypeSelector")

        self.horizontalLayout_118.addWidget(self.FormNanotypeTypeSelector)


        self.verticalLayout_96.addWidget(self.frame_116)

        self.groupBox_31 = QGroupBox(self.tab_38)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_121 = QHBoxLayout(self.groupBox_31)
        self.horizontalLayout_121.setObjectName(u"horizontalLayout_121")
        self.FormBiElementRadioArm = QRadioButton(self.groupBox_31)
        self.FormBiElementRadioArm.setObjectName(u"FormBiElementRadioArm")
        self.FormBiElementRadioArm.setChecked(True)

        self.horizontalLayout_121.addWidget(self.FormBiElementRadioArm)

        self.radioButton_3 = QRadioButton(self.groupBox_31)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_121.addWidget(self.radioButton_3)

        self.horizontalSpacer_80 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_121.addItem(self.horizontalSpacer_80)

        self.label_89 = QLabel(self.groupBox_31)
        self.label_89.setObjectName(u"label_89")

        self.horizontalLayout_121.addWidget(self.label_89)

        self.FormBiElementN = QSpinBox(self.groupBox_31)
        self.FormBiElementN.setObjectName(u"FormBiElementN")
        self.FormBiElementN.setMinimum(1)
        self.FormBiElementN.setValue(5)

        self.horizontalLayout_121.addWidget(self.FormBiElementN)


        self.verticalLayout_96.addWidget(self.groupBox_31)

        self.frame_117 = QFrame(self.tab_38)
        self.frame_117.setObjectName(u"frame_117")
        self.frame_117.setFrameShape(QFrame.StyledPanel)
        self.frame_117.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_119 = QHBoxLayout(self.frame_117)
        self.horizontalLayout_119.setObjectName(u"horizontalLayout_119")
        self.FormActionsPreRadioSWNTuselen_2 = QRadioButton(self.frame_117)
        self.FormActionsPreRadioSWNTuselen_2.setObjectName(u"FormActionsPreRadioSWNTuselen_2")
        self.FormActionsPreRadioSWNTuselen_2.setChecked(True)

        self.horizontalLayout_119.addWidget(self.FormActionsPreRadioSWNTuselen_2)

        self.FormBiElementLen = QDoubleSpinBox(self.frame_117)
        self.FormBiElementLen.setObjectName(u"FormBiElementLen")
        self.FormBiElementLen.setMinimumSize(QSize(0, 24))
        self.FormBiElementLen.setMaximumSize(QSize(16777215, 24))
        self.FormBiElementLen.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormBiElementLen.setSingleStep(0.500000000000000)
        self.FormBiElementLen.setValue(9.800000000000001)

        self.horizontalLayout_119.addWidget(self.FormBiElementLen)


        self.verticalLayout_96.addWidget(self.frame_117)

        self.frame_118 = QFrame(self.tab_38)
        self.frame_118.setObjectName(u"frame_118")
        self.frame_118.setFrameShape(QFrame.StyledPanel)
        self.frame_118.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_120 = QHBoxLayout(self.frame_118)
        self.horizontalLayout_120.setObjectName(u"horizontalLayout_120")
        self.horizontalSpacer_78 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_120.addItem(self.horizontalSpacer_78)

        self.FormActionsPreButBiElementGenerate = QPushButton(self.frame_118)
        self.FormActionsPreButBiElementGenerate.setObjectName(u"FormActionsPreButBiElementGenerate")
        self.FormActionsPreButBiElementGenerate.setEnabled(True)

        self.horizontalLayout_120.addWidget(self.FormActionsPreButBiElementGenerate)

        self.horizontalSpacer_79 = QSpacerItem(117, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_120.addItem(self.horizontalSpacer_79)


        self.verticalLayout_96.addWidget(self.frame_118)

        self.verticalSpacer_29 = QSpacerItem(20, 270, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_96.addItem(self.verticalSpacer_29)

        self.tabWidget_11.addTab(self.tab_38, "")

        self.verticalLayout_95.addWidget(self.tabWidget_11)

        self.toolBox.addItem(self.page_4, u"Nanotubes")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.verticalLayout_93 = QVBoxLayout(self.page_6)
        self.verticalLayout_93.setObjectName(u"verticalLayout_93")
        self.groupBox_40 = QGroupBox(self.page_6)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.groupBox_40.setEnabled(True)
        self.verticalLayout_92 = QVBoxLayout(self.groupBox_40)
        self.verticalLayout_92.setObjectName(u"verticalLayout_92")
        self.frame_138 = QFrame(self.groupBox_40)
        self.frame_138.setObjectName(u"frame_138")
        self.frame_138.setEnabled(True)
        self.frame_138.setFrameShape(QFrame.NoFrame)
        self.frame_138.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_148 = QHBoxLayout(self.frame_138)
        self.horizontalLayout_148.setObjectName(u"horizontalLayout_148")
        self.label_108 = QLabel(self.frame_138)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setEnabled(True)

        self.horizontalLayout_148.addWidget(self.label_108)

        self.FormActionsPreLeftElectrode_2 = QLineEdit(self.frame_138)
        self.FormActionsPreLeftElectrode_2.setObjectName(u"FormActionsPreLeftElectrode_2")
        self.FormActionsPreLeftElectrode_2.setReadOnly(True)

        self.horizontalLayout_148.addWidget(self.FormActionsPreLeftElectrode_2)

        self.FormSelectPart1File = QPushButton(self.frame_138)
        self.FormSelectPart1File.setObjectName(u"FormSelectPart1File")

        self.horizontalLayout_148.addWidget(self.FormSelectPart1File)


        self.verticalLayout_92.addWidget(self.frame_138)

        self.groupBox_41 = QGroupBox(self.groupBox_40)
        self.groupBox_41.setObjectName(u"groupBox_41")
        self.groupBox_41.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_150 = QHBoxLayout(self.groupBox_41)
        self.horizontalLayout_150.setObjectName(u"horizontalLayout_150")
        self.label_113 = QLabel(self.groupBox_41)
        self.label_113.setObjectName(u"label_113")

        self.horizontalLayout_150.addWidget(self.label_113)

        self.FormPart1RotX = QDoubleSpinBox(self.groupBox_41)
        self.FormPart1RotX.setObjectName(u"FormPart1RotX")
        self.FormPart1RotX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1RotX.setMinimum(-360.000000000000000)
        self.FormPart1RotX.setMaximum(360.000000000000000)

        self.horizontalLayout_150.addWidget(self.FormPart1RotX)

        self.label_114 = QLabel(self.groupBox_41)
        self.label_114.setObjectName(u"label_114")

        self.horizontalLayout_150.addWidget(self.label_114)

        self.FormPart1RotY = QDoubleSpinBox(self.groupBox_41)
        self.FormPart1RotY.setObjectName(u"FormPart1RotY")
        self.FormPart1RotY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1RotY.setMinimum(-360.000000000000000)
        self.FormPart1RotY.setMaximum(360.000000000000000)

        self.horizontalLayout_150.addWidget(self.FormPart1RotY)

        self.label_115 = QLabel(self.groupBox_41)
        self.label_115.setObjectName(u"label_115")

        self.horizontalLayout_150.addWidget(self.label_115)

        self.FormPart1RotZ = QDoubleSpinBox(self.groupBox_41)
        self.FormPart1RotZ.setObjectName(u"FormPart1RotZ")
        self.FormPart1RotZ.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1RotZ.setMinimum(-360.000000000000000)
        self.FormPart1RotZ.setMaximum(360.000000000000000)

        self.horizontalLayout_150.addWidget(self.FormPart1RotZ)


        self.verticalLayout_92.addWidget(self.groupBox_41)

        self.groupBox_42 = QGroupBox(self.groupBox_40)
        self.groupBox_42.setObjectName(u"groupBox_42")
        self.horizontalLayout_147 = QHBoxLayout(self.groupBox_42)
        self.horizontalLayout_147.setObjectName(u"horizontalLayout_147")
        self.FormPart1CMx = QDoubleSpinBox(self.groupBox_42)
        self.FormPart1CMx.setObjectName(u"FormPart1CMx")
        self.FormPart1CMx.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1CMx.setMinimum(-99.000000000000000)

        self.horizontalLayout_147.addWidget(self.FormPart1CMx)

        self.horizontalSpacer_104 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_147.addItem(self.horizontalSpacer_104)

        self.FormPart1CMy = QDoubleSpinBox(self.groupBox_42)
        self.FormPart1CMy.setObjectName(u"FormPart1CMy")
        self.FormPart1CMy.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1CMy.setMinimum(-99.000000000000000)

        self.horizontalLayout_147.addWidget(self.FormPart1CMy)

        self.horizontalSpacer_105 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_147.addItem(self.horizontalSpacer_105)

        self.FormPart1CMz = QDoubleSpinBox(self.groupBox_42)
        self.FormPart1CMz.setObjectName(u"FormPart1CMz")
        self.FormPart1CMz.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart1CMz.setMinimum(-99.000000000000000)

        self.horizontalLayout_147.addWidget(self.FormPart1CMz)


        self.verticalLayout_92.addWidget(self.groupBox_42)


        self.verticalLayout_93.addWidget(self.groupBox_40)

        self.groupBox_38 = QGroupBox(self.page_6)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setEnabled(True)
        self.verticalLayout_91 = QVBoxLayout(self.groupBox_38)
        self.verticalLayout_91.setObjectName(u"verticalLayout_91")
        self.frame_86 = QFrame(self.groupBox_38)
        self.frame_86.setObjectName(u"frame_86")
        self.frame_86.setFrameShape(QFrame.NoFrame)
        self.frame_86.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_117 = QHBoxLayout(self.frame_86)
        self.horizontalLayout_117.setObjectName(u"horizontalLayout_117")
        self.label_95 = QLabel(self.frame_86)
        self.label_95.setObjectName(u"label_95")

        self.horizontalLayout_117.addWidget(self.label_95)

        self.FormActionsPreScatRegion_2 = QLineEdit(self.frame_86)
        self.FormActionsPreScatRegion_2.setObjectName(u"FormActionsPreScatRegion_2")
        self.FormActionsPreScatRegion_2.setReadOnly(True)

        self.horizontalLayout_117.addWidget(self.FormActionsPreScatRegion_2)

        self.FormSelectPart2File = QPushButton(self.frame_86)
        self.FormSelectPart2File.setObjectName(u"FormSelectPart2File")

        self.horizontalLayout_117.addWidget(self.FormSelectPart2File)


        self.verticalLayout_91.addWidget(self.frame_86)

        self.groupBox_39 = QGroupBox(self.groupBox_38)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.groupBox_39.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_146 = QHBoxLayout(self.groupBox_39)
        self.horizontalLayout_146.setObjectName(u"horizontalLayout_146")
        self.label_97 = QLabel(self.groupBox_39)
        self.label_97.setObjectName(u"label_97")

        self.horizontalLayout_146.addWidget(self.label_97)

        self.FormPart2RotX = QDoubleSpinBox(self.groupBox_39)
        self.FormPart2RotX.setObjectName(u"FormPart2RotX")
        self.FormPart2RotX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2RotX.setMinimum(-360.000000000000000)
        self.FormPart2RotX.setMaximum(360.000000000000000)

        self.horizontalLayout_146.addWidget(self.FormPart2RotX)

        self.label_98 = QLabel(self.groupBox_39)
        self.label_98.setObjectName(u"label_98")

        self.horizontalLayout_146.addWidget(self.label_98)

        self.FormPart2RotY = QDoubleSpinBox(self.groupBox_39)
        self.FormPart2RotY.setObjectName(u"FormPart2RotY")
        self.FormPart2RotY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2RotY.setMinimum(-360.000000000000000)
        self.FormPart2RotY.setMaximum(360.000000000000000)

        self.horizontalLayout_146.addWidget(self.FormPart2RotY)

        self.label_103 = QLabel(self.groupBox_39)
        self.label_103.setObjectName(u"label_103")

        self.horizontalLayout_146.addWidget(self.label_103)

        self.FormPart2RotZ = QDoubleSpinBox(self.groupBox_39)
        self.FormPart2RotZ.setObjectName(u"FormPart2RotZ")
        self.FormPart2RotZ.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2RotZ.setMinimum(-360.000000000000000)
        self.FormPart2RotZ.setMaximum(360.000000000000000)

        self.horizontalLayout_146.addWidget(self.FormPart2RotZ)


        self.verticalLayout_91.addWidget(self.groupBox_39)

        self.groupBox_43 = QGroupBox(self.groupBox_38)
        self.groupBox_43.setObjectName(u"groupBox_43")
        self.horizontalLayout_149 = QHBoxLayout(self.groupBox_43)
        self.horizontalLayout_149.setObjectName(u"horizontalLayout_149")
        self.FormPart2CMx = QDoubleSpinBox(self.groupBox_43)
        self.FormPart2CMx.setObjectName(u"FormPart2CMx")
        self.FormPart2CMx.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2CMx.setMinimum(-99.000000000000000)

        self.horizontalLayout_149.addWidget(self.FormPart2CMx)

        self.horizontalSpacer_102 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_149.addItem(self.horizontalSpacer_102)

        self.FormPart2CMy = QDoubleSpinBox(self.groupBox_43)
        self.FormPart2CMy.setObjectName(u"FormPart2CMy")
        self.FormPart2CMy.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2CMy.setMinimum(-99.000000000000000)

        self.horizontalLayout_149.addWidget(self.FormPart2CMy)

        self.horizontalSpacer_103 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_149.addItem(self.horizontalSpacer_103)

        self.FormPart2CMz = QDoubleSpinBox(self.groupBox_43)
        self.FormPart2CMz.setObjectName(u"FormPart2CMz")
        self.FormPart2CMz.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormPart2CMz.setMinimum(-99.000000000000000)

        self.horizontalLayout_149.addWidget(self.FormPart2CMz)


        self.verticalLayout_91.addWidget(self.groupBox_43)


        self.verticalLayout_93.addWidget(self.groupBox_38)

        self.frame_143 = QFrame(self.page_6)
        self.frame_143.setObjectName(u"frame_143")
        self.frame_143.setFrameShape(QFrame.StyledPanel)
        self.frame_143.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_151 = QHBoxLayout(self.frame_143)
        self.horizontalLayout_151.setObjectName(u"horizontalLayout_151")
        self.horizontalSpacer_106 = QSpacerItem(106, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_151.addItem(self.horizontalSpacer_106)

        self.FormCreateModelFromParts = QPushButton(self.frame_143)
        self.FormCreateModelFromParts.setObjectName(u"FormCreateModelFromParts")

        self.horizontalLayout_151.addWidget(self.FormCreateModelFromParts)

        self.horizontalSpacer_107 = QSpacerItem(106, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_151.addItem(self.horizontalSpacer_107)


        self.verticalLayout_93.addWidget(self.frame_143)

        self.verticalSpacer_16 = QSpacerItem(20, 68, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_93.addItem(self.verticalSpacer_16)

        self.toolBox.addItem(self.page_6, u"From two parts")
        self.page_22 = QWidget()
        self.page_22.setObjectName(u"page_22")
        self.page_22.setEnabled(True)
        self.page_22.setGeometry(QRect(0, 0, 350, 700))
        self.verticalLayout_32 = QVBoxLayout(self.page_22)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.groupBox_13 = QGroupBox(self.page_22)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setEnabled(True)
        self.verticalLayout_34 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.frame_42 = QFrame(self.groupBox_13)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setEnabled(True)
        self.frame_42.setFrameShape(QFrame.NoFrame)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_37 = QLabel(self.frame_42)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setEnabled(True)

        self.horizontalLayout_39.addWidget(self.label_37)

        self.FormActionsPreLeftElectrode = QLineEdit(self.frame_42)
        self.FormActionsPreLeftElectrode.setObjectName(u"FormActionsPreLeftElectrode")
        self.FormActionsPreLeftElectrode.setReadOnly(True)

        self.horizontalLayout_39.addWidget(self.FormActionsPreLeftElectrode)

        self.FormActionsPreButSelectLeftElectrode = QPushButton(self.frame_42)
        self.FormActionsPreButSelectLeftElectrode.setObjectName(u"FormActionsPreButSelectLeftElectrode")

        self.horizontalLayout_39.addWidget(self.FormActionsPreButSelectLeftElectrode)


        self.verticalLayout_34.addWidget(self.frame_42)

        self.frame_103 = QFrame(self.groupBox_13)
        self.frame_103.setObjectName(u"frame_103")
        self.frame_103.setMinimumSize(QSize(0, 0))
        self.frame_103.setFrameShape(QFrame.StyledPanel)
        self.frame_103.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_107 = QHBoxLayout(self.frame_103)
        self.horizontalLayout_107.setObjectName(u"horizontalLayout_107")
        self.label_63 = QLabel(self.frame_103)
        self.label_63.setObjectName(u"label_63")

        self.horizontalLayout_107.addWidget(self.label_63)

        self.FormActionsPreMoveLeftElectrodeX = QDoubleSpinBox(self.frame_103)
        self.FormActionsPreMoveLeftElectrodeX.setObjectName(u"FormActionsPreMoveLeftElectrodeX")
        self.FormActionsPreMoveLeftElectrodeX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveLeftElectrodeX.setMinimum(-99.000000000000000)

        self.horizontalLayout_107.addWidget(self.FormActionsPreMoveLeftElectrodeX)

        self.label_65 = QLabel(self.frame_103)
        self.label_65.setObjectName(u"label_65")

        self.horizontalLayout_107.addWidget(self.label_65)

        self.horizontalSpacer_51 = QSpacerItem(55, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_107.addItem(self.horizontalSpacer_51)

        self.label_64 = QLabel(self.frame_103)
        self.label_64.setObjectName(u"label_64")

        self.horizontalLayout_107.addWidget(self.label_64)

        self.FormActionsPreMoveLeftElectrodeY = QDoubleSpinBox(self.frame_103)
        self.FormActionsPreMoveLeftElectrodeY.setObjectName(u"FormActionsPreMoveLeftElectrodeY")
        self.FormActionsPreMoveLeftElectrodeY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveLeftElectrodeY.setMinimum(-99.000000000000000)

        self.horizontalLayout_107.addWidget(self.FormActionsPreMoveLeftElectrodeY)

        self.label_66 = QLabel(self.frame_103)
        self.label_66.setObjectName(u"label_66")

        self.horizontalLayout_107.addWidget(self.label_66)


        self.verticalLayout_34.addWidget(self.frame_103)

        self.frame_45 = QFrame(self.groupBox_13)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setEnabled(True)
        self.frame_45.setMinimumSize(QSize(0, 0))
        self.frame_45.setFrameShape(QFrame.NoFrame)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_41 = QLabel(self.frame_45)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setEnabled(True)

        self.horizontalLayout_38.addWidget(self.label_41)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_19)

        self.FormActionsPreSpinLeftElectrodeDist = QDoubleSpinBox(self.frame_45)
        self.FormActionsPreSpinLeftElectrodeDist.setObjectName(u"FormActionsPreSpinLeftElectrodeDist")
        self.FormActionsPreSpinLeftElectrodeDist.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreSpinLeftElectrodeDist.setMinimum(-99.000000000000000)

        self.horizontalLayout_38.addWidget(self.FormActionsPreSpinLeftElectrodeDist)


        self.verticalLayout_34.addWidget(self.frame_45)


        self.verticalLayout_32.addWidget(self.groupBox_13)

        self.groupBox_14 = QGroupBox(self.page_22)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setEnabled(True)
        self.verticalLayout_33 = QVBoxLayout(self.groupBox_14)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.frame_37 = QFrame(self.groupBox_14)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.NoFrame)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_38 = QLabel(self.frame_37)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_36.addWidget(self.label_38)

        self.FormActionsPreScatRegion = QLineEdit(self.frame_37)
        self.FormActionsPreScatRegion.setObjectName(u"FormActionsPreScatRegion")
        self.FormActionsPreScatRegion.setReadOnly(True)

        self.horizontalLayout_36.addWidget(self.FormActionsPreScatRegion)

        self.FormActionsPreButSelectScatRegione = QPushButton(self.frame_37)
        self.FormActionsPreButSelectScatRegione.setObjectName(u"FormActionsPreButSelectScatRegione")

        self.horizontalLayout_36.addWidget(self.FormActionsPreButSelectScatRegione)


        self.verticalLayout_33.addWidget(self.frame_37)

        self.groupBox_36 = QGroupBox(self.groupBox_14)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_140 = QHBoxLayout(self.groupBox_36)
        self.horizontalLayout_140.setObjectName(u"horizontalLayout_140")
        self.label_78 = QLabel(self.groupBox_36)
        self.label_78.setObjectName(u"label_78")

        self.horizontalLayout_140.addWidget(self.label_78)

        self.FormActionsPreSpinScatRotX = QDoubleSpinBox(self.groupBox_36)
        self.FormActionsPreSpinScatRotX.setObjectName(u"FormActionsPreSpinScatRotX")
        self.FormActionsPreSpinScatRotX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreSpinScatRotX.setMinimum(-360.000000000000000)
        self.FormActionsPreSpinScatRotX.setMaximum(360.000000000000000)

        self.horizontalLayout_140.addWidget(self.FormActionsPreSpinScatRotX)

        self.label_79 = QLabel(self.groupBox_36)
        self.label_79.setObjectName(u"label_79")

        self.horizontalLayout_140.addWidget(self.label_79)

        self.FormActionsPreSpinScatRotY = QDoubleSpinBox(self.groupBox_36)
        self.FormActionsPreSpinScatRotY.setObjectName(u"FormActionsPreSpinScatRotY")
        self.FormActionsPreSpinScatRotY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreSpinScatRotY.setMinimum(-360.000000000000000)
        self.FormActionsPreSpinScatRotY.setMaximum(360.000000000000000)

        self.horizontalLayout_140.addWidget(self.FormActionsPreSpinScatRotY)

        self.label_80 = QLabel(self.groupBox_36)
        self.label_80.setObjectName(u"label_80")

        self.horizontalLayout_140.addWidget(self.label_80)

        self.FormActionsPreSpinScatRotZ = QDoubleSpinBox(self.groupBox_36)
        self.FormActionsPreSpinScatRotZ.setObjectName(u"FormActionsPreSpinScatRotZ")
        self.FormActionsPreSpinScatRotZ.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreSpinScatRotZ.setMinimum(-360.000000000000000)
        self.FormActionsPreSpinScatRotZ.setMaximum(360.000000000000000)

        self.horizontalLayout_140.addWidget(self.FormActionsPreSpinScatRotZ)


        self.verticalLayout_33.addWidget(self.groupBox_36)

        self.frame_104 = QFrame(self.groupBox_14)
        self.frame_104.setObjectName(u"frame_104")
        self.frame_104.setMinimumSize(QSize(0, 0))
        self.frame_104.setFrameShape(QFrame.StyledPanel)
        self.frame_104.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_109 = QHBoxLayout(self.frame_104)
        self.horizontalLayout_109.setObjectName(u"horizontalLayout_109")
        self.label_73 = QLabel(self.frame_104)
        self.label_73.setObjectName(u"label_73")

        self.horizontalLayout_109.addWidget(self.label_73)

        self.FormActionsPreMoveScatX = QDoubleSpinBox(self.frame_104)
        self.FormActionsPreMoveScatX.setObjectName(u"FormActionsPreMoveScatX")
        self.FormActionsPreMoveScatX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveScatX.setMinimum(-99.000000000000000)

        self.horizontalLayout_109.addWidget(self.FormActionsPreMoveScatX)

        self.label_71 = QLabel(self.frame_104)
        self.label_71.setObjectName(u"label_71")

        self.horizontalLayout_109.addWidget(self.label_71)

        self.horizontalSpacer_75 = QSpacerItem(52, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_109.addItem(self.horizontalSpacer_75)

        self.label_74 = QLabel(self.frame_104)
        self.label_74.setObjectName(u"label_74")

        self.horizontalLayout_109.addWidget(self.label_74)

        self.FormActionsPreMoveScatY = QDoubleSpinBox(self.frame_104)
        self.FormActionsPreMoveScatY.setObjectName(u"FormActionsPreMoveScatY")
        self.FormActionsPreMoveScatY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveScatY.setMinimum(-99.000000000000000)

        self.horizontalLayout_109.addWidget(self.FormActionsPreMoveScatY)

        self.label_72 = QLabel(self.frame_104)
        self.label_72.setObjectName(u"label_72")

        self.horizontalLayout_109.addWidget(self.label_72)

        self.horizontalSpacer_74 = QSpacerItem(37, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_109.addItem(self.horizontalSpacer_74)


        self.verticalLayout_33.addWidget(self.frame_104)


        self.verticalLayout_32.addWidget(self.groupBox_14)

        self.groupBox_19 = QGroupBox(self.page_22)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.verticalLayout_35 = QVBoxLayout(self.groupBox_19)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.frame_44 = QFrame(self.groupBox_19)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.NoFrame)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_39 = QLabel(self.frame_44)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_40.addWidget(self.label_39)

        self.FormActionsPreRightElectrode = QLineEdit(self.frame_44)
        self.FormActionsPreRightElectrode.setObjectName(u"FormActionsPreRightElectrode")
        self.FormActionsPreRightElectrode.setReadOnly(True)

        self.horizontalLayout_40.addWidget(self.FormActionsPreRightElectrode)

        self.FormActionsPreButSelectRightElectrode = QPushButton(self.frame_44)
        self.FormActionsPreButSelectRightElectrode.setObjectName(u"FormActionsPreButSelectRightElectrode")

        self.horizontalLayout_40.addWidget(self.FormActionsPreButSelectRightElectrode)


        self.verticalLayout_35.addWidget(self.frame_44)

        self.frame_105 = QFrame(self.groupBox_19)
        self.frame_105.setObjectName(u"frame_105")
        self.frame_105.setMinimumSize(QSize(0, 0))
        self.frame_105.setFrameShape(QFrame.StyledPanel)
        self.frame_105.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_108 = QHBoxLayout(self.frame_105)
        self.horizontalLayout_108.setObjectName(u"horizontalLayout_108")
        self.label_69 = QLabel(self.frame_105)
        self.label_69.setObjectName(u"label_69")

        self.horizontalLayout_108.addWidget(self.label_69)

        self.FormActionsPreMoveRightElectrodeX = QDoubleSpinBox(self.frame_105)
        self.FormActionsPreMoveRightElectrodeX.setObjectName(u"FormActionsPreMoveRightElectrodeX")
        self.FormActionsPreMoveRightElectrodeX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveRightElectrodeX.setMinimum(-99.000000000000000)

        self.horizontalLayout_108.addWidget(self.FormActionsPreMoveRightElectrodeX)

        self.label_67 = QLabel(self.frame_105)
        self.label_67.setObjectName(u"label_67")

        self.horizontalLayout_108.addWidget(self.label_67)

        self.horizontalSpacer_53 = QSpacerItem(52, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_108.addItem(self.horizontalSpacer_53)

        self.label_70 = QLabel(self.frame_105)
        self.label_70.setObjectName(u"label_70")

        self.horizontalLayout_108.addWidget(self.label_70)

        self.FormActionsPreMoveRightElectrodeY = QDoubleSpinBox(self.frame_105)
        self.FormActionsPreMoveRightElectrodeY.setObjectName(u"FormActionsPreMoveRightElectrodeY")
        self.FormActionsPreMoveRightElectrodeY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreMoveRightElectrodeY.setMinimum(-99.000000000000000)

        self.horizontalLayout_108.addWidget(self.FormActionsPreMoveRightElectrodeY)

        self.label_68 = QLabel(self.frame_105)
        self.label_68.setObjectName(u"label_68")

        self.horizontalLayout_108.addWidget(self.label_68)


        self.verticalLayout_35.addWidget(self.frame_105)

        self.frame_47 = QFrame(self.groupBox_19)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setMinimumSize(QSize(0, 0))
        self.frame_47.setFrameShape(QFrame.NoFrame)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_47)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_42 = QLabel(self.frame_47)
        self.label_42.setObjectName(u"label_42")

        self.horizontalLayout_41.addWidget(self.label_42)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_41.addItem(self.horizontalSpacer_20)

        self.FormActionsPreSpinRightElectrodeDist = QDoubleSpinBox(self.frame_47)
        self.FormActionsPreSpinRightElectrodeDist.setObjectName(u"FormActionsPreSpinRightElectrodeDist")
        self.FormActionsPreSpinRightElectrodeDist.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPreSpinRightElectrodeDist.setMinimum(-99.000000000000000)

        self.horizontalLayout_41.addWidget(self.FormActionsPreSpinRightElectrodeDist)


        self.verticalLayout_35.addWidget(self.frame_47)


        self.verticalLayout_32.addWidget(self.groupBox_19)

        self.frame_43 = QFrame(self.page_22)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setMinimumSize(QSize(0, 50))
        self.frame_43.setFrameShape(QFrame.NoFrame)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalSpacer_14 = QSpacerItem(93, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_14)

        self.FormActionsPreButCreateModelWithElectrodes = QPushButton(self.frame_43)
        self.FormActionsPreButCreateModelWithElectrodes.setObjectName(u"FormActionsPreButCreateModelWithElectrodes")

        self.horizontalLayout_37.addWidget(self.FormActionsPreButCreateModelWithElectrodes)

        self.horizontalSpacer_17 = QSpacerItem(92, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_17)


        self.verticalLayout_32.addWidget(self.frame_43)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer_2)

        self.toolBox.addItem(self.page_22, u"Model with electrodes")

        self.verticalLayout_17.addWidget(self.toolBox)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout_16 = QVBoxLayout(self.tab_7)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.toolBox_6 = QToolBox(self.tab_7)
        self.toolBox_6.setObjectName(u"toolBox_6")
        self.toolBox_6.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.toolBox_6.sizePolicy().hasHeightForWidth())
        self.toolBox_6.setSizePolicy(sizePolicy2)
        self.page_29 = QWidget()
        self.page_29.setObjectName(u"page_29")
        self.page_29.setGeometry(QRect(0, 0, 337, 258))
        self.verticalLayout_26 = QVBoxLayout(self.page_29)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.frame_28 = QFrame(self.page_29)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMinimumSize(QSize(0, 150))
        self.frame_28.setMaximumSize(QSize(16777215, 150))
        self.frame_28.setFrameShape(QFrame.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.label_8 = QLabel(self.frame_28)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 10, 83, 26))
        self.FormActionsPreComboAtomsList = QComboBox(self.frame_28)
        self.FormActionsPreComboAtomsList.setObjectName(u"FormActionsPreComboAtomsList")
        self.FormActionsPreComboAtomsList.setGeometry(QRect(90, 10, 231, 22))
        self.FormActionsPreSpinAtomsCoordX = QDoubleSpinBox(self.frame_28)
        self.FormActionsPreSpinAtomsCoordX.setObjectName(u"FormActionsPreSpinAtomsCoordX")
        self.FormActionsPreSpinAtomsCoordX.setGeometry(QRect(40, 50, 111, 24))
        self.FormActionsPreSpinAtomsCoordX.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordX.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordX.setMaximum(999.990000000000009)
        self.label_24 = QLabel(self.frame_28)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(10, 50, 31, 26))
        self.FormActionsPreSpinAtomsCoordY = QDoubleSpinBox(self.frame_28)
        self.FormActionsPreSpinAtomsCoordY.setObjectName(u"FormActionsPreSpinAtomsCoordY")
        self.FormActionsPreSpinAtomsCoordY.setGeometry(QRect(40, 80, 111, 24))
        self.FormActionsPreSpinAtomsCoordY.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordY.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordY.setMaximum(999.990000000000009)
        self.label_25 = QLabel(self.frame_28)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 80, 21, 26))
        self.label_26 = QLabel(self.frame_28)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(10, 110, 21, 26))
        self.FormActionsPreSpinAtomsCoordZ = QDoubleSpinBox(self.frame_28)
        self.FormActionsPreSpinAtomsCoordZ.setObjectName(u"FormActionsPreSpinAtomsCoordZ")
        self.FormActionsPreSpinAtomsCoordZ.setGeometry(QRect(40, 110, 111, 24))
        self.FormActionsPreSpinAtomsCoordZ.setDecimals(5)
        self.FormActionsPreSpinAtomsCoordZ.setMinimum(-999.990000000000009)
        self.FormActionsPreSpinAtomsCoordZ.setMaximum(999.990000000000009)

        self.verticalLayout_26.addWidget(self.frame_28)

        self.frame_29 = QFrame(self.page_29)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 50))
        self.frame_29.setMaximumSize(QSize(16777215, 50))
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.FormActionsPreButDeleteAtom = QPushButton(self.frame_29)
        self.FormActionsPreButDeleteAtom.setObjectName(u"FormActionsPreButDeleteAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButDeleteAtom)

        self.FormActionsPreButModifyAtom = QPushButton(self.frame_29)
        self.FormActionsPreButModifyAtom.setObjectName(u"FormActionsPreButModifyAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButModifyAtom)

        self.FormActionsPreButAddAtom = QPushButton(self.frame_29)
        self.FormActionsPreButAddAtom.setObjectName(u"FormActionsPreButAddAtom")

        self.horizontalLayout_17.addWidget(self.FormActionsPreButAddAtom)


        self.verticalLayout_26.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.page_29)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.verticalLayout_56 = QVBoxLayout(self.frame_30)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")

        self.verticalLayout_26.addWidget(self.frame_30)

        self.toolBox_6.addItem(self.page_29, u"Add or Modify Atom")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 352, 209))
        self.verticalLayout_36 = QVBoxLayout(self.page)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.frame_49 = QFrame(self.page)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setMinimumSize(QSize(0, 180))
        self.frame_49.setFrameShape(QFrame.NoFrame)
        self.frame_49.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_49)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.frame_50 = QFrame(self.frame_49)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_50.setFrameShape(QFrame.NoFrame)
        self.frame_50.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.frame_50)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditA1 = QDoubleSpinBox(self.frame_50)
        self.FormModifyCellEditA1.setObjectName(u"FormModifyCellEditA1")
        self.FormModifyCellEditA1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA1.setDecimals(6)
        self.FormModifyCellEditA1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA1.setMaximum(999.000000000000000)

        self.horizontalLayout_44.addWidget(self.FormModifyCellEditA1)

        self.FormModifyCellEditA2 = QDoubleSpinBox(self.frame_50)
        self.FormModifyCellEditA2.setObjectName(u"FormModifyCellEditA2")
        self.FormModifyCellEditA2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA2.setDecimals(6)
        self.FormModifyCellEditA2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA2.setMaximum(999.000000000000000)

        self.horizontalLayout_44.addWidget(self.FormModifyCellEditA2)

        self.FormModifyCellEditA3 = QDoubleSpinBox(self.frame_50)
        self.FormModifyCellEditA3.setObjectName(u"FormModifyCellEditA3")
        self.FormModifyCellEditA3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditA3.setDecimals(6)
        self.FormModifyCellEditA3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditA3.setMaximum(999.000000000000000)

        self.horizontalLayout_44.addWidget(self.FormModifyCellEditA3)


        self.verticalLayout_37.addWidget(self.frame_50)

        self.frame_51 = QFrame(self.frame_49)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_51.setFrameShape(QFrame.NoFrame)
        self.frame_51.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_51)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditB1 = QDoubleSpinBox(self.frame_51)
        self.FormModifyCellEditB1.setObjectName(u"FormModifyCellEditB1")
        self.FormModifyCellEditB1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormModifyCellEditB1.setDecimals(6)
        self.FormModifyCellEditB1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB1.setMaximum(999.000000000000000)

        self.horizontalLayout_45.addWidget(self.FormModifyCellEditB1)

        self.FormModifyCellEditB2 = QDoubleSpinBox(self.frame_51)
        self.FormModifyCellEditB2.setObjectName(u"FormModifyCellEditB2")
        self.FormModifyCellEditB2.setDecimals(6)
        self.FormModifyCellEditB2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB2.setMaximum(999.000000000000000)

        self.horizontalLayout_45.addWidget(self.FormModifyCellEditB2)

        self.FormModifyCellEditB3 = QDoubleSpinBox(self.frame_51)
        self.FormModifyCellEditB3.setObjectName(u"FormModifyCellEditB3")
        self.FormModifyCellEditB3.setDecimals(6)
        self.FormModifyCellEditB3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditB3.setMaximum(999.000000000000000)

        self.horizontalLayout_45.addWidget(self.FormModifyCellEditB3)


        self.verticalLayout_37.addWidget(self.frame_51)

        self.frame_52 = QFrame(self.frame_49)
        self.frame_52.setObjectName(u"frame_52")
        self.frame_52.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_52.setFrameShape(QFrame.NoFrame)
        self.frame_52.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_52)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(-1, 2, -1, 2)
        self.FormModifyCellEditC1 = QDoubleSpinBox(self.frame_52)
        self.FormModifyCellEditC1.setObjectName(u"FormModifyCellEditC1")
        self.FormModifyCellEditC1.setDecimals(6)
        self.FormModifyCellEditC1.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC1.setMaximum(999.000000000000000)

        self.horizontalLayout_46.addWidget(self.FormModifyCellEditC1)

        self.FormModifyCellEditC2 = QDoubleSpinBox(self.frame_52)
        self.FormModifyCellEditC2.setObjectName(u"FormModifyCellEditC2")
        self.FormModifyCellEditC2.setDecimals(6)
        self.FormModifyCellEditC2.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC2.setMaximum(999.000000000000000)

        self.horizontalLayout_46.addWidget(self.FormModifyCellEditC2)

        self.FormModifyCellEditC3 = QDoubleSpinBox(self.frame_52)
        self.FormModifyCellEditC3.setObjectName(u"FormModifyCellEditC3")
        self.FormModifyCellEditC3.setDecimals(6)
        self.FormModifyCellEditC3.setMinimum(-999.000000000000000)
        self.FormModifyCellEditC3.setMaximum(999.000000000000000)

        self.horizontalLayout_46.addWidget(self.FormModifyCellEditC3)


        self.verticalLayout_37.addWidget(self.frame_52)

        self.frame_53 = QFrame(self.frame_49)
        self.frame_53.setObjectName(u"frame_53")
        self.frame_53.setFrameShape(QFrame.NoFrame)
        self.frame_53.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_48 = QHBoxLayout(self.frame_53)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalSpacer_21 = QSpacerItem(92, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_21)

        self.FormModifyCellButton = QPushButton(self.frame_53)
        self.FormModifyCellButton.setObjectName(u"FormModifyCellButton")

        self.horizontalLayout_48.addWidget(self.FormModifyCellButton)

        self.horizontalSpacer_9 = QSpacerItem(91, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_9)


        self.verticalLayout_37.addWidget(self.frame_53)


        self.verticalLayout_36.addWidget(self.frame_49)

        self.verticalSpacer_6 = QSpacerItem(20, 386, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_36.addItem(self.verticalSpacer_6)

        self.toolBox_6.addItem(self.page, u"Cell")
        self.page_28 = QWidget()
        self.page_28.setObjectName(u"page_28")
        self.page_28.setGeometry(QRect(0, 0, 307, 467))
        self.verticalLayout_10 = QVBoxLayout(self.page_28)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label = QLabel(self.page_28)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.label)

        self.FormActionsPreComboFillSpace = QComboBox(self.page_28)
        self.FormActionsPreComboFillSpace.setObjectName(u"FormActionsPreComboFillSpace")

        self.verticalLayout_10.addWidget(self.FormActionsPreComboFillSpace)

        self.frame_83 = QFrame(self.page_28)
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


        self.verticalLayout_10.addWidget(self.frame_83)

        self.frame_95 = QFrame(self.page_28)
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


        self.verticalLayout_10.addWidget(self.frame_95)

        self.frame_96 = QFrame(self.page_28)
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


        self.verticalLayout_10.addWidget(self.frame_96)

        self.frame_11 = QFrame(self.page_28)
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


        self.verticalLayout_10.addWidget(self.frame_11)

        self.FormActionsPreSaveToFileFillSpace = QCheckBox(self.page_28)
        self.FormActionsPreSaveToFileFillSpace.setObjectName(u"FormActionsPreSaveToFileFillSpace")

        self.verticalLayout_10.addWidget(self.FormActionsPreSaveToFileFillSpace)

        self.frame_82 = QFrame(self.page_28)
        self.frame_82.setObjectName(u"frame_82")
        self.frame_82.setFrameShape(QFrame.NoFrame)
        self.frame_82.setFrameShadow(QFrame.Raised)
        self.frame_82.setLineWidth(0)
        self.horizontalLayout_95 = QHBoxLayout(self.frame_82)
        self.horizontalLayout_95.setObjectName(u"horizontalLayout_95")
        self.horizontalLayout_95.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_72 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_95.addItem(self.horizontalSpacer_72)

        self.FormActionsPreButFillSpace = QPushButton(self.frame_82)
        self.FormActionsPreButFillSpace.setObjectName(u"FormActionsPreButFillSpace")

        self.horizontalLayout_95.addWidget(self.FormActionsPreButFillSpace)

        self.horizontalSpacer_71 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_95.addItem(self.horizontalSpacer_71)


        self.verticalLayout_10.addWidget(self.frame_82)

        self.verticalSpacer_24 = QSpacerItem(20, 183, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_24)

        self.toolBox_6.addItem(self.page_28, u"Fill Space")
        self.page_12 = QWidget()
        self.page_12.setObjectName(u"page_12")
        self.page_12.setGeometry(QRect(0, 0, 337, 79))
        self.verticalLayout_41 = QVBoxLayout(self.page_12)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.frame_58 = QFrame(self.page_12)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setEnabled(True)
        self.frame_58.setFrameShape(QFrame.NoFrame)
        self.frame_58.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_58)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.FormModifyGrowX = QPushButton(self.frame_58)
        self.FormModifyGrowX.setObjectName(u"FormModifyGrowX")

        self.horizontalLayout_50.addWidget(self.FormModifyGrowX)

        self.FormModifyGrowY = QPushButton(self.frame_58)
        self.FormModifyGrowY.setObjectName(u"FormModifyGrowY")

        self.horizontalLayout_50.addWidget(self.FormModifyGrowY)

        self.FormModifyGrowZ = QPushButton(self.frame_58)
        self.FormModifyGrowZ.setObjectName(u"FormModifyGrowZ")

        self.horizontalLayout_50.addWidget(self.FormModifyGrowZ)


        self.verticalLayout_41.addWidget(self.frame_58)

        self.verticalSpacer_8 = QSpacerItem(20, 400, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_41.addItem(self.verticalSpacer_8)

        self.toolBox_6.addItem(self.page_12, u"Grow model")
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.page_11.setGeometry(QRect(0, 0, 262, 233))
        self.verticalLayout_38 = QVBoxLayout(self.page_11)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.frame_6 = QFrame(self.page_11)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_73 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_73.setObjectName(u"horizontalLayout_73")
        self.horizontalLayout_73.setContentsMargins(0, -1, -1, -1)
        self.label_51 = QLabel(self.frame_6)
        self.label_51.setObjectName(u"label_51")

        self.horizontalLayout_73.addWidget(self.label_51)

        self.FormModifyRotationAngle = QDoubleSpinBox(self.frame_6)
        self.FormModifyRotationAngle.setObjectName(u"FormModifyRotationAngle")
        self.FormModifyRotationAngle.setDecimals(1)
        self.FormModifyRotationAngle.setMinimum(-360.000000000000000)
        self.FormModifyRotationAngle.setMaximum(360.000000000000000)

        self.horizontalLayout_73.addWidget(self.FormModifyRotationAngle)

        self.label_53 = QLabel(self.frame_6)
        self.label_53.setObjectName(u"label_53")

        self.horizontalLayout_73.addWidget(self.label_53)

        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_73.addItem(self.horizontalSpacer_41)


        self.verticalLayout_38.addWidget(self.frame_6)

        self.frame_56 = QFrame(self.page_11)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setFrameShape(QFrame.NoFrame)
        self.frame_56.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_49 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(50, 0, 0, 0)
        self.label_54 = QLabel(self.frame_56)
        self.label_54.setObjectName(u"label_54")

        self.horizontalLayout_49.addWidget(self.label_54)

        self.FormModifyRotationX = QRadioButton(self.frame_56)
        self.FormModifyRotationX.setObjectName(u"FormModifyRotationX")
        self.FormModifyRotationX.setChecked(True)

        self.horizontalLayout_49.addWidget(self.FormModifyRotationX)

        self.FormModifyRotationY = QRadioButton(self.frame_56)
        self.FormModifyRotationY.setObjectName(u"FormModifyRotationY")

        self.horizontalLayout_49.addWidget(self.FormModifyRotationY)

        self.FormModifyRotationZ = QRadioButton(self.frame_56)
        self.FormModifyRotationZ.setObjectName(u"FormModifyRotationZ")

        self.horizontalLayout_49.addWidget(self.FormModifyRotationZ)


        self.verticalLayout_38.addWidget(self.frame_56)

        self.frame_57 = QFrame(self.page_11)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setMinimumSize(QSize(0, 0))
        self.frame_57.setFrameShape(QFrame.NoFrame)
        self.frame_57.setFrameShadow(QFrame.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frame_57)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(50, -1, -1, -1)
        self.FormModifyRotationOrigin = QRadioButton(self.frame_57)
        self.FormModifyRotationOrigin.setObjectName(u"FormModifyRotationOrigin")
        self.FormModifyRotationOrigin.setChecked(True)

        self.verticalLayout_39.addWidget(self.FormModifyRotationOrigin)

        self.FormModifyRotationCenter = QRadioButton(self.frame_57)
        self.FormModifyRotationCenter.setObjectName(u"FormModifyRotationCenter")

        self.verticalLayout_39.addWidget(self.FormModifyRotationCenter)


        self.verticalLayout_38.addWidget(self.frame_57)

        self.frame_55 = QFrame(self.page_11)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setMinimumSize(QSize(0, 50))
        self.frame_55.setFrameShape(QFrame.NoFrame)
        self.frame_55.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_47 = QHBoxLayout(self.frame_55)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_47.addItem(self.horizontalSpacer_25)

        self.FormModifyRotation = QPushButton(self.frame_55)
        self.FormModifyRotation.setObjectName(u"FormModifyRotation")

        self.horizontalLayout_47.addWidget(self.FormModifyRotation)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_47.addItem(self.horizontalSpacer_24)


        self.verticalLayout_38.addWidget(self.frame_55)

        self.verticalSpacer_7 = QSpacerItem(20, 288, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_38.addItem(self.verticalSpacer_7)

        self.toolBox_6.addItem(self.page_11, u"Rotate model")

        self.verticalLayout_16.addWidget(self.toolBox_6)

        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_24 = QWidget()
        self.tab_24.setObjectName(u"tab_24")
        self.verticalLayout_78 = QVBoxLayout(self.tab_24)
        self.verticalLayout_78.setObjectName(u"verticalLayout_78")
        self.FormActionsPreTextFDF = QTextBrowser(self.tab_24)
        self.FormActionsPreTextFDF.setObjectName(u"FormActionsPreTextFDF")
        self.FormActionsPreTextFDF.setReadOnly(False)

        self.verticalLayout_78.addWidget(self.FormActionsPreTextFDF)

        self.frame_26 = QFrame(self.tab_24)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_10)

        self.FormActionsPreButFDFGenerate = QPushButton(self.frame_26)
        self.FormActionsPreButFDFGenerate.setObjectName(u"FormActionsPreButFDFGenerate")

        self.horizontalLayout_11.addWidget(self.FormActionsPreButFDFGenerate)

        self.horizontalSpacer_57 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_57)

        self.FormActionsPreButFDFToFile = QPushButton(self.frame_26)
        self.FormActionsPreButFDFToFile.setObjectName(u"FormActionsPreButFDFToFile")

        self.horizontalLayout_11.addWidget(self.FormActionsPreButFDFToFile)

        self.horizontalSpacer_56 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_56)


        self.verticalLayout_78.addWidget(self.frame_26)

        self.tabWidget_3.addTab(self.tab_24, "")

        self.verticalLayout_2.addWidget(self.tabWidget_3)

        self.tabWidget.addTab(self.FormTabActions, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_8 = QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.toolBox_2 = QToolBox(self.tab)
        self.toolBox_2.setObjectName(u"toolBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.toolBox_2.sizePolicy().hasHeightForWidth())
        self.toolBox_2.setSizePolicy(sizePolicy3)
        self.toolBox_2.setMinimumSize(QSize(0, 600))
        self.toolBox_2.setLayoutDirection(Qt.LeftToRight)
        self.toolBox_2.setAutoFillBackground(False)
        self.toolBox_2.setStyleSheet(u"")
        self.page_19 = QWidget()
        self.page_19.setObjectName(u"page_19")
        self.page_19.setGeometry(QRect(0, 0, 399, 675))
        self.verticalLayout_6 = QVBoxLayout(self.page_19)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_5 = QTabWidget(self.page_19)
        self.tabWidget_5.setObjectName(u"tabWidget_5")
        self.tab_18 = QWidget()
        self.tab_18.setObjectName(u"tab_18")
        self.verticalLayout_7 = QVBoxLayout(self.tab_18)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.FormActionsLineBANDSfile = QLineEdit(self.tab_18)
        self.FormActionsLineBANDSfile.setObjectName(u"FormActionsLineBANDSfile")

        self.verticalLayout_7.addWidget(self.FormActionsLineBANDSfile)

        self.frame_54 = QFrame(self.tab_18)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setFrameShape(QFrame.NoFrame)
        self.frame_54.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_94 = QHBoxLayout(self.frame_54)
        self.horizontalLayout_94.setObjectName(u"horizontalLayout_94")
        self.horizontalSpacer_70 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_94.addItem(self.horizontalSpacer_70)

        self.FormActionsButtonParseBANDS = QPushButton(self.frame_54)
        self.FormActionsButtonParseBANDS.setObjectName(u"FormActionsButtonParseBANDS")
        self.FormActionsButtonParseBANDS.setEnabled(False)

        self.horizontalLayout_94.addWidget(self.FormActionsButtonParseBANDS)

        self.horizontalSpacer_69 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_94.addItem(self.horizontalSpacer_69)


        self.verticalLayout_7.addWidget(self.frame_54)

        self.groupBox_15 = QGroupBox(self.tab_18)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMinimumSize(QSize(0, 0))
        self.groupBox_15.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_19 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 2, -1, 5)
        self.FormActionsSpinBANDSxmin = QDoubleSpinBox(self.groupBox_15)
        self.FormActionsSpinBANDSxmin.setObjectName(u"FormActionsSpinBANDSxmin")

        self.horizontalLayout_19.addWidget(self.FormActionsSpinBANDSxmin)

        self.FormActionsSpinBANDSxmax = QDoubleSpinBox(self.groupBox_15)
        self.FormActionsSpinBANDSxmax.setObjectName(u"FormActionsSpinBANDSxmax")

        self.horizontalLayout_19.addWidget(self.FormActionsSpinBANDSxmax)


        self.verticalLayout_7.addWidget(self.groupBox_15)

        self.groupBox_16 = QGroupBox(self.tab_18)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setMinimumSize(QSize(0, 0))
        self.groupBox_16.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_22 = QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 2, -1, 5)
        self.FormActionsSpinBANDSemin = QDoubleSpinBox(self.groupBox_16)
        self.FormActionsSpinBANDSemin.setObjectName(u"FormActionsSpinBANDSemin")

        self.horizontalLayout_22.addWidget(self.FormActionsSpinBANDSemin)

        self.FormActionsSpinBANDSemax = QDoubleSpinBox(self.groupBox_16)
        self.FormActionsSpinBANDSemax.setObjectName(u"FormActionsSpinBANDSemax")

        self.horizontalLayout_22.addWidget(self.FormActionsSpinBANDSemax)


        self.verticalLayout_7.addWidget(self.groupBox_16)

        self.FormActionsCheckBANDSfermyShow = QCheckBox(self.tab_18)
        self.FormActionsCheckBANDSfermyShow.setObjectName(u"FormActionsCheckBANDSfermyShow")

        self.verticalLayout_7.addWidget(self.FormActionsCheckBANDSfermyShow)

        self.FormActionsGrBoxBANDSspin = QGroupBox(self.tab_18)
        self.FormActionsGrBoxBANDSspin.setObjectName(u"FormActionsGrBoxBANDSspin")
        self.FormActionsGrBoxBANDSspin.setEnabled(False)
        self.FormActionsGrBoxBANDSspin.setMinimumSize(QSize(0, 0))
        self.FormActionsGrBoxBANDSspin.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_31 = QHBoxLayout(self.FormActionsGrBoxBANDSspin)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 2, -1, 5)
        self.FormActionsCheckBANDSspinUp = QRadioButton(self.FormActionsGrBoxBANDSspin)
        self.FormActionsCheckBANDSspinUp.setObjectName(u"FormActionsCheckBANDSspinUp")
        self.FormActionsCheckBANDSspinUp.setChecked(True)

        self.horizontalLayout_31.addWidget(self.FormActionsCheckBANDSspinUp)

        self.FormActionsCheckBANDSspinDown = QRadioButton(self.FormActionsGrBoxBANDSspin)
        self.FormActionsCheckBANDSspinDown.setObjectName(u"FormActionsCheckBANDSspinDown")

        self.horizontalLayout_31.addWidget(self.FormActionsCheckBANDSspinDown)


        self.verticalLayout_7.addWidget(self.FormActionsGrBoxBANDSspin)

        self.frame_35 = QFrame(self.tab_18)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.NoFrame)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalSpacer_44 = QSpacerItem(129, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_44)

        self.FormActionsButtonPlotBANDS = QPushButton(self.frame_35)
        self.FormActionsButtonPlotBANDS.setObjectName(u"FormActionsButtonPlotBANDS")
        self.FormActionsButtonPlotBANDS.setEnabled(False)

        self.horizontalLayout_24.addWidget(self.FormActionsButtonPlotBANDS)

        self.horizontalSpacer_46 = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_46)


        self.verticalLayout_7.addWidget(self.frame_35)

        self.frame_31 = QFrame(self.tab_18)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMinimumSize(QSize(0, 50))
        self.frame_31.setFrameShape(QFrame.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.frame_31.setLineWidth(0)
        self.horizontalLayout_79 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_79.setObjectName(u"horizontalLayout_79")
        self.FormActionsLabelBANDSgap = QLabel(self.frame_31)
        self.FormActionsLabelBANDSgap.setObjectName(u"FormActionsLabelBANDSgap")
        self.FormActionsLabelBANDSgap.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_79.addWidget(self.FormActionsLabelBANDSgap)


        self.verticalLayout_7.addWidget(self.frame_31)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_22)

        self.tabWidget_5.addTab(self.tab_18, "")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.verticalLayout_9 = QVBoxLayout(self.tab_14)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.FormActionsTabeDOSProperty = QTableWidget(self.tab_14)
        self.FormActionsTabeDOSProperty.setObjectName(u"FormActionsTabeDOSProperty")

        self.verticalLayout_9.addWidget(self.FormActionsTabeDOSProperty)

        self.frame_34 = QFrame(self.tab_14)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setMinimumSize(QSize(0, 40))
        self.frame_34.setFrameShape(QFrame.NoFrame)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.FormActionsCheckBANDSfermyShow_3 = QCheckBox(self.frame_34)
        self.FormActionsCheckBANDSfermyShow_3.setObjectName(u"FormActionsCheckBANDSfermyShow_3")

        self.horizontalLayout_29.addWidget(self.FormActionsCheckBANDSfermyShow_3)


        self.verticalLayout_9.addWidget(self.frame_34)

        self.frame_2 = QFrame(self.tab_14)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 40))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.FormActionsCheckDOS = QCheckBox(self.frame_2)
        self.FormActionsCheckDOS.setObjectName(u"FormActionsCheckDOS")

        self.horizontalLayout_9.addWidget(self.FormActionsCheckDOS)

        self.horizontalSpacer_8 = QSpacerItem(78, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)

        self.FormActionsCheckDOS_2 = QCheckBox(self.frame_2)
        self.FormActionsCheckDOS_2.setObjectName(u"FormActionsCheckDOS_2")

        self.horizontalLayout_9.addWidget(self.FormActionsCheckDOS_2)

        self.horizontalSpacer_5 = QSpacerItem(77, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_9.addWidget(self.frame_2)

        self.frame_20 = QFrame(self.tab_14)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 50))
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.FormActionsButtonAddDOSFile = QPushButton(self.frame_20)
        self.FormActionsButtonAddDOSFile.setObjectName(u"FormActionsButtonAddDOSFile")

        self.horizontalLayout_8.addWidget(self.FormActionsButtonAddDOSFile)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.FormActionsButtonClearDOS = QPushButton(self.frame_20)
        self.FormActionsButtonClearDOS.setObjectName(u"FormActionsButtonClearDOS")

        self.horizontalLayout_8.addWidget(self.FormActionsButtonClearDOS)

        self.horizontalSpacer_7 = QSpacerItem(21, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.FormActionsButtonPlotDOS = QPushButton(self.frame_20)
        self.FormActionsButtonPlotDOS.setObjectName(u"FormActionsButtonPlotDOS")

        self.horizontalLayout_8.addWidget(self.FormActionsButtonPlotDOS)


        self.verticalLayout_9.addWidget(self.frame_20)

        self.tabWidget_5.addTab(self.tab_14, "")
        self.tab_15 = QWidget()
        self.tab_15.setObjectName(u"tab_15")
        self.verticalLayout_18 = QVBoxLayout(self.tab_15)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.FormActionsLinePDOSfile = QLineEdit(self.tab_15)
        self.FormActionsLinePDOSfile.setObjectName(u"FormActionsLinePDOSfile")
        self.FormActionsLinePDOSfile.setReadOnly(True)

        self.verticalLayout_18.addWidget(self.FormActionsLinePDOSfile)

        self.tabWidget_4 = QTabWidget(self.tab_15)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tabWidget_4.setMinimumSize(QSize(0, 150))
        self.tabWidget_4.setMaximumSize(QSize(16777215, 250))
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_53 = QVBoxLayout(self.tab_8)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.groupBox_22 = QGroupBox(self.tab_8)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setMinimumSize(QSize(0, 0))
        self.verticalLayout_42 = QVBoxLayout(self.groupBox_22)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.FormActionsComboPDOSIndexes = QComboBox(self.groupBox_22)
        self.FormActionsComboPDOSIndexes.setObjectName(u"FormActionsComboPDOSIndexes")
        self.FormActionsComboPDOSIndexes.setStyleSheet(u"QComboBox { combobox-popup: 1px }")

        self.verticalLayout_42.addWidget(self.FormActionsComboPDOSIndexes)

        self.FormActionsPDOSIndexes = QPlainTextEdit(self.groupBox_22)
        self.FormActionsPDOSIndexes.setObjectName(u"FormActionsPDOSIndexes")

        self.verticalLayout_42.addWidget(self.FormActionsPDOSIndexes)


        self.verticalLayout_53.addWidget(self.groupBox_22)

        self.tabWidget_4.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_51 = QVBoxLayout(self.tab_9)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.groupBox_23 = QGroupBox(self.tab_9)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.groupBox_23.setMinimumSize(QSize(0, 100))
        self.verticalLayout_46 = QVBoxLayout(self.groupBox_23)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.FormActionsComboPDOSspecies = QComboBox(self.groupBox_23)
        self.FormActionsComboPDOSspecies.setObjectName(u"FormActionsComboPDOSspecies")
        self.FormActionsComboPDOSspecies.setStyleSheet(u"QComboBox { combobox-popup: 1px }")

        self.verticalLayout_46.addWidget(self.FormActionsComboPDOSspecies)

        self.FormActionsPDOSSpecieces = QPlainTextEdit(self.groupBox_23)
        self.FormActionsPDOSSpecieces.setObjectName(u"FormActionsPDOSSpecieces")

        self.verticalLayout_46.addWidget(self.FormActionsPDOSSpecieces)


        self.verticalLayout_51.addWidget(self.groupBox_23)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_51.addItem(self.verticalSpacer_15)

        self.tabWidget_4.addTab(self.tab_9, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.verticalLayout_50 = QVBoxLayout(self.tab_12)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.groupBox_25 = QGroupBox(self.tab_12)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setMinimumSize(QSize(0, 90))
        self.groupBox_25.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_47 = QVBoxLayout(self.groupBox_25)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.frame_40 = QFrame(self.groupBox_25)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setMinimumSize(QSize(0, 40))
        self.frame_40.setMaximumSize(QSize(16777215, 40))
        self.frame_40.setFrameShape(QFrame.NoFrame)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.frame_40.setLineWidth(0)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.FormActionsComboPDOSn1 = QCheckBox(self.frame_40)
        self.FormActionsComboPDOSn1.setObjectName(u"FormActionsComboPDOSn1")
        self.FormActionsComboPDOSn1.setChecked(True)

        self.horizontalLayout_28.addWidget(self.FormActionsComboPDOSn1)

        self.FormActionsComboPDOSn2 = QCheckBox(self.frame_40)
        self.FormActionsComboPDOSn2.setObjectName(u"FormActionsComboPDOSn2")
        self.FormActionsComboPDOSn2.setChecked(True)

        self.horizontalLayout_28.addWidget(self.FormActionsComboPDOSn2)

        self.FormActionsComboPDOSn3 = QCheckBox(self.frame_40)
        self.FormActionsComboPDOSn3.setObjectName(u"FormActionsComboPDOSn3")
        self.FormActionsComboPDOSn3.setChecked(True)

        self.horizontalLayout_28.addWidget(self.FormActionsComboPDOSn3)

        self.FormActionsComboPDOSn4 = QCheckBox(self.frame_40)
        self.FormActionsComboPDOSn4.setObjectName(u"FormActionsComboPDOSn4")
        self.FormActionsComboPDOSn4.setChecked(True)

        self.horizontalLayout_28.addWidget(self.FormActionsComboPDOSn4)


        self.verticalLayout_47.addWidget(self.frame_40)

        self.frame_39 = QFrame(self.groupBox_25)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setMinimumSize(QSize(0, 40))
        self.frame_39.setMaximumSize(QSize(16777215, 40))
        self.frame_39.setFrameShape(QFrame.NoFrame)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.frame_39.setLineWidth(0)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.FormActionsComboPDOSn5 = QCheckBox(self.frame_39)
        self.FormActionsComboPDOSn5.setObjectName(u"FormActionsComboPDOSn5")
        self.FormActionsComboPDOSn5.setChecked(True)

        self.horizontalLayout_27.addWidget(self.FormActionsComboPDOSn5)

        self.FormActionsComboPDOSn6 = QCheckBox(self.frame_39)
        self.FormActionsComboPDOSn6.setObjectName(u"FormActionsComboPDOSn6")
        self.FormActionsComboPDOSn6.setChecked(True)

        self.horizontalLayout_27.addWidget(self.FormActionsComboPDOSn6)

        self.FormActionsComboPDOSn7 = QCheckBox(self.frame_39)
        self.FormActionsComboPDOSn7.setObjectName(u"FormActionsComboPDOSn7")
        self.FormActionsComboPDOSn7.setChecked(True)

        self.horizontalLayout_27.addWidget(self.FormActionsComboPDOSn7)

        self.FormActionsComboPDOSn8 = QCheckBox(self.frame_39)
        self.FormActionsComboPDOSn8.setObjectName(u"FormActionsComboPDOSn8")
        self.FormActionsComboPDOSn8.setChecked(True)

        self.horizontalLayout_27.addWidget(self.FormActionsComboPDOSn8)


        self.verticalLayout_47.addWidget(self.frame_39)


        self.verticalLayout_50.addWidget(self.groupBox_25)

        self.verticalSpacer_13 = QSpacerItem(20, 89, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_50.addItem(self.verticalSpacer_13)

        self.tabWidget_4.addTab(self.tab_12, "")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.verticalLayout_29 = QVBoxLayout(self.tab_13)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.groupBox_26 = QGroupBox(self.tab_13)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.groupBox_26.setMinimumSize(QSize(0, 120))
        self.groupBox_26.setMaximumSize(QSize(16777215, 130))
        self.verticalLayout_49 = QVBoxLayout(self.groupBox_26)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.frame_25 = QFrame(self.groupBox_26)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(0, 40))
        self.frame_25.setMaximumSize(QSize(16777215, 40))
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.FormActionsComboPDOSL0 = QCheckBox(self.frame_25)
        self.FormActionsComboPDOSL0.setObjectName(u"FormActionsComboPDOSL0")
        self.FormActionsComboPDOSL0.setChecked(True)

        self.horizontalLayout_14.addWidget(self.FormActionsComboPDOSL0)

        self.FormActionsComboPDOSL1 = QCheckBox(self.frame_25)
        self.FormActionsComboPDOSL1.setObjectName(u"FormActionsComboPDOSL1")
        self.FormActionsComboPDOSL1.setChecked(True)

        self.horizontalLayout_14.addWidget(self.FormActionsComboPDOSL1)

        self.FormActionsComboPDOSL2 = QCheckBox(self.frame_25)
        self.FormActionsComboPDOSL2.setObjectName(u"FormActionsComboPDOSL2")
        self.FormActionsComboPDOSL2.setChecked(True)

        self.horizontalLayout_14.addWidget(self.FormActionsComboPDOSL2)

        self.FormActionsComboPDOSL3 = QCheckBox(self.frame_25)
        self.FormActionsComboPDOSL3.setObjectName(u"FormActionsComboPDOSL3")
        self.FormActionsComboPDOSL3.setChecked(True)

        self.horizontalLayout_14.addWidget(self.FormActionsComboPDOSL3)


        self.verticalLayout_49.addWidget(self.frame_25)

        self.frame_46 = QFrame(self.groupBox_26)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setMinimumSize(QSize(0, 40))
        self.frame_46.setFrameShape(QFrame.NoFrame)
        self.frame_46.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.FormActionsComboPDOSL4 = QCheckBox(self.frame_46)
        self.FormActionsComboPDOSL4.setObjectName(u"FormActionsComboPDOSL4")
        self.FormActionsComboPDOSL4.setChecked(True)

        self.horizontalLayout_35.addWidget(self.FormActionsComboPDOSL4)

        self.FormActionsComboPDOSL5 = QCheckBox(self.frame_46)
        self.FormActionsComboPDOSL5.setObjectName(u"FormActionsComboPDOSL5")
        self.FormActionsComboPDOSL5.setChecked(True)

        self.horizontalLayout_35.addWidget(self.FormActionsComboPDOSL5)

        self.FormActionsComboPDOSL6 = QCheckBox(self.frame_46)
        self.FormActionsComboPDOSL6.setObjectName(u"FormActionsComboPDOSL6")
        self.FormActionsComboPDOSL6.setChecked(True)

        self.horizontalLayout_35.addWidget(self.FormActionsComboPDOSL6)

        self.FormActionsComboPDOSL7 = QCheckBox(self.frame_46)
        self.FormActionsComboPDOSL7.setObjectName(u"FormActionsComboPDOSL7")
        self.FormActionsComboPDOSL7.setChecked(True)

        self.horizontalLayout_35.addWidget(self.FormActionsComboPDOSL7)


        self.verticalLayout_49.addWidget(self.frame_46)


        self.verticalLayout_29.addWidget(self.groupBox_26)

        self.verticalSpacer_12 = QSpacerItem(20, 59, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_12)

        self.tabWidget_4.addTab(self.tab_13, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.verticalLayout_28 = QVBoxLayout(self.tab_10)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.groupBox_27 = QGroupBox(self.tab_10)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setMinimumSize(QSize(0, 180))
        self.groupBox_27.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_48 = QVBoxLayout(self.groupBox_27)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.frame_74 = QFrame(self.groupBox_27)
        self.frame_74.setObjectName(u"frame_74")
        self.frame_74.setMinimumSize(QSize(0, 40))
        self.frame_74.setMaximumSize(QSize(16777215, 40))
        self.frame_74.setFrameShape(QFrame.NoFrame)
        self.frame_74.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_74)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.FormActionsComboPDOSMm7 = QCheckBox(self.frame_74)
        self.FormActionsComboPDOSMm7.setObjectName(u"FormActionsComboPDOSMm7")
        self.FormActionsComboPDOSMm7.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm7.setChecked(True)

        self.horizontalLayout_67.addWidget(self.FormActionsComboPDOSMm7)

        self.FormActionsComboPDOSMm6 = QCheckBox(self.frame_74)
        self.FormActionsComboPDOSMm6.setObjectName(u"FormActionsComboPDOSMm6")
        self.FormActionsComboPDOSMm6.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm6.setChecked(True)

        self.horizontalLayout_67.addWidget(self.FormActionsComboPDOSMm6)

        self.FormActionsComboPDOSMm5 = QCheckBox(self.frame_74)
        self.FormActionsComboPDOSMm5.setObjectName(u"FormActionsComboPDOSMm5")
        self.FormActionsComboPDOSMm5.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm5.setChecked(True)

        self.horizontalLayout_67.addWidget(self.FormActionsComboPDOSMm5)

        self.FormActionsComboPDOSMm4 = QCheckBox(self.frame_74)
        self.FormActionsComboPDOSMm4.setObjectName(u"FormActionsComboPDOSMm4")
        self.FormActionsComboPDOSMm4.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm4.setChecked(True)

        self.horizontalLayout_67.addWidget(self.FormActionsComboPDOSMm4)

        self.FormActionsComboPDOSMm3 = QCheckBox(self.frame_74)
        self.FormActionsComboPDOSMm3.setObjectName(u"FormActionsComboPDOSMm3")
        self.FormActionsComboPDOSMm3.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm3.setChecked(True)

        self.horizontalLayout_67.addWidget(self.FormActionsComboPDOSMm3)


        self.verticalLayout_48.addWidget(self.frame_74)

        self.frame_75 = QFrame(self.groupBox_27)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setMinimumSize(QSize(0, 40))
        self.frame_75.setMaximumSize(QSize(16777215, 40))
        self.frame_75.setFrameShape(QFrame.NoFrame)
        self.frame_75.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_75)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.FormActionsComboPDOSMm2 = QCheckBox(self.frame_75)
        self.FormActionsComboPDOSMm2.setObjectName(u"FormActionsComboPDOSMm2")
        self.FormActionsComboPDOSMm2.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm2.setChecked(True)

        self.horizontalLayout_68.addWidget(self.FormActionsComboPDOSMm2)

        self.FormActionsComboPDOSMm1 = QCheckBox(self.frame_75)
        self.FormActionsComboPDOSMm1.setObjectName(u"FormActionsComboPDOSMm1")
        self.FormActionsComboPDOSMm1.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMm1.setChecked(True)

        self.horizontalLayout_68.addWidget(self.FormActionsComboPDOSMm1)

        self.FormActionsComboPDOSMp0 = QCheckBox(self.frame_75)
        self.FormActionsComboPDOSMp0.setObjectName(u"FormActionsComboPDOSMp0")
        self.FormActionsComboPDOSMp0.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp0.setChecked(True)

        self.horizontalLayout_68.addWidget(self.FormActionsComboPDOSMp0)

        self.FormActionsComboPDOSMp1 = QCheckBox(self.frame_75)
        self.FormActionsComboPDOSMp1.setObjectName(u"FormActionsComboPDOSMp1")
        self.FormActionsComboPDOSMp1.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp1.setChecked(True)

        self.horizontalLayout_68.addWidget(self.FormActionsComboPDOSMp1)

        self.FormActionsComboPDOSMp2 = QCheckBox(self.frame_75)
        self.FormActionsComboPDOSMp2.setObjectName(u"FormActionsComboPDOSMp2")
        self.FormActionsComboPDOSMp2.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp2.setChecked(True)

        self.horizontalLayout_68.addWidget(self.FormActionsComboPDOSMp2)


        self.verticalLayout_48.addWidget(self.frame_75)

        self.frame_73 = QFrame(self.groupBox_27)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setFrameShape(QFrame.NoFrame)
        self.frame_73.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_69 = QHBoxLayout(self.frame_73)
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.FormActionsComboPDOSMp3 = QCheckBox(self.frame_73)
        self.FormActionsComboPDOSMp3.setObjectName(u"FormActionsComboPDOSMp3")
        self.FormActionsComboPDOSMp3.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp3.setChecked(True)

        self.horizontalLayout_69.addWidget(self.FormActionsComboPDOSMp3)

        self.FormActionsComboPDOSMp4 = QCheckBox(self.frame_73)
        self.FormActionsComboPDOSMp4.setObjectName(u"FormActionsComboPDOSMp4")
        self.FormActionsComboPDOSMp4.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp4.setChecked(True)

        self.horizontalLayout_69.addWidget(self.FormActionsComboPDOSMp4)

        self.FormActionsComboPDOSMp5 = QCheckBox(self.frame_73)
        self.FormActionsComboPDOSMp5.setObjectName(u"FormActionsComboPDOSMp5")
        self.FormActionsComboPDOSMp5.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp5.setChecked(True)

        self.horizontalLayout_69.addWidget(self.FormActionsComboPDOSMp5)

        self.FormActionsComboPDOSMp6 = QCheckBox(self.frame_73)
        self.FormActionsComboPDOSMp6.setObjectName(u"FormActionsComboPDOSMp6")
        self.FormActionsComboPDOSMp6.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp6.setChecked(True)

        self.horizontalLayout_69.addWidget(self.FormActionsComboPDOSMp6)

        self.FormActionsComboPDOSMp7 = QCheckBox(self.frame_73)
        self.FormActionsComboPDOSMp7.setObjectName(u"FormActionsComboPDOSMp7")
        self.FormActionsComboPDOSMp7.setMinimumSize(QSize(42, 0))
        self.FormActionsComboPDOSMp7.setChecked(True)

        self.horizontalLayout_69.addWidget(self.FormActionsComboPDOSMp7)


        self.verticalLayout_48.addWidget(self.frame_73)


        self.verticalLayout_28.addWidget(self.groupBox_27)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_28.addItem(self.verticalSpacer_11)

        self.tabWidget_4.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.verticalLayout_54 = QVBoxLayout(self.tab_11)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.groupBox_28 = QGroupBox(self.tab_11)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.groupBox_28.setMinimumSize(QSize(0, 60))
        self.horizontalLayout_23 = QHBoxLayout(self.groupBox_28)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.frame_41 = QFrame(self.groupBox_28)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setMinimumSize(QSize(0, 40))
        self.frame_41.setMaximumSize(QSize(16777215, 40))
        self.frame_41.setFrameShape(QFrame.NoFrame)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.frame_41.setLineWidth(0)
        self.horizontalLayout_70 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.FormActionsComboPDOSz1 = QCheckBox(self.frame_41)
        self.FormActionsComboPDOSz1.setObjectName(u"FormActionsComboPDOSz1")
        self.FormActionsComboPDOSz1.setChecked(True)

        self.horizontalLayout_70.addWidget(self.FormActionsComboPDOSz1)

        self.FormActionsComboPDOSz2 = QCheckBox(self.frame_41)
        self.FormActionsComboPDOSz2.setObjectName(u"FormActionsComboPDOSz2")
        self.FormActionsComboPDOSz2.setChecked(True)

        self.horizontalLayout_70.addWidget(self.FormActionsComboPDOSz2)

        self.FormActionsComboPDOSz3 = QCheckBox(self.frame_41)
        self.FormActionsComboPDOSz3.setObjectName(u"FormActionsComboPDOSz3")
        self.FormActionsComboPDOSz3.setChecked(True)

        self.horizontalLayout_70.addWidget(self.FormActionsComboPDOSz3)

        self.FormActionsComboPDOSz4 = QCheckBox(self.frame_41)
        self.FormActionsComboPDOSz4.setObjectName(u"FormActionsComboPDOSz4")
        self.FormActionsComboPDOSz4.setChecked(True)

        self.horizontalLayout_70.addWidget(self.FormActionsComboPDOSz4)

        self.FormActionsComboPDOSz5 = QCheckBox(self.frame_41)
        self.FormActionsComboPDOSz5.setObjectName(u"FormActionsComboPDOSz5")
        self.FormActionsComboPDOSz5.setChecked(True)

        self.horizontalLayout_70.addWidget(self.FormActionsComboPDOSz5)


        self.horizontalLayout_23.addWidget(self.frame_41)


        self.verticalLayout_54.addWidget(self.groupBox_28)

        self.verticalSpacer_17 = QSpacerItem(20, 109, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_54.addItem(self.verticalSpacer_17)

        self.tabWidget_4.addTab(self.tab_11, "")

        self.verticalLayout_18.addWidget(self.tabWidget_4)

        self.groupBox_12 = QGroupBox(self.tab_15)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(0, 0))
        self.groupBox_12.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_26 = QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 2, -1, 5)
        self.FormActionsCheckPDOS = QCheckBox(self.groupBox_12)
        self.FormActionsCheckPDOS.setObjectName(u"FormActionsCheckPDOS")

        self.horizontalLayout_26.addWidget(self.FormActionsCheckPDOS)

        self.FormActionsCheckPDOS_2 = QCheckBox(self.groupBox_12)
        self.FormActionsCheckPDOS_2.setObjectName(u"FormActionsCheckPDOS_2")

        self.horizontalLayout_26.addWidget(self.FormActionsCheckPDOS_2)


        self.verticalLayout_18.addWidget(self.groupBox_12)

        self.FormActionsCheckBANDSfermyShow_2 = QCheckBox(self.tab_15)
        self.FormActionsCheckBANDSfermyShow_2.setObjectName(u"FormActionsCheckBANDSfermyShow_2")

        self.verticalLayout_18.addWidget(self.FormActionsCheckBANDSfermyShow_2)

        self.frame_48 = QFrame(self.tab_15)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setMinimumSize(QSize(0, 0))
        self.frame_48.setFrameShape(QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.frame_48)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.FormActionsButtonPlotPDOS = QPushButton(self.frame_48)
        self.FormActionsButtonPlotPDOS.setObjectName(u"FormActionsButtonPlotPDOS")
        self.FormActionsButtonPlotPDOS.setEnabled(False)

        self.horizontalLayout_42.addWidget(self.FormActionsButtonPlotPDOS)

        self.FormActionsEditPDOSLabel = QLineEdit(self.frame_48)
        self.FormActionsEditPDOSLabel.setObjectName(u"FormActionsEditPDOSLabel")

        self.horizontalLayout_42.addWidget(self.FormActionsEditPDOSLabel)


        self.verticalLayout_18.addWidget(self.frame_48)

        self.FormActionsListPDOS = QListWidget(self.tab_15)
        self.FormActionsListPDOS.setObjectName(u"FormActionsListPDOS")
        self.FormActionsListPDOS.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_18.addWidget(self.FormActionsListPDOS)

        self.frame_71 = QFrame(self.tab_15)
        self.frame_71.setObjectName(u"frame_71")
        self.frame_71.setMinimumSize(QSize(0, 0))
        self.frame_71.setFrameShape(QFrame.NoFrame)
        self.frame_71.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_65 = QHBoxLayout(self.frame_71)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalSpacer_45 = QSpacerItem(19, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_65.addItem(self.horizontalSpacer_45)

        self.FormActionsButtonPlotPDOSselected = QPushButton(self.frame_71)
        self.FormActionsButtonPlotPDOSselected.setObjectName(u"FormActionsButtonPlotPDOSselected")
        self.FormActionsButtonPlotPDOSselected.setEnabled(False)

        self.horizontalLayout_65.addWidget(self.FormActionsButtonPlotPDOSselected)

        self.horizontalSpacer_38 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_65.addItem(self.horizontalSpacer_38)


        self.verticalLayout_18.addWidget(self.frame_71)

        self.tabWidget_5.addTab(self.tab_15, "")

        self.verticalLayout_6.addWidget(self.tabWidget_5)

        self.toolBox_2.addItem(self.page_19, u"Electronic properties")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 359, 668))
        self.verticalLayout_12 = QVBoxLayout(self.page_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tabWidget_2 = QTabWidget(self.page_2)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setMinimumSize(QSize(0, 646))
        self.tabWidget_2.setMaximumSize(QSize(16777215, 16777215))
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.FormActionsPostList3DData = QListWidget(self.tab_2)
        self.FormActionsPostList3DData.setObjectName(u"FormActionsPostList3DData")

        self.verticalLayout_4.addWidget(self.FormActionsPostList3DData)

        self.frame_69 = QFrame(self.tab_2)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setFrameShape(QFrame.NoFrame)
        self.frame_69.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_69)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.horizontalSpacer_59 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_61.addItem(self.horizontalSpacer_59)

        self.FormActionsPostButSurfaceParse = QPushButton(self.frame_69)
        self.FormActionsPostButSurfaceParse.setObjectName(u"FormActionsPostButSurfaceParse")
        self.FormActionsPostButSurfaceParse.setEnabled(False)

        self.horizontalLayout_61.addWidget(self.FormActionsPostButSurfaceParse)

        self.horizontalSpacer_58 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_61.addItem(self.horizontalSpacer_58)


        self.verticalLayout_4.addWidget(self.frame_69)

        self.FormActionsPostTreeSurface = QTreeWidget(self.tab_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.FormActionsPostTreeSurface.setHeaderItem(__qtreewidgetitem)
        self.FormActionsPostTreeSurface.setObjectName(u"FormActionsPostTreeSurface")
        self.FormActionsPostTreeSurface.header().setVisible(False)

        self.verticalLayout_4.addWidget(self.FormActionsPostTreeSurface)

        self.frame_92 = QFrame(self.tab_2)
        self.frame_92.setObjectName(u"frame_92")
        self.frame_92.setFrameShape(QFrame.NoFrame)
        self.frame_92.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_91 = QHBoxLayout(self.frame_92)
        self.horizontalLayout_91.setObjectName(u"horizontalLayout_91")
        self.horizontalSpacer_61 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_91.addItem(self.horizontalSpacer_61)

        self.FormActionsPostButSurfaceLoadData = QPushButton(self.frame_92)
        self.FormActionsPostButSurfaceLoadData.setObjectName(u"FormActionsPostButSurfaceLoadData")
        self.FormActionsPostButSurfaceLoadData.setEnabled(False)

        self.horizontalLayout_91.addWidget(self.FormActionsPostButSurfaceLoadData)

        self.horizontalSpacer_60 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_91.addItem(self.horizontalSpacer_60)


        self.verticalLayout_4.addWidget(self.frame_92)

        self.groupBox_6 = QGroupBox(self.tab_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_33 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, 2, -1, 2)
        self.FormActionsPostLabelSurfaceMin = QLabel(self.groupBox_6)
        self.FormActionsPostLabelSurfaceMin.setObjectName(u"FormActionsPostLabelSurfaceMin")
        self.FormActionsPostLabelSurfaceMin.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_33.addWidget(self.FormActionsPostLabelSurfaceMin)

        self.FormActionsPostLabelSurfaceMax = QLabel(self.groupBox_6)
        self.FormActionsPostLabelSurfaceMax.setObjectName(u"FormActionsPostLabelSurfaceMax")

        self.horizontalLayout_33.addWidget(self.FormActionsPostLabelSurfaceMax)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.verticalSpacer_23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_23)

        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_40 = QVBoxLayout(self.tab_6)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.FormActionsPosEdit3DData2 = QLineEdit(self.tab_6)
        self.FormActionsPosEdit3DData2.setObjectName(u"FormActionsPosEdit3DData2")

        self.verticalLayout_40.addWidget(self.FormActionsPosEdit3DData2)

        self.frame_94 = QFrame(self.tab_6)
        self.frame_94.setObjectName(u"frame_94")
        self.frame_94.setFrameShape(QFrame.NoFrame)
        self.frame_94.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_93 = QHBoxLayout(self.frame_94)
        self.horizontalLayout_93.setObjectName(u"horizontalLayout_93")
        self.horizontalSpacer_65 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_93.addItem(self.horizontalSpacer_65)

        self.FormActionsPostButSurfaceParse2 = QPushButton(self.frame_94)
        self.FormActionsPostButSurfaceParse2.setObjectName(u"FormActionsPostButSurfaceParse2")
        self.FormActionsPostButSurfaceParse2.setEnabled(False)

        self.horizontalLayout_93.addWidget(self.FormActionsPostButSurfaceParse2)

        self.horizontalSpacer_64 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_93.addItem(self.horizontalSpacer_64)


        self.verticalLayout_40.addWidget(self.frame_94)

        self.FormActionsPostTreeSurface2 = QTreeWidget(self.tab_6)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.FormActionsPostTreeSurface2.setHeaderItem(__qtreewidgetitem1)
        self.FormActionsPostTreeSurface2.setObjectName(u"FormActionsPostTreeSurface2")
        self.FormActionsPostTreeSurface2.setMaximumSize(QSize(16777215, 100))
        self.FormActionsPostTreeSurface2.header().setVisible(False)

        self.verticalLayout_40.addWidget(self.FormActionsPostTreeSurface2)

        self.frame_93 = QFrame(self.tab_6)
        self.frame_93.setObjectName(u"frame_93")
        self.frame_93.setFrameShape(QFrame.NoFrame)
        self.frame_93.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_92 = QHBoxLayout(self.frame_93)
        self.horizontalLayout_92.setObjectName(u"horizontalLayout_92")
        self.horizontalSpacer_63 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_92.addItem(self.horizontalSpacer_63)

        self.FormActionsPostButSurfaceLoadData2 = QPushButton(self.frame_93)
        self.FormActionsPostButSurfaceLoadData2.setObjectName(u"FormActionsPostButSurfaceLoadData2")
        self.FormActionsPostButSurfaceLoadData2.setEnabled(False)

        self.horizontalLayout_92.addWidget(self.FormActionsPostButSurfaceLoadData2)

        self.horizontalSpacer_62 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_92.addItem(self.horizontalSpacer_62)


        self.verticalLayout_40.addWidget(self.frame_93)

        self.VolumrricDataGrid2 = QGroupBox(self.tab_6)
        self.VolumrricDataGrid2.setObjectName(u"VolumrricDataGrid2")
        self.VolumrricDataGrid2.setMinimumSize(QSize(0, 60))
        self.horizontalLayout_52 = QHBoxLayout(self.VolumrricDataGrid2)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.FormActionsPostLabelSurfaceNx = QLabel(self.VolumrricDataGrid2)
        self.FormActionsPostLabelSurfaceNx.setObjectName(u"FormActionsPostLabelSurfaceNx")
        self.FormActionsPostLabelSurfaceNx.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_52.addWidget(self.FormActionsPostLabelSurfaceNx)

        self.FormActionsPostLabelSurfaceNy = QLabel(self.VolumrricDataGrid2)
        self.FormActionsPostLabelSurfaceNy.setObjectName(u"FormActionsPostLabelSurfaceNy")

        self.horizontalLayout_52.addWidget(self.FormActionsPostLabelSurfaceNy)

        self.FormActionsPostLabelSurfaceNz = QLabel(self.VolumrricDataGrid2)
        self.FormActionsPostLabelSurfaceNz.setObjectName(u"FormActionsPostLabelSurfaceNz")

        self.horizontalLayout_52.addWidget(self.FormActionsPostLabelSurfaceNz)


        self.verticalLayout_40.addWidget(self.VolumrricDataGrid2)

        self.VolumrricDataGridCalculate = QGroupBox(self.tab_6)
        self.VolumrricDataGridCalculate.setObjectName(u"VolumrricDataGridCalculate")
        self.VolumrricDataGridCalculate.setEnabled(False)
        self.VolumrricDataGridCalculate.setMinimumSize(QSize(0, 70))
        self.horizontalLayout_63 = QHBoxLayout(self.VolumrricDataGridCalculate)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_63.addItem(self.horizontalSpacer_33)

        self.CalculateTheVolumericDataDifference = QPushButton(self.VolumrricDataGridCalculate)
        self.CalculateTheVolumericDataDifference.setObjectName(u"CalculateTheVolumericDataDifference")
        self.CalculateTheVolumericDataDifference.setEnabled(False)

        self.horizontalLayout_63.addWidget(self.CalculateTheVolumericDataDifference)

        self.horizontalSpacer_32 = QSpacerItem(27, 18, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_63.addItem(self.horizontalSpacer_32)

        self.CalculateTheVolumericDataSum = QPushButton(self.VolumrricDataGridCalculate)
        self.CalculateTheVolumericDataSum.setObjectName(u"CalculateTheVolumericDataSum")
        self.CalculateTheVolumericDataSum.setEnabled(False)

        self.horizontalLayout_63.addWidget(self.CalculateTheVolumericDataSum)

        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_63.addItem(self.horizontalSpacer_34)


        self.verticalLayout_40.addWidget(self.VolumrricDataGridCalculate)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_10)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_22 = QWidget()
        self.tab_22.setObjectName(u"tab_22")
        self.verticalLayout_70 = QVBoxLayout(self.tab_22)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.groupBox_18 = QGroupBox(self.tab_22)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.verticalLayout_77 = QVBoxLayout(self.groupBox_18)
        self.verticalLayout_77.setObjectName(u"verticalLayout_77")
        self.frame_107 = QFrame(self.groupBox_18)
        self.frame_107.setObjectName(u"frame_107")
        self.frame_107.setFrameShape(QFrame.StyledPanel)
        self.frame_107.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_128 = QHBoxLayout(self.frame_107)
        self.horizontalLayout_128.setObjectName(u"horizontalLayout_128")
        self.label_33 = QLabel(self.frame_107)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_128.addWidget(self.label_33)

        self.FormVolDataExportX1 = QSpinBox(self.frame_107)
        self.FormVolDataExportX1.setObjectName(u"FormVolDataExportX1")

        self.horizontalLayout_128.addWidget(self.FormVolDataExportX1)

        self.label_96 = QLabel(self.frame_107)
        self.label_96.setObjectName(u"label_96")

        self.horizontalLayout_128.addWidget(self.label_96)

        self.FormVolDataExportX2 = QSpinBox(self.frame_107)
        self.FormVolDataExportX2.setObjectName(u"FormVolDataExportX2")

        self.horizontalLayout_128.addWidget(self.FormVolDataExportX2)

        self.horizontalSpacer_89 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_128.addItem(self.horizontalSpacer_89)


        self.verticalLayout_77.addWidget(self.frame_107)

        self.frame_123 = QFrame(self.groupBox_18)
        self.frame_123.setObjectName(u"frame_123")
        self.frame_123.setFrameShape(QFrame.StyledPanel)
        self.frame_123.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_145 = QHBoxLayout(self.frame_123)
        self.horizontalLayout_145.setObjectName(u"horizontalLayout_145")
        self.label_99 = QLabel(self.frame_123)
        self.label_99.setObjectName(u"label_99")

        self.horizontalLayout_145.addWidget(self.label_99)

        self.FormVolDataExportY1 = QSpinBox(self.frame_123)
        self.FormVolDataExportY1.setObjectName(u"FormVolDataExportY1")

        self.horizontalLayout_145.addWidget(self.FormVolDataExportY1)

        self.label_100 = QLabel(self.frame_123)
        self.label_100.setObjectName(u"label_100")

        self.horizontalLayout_145.addWidget(self.label_100)

        self.FormVolDataExportY2 = QSpinBox(self.frame_123)
        self.FormVolDataExportY2.setObjectName(u"FormVolDataExportY2")

        self.horizontalLayout_145.addWidget(self.FormVolDataExportY2)

        self.horizontalSpacer_100 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_145.addItem(self.horizontalSpacer_100)


        self.verticalLayout_77.addWidget(self.frame_123)

        self.frame_124 = QFrame(self.groupBox_18)
        self.frame_124.setObjectName(u"frame_124")
        self.frame_124.setFrameShape(QFrame.StyledPanel)
        self.frame_124.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_144 = QHBoxLayout(self.frame_124)
        self.horizontalLayout_144.setObjectName(u"horizontalLayout_144")
        self.label_101 = QLabel(self.frame_124)
        self.label_101.setObjectName(u"label_101")

        self.horizontalLayout_144.addWidget(self.label_101)

        self.FormVolDataExportZ1 = QSpinBox(self.frame_124)
        self.FormVolDataExportZ1.setObjectName(u"FormVolDataExportZ1")

        self.horizontalLayout_144.addWidget(self.FormVolDataExportZ1)

        self.label_102 = QLabel(self.frame_124)
        self.label_102.setObjectName(u"label_102")

        self.horizontalLayout_144.addWidget(self.label_102)

        self.FormVolDataExportZ2 = QSpinBox(self.frame_124)
        self.FormVolDataExportZ2.setObjectName(u"FormVolDataExportZ2")

        self.horizontalLayout_144.addWidget(self.FormVolDataExportZ2)

        self.horizontalSpacer_101 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_144.addItem(self.horizontalSpacer_101)


        self.verticalLayout_77.addWidget(self.frame_124)


        self.verticalLayout_70.addWidget(self.groupBox_18)

        self.VolumrricDataGridExport = QFrame(self.tab_22)
        self.VolumrricDataGridExport.setObjectName(u"VolumrricDataGridExport")
        self.VolumrricDataGridExport.setFrameShape(QFrame.StyledPanel)
        self.VolumrricDataGridExport.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_64 = QHBoxLayout(self.VolumrricDataGridExport)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalSpacer_37 = QSpacerItem(25, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_64.addItem(self.horizontalSpacer_37)

        self.ExportTheVolumericDataXSF = QPushButton(self.VolumrricDataGridExport)
        self.ExportTheVolumericDataXSF.setObjectName(u"ExportTheVolumericDataXSF")

        self.horizontalLayout_64.addWidget(self.ExportTheVolumericDataXSF)

        self.horizontalSpacer_35 = QSpacerItem(25, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_64.addItem(self.horizontalSpacer_35)

        self.ExportTheVolumericDataCube = QPushButton(self.VolumrricDataGridExport)
        self.ExportTheVolumericDataCube.setObjectName(u"ExportTheVolumericDataCube")
        self.ExportTheVolumericDataCube.setEnabled(True)

        self.horizontalLayout_64.addWidget(self.ExportTheVolumericDataCube)

        self.horizontalSpacer_36 = QSpacerItem(41, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_64.addItem(self.horizontalSpacer_36)


        self.verticalLayout_70.addWidget(self.VolumrricDataGridExport)

        self.verticalSpacer_25 = QSpacerItem(20, 542, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_70.addItem(self.verticalSpacer_25)

        self.tabWidget_2.addTab(self.tab_22, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_15 = QVBoxLayout(self.tab_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.FormActionsPostCheckSurface = QCheckBox(self.tab_3)
        self.FormActionsPostCheckSurface.setObjectName(u"FormActionsPostCheckSurface")

        self.verticalLayout_15.addWidget(self.FormActionsPostCheckSurface)

        self.IsosurfaceColorsTable = QTableWidget(self.tab_3)
        self.IsosurfaceColorsTable.setObjectName(u"IsosurfaceColorsTable")

        self.verticalLayout_15.addWidget(self.IsosurfaceColorsTable)

        self.frame_15 = QFrame(self.tab_3)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 100))
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_15)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.frame_27 = QFrame(self.frame_15)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMinimumSize(QSize(0, 55))
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_10 = QLabel(self.frame_27)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_18.addWidget(self.label_10)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_11)

        self.FormActionsPostLabelSurfaceValue = QDoubleSpinBox(self.frame_27)
        self.FormActionsPostLabelSurfaceValue.setObjectName(u"FormActionsPostLabelSurfaceValue")
        self.FormActionsPostLabelSurfaceValue.setMinimumSize(QSize(0, 24))
        self.FormActionsPostLabelSurfaceValue.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPostLabelSurfaceValue.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.FormActionsPostLabelSurfaceValue.setDecimals(6)
        self.FormActionsPostLabelSurfaceValue.setMinimum(-99.000000000000000)
        self.FormActionsPostLabelSurfaceValue.setSingleStep(0.010000000000000)

        self.horizontalLayout_18.addWidget(self.FormActionsPostLabelSurfaceValue)

        self.horizontalSpacer_66 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_66)

        self.FormActionsPostButSurfaceAdd = QPushButton(self.frame_27)
        self.FormActionsPostButSurfaceAdd.setObjectName(u"FormActionsPostButSurfaceAdd")
        self.FormActionsPostButSurfaceAdd.setEnabled(False)

        self.horizontalLayout_18.addWidget(self.FormActionsPostButSurfaceAdd)


        self.verticalLayout_22.addWidget(self.frame_27)

        self.frame_17 = QFrame(self.frame_15)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 50))
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(105, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.FormActionsPostButSurfaceDelete = QPushButton(self.frame_18)
        self.FormActionsPostButSurfaceDelete.setObjectName(u"FormActionsPostButSurfaceDelete")
        self.FormActionsPostButSurfaceDelete.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.FormActionsPostButSurfaceDelete)

        self.horizontalSpacer_68 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_68)

        self.FormActionsPostButSurface = QPushButton(self.frame_18)
        self.FormActionsPostButSurface.setObjectName(u"FormActionsPostButSurface")
        self.FormActionsPostButSurface.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.FormActionsPostButSurface)

        self.horizontalSpacer_2 = QSpacerItem(105, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_5.addWidget(self.frame_18)


        self.verticalLayout_22.addWidget(self.frame_17)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_21)


        self.verticalLayout_15.addWidget(self.frame_15)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_9 = QFrame(self.tab_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 40))
        self.frame_9.setMaximumSize(QSize(16777215, 40))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.FormActionsPostRadioContour = QRadioButton(self.frame_9)
        self.FormActionsPostRadioContour.setObjectName(u"FormActionsPostRadioContour")
        self.FormActionsPostRadioContour.setChecked(True)

        self.horizontalLayout_6.addWidget(self.FormActionsPostRadioContour)

        self.FormActionsPostRadioColorPlane = QRadioButton(self.frame_9)
        self.FormActionsPostRadioColorPlane.setObjectName(u"FormActionsPostRadioColorPlane")

        self.horizontalLayout_6.addWidget(self.FormActionsPostRadioColorPlane)

        self.FormActionsPostRadioColorPlaneContours = QRadioButton(self.frame_9)
        self.FormActionsPostRadioColorPlaneContours.setObjectName(u"FormActionsPostRadioColorPlaneContours")

        self.horizontalLayout_6.addWidget(self.FormActionsPostRadioColorPlaneContours)


        self.verticalLayout_5.addWidget(self.frame_9)

        self.groupBox_4 = QGroupBox(self.tab_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 0))
        self.groupBox_4.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_61 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.frame_831 = QFrame(self.groupBox_4)
        self.frame_831.setObjectName(u"frame_831")
        self.frame_831.setFrameShape(QFrame.NoFrame)
        self.frame_831.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_961 = QHBoxLayout(self.frame_831)
        self.horizontalLayout_961.setObjectName(u"horizontalLayout_961")
        self.FormActionsPostCheckContourXY = QCheckBox(self.frame_831)
        self.FormActionsPostCheckContourXY.setObjectName(u"FormActionsPostCheckContourXY")

        self.horizontalLayout_961.addWidget(self.FormActionsPostCheckContourXY)

        self.FormActionsPostLabelSurfaceNcontoursXY = QSpinBox(self.frame_831)
        self.FormActionsPostLabelSurfaceNcontoursXY.setObjectName(u"FormActionsPostLabelSurfaceNcontoursXY")
        self.FormActionsPostLabelSurfaceNcontoursXY.setMinimumSize(QSize(0, 24))
        self.FormActionsPostLabelSurfaceNcontoursXY.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPostLabelSurfaceNcontoursXY.setValue(5)

        self.horizontalLayout_961.addWidget(self.FormActionsPostLabelSurfaceNcontoursXY)

        self.label_11 = QLabel(self.frame_831)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_961.addWidget(self.label_11)


        self.verticalLayout_61.addWidget(self.frame_831)

        self.FormActionsPostSliderContourXY = QSlider(self.groupBox_4)
        self.FormActionsPostSliderContourXY.setObjectName(u"FormActionsPostSliderContourXY")
        self.FormActionsPostSliderContourXY.setOrientation(Qt.Horizontal)
        self.FormActionsPostSliderContourXY.setTickPosition(QSlider.TicksBelow)

        self.verticalLayout_61.addWidget(self.FormActionsPostSliderContourXY)

        self.FormActionsPostLabelContourXYposition = QLabel(self.groupBox_4)
        self.FormActionsPostLabelContourXYposition.setObjectName(u"FormActionsPostLabelContourXYposition")
        self.FormActionsPostLabelContourXYposition.setMinimumSize(QSize(0, 30))

        self.verticalLayout_61.addWidget(self.FormActionsPostLabelContourXYposition)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 0))
        self.groupBox_5.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_62 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.frame_951 = QFrame(self.groupBox_5)
        self.frame_951.setObjectName(u"frame_951")
        self.frame_951.setFrameShape(QFrame.NoFrame)
        self.frame_951.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_971 = QHBoxLayout(self.frame_951)
        self.horizontalLayout_971.setObjectName(u"horizontalLayout_971")
        self.FormActionsPostCheckContourYZ = QCheckBox(self.frame_951)
        self.FormActionsPostCheckContourYZ.setObjectName(u"FormActionsPostCheckContourYZ")

        self.horizontalLayout_971.addWidget(self.FormActionsPostCheckContourYZ)

        self.FormActionsPostLabelSurfaceNcontoursYZ = QSpinBox(self.frame_951)
        self.FormActionsPostLabelSurfaceNcontoursYZ.setObjectName(u"FormActionsPostLabelSurfaceNcontoursYZ")
        self.FormActionsPostLabelSurfaceNcontoursYZ.setMinimumSize(QSize(0, 24))
        self.FormActionsPostLabelSurfaceNcontoursYZ.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPostLabelSurfaceNcontoursYZ.setValue(5)

        self.horizontalLayout_971.addWidget(self.FormActionsPostLabelSurfaceNcontoursYZ)

        self.label_13 = QLabel(self.frame_951)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_971.addWidget(self.label_13)


        self.verticalLayout_62.addWidget(self.frame_951)

        self.FormActionsPostSliderContourYZ = QSlider(self.groupBox_5)
        self.FormActionsPostSliderContourYZ.setObjectName(u"FormActionsPostSliderContourYZ")
        self.FormActionsPostSliderContourYZ.setOrientation(Qt.Horizontal)
        self.FormActionsPostSliderContourYZ.setTickPosition(QSlider.TicksBelow)

        self.verticalLayout_62.addWidget(self.FormActionsPostSliderContourYZ)

        self.FormActionsPostLabelContourYZposition = QLabel(self.groupBox_5)
        self.FormActionsPostLabelContourYZposition.setObjectName(u"FormActionsPostLabelContourYZposition")
        self.FormActionsPostLabelContourYZposition.setMinimumSize(QSize(0, 30))

        self.verticalLayout_62.addWidget(self.FormActionsPostLabelContourYZposition)


        self.verticalLayout_5.addWidget(self.groupBox_5)

        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(0, 0))
        self.groupBox_7.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_63 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.frame_961 = QFrame(self.groupBox_7)
        self.frame_961.setObjectName(u"frame_961")
        self.frame_961.setFrameShape(QFrame.NoFrame)
        self.frame_961.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_981 = QHBoxLayout(self.frame_961)
        self.horizontalLayout_981.setObjectName(u"horizontalLayout_981")
        self.FormActionsPostCheckContourXZ = QCheckBox(self.frame_961)
        self.FormActionsPostCheckContourXZ.setObjectName(u"FormActionsPostCheckContourXZ")

        self.horizontalLayout_981.addWidget(self.FormActionsPostCheckContourXZ)

        self.FormActionsPostLabelSurfaceNcontoursXZ = QSpinBox(self.frame_961)
        self.FormActionsPostLabelSurfaceNcontoursXZ.setObjectName(u"FormActionsPostLabelSurfaceNcontoursXZ")
        self.FormActionsPostLabelSurfaceNcontoursXZ.setMinimumSize(QSize(0, 24))
        self.FormActionsPostLabelSurfaceNcontoursXZ.setMaximumSize(QSize(16777215, 24))
        self.FormActionsPostLabelSurfaceNcontoursXZ.setValue(5)

        self.horizontalLayout_981.addWidget(self.FormActionsPostLabelSurfaceNcontoursXZ)

        self.label_12 = QLabel(self.frame_961)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_981.addWidget(self.label_12)


        self.verticalLayout_63.addWidget(self.frame_961)

        self.FormActionsPostSliderContourXZ = QSlider(self.groupBox_7)
        self.FormActionsPostSliderContourXZ.setObjectName(u"FormActionsPostSliderContourXZ")
        self.FormActionsPostSliderContourXZ.setOrientation(Qt.Horizontal)
        self.FormActionsPostSliderContourXZ.setTickPosition(QSlider.TicksBelow)

        self.verticalLayout_63.addWidget(self.FormActionsPostSliderContourXZ)

        self.FormActionsPostLabelContourXZposition = QLabel(self.groupBox_7)
        self.FormActionsPostLabelContourXZposition.setObjectName(u"FormActionsPostLabelContourXZposition")
        self.FormActionsPostLabelContourXZposition.setMinimumSize(QSize(0, 30))

        self.verticalLayout_63.addWidget(self.FormActionsPostLabelContourXZposition)


        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.frame_14 = QFrame(self.tab_4)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_74 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_74.setObjectName(u"horizontalLayout_74")
        self.horizontalSpacer_48 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_74.addItem(self.horizontalSpacer_48)

        self.FormActionsPostButContour = QPushButton(self.frame_14)
        self.FormActionsPostButContour.setObjectName(u"FormActionsPostButContour")
        self.FormActionsPostButContour.setEnabled(False)

        self.horizontalLayout_74.addWidget(self.FormActionsPostButContour)

        self.horizontalSpacer_49 = QSpacerItem(117, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_74.addItem(self.horizontalSpacer_49)


        self.verticalLayout_5.addWidget(self.frame_14)

        self.tabWidget_2.addTab(self.tab_4, "")

        self.verticalLayout_12.addWidget(self.tabWidget_2)

        self.toolBox_2.addItem(self.page_2, u"Isosurface and Contours")
        self.page_24 = QWidget()
        self.page_24.setObjectName(u"page_24")
        self.page_24.setGeometry(QRect(0, 0, 370, 482))
        self.verticalLayout_44 = QVBoxLayout(self.page_24)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.tabWidget_6 = QTabWidget(self.page_24)
        self.tabWidget_6.setObjectName(u"tabWidget_6")
        self.tab_16 = QWidget()
        self.tab_16.setObjectName(u"tab_16")
        self.verticalLayout_25 = QVBoxLayout(self.tab_16)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.frame_60 = QFrame(self.tab_16)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setFrameShape(QFrame.NoFrame)
        self.frame_60.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_22)

        self.FormActionsPostButGetBonds = QPushButton(self.frame_60)
        self.FormActionsPostButGetBonds.setObjectName(u"FormActionsPostButGetBonds")

        self.horizontalLayout_51.addWidget(self.FormActionsPostButGetBonds)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_23)


        self.verticalLayout_25.addWidget(self.frame_60)

        self.FormActionsPosTableBonds = QTableWidget(self.tab_16)
        self.FormActionsPosTableBonds.setObjectName(u"FormActionsPosTableBonds")

        self.verticalLayout_25.addWidget(self.FormActionsPosTableBonds)

        self.frame_8 = QFrame(self.tab_16)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 80))
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_8)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.FormActionsPostComboBonds = QComboBox(self.frame_8)
        self.FormActionsPostComboBonds.setObjectName(u"FormActionsPostComboBonds")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.FormActionsPostComboBonds.sizePolicy().hasHeightForWidth())
        self.FormActionsPostComboBonds.setSizePolicy(sizePolicy4)

        self.verticalLayout_30.addWidget(self.FormActionsPostComboBonds)

        self.FormActionsPostLabelMeanBond = QLabel(self.frame_8)
        self.FormActionsPostLabelMeanBond.setObjectName(u"FormActionsPostLabelMeanBond")

        self.verticalLayout_30.addWidget(self.FormActionsPostLabelMeanBond)


        self.verticalLayout_25.addWidget(self.frame_8)

        self.frame_7 = QFrame(self.tab_16)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 40))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.frame_7.setLineWidth(0)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_27)

        self.FormActionsPostPlotBondsHistogramN = QSpinBox(self.frame_7)
        self.FormActionsPostPlotBondsHistogramN.setObjectName(u"FormActionsPostPlotBondsHistogramN")
        self.FormActionsPostPlotBondsHistogramN.setMinimum(1)
        self.FormActionsPostPlotBondsHistogramN.setValue(5)

        self.horizontalLayout_32.addWidget(self.FormActionsPostPlotBondsHistogramN)

        self.FormActionsPostButPlotBondsHistogram = QPushButton(self.frame_7)
        self.FormActionsPostButPlotBondsHistogram.setObjectName(u"FormActionsPostButPlotBondsHistogram")
        self.FormActionsPostButPlotBondsHistogram.setEnabled(False)

        self.horizontalLayout_32.addWidget(self.FormActionsPostButPlotBondsHistogram)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_26)


        self.verticalLayout_25.addWidget(self.frame_7)

        self.tabWidget_6.addTab(self.tab_16, "")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.verticalLayout_55 = QVBoxLayout(self.tab_17)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.frame_4 = QFrame(self.tab_17)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setMaximumSize(QSize(16777215, 50))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.FormActionsPostComboCellParam = QComboBox(self.frame_4)
        self.FormActionsPostComboCellParam.setObjectName(u"FormActionsPostComboCellParam")

        self.horizontalLayout_10.addWidget(self.FormActionsPostComboCellParam)

        self.FormActionsPostComboCellParamX = QComboBox(self.frame_4)
        self.FormActionsPostComboCellParamX.setObjectName(u"FormActionsPostComboCellParamX")

        self.horizontalLayout_10.addWidget(self.FormActionsPostComboCellParamX)


        self.verticalLayout_55.addWidget(self.frame_4)

        self.FormActionsPostTableCellParam = QTableWidget(self.tab_17)
        self.FormActionsPostTableCellParam.setObjectName(u"FormActionsPostTableCellParam")
        self.FormActionsPostTableCellParam.setMinimumSize(QSize(0, 100))

        self.verticalLayout_55.addWidget(self.FormActionsPostTableCellParam)

        self.frame = QFrame(self.tab_17)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 50))
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 2, -1, 2)
        self.FormActionsPostButAddRowCellParam = QPushButton(self.frame)
        self.FormActionsPostButAddRowCellParam.setObjectName(u"FormActionsPostButAddRowCellParam")

        self.horizontalLayout_15.addWidget(self.FormActionsPostButAddRowCellParam)

        self.FormActionsPostButDeleteRowCellParam = QPushButton(self.frame)
        self.FormActionsPostButDeleteRowCellParam.setObjectName(u"FormActionsPostButDeleteRowCellParam")

        self.horizontalLayout_15.addWidget(self.FormActionsPostButDeleteRowCellParam)

        self.FormActionsPostButPlusCellParam = QPushButton(self.frame)
        self.FormActionsPostButPlusCellParam.setObjectName(u"FormActionsPostButPlusCellParam")
        self.FormActionsPostButPlusCellParam.setStyleSheet(u"")

        self.horizontalLayout_15.addWidget(self.FormActionsPostButPlusCellParam)


        self.verticalLayout_55.addWidget(self.frame)

        self.frame_21 = QFrame(self.tab_17)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMinimumSize(QSize(0, 50))
        self.frame_21.setMaximumSize(QSize(16777215, 50))
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, 2, -1, 2)
        self.FormActionsPostButPlusDataCellParam = QPushButton(self.frame_21)
        self.FormActionsPostButPlusDataCellParam.setObjectName(u"FormActionsPostButPlusDataCellParam")

        self.horizontalLayout_16.addWidget(self.FormActionsPostButPlusDataCellParam)

        self.FormActionsPostButOptimizeCellParam = QPushButton(self.frame_21)
        self.FormActionsPostButOptimizeCellParam.setObjectName(u"FormActionsPostButOptimizeCellParam")

        self.horizontalLayout_16.addWidget(self.FormActionsPostButOptimizeCellParam)


        self.verticalLayout_55.addWidget(self.frame_21)

        self.frame_3 = QFrame(self.tab_17)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setEnabled(True)
        self.frame_3.setMinimumSize(QSize(0, 130))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.FormActionsPostLabelCellParamOptimExpr = QLabel(self.frame_3)
        self.FormActionsPostLabelCellParamOptimExpr.setObjectName(u"FormActionsPostLabelCellParamOptimExpr")
        self.FormActionsPostLabelCellParamOptimExpr.setGeometry(QRect(20, 70, 141, 16))
        self.FormActionsPostLabelCellParamFig = QLabel(self.frame_3)
        self.FormActionsPostLabelCellParamFig.setObjectName(u"FormActionsPostLabelCellParamFig")
        self.FormActionsPostLabelCellParamFig.setGeometry(QRect(10, 0, 321, 41))
        self.FormActionsPostLabelCellParamOptimExpr2 = QLabel(self.frame_3)
        self.FormActionsPostLabelCellParamOptimExpr2.setObjectName(u"FormActionsPostLabelCellParamOptimExpr2")
        self.FormActionsPostLabelCellParamOptimExpr2.setGeometry(QRect(20, 100, 151, 16))
        self.FormActionsPostLabelCellParamOptimExpr3 = QLabel(self.frame_3)
        self.FormActionsPostLabelCellParamOptimExpr3.setObjectName(u"FormActionsPostLabelCellParamOptimExpr3")
        self.FormActionsPostLabelCellParamOptimExpr3.setGeometry(QRect(200, 70, 121, 16))
        self.FormActionsPostLabelCellParamOptimExpr4 = QLabel(self.frame_3)
        self.FormActionsPostLabelCellParamOptimExpr4.setObjectName(u"FormActionsPostLabelCellParamOptimExpr4")
        self.FormActionsPostLabelCellParamOptimExpr4.setGeometry(QRect(200, 100, 121, 16))

        self.verticalLayout_55.addWidget(self.frame_3)

        self.tabWidget_6.addTab(self.tab_17, "")
        self.tab_21 = QWidget()
        self.tab_21.setObjectName(u"tab_21")
        self.verticalLayout_59 = QVBoxLayout(self.tab_21)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.AtomPropertiesText = QTextBrowser(self.tab_21)
        self.AtomPropertiesText.setObjectName(u"AtomPropertiesText")

        self.verticalLayout_59.addWidget(self.AtomPropertiesText)

        self.groupBox_20 = QGroupBox(self.tab_21)
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


        self.verticalLayout_59.addWidget(self.groupBox_20)

        self.tabWidget_6.addTab(self.tab_21, "")
        self.tab_19 = QWidget()
        self.tab_19.setObjectName(u"tab_19")
        self.verticalLayout_60 = QVBoxLayout(self.tab_19)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.frame_22 = QFrame(self.tab_19)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(0, 40))
        self.frame_22.setFrameShape(QFrame.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_21 = QLabel(self.frame_22)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_12.addWidget(self.label_21)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_12)

        self.FormActionsPostTextVoronoiMaxDist = QSpinBox(self.frame_22)
        self.FormActionsPostTextVoronoiMaxDist.setObjectName(u"FormActionsPostTextVoronoiMaxDist")
        self.FormActionsPostTextVoronoiMaxDist.setMinimumSize(QSize(60, 24))
        self.FormActionsPostTextVoronoiMaxDist.setMaximumSize(QSize(100, 24))
        self.FormActionsPostTextVoronoiMaxDist.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.FormActionsPostTextVoronoiMaxDist.setValue(5)

        self.horizontalLayout_12.addWidget(self.FormActionsPostTextVoronoiMaxDist)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_13)


        self.verticalLayout_60.addWidget(self.frame_22)

        self.frame_19 = QFrame(self.tab_19)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(125, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.FormActionsPostButVoronoi = QPushButton(self.frame_19)
        self.FormActionsPostButVoronoi.setObjectName(u"FormActionsPostButVoronoi")

        self.horizontalLayout_7.addWidget(self.FormActionsPostButVoronoi)

        self.horizontalSpacer_4 = QSpacerItem(125, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.verticalLayout_60.addWidget(self.frame_19)

        self.FormActionsPostLabelVoronoiAtom = QLabel(self.tab_19)
        self.FormActionsPostLabelVoronoiAtom.setObjectName(u"FormActionsPostLabelVoronoiAtom")
        self.FormActionsPostLabelVoronoiAtom.setMinimumSize(QSize(0, 30))

        self.verticalLayout_60.addWidget(self.FormActionsPostLabelVoronoiAtom)

        self.FormActionsPostLabelVoronoiVolume = QLabel(self.tab_19)
        self.FormActionsPostLabelVoronoiVolume.setObjectName(u"FormActionsPostLabelVoronoiVolume")
        self.FormActionsPostLabelVoronoiVolume.setMinimumSize(QSize(0, 30))

        self.verticalLayout_60.addWidget(self.FormActionsPostLabelVoronoiVolume)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_60.addItem(self.verticalSpacer_3)

        self.tabWidget_6.addTab(self.tab_19, "")

        self.verticalLayout_44.addWidget(self.tabWidget_6)

        self.toolBox_2.addItem(self.page_24, u"Structural properties")
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.page_13.setGeometry(QRect(0, 0, 339, 57))
        self.verticalLayout_43 = QVBoxLayout(self.page_13)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.frame_59 = QFrame(self.page_13)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setMinimumSize(QSize(0, 35))
        self.frame_59.setFrameShape(QFrame.NoFrame)
        self.frame_59.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_59)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_36 = QFrame(self.frame_59)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.NoFrame)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_71 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_71.setObjectName(u"horizontalLayout_71")
        self.horizontalLayout_71.setContentsMargins(0, -1, 0, -1)
        self.ColorAtomsWithProperty = QCheckBox(self.frame_36)
        self.ColorAtomsWithProperty.setObjectName(u"ColorAtomsWithProperty")

        self.horizontalLayout_71.addWidget(self.ColorAtomsWithProperty)

        self.PropertyForColorOfAtoms = QComboBox(self.frame_36)
        self.PropertyForColorOfAtoms.setObjectName(u"PropertyForColorOfAtoms")

        self.horizontalLayout_71.addWidget(self.PropertyForColorOfAtoms)


        self.verticalLayout_27.addWidget(self.frame_36)

        self.ActivateFragmentSelectionModeCheckBox = QCheckBox(self.frame_59)
        self.ActivateFragmentSelectionModeCheckBox.setObjectName(u"ActivateFragmentSelectionModeCheckBox")

        self.verticalLayout_27.addWidget(self.ActivateFragmentSelectionModeCheckBox)

        self.groupBox_21 = QGroupBox(self.frame_59)
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

        self.horizontalSpacer_47 = QSpacerItem(228, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_72.addItem(self.horizontalSpacer_47)


        self.verticalLayout_27.addWidget(self.groupBox_21)

        self.AtomsInSelectedFragment = QListWidget(self.frame_59)
        self.AtomsInSelectedFragment.setObjectName(u"AtomsInSelectedFragment")

        self.verticalLayout_27.addWidget(self.AtomsInSelectedFragment)

        self.frame_61 = QFrame(self.frame_59)
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


        self.verticalLayout_27.addWidget(self.frame_61)

        self.frame_62 = QFrame(self.frame_59)
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


        self.verticalLayout_27.addWidget(self.frame_62)

        self.frame_63 = QFrame(self.frame_59)
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


        self.verticalLayout_27.addWidget(self.frame_63)

        self.frame_64 = QFrame(self.frame_59)
        self.frame_64.setObjectName(u"frame_64")
        self.frame_64.setMinimumSize(QSize(0, 40))
        self.frame_64.setFrameShape(QFrame.NoFrame)
        self.frame_64.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_64)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_28 = QSpacerItem(107, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_28)

        self.fragment1Clear = QPushButton(self.frame_64)
        self.fragment1Clear.setObjectName(u"fragment1Clear")
        self.fragment1Clear.setEnabled(False)

        self.horizontalLayout_56.addWidget(self.fragment1Clear)

        self.horizontalSpacer_29 = QSpacerItem(106, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_29)


        self.verticalLayout_27.addWidget(self.frame_64)


        self.verticalLayout_43.addWidget(self.frame_59)

        self.toolBox_2.addItem(self.page_13, u"Coloring")

        self.verticalLayout_8.addWidget(self.toolBox_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_23 = QWidget()
        self.tab_23.setObjectName(u"tab_23")
        self.verticalLayout_71 = QVBoxLayout(self.tab_23)
        self.verticalLayout_71.setObjectName(u"verticalLayout_71")
        self.toolBox_4 = QToolBox(self.tab_23)
        self.toolBox_4.setObjectName(u"toolBox_4")
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.page_9.setGeometry(QRect(0, 0, 399, 675))
        self.verticalLayout_72 = QVBoxLayout(self.page_9)
        self.verticalLayout_72.setObjectName(u"verticalLayout_72")
        self.textBrowser = QTextBrowser(self.page_9)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(True)

        self.verticalLayout_72.addWidget(self.textBrowser)

        self.toolBox_4.addItem(self.page_9, u"Import")
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.page_10.setGeometry(QRect(0, 0, 384, 455))
        self.verticalLayout_75 = QVBoxLayout(self.page_10)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.groupBox_11 = QGroupBox(self.page_10)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_74 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_74.setObjectName(u"verticalLayout_74")
        self.label_36 = QLabel(self.groupBox_11)
        self.label_36.setObjectName(u"label_36")

        self.verticalLayout_74.addWidget(self.label_36)


        self.verticalLayout_75.addWidget(self.groupBox_11)

        self.groupBox_24 = QGroupBox(self.page_10)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.verticalLayout_73 = QVBoxLayout(self.groupBox_24)
        self.verticalLayout_73.setObjectName(u"verticalLayout_73")
        self.label_35 = QLabel(self.groupBox_24)
        self.label_35.setObjectName(u"label_35")

        self.verticalLayout_73.addWidget(self.label_35)


        self.verticalLayout_75.addWidget(self.groupBox_24)

        self.groupBox_29 = QGroupBox(self.page_10)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(0, 300))
        self.label_81 = QLabel(self.groupBox_29)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setGeometry(QRect(10, 40, 261, 16))
        self.groupBox_32 = QGroupBox(self.groupBox_29)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setGeometry(QRect(10, 70, 363, 63))
        self.horizontalLayout_122 = QHBoxLayout(self.groupBox_32)
        self.horizontalLayout_122.setObjectName(u"horizontalLayout_122")
        self.radioButton = QRadioButton(self.groupBox_32)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setCheckable(False)
        self.radioButton.setChecked(False)

        self.horizontalLayout_122.addWidget(self.radioButton)

        self.horizontalSpacer_81 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_122.addItem(self.horizontalSpacer_81)

        self.radioButton_4 = QRadioButton(self.groupBox_32)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setCheckable(False)

        self.horizontalLayout_122.addWidget(self.radioButton_4)

        self.horizontalSpacer_82 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_122.addItem(self.horizontalSpacer_82)

        self.crystal_d12_1d = QRadioButton(self.groupBox_32)
        self.crystal_d12_1d.setObjectName(u"crystal_d12_1d")
        self.crystal_d12_1d.setChecked(True)

        self.horizontalLayout_122.addWidget(self.crystal_d12_1d)

        self.horizontalSpacer_83 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_122.addItem(self.horizontalSpacer_83)

        self.radioButton_6 = QRadioButton(self.groupBox_32)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setCheckable(False)

        self.horizontalLayout_122.addWidget(self.radioButton_6)

        self.tabWidget_7 = QTabWidget(self.groupBox_29)
        self.tabWidget_7.setObjectName(u"tabWidget_7")
        self.tabWidget_7.setGeometry(QRect(10, 140, 361, 91))
        self.tab_25 = QWidget()
        self.tab_25.setObjectName(u"tab_25")
        self.tabWidget_7.addTab(self.tab_25, "")
        self.tab_26 = QWidget()
        self.tab_26.setObjectName(u"tab_26")
        self.tabWidget_7.addTab(self.tab_26, "")
        self.tab_27 = QWidget()
        self.tab_27.setObjectName(u"tab_27")
        self.frame_119 = QFrame(self.tab_27)
        self.frame_119.setObjectName(u"frame_119")
        self.frame_119.setGeometry(QRect(10, 10, 322, 47))
        self.frame_119.setFrameShape(QFrame.StyledPanel)
        self.frame_119.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_123 = QHBoxLayout(self.frame_119)
        self.horizontalLayout_123.setObjectName(u"horizontalLayout_123")
        self.label_90 = QLabel(self.frame_119)
        self.label_90.setObjectName(u"label_90")

        self.horizontalLayout_123.addWidget(self.label_90)

        self.tabWidget_7.addTab(self.tab_27, "")
        self.tab_28 = QWidget()
        self.tab_28.setObjectName(u"tab_28")
        self.tabWidget_7.addTab(self.tab_28, "")
        self.FormIEd12Generate = QPushButton(self.groupBox_29)
        self.FormIEd12Generate.setObjectName(u"FormIEd12Generate")
        self.FormIEd12Generate.setGeometry(QRect(140, 250, 93, 28))

        self.verticalLayout_75.addWidget(self.groupBox_29)

        self.verticalSpacer_26 = QSpacerItem(20, 529, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_75.addItem(self.verticalSpacer_26)

        self.toolBox_4.addItem(self.page_10, u"Export")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 218, 557))
        self.verticalLayout_69 = QVBoxLayout(self.page_3)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.frame_127 = QFrame(self.page_3)
        self.frame_127.setObjectName(u"frame_127")
        self.frame_127.setFrameShape(QFrame.StyledPanel)
        self.frame_127.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_131 = QHBoxLayout(self.frame_127)
        self.horizontalLayout_131.setObjectName(u"horizontalLayout_131")
        self.horizontalSpacer_84 = QSpacerItem(106, 25, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_131.addItem(self.horizontalSpacer_84)

        self.FormASERamanAndIRscriptCreate = QPushButton(self.frame_127)
        self.FormASERamanAndIRscriptCreate.setObjectName(u"FormASERamanAndIRscriptCreate")

        self.horizontalLayout_131.addWidget(self.FormASERamanAndIRscriptCreate)

        self.horizontalSpacer_85 = QSpacerItem(118, 25, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_131.addItem(self.horizontalSpacer_85)


        self.verticalLayout_69.addWidget(self.frame_127)

        self.frame_128 = QFrame(self.page_3)
        self.frame_128.setObjectName(u"frame_128")
        self.frame_128.setFrameShape(QFrame.StyledPanel)
        self.frame_128.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_132 = QHBoxLayout(self.frame_128)
        self.horizontalLayout_132.setObjectName(u"horizontalLayout_132")
        self.horizontalSpacer_90 = QSpacerItem(120, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_132.addItem(self.horizontalSpacer_90)

        self.FormASERamanAndIRscriptParse = QPushButton(self.frame_128)
        self.FormASERamanAndIRscriptParse.setObjectName(u"FormASERamanAndIRscriptParse")

        self.horizontalLayout_132.addWidget(self.FormASERamanAndIRscriptParse)

        self.horizontalSpacer_91 = QSpacerItem(120, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_132.addItem(self.horizontalSpacer_91)


        self.verticalLayout_69.addWidget(self.frame_128)

        self.tabWidget_8 = QTabWidget(self.page_3)
        self.tabWidget_8.setObjectName(u"tabWidget_8")
        self.tab_30 = QWidget()
        self.tab_30.setObjectName(u"tab_30")
        self.verticalLayout_84 = QVBoxLayout(self.tab_30)
        self.verticalLayout_84.setObjectName(u"verticalLayout_84")
        self.FormRamanSpectraText = QPlainTextEdit(self.tab_30)
        self.FormRamanSpectraText.setObjectName(u"FormRamanSpectraText")
        self.FormRamanSpectraText.setReadOnly(True)

        self.verticalLayout_84.addWidget(self.FormRamanSpectraText)

        self.tabWidget_8.addTab(self.tab_30, "")
        self.tab_31 = QWidget()
        self.tab_31.setObjectName(u"tab_31")
        self.verticalLayout_81 = QVBoxLayout(self.tab_31)
        self.verticalLayout_81.setObjectName(u"verticalLayout_81")
        self.FormIrSpectraText = QPlainTextEdit(self.tab_31)
        self.FormIrSpectraText.setObjectName(u"FormIrSpectraText")
        self.FormIrSpectraText.setReadOnly(True)

        self.verticalLayout_81.addWidget(self.FormIrSpectraText)

        self.tabWidget_8.addTab(self.tab_31, "")

        self.verticalLayout_69.addWidget(self.tabWidget_8)

        self.groupBox_33 = QGroupBox(self.page_3)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.groupBox_33.setMinimumSize(QSize(0, 0))
        self.verticalLayout_85 = QVBoxLayout(self.groupBox_33)
        self.verticalLayout_85.setObjectName(u"verticalLayout_85")
        self.frame_130 = QFrame(self.groupBox_33)
        self.frame_130.setObjectName(u"frame_130")
        self.frame_130.setFrameShape(QFrame.StyledPanel)
        self.frame_130.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_124 = QHBoxLayout(self.frame_130)
        self.horizontalLayout_124.setObjectName(u"horizontalLayout_124")
        self.label_94 = QLabel(self.frame_130)
        self.label_94.setObjectName(u"label_94")

        self.horizontalLayout_124.addWidget(self.label_94)

        self.formGaussWidth = QDoubleSpinBox(self.frame_130)
        self.formGaussWidth.setObjectName(u"formGaussWidth")
        self.formGaussWidth.setDecimals(3)
        self.formGaussWidth.setMaximum(100.000000000000000)
        self.formGaussWidth.setSingleStep(0.100000000000000)
        self.formGaussWidth.setValue(0.010000000000000)

        self.horizontalLayout_124.addWidget(self.formGaussWidth)

        self.horizontalSpacer_92 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_124.addItem(self.horizontalSpacer_92)


        self.verticalLayout_85.addWidget(self.frame_130)

        self.frame_131 = QFrame(self.groupBox_33)
        self.frame_131.setObjectName(u"frame_131")
        self.frame_131.setFrameShape(QFrame.StyledPanel)
        self.frame_131.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_134 = QHBoxLayout(self.frame_131)
        self.horizontalLayout_134.setObjectName(u"horizontalLayout_134")
        self.frame_129 = QFrame(self.frame_131)
        self.frame_129.setObjectName(u"frame_129")
        self.frame_129.setFrameShape(QFrame.StyledPanel)
        self.frame_129.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_133 = QHBoxLayout(self.frame_129)
        self.horizontalLayout_133.setObjectName(u"horizontalLayout_133")
        self.form_raman_radio = QRadioButton(self.frame_129)
        self.form_raman_radio.setObjectName(u"form_raman_radio")
        self.form_raman_radio.setChecked(True)

        self.horizontalLayout_133.addWidget(self.form_raman_radio)

        self.radioButton_7 = QRadioButton(self.frame_129)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.horizontalLayout_133.addWidget(self.radioButton_7)

        self.horizontalSpacer_96 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_133.addItem(self.horizontalSpacer_96)


        self.horizontalLayout_134.addWidget(self.frame_129)


        self.verticalLayout_85.addWidget(self.frame_131)

        self.frame_132 = QFrame(self.groupBox_33)
        self.frame_132.setObjectName(u"frame_132")
        self.frame_132.setFrameShape(QFrame.StyledPanel)
        self.frame_132.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_136 = QHBoxLayout(self.frame_132)
        self.horizontalLayout_136.setObjectName(u"horizontalLayout_136")
        self.form_spectra_mev_radio = QRadioButton(self.frame_132)
        self.form_spectra_mev_radio.setObjectName(u"form_spectra_mev_radio")
        self.form_spectra_mev_radio.setChecked(True)

        self.horizontalLayout_136.addWidget(self.form_spectra_mev_radio)

        self.radioButton_8 = QRadioButton(self.frame_132)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.horizontalLayout_136.addWidget(self.radioButton_8)

        self.horizontalSpacer_95 = QSpacerItem(194, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_136.addItem(self.horizontalSpacer_95)


        self.verticalLayout_85.addWidget(self.frame_132)

        self.frame_133 = QFrame(self.groupBox_33)
        self.frame_133.setObjectName(u"frame_133")
        self.frame_133.setFrameShape(QFrame.StyledPanel)
        self.frame_133.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_135 = QHBoxLayout(self.frame_133)
        self.horizontalLayout_135.setObjectName(u"horizontalLayout_135")
        self.horizontalSpacer_93 = QSpacerItem(108, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_135.addItem(self.horizontalSpacer_93)

        self.FormASERamanAndIRscriptPlot = QPushButton(self.frame_133)
        self.FormASERamanAndIRscriptPlot.setObjectName(u"FormASERamanAndIRscriptPlot")

        self.horizontalLayout_135.addWidget(self.FormASERamanAndIRscriptPlot)

        self.horizontalSpacer_94 = QSpacerItem(108, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_135.addItem(self.horizontalSpacer_94)


        self.verticalLayout_85.addWidget(self.frame_133)


        self.verticalLayout_69.addWidget(self.groupBox_33)

        self.toolBox_4.addItem(self.page_3, u"Raman and IR (ASE)")
        self.page_23 = QWidget()
        self.page_23.setObjectName(u"page_23")
        self.page_23.setGeometry(QRect(0, 0, 371, 716))
        self.verticalLayout_83 = QVBoxLayout(self.page_23)
        self.verticalLayout_83.setObjectName(u"verticalLayout_83")
        self.FormButtonAddCroData = QPushButton(self.page_23)
        self.FormButtonAddCroData.setObjectName(u"FormButtonAddCroData")

        self.verticalLayout_83.addWidget(self.FormButtonAddCroData)

        self.frame_109 = QFrame(self.page_23)
        self.frame_109.setObjectName(u"frame_109")
        self.frame_109.setMinimumSize(QSize(150, 0))
        self.frame_109.setFrameShape(QFrame.StyledPanel)
        self.frame_109.setFrameShadow(QFrame.Raised)
        self.verticalLayout_80 = QVBoxLayout(self.frame_109)
        self.verticalLayout_80.setObjectName(u"verticalLayout_80")
        self.groupBox_30 = QGroupBox(self.frame_109)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.verticalLayout_79 = QVBoxLayout(self.groupBox_30)
        self.verticalLayout_79.setObjectName(u"verticalLayout_79")
        self.frame_110 = QFrame(self.groupBox_30)
        self.frame_110.setObjectName(u"frame_110")
        self.frame_110.setFrameShape(QFrame.NoFrame)
        self.frame_110.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_112 = QHBoxLayout(self.frame_110)
        self.horizontalLayout_112.setObjectName(u"horizontalLayout_112")
        self.label_82 = QLabel(self.frame_110)
        self.label_82.setObjectName(u"label_82")

        self.horizontalLayout_112.addWidget(self.label_82)

        self.FormSelectedCP = QLabel(self.frame_110)
        self.FormSelectedCP.setObjectName(u"FormSelectedCP")

        self.horizontalLayout_112.addWidget(self.FormSelectedCP)


        self.verticalLayout_79.addWidget(self.frame_110)

        self.frame_111 = QFrame(self.groupBox_30)
        self.frame_111.setObjectName(u"frame_111")
        self.frame_111.setFrameShape(QFrame.NoFrame)
        self.frame_111.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_113 = QHBoxLayout(self.frame_111)
        self.horizontalLayout_113.setObjectName(u"horizontalLayout_113")
        self.label_84 = QLabel(self.frame_111)
        self.label_84.setObjectName(u"label_84")

        self.horizontalLayout_113.addWidget(self.label_84)

        self.FormSelectedCP_f = QLabel(self.frame_111)
        self.FormSelectedCP_f.setObjectName(u"FormSelectedCP_f")

        self.horizontalLayout_113.addWidget(self.FormSelectedCP_f)


        self.verticalLayout_79.addWidget(self.frame_111)

        self.frame_112 = QFrame(self.groupBox_30)
        self.frame_112.setObjectName(u"frame_112")
        self.frame_112.setFrameShape(QFrame.NoFrame)
        self.frame_112.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_114 = QHBoxLayout(self.frame_112)
        self.horizontalLayout_114.setObjectName(u"horizontalLayout_114")
        self.label_85 = QLabel(self.frame_112)
        self.label_85.setObjectName(u"label_85")

        self.horizontalLayout_114.addWidget(self.label_85)

        self.FormSelectedCP_g = QLabel(self.frame_112)
        self.FormSelectedCP_g.setObjectName(u"FormSelectedCP_g")

        self.horizontalLayout_114.addWidget(self.FormSelectedCP_g)


        self.verticalLayout_79.addWidget(self.frame_112)

        self.frame_113 = QFrame(self.groupBox_30)
        self.frame_113.setObjectName(u"frame_113")
        self.frame_113.setFrameShape(QFrame.NoFrame)
        self.frame_113.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_115 = QHBoxLayout(self.frame_113)
        self.horizontalLayout_115.setObjectName(u"horizontalLayout_115")
        self.label_87 = QLabel(self.frame_113)
        self.label_87.setObjectName(u"label_87")

        self.horizontalLayout_115.addWidget(self.label_87)

        self.FormSelectedCP_lap = QLabel(self.frame_113)
        self.FormSelectedCP_lap.setObjectName(u"FormSelectedCP_lap")

        self.horizontalLayout_115.addWidget(self.FormSelectedCP_lap)


        self.verticalLayout_79.addWidget(self.frame_113)


        self.verticalLayout_80.addWidget(self.groupBox_30)

        self.FormCPaddToList = QPushButton(self.frame_109)
        self.FormCPaddToList.setObjectName(u"FormCPaddToList")

        self.verticalLayout_80.addWidget(self.FormCPaddToList)


        self.verticalLayout_83.addWidget(self.frame_109)

        self.tabWidget_10 = QTabWidget(self.page_23)
        self.tabWidget_10.setObjectName(u"tabWidget_10")
        self.tab_35 = QWidget()
        self.tab_35.setObjectName(u"tab_35")
        self.verticalLayout_11 = QVBoxLayout(self.tab_35)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.FormCPlist = QListWidget(self.tab_35)
        self.FormCPlist.setObjectName(u"FormCPlist")
        self.FormCPlist.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_11.addWidget(self.FormCPlist)

        self.FormCPdeleteFromList = QPushButton(self.tab_35)
        self.FormCPdeleteFromList.setObjectName(u"FormCPdeleteFromList")

        self.verticalLayout_11.addWidget(self.FormCPdeleteFromList)

        self.tabWidget_10.addTab(self.tab_35, "")
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.verticalLayout_90 = QVBoxLayout(self.tab_20)
        self.verticalLayout_90.setObjectName(u"verticalLayout_90")
        self.groupBox_34 = QGroupBox(self.tab_20)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setMinimumSize(QSize(0, 0))
        self.verticalLayout_87 = QVBoxLayout(self.groupBox_34)
        self.verticalLayout_87.setObjectName(u"verticalLayout_87")
        self.verticalLayout_87.setContentsMargins(-1, -1, 0, -1)
        self.frame_140 = QFrame(self.groupBox_34)
        self.frame_140.setObjectName(u"frame_140")
        self.frame_140.setFrameShape(QFrame.NoFrame)
        self.frame_140.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_143 = QHBoxLayout(self.frame_140)
        self.horizontalLayout_143.setObjectName(u"horizontalLayout_143")
        self.form_critic_all_cp = QCheckBox(self.frame_140)
        self.form_critic_all_cp.setObjectName(u"form_critic_all_cp")

        self.horizontalLayout_143.addWidget(self.form_critic_all_cp)


        self.verticalLayout_87.addWidget(self.frame_140)

        self.frame_134 = QFrame(self.groupBox_34)
        self.frame_134.setObjectName(u"frame_134")
        self.frame_134.setFrameShape(QFrame.NoFrame)
        self.frame_134.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_137 = QHBoxLayout(self.frame_134)
        self.horizontalLayout_137.setObjectName(u"horizontalLayout_137")
        self.horizontalLayout_137.setContentsMargins(-1, -1, 0, -1)
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

        self.groupBox_37 = QGroupBox(self.groupBox_34)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.verticalLayout_86 = QVBoxLayout(self.groupBox_37)
        self.verticalLayout_86.setObjectName(u"verticalLayout_86")
        self.verticalLayout_86.setContentsMargins(-1, -1, 0, -1)
        self.frame_135 = QFrame(self.groupBox_37)
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

        self.frame_136 = QFrame(self.groupBox_37)
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


        self.verticalLayout_87.addWidget(self.groupBox_37)

        self.frame_115 = QFrame(self.groupBox_34)
        self.frame_115.setObjectName(u"frame_115")
        self.frame_115.setMinimumSize(QSize(0, 0))
        self.frame_115.setFrameShape(QFrame.NoFrame)
        self.frame_115.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_141 = QHBoxLayout(self.frame_115)
        self.horizontalLayout_141.setObjectName(u"horizontalLayout_141")
        self.horizontalSpacer_77 = QSpacerItem(95, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_141.addItem(self.horizontalSpacer_77)

        self.FormCreateCriFile = QPushButton(self.frame_115)
        self.FormCreateCriFile.setObjectName(u"FormCreateCriFile")

        self.horizontalLayout_141.addWidget(self.FormCreateCriFile)

        self.horizontalSpacer_97 = QSpacerItem(95, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_141.addItem(self.horizontalSpacer_97)


        self.verticalLayout_87.addWidget(self.frame_115)


        self.verticalLayout_90.addWidget(self.groupBox_34)

        self.tabWidget_10.addTab(self.tab_20, "")
        self.tab_34 = QWidget()
        self.tab_34.setObjectName(u"tab_34")
        self.verticalLayout_88 = QVBoxLayout(self.tab_34)
        self.verticalLayout_88.setObjectName(u"verticalLayout_88")
        self.groupBox_35 = QGroupBox(self.tab_34)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setMinimumSize(QSize(0, 0))
        self.verticalLayout_89 = QVBoxLayout(self.groupBox_35)
        self.verticalLayout_89.setObjectName(u"verticalLayout_89")
        self.frame_125 = QFrame(self.groupBox_35)
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


        self.verticalLayout_89.addWidget(self.frame_125)

        self.frame_139 = QFrame(self.groupBox_35)
        self.frame_139.setObjectName(u"frame_139")
        self.frame_139.setFrameShape(QFrame.NoFrame)
        self.frame_139.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_142 = QHBoxLayout(self.frame_139)
        self.horizontalLayout_142.setObjectName(u"horizontalLayout_142")
        self.horizontalSpacer_98 = QSpacerItem(93, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_142.addItem(self.horizontalSpacer_98)

        self.FormCreateCriXYZFile = QPushButton(self.frame_139)
        self.FormCreateCriXYZFile.setObjectName(u"FormCreateCriXYZFile")

        self.horizontalLayout_142.addWidget(self.FormCreateCriXYZFile)

        self.horizontalSpacer_99 = QSpacerItem(93, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_142.addItem(self.horizontalSpacer_99)


        self.verticalLayout_89.addWidget(self.frame_139)


        self.verticalLayout_88.addWidget(self.groupBox_35)

        self.verticalSpacer = QSpacerItem(20, 158, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_88.addItem(self.verticalSpacer)

        self.tabWidget_10.addTab(self.tab_34, "")

        self.verticalLayout_83.addWidget(self.tabWidget_10)

        self.toolBox_4.addItem(self.page_23, u"Critical points (Critic2 *.cri file)")

        self.verticalLayout_71.addWidget(self.toolBox_4)

        self.tabWidget.addTab(self.tab_23, "")
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
        self.frame_65 = QFrame(self.tab_32)
        self.frame_65.setObjectName(u"frame_65")
        self.frame_65.setMinimumSize(QSize(200, 0))
        self.frame_65.setFrameShape(QFrame.StyledPanel)
        self.frame_65.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_65)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsViewCheckShowAtoms = QCheckBox(self.frame_65)
        self.FormSettingsViewCheckShowAtoms.setObjectName(u"FormSettingsViewCheckShowAtoms")
        self.FormSettingsViewCheckShowAtoms.setEnabled(True)

        self.horizontalLayout_57.addWidget(self.FormSettingsViewCheckShowAtoms)


        self.verticalLayout_31.addWidget(self.frame_65)

        self.frame_91 = QFrame(self.tab_32)
        self.frame_91.setObjectName(u"frame_91")
        self.frame_91.setFrameShape(QFrame.StyledPanel)
        self.frame_91.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_139 = QHBoxLayout(self.frame_91)
        self.horizontalLayout_139.setObjectName(u"horizontalLayout_139")
        self.horizontalLayout_139.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsViewCheckShowAtomNumber = QCheckBox(self.frame_91)
        self.FormSettingsViewCheckShowAtomNumber.setObjectName(u"FormSettingsViewCheckShowAtomNumber")
        self.FormSettingsViewCheckShowAtomNumber.setEnabled(True)

        self.horizontalLayout_139.addWidget(self.FormSettingsViewCheckShowAtomNumber)


        self.verticalLayout_31.addWidget(self.frame_91)

        self.frame_66 = QFrame(self.tab_32)
        self.frame_66.setObjectName(u"frame_66")
        self.frame_66.setMinimumSize(QSize(200, 0))
        self.frame_66.setFrameShape(QFrame.StyledPanel)
        self.frame_66.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_66)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.horizontalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsViewCheckShowBox = QCheckBox(self.frame_66)
        self.FormSettingsViewCheckShowBox.setObjectName(u"FormSettingsViewCheckShowBox")
        self.FormSettingsViewCheckShowBox.setStyleSheet(u"")

        self.horizontalLayout_58.addWidget(self.FormSettingsViewCheckShowBox)


        self.verticalLayout_31.addWidget(self.frame_66)

        self.frame_67 = QFrame(self.tab_32)
        self.frame_67.setObjectName(u"frame_67")
        self.frame_67.setMinimumSize(QSize(200, 0))
        self.frame_67.setFrameShape(QFrame.StyledPanel)
        self.frame_67.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_67)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.horizontalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsViewCheckShowAxes = QCheckBox(self.frame_67)
        self.FormSettingsViewCheckShowAxes.setObjectName(u"FormSettingsViewCheckShowAxes")

        self.horizontalLayout_59.addWidget(self.FormSettingsViewCheckShowAxes)


        self.verticalLayout_31.addWidget(self.frame_67)

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

        self.horizontalSpacer_55 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_55)

        self.FormSettingsViewSpinContourWidth = QSpinBox(self.frame_70)
        self.FormSettingsViewSpinContourWidth.setObjectName(u"FormSettingsViewSpinContourWidth")
        self.FormSettingsViewSpinContourWidth.setMinimumSize(QSize(120, 24))
        self.FormSettingsViewSpinContourWidth.setMaximumSize(QSize(120, 24))
        self.FormSettingsViewSpinContourWidth.setValue(20)

        self.horizontalLayout_62.addWidget(self.FormSettingsViewSpinContourWidth)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_31)


        self.verticalLayout_31.addWidget(self.frame_70)

        self.groupBox = QGroupBox(self.tab_32)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 150))
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

        self.horizontalSpacer_54 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_60.addItem(self.horizontalSpacer_54)

        self.FormSettingsViewSpinBondWidth = QSpinBox(self.frame_68)
        self.FormSettingsViewSpinBondWidth.setObjectName(u"FormSettingsViewSpinBondWidth")
        self.FormSettingsViewSpinBondWidth.setMinimumSize(QSize(120, 24))
        self.FormSettingsViewSpinBondWidth.setMaximumSize(QSize(120, 24))
        self.FormSettingsViewSpinBondWidth.setValue(20)

        self.horizontalLayout_60.addWidget(self.FormSettingsViewSpinBondWidth)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_60.addItem(self.horizontalSpacer_30)


        self.verticalLayout_68.addWidget(self.frame_68)

        self.frame_114 = QFrame(self.groupBox)
        self.frame_114.setObjectName(u"frame_114")
        self.frame_114.setMinimumSize(QSize(0, 50))
        self.frame_114.setFrameShape(QFrame.StyledPanel)
        self.frame_114.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_116 = QHBoxLayout(self.frame_114)
        self.horizontalLayout_116.setObjectName(u"horizontalLayout_116")
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
        self.frame_106.setFrameShape(QFrame.StyledPanel)
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

        self.horizontalSpacer_76 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_110.addItem(self.horizontalSpacer_76)

        self.FormBondLenSpinBox = QDoubleSpinBox(self.frame_106)
        self.FormBondLenSpinBox.setObjectName(u"FormBondLenSpinBox")
        self.FormBondLenSpinBox.setReadOnly(True)

        self.horizontalLayout_110.addWidget(self.FormBondLenSpinBox)

        self.label_30 = QLabel(self.frame_106)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_110.addWidget(self.label_30)


        self.verticalLayout_68.addWidget(self.frame_106)


        self.verticalLayout_31.addWidget(self.groupBox)

        self.verticalSpacer_9 = QSpacerItem(20, 374, QSizePolicy.Minimum, QSizePolicy.Expanding)

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

        self.horizontalSpacer_73 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.horizontalSpacer_18 = QSpacerItem(187, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.horizontalSpacer_67 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.horizontalSpacer_88 = QSpacerItem(208, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_126.addItem(self.horizontalSpacer_88)


        self.verticalLayout_76.addWidget(self.frame_121)


        self.verticalLayout_58.addWidget(self.groupBox_17)

        self.frame_120 = QFrame(self.tab_33)
        self.frame_120.setObjectName(u"frame_120")
        self.frame_120.setFrameShape(QFrame.StyledPanel)
        self.frame_120.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_120)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalSpacer_86 = QSpacerItem(117, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_86)

        self.FormStylesFor2DGraph = QPushButton(self.frame_120)
        self.FormStylesFor2DGraph.setObjectName(u"FormStylesFor2DGraph")

        self.horizontalLayout_34.addWidget(self.FormStylesFor2DGraph)

        self.horizontalSpacer_87 = QSpacerItem(117, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_87)


        self.verticalLayout_58.addWidget(self.frame_120)

        self.verticalSpacer_27 = QSpacerItem(20, 531, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_58.addItem(self.verticalSpacer_27)

        self.tabWidget_9.addTab(self.tab_33, "")

        self.verticalLayout_23.addWidget(self.tabWidget_9)

        self.tabWidget.addTab(self.tab_29, "")
        self.FormTabSettings = QWidget()
        self.FormTabSettings.setObjectName(u"FormTabSettings")
        self.verticalLayout_3 = QVBoxLayout(self.FormTabSettings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolBox_3 = QToolBox(self.FormTabSettings)
        self.toolBox_3.setObjectName(u"toolBox_3")
        self.toolBox_3.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.toolBox_3.sizePolicy().hasHeightForWidth())
        self.toolBox_3.setSizePolicy(sizePolicy2)
        self.toolBox_3.setMinimumSize(QSize(0, 0))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setGeometry(QRect(0, 0, 399, 706))
        self.verticalLayout_13 = QVBoxLayout(self.page_5)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame_88 = QFrame(self.page_5)
        self.frame_88.setObjectName(u"frame_88")
        self.frame_88.setFrameShape(QFrame.NoFrame)
        self.frame_88.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.frame_88)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.horizontalLayout_88.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsOpeningCheckOnlyOptimal = QCheckBox(self.frame_88)
        self.FormSettingsOpeningCheckOnlyOptimal.setObjectName(u"FormSettingsOpeningCheckOnlyOptimal")
        self.FormSettingsOpeningCheckOnlyOptimal.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_88.addWidget(self.FormSettingsOpeningCheckOnlyOptimal)


        self.verticalLayout_13.addWidget(self.frame_88)

        self.frame_87 = QFrame(self.page_5)
        self.frame_87.setObjectName(u"frame_87")
        self.frame_87.setFrameShape(QFrame.NoFrame)
        self.frame_87.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frame_87)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.horizontalLayout_87.setContentsMargins(0, 0, 0, 0)
        self.FormSettingsParseAtomicProperties = QCheckBox(self.frame_87)
        self.FormSettingsParseAtomicProperties.setObjectName(u"FormSettingsParseAtomicProperties")

        self.horizontalLayout_87.addWidget(self.FormSettingsParseAtomicProperties)


        self.verticalLayout_13.addWidget(self.frame_87)

        self.frame_108 = QFrame(self.page_5)
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


        self.verticalLayout_13.addWidget(self.frame_108)

        self.FormSettingsViewCheckXYZasCritic2 = QCheckBox(self.page_5)
        self.FormSettingsViewCheckXYZasCritic2.setObjectName(u"FormSettingsViewCheckXYZasCritic2")

        self.verticalLayout_13.addWidget(self.FormSettingsViewCheckXYZasCritic2)

        self.frame_122 = QFrame(self.page_5)
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


        self.verticalLayout_13.addWidget(self.frame_122)

        self.frame_80 = QFrame(self.page_5)
        self.frame_80.setObjectName(u"frame_80")
        self.frame_80.setFrameShape(QFrame.NoFrame)
        self.frame_80.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_84 = QHBoxLayout(self.frame_80)
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.horizontalLayout_84.setContentsMargins(0, 0, 0, 0)
        self.label_49 = QLabel(self.frame_80)
        self.label_49.setObjectName(u"label_49")

        self.horizontalLayout_84.addWidget(self.label_49)

        self.FormSettingsPreferredCoordinates = QComboBox(self.frame_80)
        self.FormSettingsPreferredCoordinates.setObjectName(u"FormSettingsPreferredCoordinates")
        self.FormSettingsPreferredCoordinates.setEditable(False)

        self.horizontalLayout_84.addWidget(self.FormSettingsPreferredCoordinates)


        self.verticalLayout_13.addWidget(self.frame_80)

        self.frame_85 = QFrame(self.page_5)
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


        self.verticalLayout_13.addWidget(self.frame_85)

        self.verticalSpacer_18 = QSpacerItem(20, 478, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_18)

        self.toolBox_3.addItem(self.page_5, u"Mode")
        self.page_20 = QWidget()
        self.page_20.setObjectName(u"page_20")
        self.page_20.setGeometry(QRect(0, 0, 215, 217))
        self.verticalLayout_14 = QVBoxLayout(self.page_20)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.frame_16 = QFrame(self.page_20)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 0))
        self.frame_16.setMaximumSize(QSize(16777215, 16777215))
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_16)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.frame_16)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_20.addWidget(self.label_20)


        self.verticalLayout_14.addWidget(self.frame_16)

        self.ColorsOfAtomsTable = QTableWidget(self.page_20)
        self.ColorsOfAtomsTable.setObjectName(u"ColorsOfAtomsTable")
        self.ColorsOfAtomsTable.setMinimumSize(QSize(0, 30))

        self.verticalLayout_14.addWidget(self.ColorsOfAtomsTable)

        self.frame_77 = QFrame(self.page_20)
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


        self.verticalLayout_14.addWidget(self.frame_77)

        self.frame_78 = QFrame(self.page_20)
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


        self.verticalLayout_14.addWidget(self.frame_78)

        self.frame_79 = QFrame(self.page_20)
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


        self.verticalLayout_14.addWidget(self.frame_79)

        self.frame_10 = QFrame(self.page_20)
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


        self.verticalLayout_14.addWidget(self.frame_10)

        self.toolBox_3.addItem(self.page_20, u"Colors of model")
        self.page_18 = QWidget()
        self.page_18.setObjectName(u"page_18")
        self.page_18.setGeometry(QRect(0, 0, 379, 324))
        self.verticalLayout_21 = QVBoxLayout(self.page_18)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.frame_76 = QFrame(self.page_18)
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


        self.verticalLayout_21.addWidget(self.frame_76)

        self.ColorRow = PyqtGraphWidgetImage(self.page_18)
        self.ColorRow.setObjectName(u"ColorRow")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ColorRow.sizePolicy().hasHeightForWidth())
        self.ColorRow.setSizePolicy(sizePolicy5)
        self.ColorRow.setMinimumSize(QSize(0, 40))
        self.ColorRow.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_21.addWidget(self.ColorRow)

        self.frame_102 = QFrame(self.page_18)
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


        self.verticalLayout_21.addWidget(self.frame_102)

        self.frame_72 = QFrame(self.page_18)
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


        self.verticalLayout_21.addWidget(self.frame_72)

        self.frame_5 = QFrame(self.page_18)
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


        self.verticalLayout_21.addWidget(self.frame_5)

        self.frame_89 = QFrame(self.page_18)
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

        self.horizontalSpacer_50 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_90.addItem(self.horizontalSpacer_50)


        self.verticalLayout_21.addWidget(self.frame_89)

        self.frame_90 = QFrame(self.page_18)
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

        self.horizontalSpacer_52 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_89.addItem(self.horizontalSpacer_52)


        self.verticalLayout_21.addWidget(self.frame_90)

        self.verticalSpacer_19 = QSpacerItem(20, 308, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_21.addItem(self.verticalSpacer_19)

        self.toolBox_3.addItem(self.page_18, u"Colors of isosurfaces and contours")

        self.verticalLayout_3.addWidget(self.toolBox_3)

        self.tabWidget.addTab(self.FormTabSettings, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.Form3Dand2DTabs = QToolBox(self.centralwidget)
        self.Form3Dand2DTabs.setObjectName(u"Form3Dand2DTabs")
        sizePolicy5.setHeightForWidth(self.Form3Dand2DTabs.sizePolicy().hasHeightForWidth())
        self.Form3Dand2DTabs.setSizePolicy(sizePolicy5)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.page_7.setGeometry(QRect(0, 0, 642, 765))
        self.horizontalLayout_3 = QHBoxLayout(self.page_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.openGLWidget = QOpenGLWidget(self.page_7)
        self.openGLWidget.setObjectName(u"openGLWidget")

        self.horizontalLayout_3.addWidget(self.openGLWidget)

        self.Form3Dand2DTabs.addItem(self.page_7, u"3D View")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.page_8.setGeometry(QRect(0, 0, 642, 765))
        self.horizontalLayout = QHBoxLayout(self.page_8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.PyqtGraphWidget = PyqtGraphWidget(self.page_8)
        self.PyqtGraphWidget.setObjectName(u"PyqtGraphWidget")
        sizePolicy5.setHeightForWidth(self.PyqtGraphWidget.sizePolicy().hasHeightForWidth())
        self.PyqtGraphWidget.setSizePolicy(sizePolicy5)
        self.PyqtGraphWidget.setMinimumSize(QSize(0, 100))

        self.horizontalLayout.addWidget(self.PyqtGraphWidget)

        self.Form3Dand2DTabs.addItem(self.page_8, u"2D Figure")

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

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.tabWidget_11.setCurrentIndex(0)
        self.toolBox_6.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_6.setCurrentIndex(0)
        self.toolBox_4.setCurrentIndex(0)
        self.tabWidget_7.setCurrentIndex(2)
        self.tabWidget_8.setCurrentIndex(0)
        self.tabWidget_10.setCurrentIndex(1)
        self.tabWidget_9.setCurrentIndex(0)
        self.toolBox_3.setCurrentIndex(0)
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabModel), QCoreApplication.translate("MainWindow", u"Model", None))
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"n:", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"m:", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"length:", None))
        self.FormActionsPreButGrapheneGenerate.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_17), QCoreApplication.translate("MainWindow", u"Graphene", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Type", None))
        self.FormActionsPreRadioSWNT.setText(QCoreApplication.translate("MainWindow", u"SWCNT", None))
        self.FormActionsPreRadioSWNTcap.setText(QCoreApplication.translate("MainWindow", u"SWCNT with cap", None))
        self.FormActionsPreRadioSWNTcap_2.setText(QCoreApplication.translate("MainWindow", u"SWCNT with 2 caps", None))
        self.FormCreateGroupFirstCap.setTitle(QCoreApplication.translate("MainWindow", u"First", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Distance", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Angle", None))
        self.FormCreateGroupSecondCap.setTitle(QCoreApplication.translate("MainWindow", u"Second", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Distance", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Angle", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Chirality", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"(", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u",", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Size", None))
        self.FormActionsPreRadioSWNTuselen.setText(QCoreApplication.translate("MainWindow", u"lenght (A)", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"cells", None))
        self.FormActionsPreButSWNTGenerate.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.tabWidget_11.setTabText(self.tabWidget_11.indexOf(self.tab_36), QCoreApplication.translate("MainWindow", u"SWCNT", None))
        self.tabWidget_11.setTabText(self.tabWidget_11.indexOf(self.tab_37), QCoreApplication.translate("MainWindow", u"SWGNT", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"Nanotube type", None))
        self.groupBox_31.setTitle(QCoreApplication.translate("MainWindow", u"Chirality", None))
        self.FormBiElementRadioArm.setText(QCoreApplication.translate("MainWindow", u"armchair", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"zigzag", None))
        self.label_89.setText(QCoreApplication.translate("MainWindow", u"n", None))
        self.FormActionsPreRadioSWNTuselen_2.setText(QCoreApplication.translate("MainWindow", u"lenght (A)", None))
        self.FormActionsPreButBiElementGenerate.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.tabWidget_11.setTabText(self.tabWidget_11.indexOf(self.tab_38), QCoreApplication.translate("MainWindow", u"Bi element", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QCoreApplication.translate("MainWindow", u"Nanotubes", None))
        self.groupBox_40.setTitle(QCoreApplication.translate("MainWindow", u"Part 1", None))
        self.label_108.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.FormSelectPart1File.setText("")
        self.groupBox_41.setTitle(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_113.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_114.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_115.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.groupBox_42.setTitle(QCoreApplication.translate("MainWindow", u"Center of mass", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("MainWindow", u"Part 2", None))
        self.label_95.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.FormSelectPart2File.setText("")
        self.groupBox_39.setTitle(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_97.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_98.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_103.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.groupBox_43.setTitle(QCoreApplication.translate("MainWindow", u"Center of mass", None))
        self.FormCreateModelFromParts.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), QCoreApplication.translate("MainWindow", u"From two parts", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Left electrode", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"*.fdf file", None))
        self.FormActionsPreButSelectLeftElectrode.setText("")
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Move X", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"Move Y", None))
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Distance to scat. region", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Scatering region", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"*.fdf file", None))
        self.FormActionsPreButSelectScatRegione.setText("")
        self.groupBox_36.setTitle(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Move X", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"Move Y", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Right electrode", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"*.fdf file", None))
        self.FormActionsPreButSelectRightElectrode.setText("")
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Move X", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"Move Y", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Distance to scat. region", None))
        self.FormActionsPreButCreateModelWithElectrodes.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_22), QCoreApplication.translate("MainWindow", u"Model with electrodes", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Create", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Element", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.FormActionsPreButDeleteAtom.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.FormActionsPreButModifyAtom.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.FormActionsPreButAddAtom.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_29), QCoreApplication.translate("MainWindow", u"Add or Modify Atom", None))
        self.FormModifyCellButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Cell", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This tab is designed to search for various configurations of a given number of atoms within a given cylindrical volume.</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"nAtoms", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"charge of atoms", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"delta", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"nPrompts", None))
        self.cylinder.setText(QCoreApplication.translate("MainWindow", u"radius of cylinder (center in the origin)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"height of cylinder (Z direction)", None))
        self.FormActionsPreSaveToFileFillSpace.setText(QCoreApplication.translate("MainWindow", u"Save to files", None))
        self.FormActionsPreButFillSpace.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_28), QCoreApplication.translate("MainWindow", u"Fill Space", None))
        self.FormModifyGrowX.setText(QCoreApplication.translate("MainWindow", u"Grow X", None))
        self.FormModifyGrowY.setText(QCoreApplication.translate("MainWindow", u"Grow Y", None))
        self.FormModifyGrowZ.setText(QCoreApplication.translate("MainWindow", u"Grow Z", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_12), QCoreApplication.translate("MainWindow", u"Grow model", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"degrees", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"around axes", None))
        self.FormModifyRotationX.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.FormModifyRotationY.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.FormModifyRotationZ.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.FormModifyRotationOrigin.setText(QCoreApplication.translate("MainWindow", u"Around the origin", None))
        self.FormModifyRotationCenter.setText(QCoreApplication.translate("MainWindow", u"Around the center of mass", None))
        self.FormModifyRotation.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_11), QCoreApplication.translate("MainWindow", u"Rotate model", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Modify", None))
        self.FormActionsPreButFDFGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.FormActionsPreButFDFToFile.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_24), QCoreApplication.translate("MainWindow", u"*.fdf file generator", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FormTabActions), QCoreApplication.translate("MainWindow", u"Preprocessing", None))
        self.FormActionsButtonParseBANDS.setText(QCoreApplication.translate("MainWindow", u"parse BANDS", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"k-range", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Energy range", None))
        self.FormActionsCheckBANDSfermyShow.setText(QCoreApplication.translate("MainWindow", u"Show Fermi level", None))
        self.FormActionsGrBoxBANDSspin.setTitle(QCoreApplication.translate("MainWindow", u"Spin", None))
        self.FormActionsCheckBANDSspinUp.setText(QCoreApplication.translate("MainWindow", u"Up", None))
        self.FormActionsCheckBANDSspinDown.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.FormActionsButtonPlotBANDS.setText(QCoreApplication.translate("MainWindow", u"plot BANDS", None))
        self.FormActionsLabelBANDSgap.setText("")
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_18), QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.FormActionsCheckBANDSfermyShow_3.setText(QCoreApplication.translate("MainWindow", u"Show Fermi level", None))
        self.FormActionsCheckDOS.setText(QCoreApplication.translate("MainWindow", u"Plot Up and Down spin", None))
        self.FormActionsCheckDOS_2.setText(QCoreApplication.translate("MainWindow", u"Invert Down", None))
        self.FormActionsButtonAddDOSFile.setText(QCoreApplication.translate("MainWindow", u"Add .out file", None))
        self.FormActionsButtonClearDOS.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.FormActionsButtonPlotDOS.setText(QCoreApplication.translate("MainWindow", u"Plot DOS", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_14), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Indexes:", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Indexes", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Species:", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"Species", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"n", None))
        self.FormActionsComboPDOSn1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.FormActionsComboPDOSn2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.FormActionsComboPDOSn3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.FormActionsComboPDOSn4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.FormActionsComboPDOSn5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.FormActionsComboPDOSn6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.FormActionsComboPDOSn7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.FormActionsComboPDOSn8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"n", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"l", None))
        self.FormActionsComboPDOSL0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.FormActionsComboPDOSL1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.FormActionsComboPDOSL2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.FormActionsComboPDOSL3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.FormActionsComboPDOSL4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.FormActionsComboPDOSL5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.FormActionsComboPDOSL6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.FormActionsComboPDOSL7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_13), QCoreApplication.translate("MainWindow", u"l", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"m", None))
        self.FormActionsComboPDOSMm7.setText(QCoreApplication.translate("MainWindow", u"-7", None))
        self.FormActionsComboPDOSMm6.setText(QCoreApplication.translate("MainWindow", u"-6", None))
        self.FormActionsComboPDOSMm5.setText(QCoreApplication.translate("MainWindow", u"-5", None))
        self.FormActionsComboPDOSMm4.setText(QCoreApplication.translate("MainWindow", u"-4", None))
        self.FormActionsComboPDOSMm3.setText(QCoreApplication.translate("MainWindow", u"-3", None))
        self.FormActionsComboPDOSMm2.setText(QCoreApplication.translate("MainWindow", u"-2", None))
        self.FormActionsComboPDOSMm1.setText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.FormActionsComboPDOSMp0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.FormActionsComboPDOSMp1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.FormActionsComboPDOSMp2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.FormActionsComboPDOSMp3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.FormActionsComboPDOSMp4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.FormActionsComboPDOSMp5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.FormActionsComboPDOSMp6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.FormActionsComboPDOSMp7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"m", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"zeta", None))
        self.FormActionsComboPDOSz1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.FormActionsComboPDOSz2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.FormActionsComboPDOSz3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.FormActionsComboPDOSz4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.FormActionsComboPDOSz5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"zeta", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Spin", None))
        self.FormActionsCheckPDOS.setText(QCoreApplication.translate("MainWindow", u"Plot Up and Down spin", None))
        self.FormActionsCheckPDOS_2.setText(QCoreApplication.translate("MainWindow", u"Invert Down", None))
        self.FormActionsCheckBANDSfermyShow_2.setText(QCoreApplication.translate("MainWindow", u"Show Fermi level", None))
        self.FormActionsButtonPlotPDOS.setText(QCoreApplication.translate("MainWindow", u"plot single PDOS and add to list", None))
        self.FormActionsButtonPlotPDOSselected.setText(QCoreApplication.translate("MainWindow", u"plot selected PDOS", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_15), QCoreApplication.translate("MainWindow", u"PDOS", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_19), QCoreApplication.translate("MainWindow", u"Electronic properties", None))
        self.FormActionsPostButSurfaceParse.setText(QCoreApplication.translate("MainWindow", u"Parse", None))
        self.FormActionsPostButSurfaceLoadData.setText(QCoreApplication.translate("MainWindow", u"Load Data", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Values", None))
        self.FormActionsPostLabelSurfaceMin.setText("")
        self.FormActionsPostLabelSurfaceMax.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Data 1", None))
        self.FormActionsPostButSurfaceParse2.setText(QCoreApplication.translate("MainWindow", u"Open *.XSF or *.CUBE file", None))
        self.FormActionsPostButSurfaceLoadData2.setText(QCoreApplication.translate("MainWindow", u"Load Data", None))
        self.VolumrricDataGrid2.setTitle(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.FormActionsPostLabelSurfaceNx.setText("")
        self.FormActionsPostLabelSurfaceNy.setText("")
        self.FormActionsPostLabelSurfaceNz.setText("")
        self.VolumrricDataGridCalculate.setTitle(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.CalculateTheVolumericDataDifference.setText(QCoreApplication.translate("MainWindow", u"Difference", None))
        self.CalculateTheVolumericDataSum.setText(QCoreApplication.translate("MainWindow", u"Sum", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Data 2", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Limit to", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Vector 1", None))
        self.label_96.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_99.setText(QCoreApplication.translate("MainWindow", u"Vector 2", None))
        self.label_100.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_101.setText(QCoreApplication.translate("MainWindow", u"Vector 3", None))
        self.label_102.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ExportTheVolumericDataXSF.setText(QCoreApplication.translate("MainWindow", u"XSF", None))
        self.ExportTheVolumericDataCube.setText(QCoreApplication.translate("MainWindow", u"cube", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_22), QCoreApplication.translate("MainWindow", u"Export", None))
        self.FormActionsPostCheckSurface.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.FormActionsPostButSurfaceAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.FormActionsPostButSurfaceDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.FormActionsPostButSurface.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Isosurface", None))
        self.FormActionsPostRadioContour.setText(QCoreApplication.translate("MainWindow", u"Contours", None))
        self.FormActionsPostRadioColorPlane.setText(QCoreApplication.translate("MainWindow", u"Planes", None))
        self.FormActionsPostRadioColorPlaneContours.setText(QCoreApplication.translate("MainWindow", u"Planes + Contours", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"XY-plane", None))
        self.FormActionsPostCheckContourXY.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"levels", None))
        self.FormActionsPostLabelContourXYposition.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"YZ-plane", None))
        self.FormActionsPostCheckContourYZ.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"levels", None))
        self.FormActionsPostLabelContourYZposition.setText("")
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"XZ-plane", None))
        self.FormActionsPostCheckContourXZ.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"levels", None))
        self.FormActionsPostLabelContourXZposition.setText("")
        self.FormActionsPostButContour.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Contours", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Isosurface and Contours", None))
        self.FormActionsPostButGetBonds.setText(QCoreApplication.translate("MainWindow", u"Get bonds", None))
        self.FormActionsPostLabelMeanBond.setText("")
        self.FormActionsPostButPlotBondsHistogram.setText(QCoreApplication.translate("MainWindow", u"Plot histogram", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_16), QCoreApplication.translate("MainWindow", u"Bonds", None))
        self.FormActionsPostButAddRowCellParam.setText(QCoreApplication.translate("MainWindow", u"Add Row", None))
        self.FormActionsPostButDeleteRowCellParam.setText(QCoreApplication.translate("MainWindow", u"Delete Selected", None))
        self.FormActionsPostButPlusCellParam.setText(QCoreApplication.translate("MainWindow", u"Add File", None))
        self.FormActionsPostButPlusDataCellParam.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.FormActionsPostButOptimizeCellParam.setText(QCoreApplication.translate("MainWindow", u"Optimize", None))
        self.FormActionsPostLabelCellParamOptimExpr.setText("")
        self.FormActionsPostLabelCellParamFig.setText("")
        self.FormActionsPostLabelCellParamOptimExpr2.setText("")
        self.FormActionsPostLabelCellParamOptimExpr3.setText("")
        self.FormActionsPostLabelCellParamOptimExpr4.setText("")
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_17), QCoreApplication.translate("MainWindow", u"Cell parameter", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Atom - atom distance", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.PropertyAtomAtomDistanceGet.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_21), QCoreApplication.translate("MainWindow", u"Selection history", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Maximun  distance", None))
        self.FormActionsPostButVoronoi.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.FormActionsPostLabelVoronoiAtom.setText("")
        self.FormActionsPostLabelVoronoiVolume.setText("")
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_19), QCoreApplication.translate("MainWindow", u"Voronoi", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_24), QCoreApplication.translate("MainWindow", u"Structural properties", None))
        self.ColorAtomsWithProperty.setText(QCoreApplication.translate("MainWindow", u"Color with property", None))
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
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_13), QCoreApplication.translate("MainWindow", u"Coloring", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Postprocessing", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can open some non-SEISETA files as easily as regular SEISETA files:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1) VASP POSCAR/CONTCAR files</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2) Critic2 *.XYZ files with information about critical points and bond critical paths. It is nesessary to change Settings  </p></body></html>", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_9), QCoreApplication.translate("MainWindow", u"Import", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"to VASP POSCAR", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Just specify the extension of the exported file to \".POSCAR\"", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"to FireFly inp file", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Just specify the extension of the exported file to \".inp\"", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"to CRYSTAL *.d12 file", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"coming soon (1D only in test)", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Translational symmetry", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"3D", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"2D", None))
        self.crystal_d12_1d.setText(QCoreApplication.translate("MainWindow", u"1D", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"0D", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_25), QCoreApplication.translate("MainWindow", u"3D", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_26), QCoreApplication.translate("MainWindow", u"2D", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"IGR = 1", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_27), QCoreApplication.translate("MainWindow", u"1D", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_28), QCoreApplication.translate("MainWindow", u"0D", None))
        self.FormIEd12Generate.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_10), QCoreApplication.translate("MainWindow", u"Export", None))
        self.FormASERamanAndIRscriptCreate.setText(QCoreApplication.translate("MainWindow", u"Create ASE script", None))
        self.FormASERamanAndIRscriptParse.setText(QCoreApplication.translate("MainWindow", u"Parse results", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_30), QCoreApplication.translate("MainWindow", u"Raman", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_31), QCoreApplication.translate("MainWindow", u"IR", None))
        self.groupBox_33.setTitle(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.label_94.setText(QCoreApplication.translate("MainWindow", u"Peak width", None))
        self.form_raman_radio.setText(QCoreApplication.translate("MainWindow", u"Raman", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"IR", None))
        self.form_spectra_mev_radio.setText(QCoreApplication.translate("MainWindow", u"meV", None))
        self.radioButton_8.setText(QCoreApplication.translate("MainWindow", u"cm^-1", None))
        self.FormASERamanAndIRscriptPlot.setText(QCoreApplication.translate("MainWindow", u"Plot Spectra", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"Raman and IR (ASE)", None))
        self.FormButtonAddCroData.setText(QCoreApplication.translate("MainWindow", u"Add data from *.cro file (for opened *.xyz file)", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Selected CP", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.FormSelectedCP.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"Field:", None))
        self.FormSelectedCP_f.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"|grad|:", None))
        self.FormSelectedCP_g.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"Lap:", None))
        self.FormSelectedCP_lap.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.FormCPaddToList.setText(QCoreApplication.translate("MainWindow", u"Add to List", None))
        self.FormCPdeleteFromList.setText(QCoreApplication.translate("MainWindow", u"Delete selected from List", None))
        self.tabWidget_10.setTabText(self.tabWidget_10.indexOf(self.tab_35), QCoreApplication.translate("MainWindow", u"List of CP", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"*.cri file", None))
        self.form_critic_all_cp.setText(QCoreApplication.translate("MainWindow", u"All CP", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"CP only", None))
        self.formCriticBPradio.setText(QCoreApplication.translate("MainWindow", u"BP with", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"extra points", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("MainWindow", u"Properties:", None))
        self.form_critic_prop_lag.setText(QCoreApplication.translate("MainWindow", u"lag", None))
        self.form_critic_prop_htf_kir.setText(QCoreApplication.translate("MainWindow", u"htf_kir", None))
        self.form_critic_prop_htf.setText(QCoreApplication.translate("MainWindow", u"htf", None))
        self.form_critic_prop_gtf.setText(QCoreApplication.translate("MainWindow", u"gtf", None))
        self.form_critic_prop_gtf_kir.setText(QCoreApplication.translate("MainWindow", u"gtf_kir", None))
        self.form_critic_prop_lol_kir.setText(QCoreApplication.translate("MainWindow", u"lol_kir", None))
        self.form_critic_prop_rdg.setText(QCoreApplication.translate("MainWindow", u"rdg", None))
        self.form_critic_prop_vtf.setText(QCoreApplication.translate("MainWindow", u"vtf", None))
        self.form_critic_prop_vtf_kir.setText(QCoreApplication.translate("MainWindow", u"vtf_kir", None))
        self.FormCreateCriFile.setText(QCoreApplication.translate("MainWindow", u"Create *.cri file", None))
        self.tabWidget_10.setTabText(self.tabWidget_10.indexOf(self.tab_20), QCoreApplication.translate("MainWindow", u"Export to *.cri", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("MainWindow", u"*.xyz file", None))
        self.radio_with_cp.setText(QCoreApplication.translate("MainWindow", u"with", None))
        self.radio_without_cp.setText(QCoreApplication.translate("MainWindow", u"without", None))
        self.label_93.setText(QCoreApplication.translate("MainWindow", u"selected CP", None))
        self.FormCreateCriXYZFile.setText(QCoreApplication.translate("MainWindow", u"Create *.xyz file", None))
        self.tabWidget_10.setTabText(self.tabWidget_10.indexOf(self.tab_34), QCoreApplication.translate("MainWindow", u"Export to *.xyz", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_23), QCoreApplication.translate("MainWindow", u"Critical points (Critic2 *.cri file)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_23), QCoreApplication.translate("MainWindow", u"Third party", None))
        self.FormSettingsViewCheckShowAtoms.setText(QCoreApplication.translate("MainWindow", u"Show atoms", None))
        self.FormSettingsViewCheckShowAtomNumber.setText(QCoreApplication.translate("MainWindow", u"Show atom number", None))
        self.FormSettingsViewCheckShowBox.setText(QCoreApplication.translate("MainWindow", u"Show box", None))
        self.FormSettingsViewCheckShowAxes.setText(QCoreApplication.translate("MainWindow", u"Show axes", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Contours width", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Bonds", None))
        self.FormSettingsViewCheckShowBonds.setText(QCoreApplication.translate("MainWindow", u"Show bonds", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Bonds width", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.FormSettingsViewRadioColorBondsManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.FormSettingsViewRadioColorBondsByAtoms.setText(QCoreApplication.translate("MainWindow", u"By atoms color", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Bond parameter", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"A", None))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_29), QCoreApplication.translate("MainWindow", u"View", None))
        self.FormSettingsOpeningCheckOnlyOptimal.setText(QCoreApplication.translate("MainWindow", u"Get only optimal structures", None))
        self.FormSettingsParseAtomicProperties.setText(QCoreApplication.translate("MainWindow", u"Parse atomic properties", None))
        self.FormSettingsViewCheckAtomSelection.setText(QCoreApplication.translate("MainWindow", u"Allow atom selection", None))
        self.FormSettingsViewCheckModelMove.setText(QCoreApplication.translate("MainWindow", u"Allow model move", None))
        self.FormSettingsViewCheckXYZasCritic2.setText(QCoreApplication.translate("MainWindow", u"XYZ as critic2 output", None))
        self.label_92.setText(QCoreApplication.translate("MainWindow", u"Preferred units", None))
        self.FormSettingsPreferredUnits.setCurrentText("")
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Preferred coordinates", None))
        self.FormSettingsPreferredCoordinates.setCurrentText("")
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Preferred lattice", None))
        self.FormSettingsPreferredLattice.setCurrentText("")
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Atoms", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Bonds color", None))
        self.ColorBondDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Box color", None))
        self.ColorBoxDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Axes color", None))
        self.ColorAxesDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Voronoi color", None))
        self.ColorVoronoiDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_20), QCoreApplication.translate("MainWindow", u"Colors of model", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Color scheme", None))
        self.FormSettingsColorsScale.setCurrentText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.FormSettingsColorsScaleType.setCurrentText("")
        self.FormSettingsContourColorFixed.setText(QCoreApplication.translate("MainWindow", u"Contour color", None))
        self.ColorContourDialogButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.FormSettingsColorsFixed.setText(QCoreApplication.translate("MainWindow", u"Use fixed colors range", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Min value", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Max value", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_18), QCoreApplication.translate("MainWindow", u"Colors of isosurfaces and contours", None))
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

