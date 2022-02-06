# -*- coding: utf-8 -*-

from copy import deepcopy
import os
from utils.atomic_model import TAtomicModel
from utils.periodic_table import TPeriodTable
from utils import helpers
import numpy as np
import math
import skimage
if skimage.__version__ >= '0.17.2':
    from skimage.measure import marching_cubes
else:
    from skimage.measure import marching_cubes_lewiner
from skimage.measure import find_contours
from PySide2.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QMainWindow
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel
from PySide2.QtGui import QStandardItem
from image3D import Ui_MainWindow as Ui_image3D
from ui.atomsidentify import Ui_Dialog as Ui_Dialog_Atoms
from guiopengl import GuiOpenGL


##################################################################
############################ TXSF ################################
##################################################################


class TVolumericDataBlock:

    def __init__(self, title):
        self.title = title
        self.max = None
        self.min = None


class TVolumericData:
    def __init__(self):
        self.filename = ""
        self.Nx = None
        self.Ny = None
        self.Nz = None
        self.blocks = []
        self.atoms = []
        self.data3D = np.zeros((1, 1))
        self.spacing = (0, 0, 0)
        self.origin = np.zeros(3)
        self.origin_to_export = np.zeros(3)
        self.type = "TVolumericData"

    def volumeric_data_read(self, f, orderData):
        ind = 0
        while ind < self.Nx * self.Ny * self.Nz:
            row = f.readline().split()
            for data in row:
                self.data3D[0, ind] = float(data)
                ind += 1
        f.readline()
        helpers.spacedel(f.readline())

        self.min = np.min(self.data3D)
        self.max = np.max(self.data3D)
        self.data3D = self.data3D.reshape((self.Nx, self.Ny, self.Nz), order=orderData)

    def difference(self, secondData, mult=1):
        if (self.Nx == secondData.Nx) and (self.Ny == secondData.Ny) and (self.Nz == secondData.Nz):
            for i in range(0, self.Nx):
                for j in range(0, self.Ny):
                    for k in range(0, self.Nz):
                        self.data3D[i][j][k] -= mult * secondData.data3D[i][j][k]
        self.min = np.min(self.data3D)
        self.max = np.max(self.data3D)

    def isosurface(self, value):
        if skimage.__version__ < '0.17.2':
            verts, faces, normals, values = marching_cubes_lewiner(self.data3D, level=value, spacing=self.spacing, gradient_direction='descent', step_size=1, allow_degenerate=True, use_classic=False)
        else:
            verts, faces, normals, values = marching_cubes(self.data3D, level=value, spacing=self.spacing, gradient_direction='descent', step_size=1, allow_degenerate=True, method='lewiner')

        for i in range(0, len(verts)):
            verts[i] += self.origin
        return verts, faces, normals

    def contours(self, values, type_of_plane="xy", _slice=5):
        conts = []
        spacing = self.spacing
        origin = self.origin
        r = []
        if type_of_plane == "xy":
            r = self.data3D[:, :, _slice]
        if type_of_plane == "xz":
            r = self.data3D[:, _slice, :]
        if type_of_plane == "yz":
            r = self.data3D[_slice, :, :]
        for value in values:
            cont = find_contours(r, value)
            contours = []
            for i in range(0, len(cont)):
                contour = []
                for j in range(0, len(cont[i])):
                    if type_of_plane == "xy":
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + cont[i][j][1] * spacing[1], origin[2] + _slice * spacing[2]])
                    if type_of_plane == "xz":
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + _slice * spacing[1], origin[2] + cont[i][j][1] * spacing[2]])
                    if type_of_plane == "yz":
                        contour.append([origin[0] + _slice * spacing[0], origin[1] + cont[i][j][0] * spacing[1], origin[2] + cont[i][j][1] * spacing[2]])
                contours.append(contour)
            conts.append(contours)
        return conts

    def plane(self, type_of_plane="xy", _slice=5):
        origin = deepcopy(self.origin)
        r = []
        spacing = [0, 0]
        if type_of_plane == "xy":
            r = self.data3D[:, :, _slice]
            origin[2] = self.origin[2] + _slice * self.spacing[2]
            spacing = [self.spacing[0], self.spacing[1]]

        if type_of_plane == "xz":
            r = self.data3D[:, _slice, :]
            origin[1] = self.origin[1] + _slice * self.spacing[1]
            spacing = [self.spacing[0], self.spacing[2]]

        if type_of_plane == "yz":
            r = self.data3D[_slice, :, :]
            origin[0] = self.origin[0] + _slice * self.spacing[0]
            spacing = [self.spacing[0], self.spacing[2]]

        Nx = len(r)
        Ny = len(r[0])
        points = []
        for i in range(0, Nx):
            row = []
            for j in range(0, Ny):
                x = i * spacing[0]
                y = j * spacing[1]
                z = 0
                if type_of_plane == "xz":
                    x, y, z = x, z, y
                if type_of_plane == "yz":
                    x, y, z = z, x, y
                x += origin[0]
                y += origin[1]
                z += origin[2]
                row.append([x, y, z, r[i][j]])
            points.append(row)
        return points


