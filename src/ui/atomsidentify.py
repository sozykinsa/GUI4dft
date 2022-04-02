# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'atomsidentify.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(324, 539)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TheTable = QTableWidget(Dialog)
        self.TheTable.setObjectName(u"TheTable")

        self.verticalLayout.addWidget(self.TheTable)

        self.okButton = QPushButton(Dialog)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setAcceptDrops(False)

        self.verticalLayout.addWidget(self.okButton)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Spesify atoms types", None))
        self.okButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
    # retranslateUi

