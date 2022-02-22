# -*- coding: utf-8 -*-

from utils.periodic_table import TPeriodTable
from PySide2.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QMainWindow
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel
from PySide2.QtGui import QStandardItem
from ui.atomsidentify import Ui_Dialog as Ui_Dialog_Atoms


class AtomsIdentifier(QDialog):
    def __init__(self, problemAtoms):
        super(AtomsIdentifier, self).__init__()
        self.ui = Ui_Dialog_Atoms()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui.okButton.clicked.connect(self.okButtonClick)
        self.ansv = []

        self.ui.TheTable.setColumnCount(2)
        self.ui.TheTable.setHorizontalHeaderLabels(["Atom Type", "get_species"])
        self.ui.TheTable.setColumnWidth(0, 90)
        self.ui.TheTable.setColumnWidth(1, 90)

        model = QStandardItemModel()
        model.appendRow(QStandardItem("select"))
        Mendeley = TPeriodTable()
        atoms_list = Mendeley.get_all_letters()
        for i in range(1, len(atoms_list)):
            model.appendRow(QStandardItem(atoms_list[i]))

        problemAtoms = list(problemAtoms)
        problemAtoms.sort()

        for problem in problemAtoms:
            self.ui.TheTable.setRowCount(self.ui.TheTable.rowCount()+1)  # и одну строку в таблице
            data_cell = QTableWidgetItem(str(problem-199))
            data_cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.ui.TheTable.setItem(self.ui.TheTable.rowCount() - 1, 0, data_cell)
            atom_cell = QComboBox()

            atom_cell.setModel(model)
            atom_cell.setCurrentIndex(0)
            self.ui.TheTable.setCellWidget(self.ui.TheTable.rowCount() - 1, 1, atom_cell)

    def okButtonClick(self):
        self.ansv = []
        for i in range(0, self.ui.TheTable.rowCount()):
            at_type = self.ui.TheTable.cellWidget(i, 1).currentText()
            if at_type != "select":
                self.ansv.append([200+i, at_type])
        if len(self.ansv) == self.ui.TheTable.rowCount():
            self.close()