class TXSF(TVolumericData):
    def __init__(self):
        TVolumericData.__init__(self)
        self.type = "TXSF"

    @staticmethod
    def get_atoms(filename):
        periodTable = TPeriodTable()

        Molecules = []
        if os.path.exists(filename):
            f = open(filename)
            row = f.readline()
            atoms = []
            while row != '':
                if row.find("ATOMS") > -1:
                    while row.find("BEGIN") == -1:
                        row = f.readline()
                        if row.find("BEGIN") == -1:
                            row1 = row.split()
                            charge = int(row1[0])
                            x = float(row1[1])
                            y = float(row1[2])
                            z = float(row1[3])
                            atoms.append([x, y, z, periodTable.get_let(charge), charge])

                if row.find("BEGIN_BLOCK_DATAGRID") > -1:
                    row = f.readline()
                    while row.find("DATA_from:") > -1:
                        row = helpers.spacedel(f.readline())
                        while row.find("BEGIN_DATAGRID") > -1:
                            row = f.readline()
                            origin = f.readline()
                            vec1 = f.readline().split()
                            vec1 = helpers.list_str_to_float(vec1)
                            vec2 = f.readline().split()
                            vec2 = helpers.list_str_to_float(vec2)
                            vec3 = f.readline().split()
                            vec3 = helpers.list_str_to_float(vec3)
                            f.close()

                            AllAtoms = TAtomicModel(atoms)
                            AllAtoms.set_lat_vectors(vec1, vec2, vec3)
                            Molecules.append(AllAtoms)
                            return Molecules
                row = f.readline()
            f.close()
        return Molecules

    def parse(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):
            model = TXSF.get_atoms(self.filename)[0]
            self.atoms = model.atoms
            f = open(self.filename)
            row = f.readline()
            while row != '':
                if row.find("BEGIN_BLOCK_DATAGRID") > -1:
                    row = f.readline()
                    while row.find("DATA_from:") > -1:
                        datas = []
                        row = f.readline()
                        while row.find("BEGIN_DATAGRID") > -1:
                            row = helpers.spacedel(row)
                            data3D = TVolumericDataBlock(row)
                            while row.find("END_") == -1:
                                row = f.readline()
                            datas.append(data3D)
                            row = f.readline()
                        self.blocks.append(datas)
                row = f.readline()
            f.close()
            return True
        return False

    def load_data(self, getChildNode):
        f = open(self.filename)
        row = f.readline()
        while row != '':
            if row.find(getChildNode) > -1:
                row = helpers.spacedel(f.readline()).split()
                self.Nx = int(row[0])
                self.Ny = int(row[1])
                self.Nz = int(row[2])
                self.data3D = np.zeros((1, self.Nx*self.Ny*self.Nz))

                origin = helpers.list_str_to_float(f.readline().split())
                self.origin = np.array(origin)
                self.origin_to_export = deepcopy(self.origin)
                tmp_model = TAtomicModel(self.atoms)
                center_mass = tmp_model.centr_mass()
                self.origin -= np.array([center_mass[0], center_mass[1], center_mass[2]])
                vec1 = f.readline().split()
                vec2 = f.readline().split()
                vec3 = f.readline().split()
                vec1 = float(vec1[0])
                vec2 = float(vec2[1])
                vec3 = float(vec3[2])
                self.spacing = (vec1 / self.Nx, vec2 / self.Ny, vec3 / self.Nz)

                orderData = 'F'

                self.volumeric_data_read(f, orderData)
                f.close()
                return self.atoms
            row = f.readline()
        f.close()


class TGaussianCube(TVolumericData):
    def __init__(self):
        TVolumericData.__init__(self)
        self.type = "TGaussianCube"

    @staticmethod
    def get_atoms(filename):
        periodTable = TPeriodTable()
        Molecules = []
        if os.path.exists(filename):
            f = open(filename)
            row = f.readline()
            row = f.readline()
            row = f.readline().split()
            nAtoms = int(row[0])
            origin = (float(row[1]), float(row[2]), float(row[3]))

            Nx, vec1, mult = TGaussianCube.local_get_N_vect(f.readline().split())
            Ny, vec2, mult = TGaussianCube.local_get_N_vect(f.readline().split())
            Nz, vec3, mult = TGaussianCube.local_get_N_vect(f.readline().split())

            atoms = []

            for i in range(0, nAtoms):
                row = f.readline().split()
                charge = int(row[0])
                atoms.append([float(row[2]), float(row[3]), float(row[4]), periodTable.get_let(charge), charge])
            f.close()
            AllAtoms = TAtomicModel(atoms)
            AllAtoms.set_lat_vectors(vec1, vec2, vec3)
            AllAtoms.convert_from_scaled_to_cart(mult)

            Molecules.append(AllAtoms)
        return Molecules

    @staticmethod
    def local_get_N_vect(row):
        Nx = int(row[0])
        mult = 1
        if Nx > 0:
            mult = 0.52917720859
        Nx = int(math.fabs(Nx))
        vec1 = mult * Nx * np.array([float(row[1]), float(row[2]), float(row[3])])
        return Nx, vec1, mult

    def parse(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):
            model = TGaussianCube.get_atoms(self.filename)[0]
            self.atoms = model.atoms

            f = open(self.filename)
            row = f.readline()
            data3D = TVolumericDataBlock(row)
            self.blocks.append([data3D])
            f.close()
            return True
        return False

    def load_data(self, getChildNode):
        if os.path.exists(self.filename):
            f = open(self.filename)
            row = f.readline()
            row = f.readline()
            row = f.readline().split()
            nAtoms = int(row[0])
            origin = (float(row[1]), float(row[2]), float(row[3]))

            self.Nx, vec1, mult = TGaussianCube.local_get_N_vect(f.readline().split())
            self.Ny, vec2, mult = TGaussianCube.local_get_N_vect(f.readline().split())
            self.Nz, vec3, mult = TGaussianCube.local_get_N_vect(f.readline().split())

            for i in range(0, nAtoms):
                row = f.readline().split()

            self.data3D = np.zeros((1, self.Nx * self.Ny * self.Nz))
            self.origin = mult*np.array(origin)
            self.origin_to_export = deepcopy(self.origin)
            tmp_model = TAtomicModel(self.atoms)
            center_mass = tmp_model.centr_mass()
            self.origin -= np.array([center_mass[0], center_mass[1], center_mass[2]])
            vec1 = float(vec1[0])
            vec2 = float(vec2[1])
            vec3 = float(vec3[2])
            self.spacing = (vec1 / self.Nx, vec2 / self.Ny, vec3 / self.Nz)
            orderData = 'C'
            self.volumeric_data_read(f, orderData)
            f.close()
        return self.atoms


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


class Image3Dexporter(QMainWindow):
    def __init__(self, windowsWidth, windowsHeight, quality):
        super(Image3Dexporter, self).__init__()
        self.ui = Ui_image3D()
        self.ui.setupUi(self)
        self.setFixedSize(QSize(windowsWidth, windowsHeight))

        self.MainForm = GuiOpenGL(self.ui.openGLWidget, None, quality=quality)
        self.MainForm.filter = None
        self.show()
