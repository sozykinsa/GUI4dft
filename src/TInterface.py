# -*- coding: utf-8 -*-

from copy import deepcopy
import os

from AdvancedTools import TAtomicModel
from AdvancedTools import TCalculators
from AdvancedTools import TFDFFile
from AdvancedTools import TSIESTA
from AdvancedTools import TPeriodTable
from AdvancedTools import Helpers
import numpy as np
from skimage.measure import marching_cubes_lewiner
from skimage.measure import find_contours

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from image3D import Ui_MainWindow as Ui_image3D
from atomsidentify import Ui_Dialog as Ui_Dialog_Atoms
from TGui import GuiOpenGL



class Calculator(object):

    @staticmethod
    def M11S11(DOS):
        """Check DOS file for fdf/out filename"""
        return TCalculators.M11S11(DOS)

    @staticmethod
    def ApproxParabola(ListN2):
        """List N x 2"""
        return TCalculators.ApproxParabola(ListN2)

    @staticmethod
    def ApproxMurnaghan(ListN2):
        """List N x 2"""
        return TCalculators.ApproxMurnaghan(ListN2)

    @staticmethod
    def ApproxBirchMurnaghan(ListN2):
        """List N x 2"""
        return TCalculators.ApproxBirchMurnaghan(ListN2)

    @staticmethod
    def FillTube(radTube, length, nAtoms, radAtom, delta, nPrompts, let, charge):
        return TCalculators.FillTube(radTube, length, nAtoms, radAtom, delta, nPrompts, let, charge)

class Importer(object):

    @staticmethod
    def checkFormat(filename):
        """check file format"""
        if filename.endswith(".fdf") or filename.endswith(".FDF"):
            return "SIESTAfdf"

        if filename.endswith(".out") or filename.endswith(".OUT"):
            return "SIESTAout"

        if filename.endswith(".ani") or filename.endswith(".ANI"):
            return "SIESTAANI"

        if filename.endswith(".xyz") or filename.endswith(".XYZ"):
            return "SIESTAXYZ"

        if filename.endswith(".STRUCT_OUT"):
            return "SIESTASTRUCT_OUT"

        if filename.endswith(".MD_CAR"):
            return "SIESTAMD_CAR"

        if filename.endswith(".XSF"):
            return "SIESTAXSF"

        return "unknown"

    @staticmethod
    def Import(filename, fl='all'):
        """import file"""
        if os.path.exists(filename):
            models = []
            fdf = TFDFFile()
            fileFormat = Importer.checkFormat(filename)

            if fileFormat == "SIESTAfdf":
                models = TSIESTA.atoms_from_fdf(filename)
                fdf.from_fdf_file(filename)

            if fileFormat == "SIESTAout":
                if fl == 'opt':
                    models = TSIESTA.atoms_from_output_optim(filename)
                else:
                    type_of_run = (TSIESTA.TypeOfRun(filename).split())[0].lower()
                    if type_of_run == 'cg':
                        models = TSIESTA.atoms_from_output_cg(filename)
                    else:
                        models = TSIESTA.atoms_from_output_md(filename)
                fdf.from_out_file(filename)

            if fileFormat == "SIESTAANI":
                models = TSIESTA.atoms_from_ani(filename)
                fdf = "#"

            if fileFormat == "SIESTASTRUCT_OUT":
                models = TSIESTA.atoms_from_struct_out(filename)
                fdf = "#"

            if fileFormat == "SIESTAMD_CAR":
                models = TSIESTA.atoms_from_md_car(filename)
                fdf = "#"

            if fileFormat == "SIESTAXSF":
                models = TXSF.get_atoms(filename)
                fdf = "#"

            if fileFormat == "SIESTAXYZ":
                models = TSIESTA.atoms_from_xyz(filename)
                fdf = "#"
        return models, fdf

    @staticmethod
    def CheckDOSfile(filename):
        """Check DOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".DOS"
        if os.path.exists(file):
            return file
        else:
            return False

    @staticmethod
    def CheckPDOSfile(filename):
        """Check PDOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".PDOS"
        if os.path.exists(file):
            return file
        else:
            return False


    @staticmethod
    def DOSSIESTA(filename, eF=0):
        """Import DOS from file filename"""
        if os.path.exists(filename):
            DOS = TSIESTA.DOSsiesta(filename, eF)
            return DOS

    @staticmethod
    def EFermySIESTA(filename):
        """Import Fermy Energy from file filename"""
        if os.path.exists(filename):
            EF = TSIESTA.FermiEnergy(filename)
            return EF

    @staticmethod
    def Volume(filename):
        """Import Cell Volume from file filename"""
        if os.path.exists(filename):
            EF = TSIESTA.Volume(filename)
            return EF

    @staticmethod
    def Energy(filename):
        """Import Etot from file filename"""
        if os.path.exists(filename):
            E = TSIESTA.Etot(filename)
            return E

##################################################################
############################ TXSF ################################
##################################################################

class TXSFblock:
    def __init__(self, title):
        self.title = title
        self.max = None
        self.min = None

class TXSF:
    def __init__(self):
        self.blocks = []
        self.atoms = []
        self.data3D = np.zeros((1, 1))
        self.filename = ""

    @staticmethod
    def get_atoms(filename):
        periodTable = TPeriodTable()

        Molecules = []
        box = [0,0,0]
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

                if row.find("BEGIN_BLOCK_DATAGRID_3D") > -1:
                    row = f.readline()
                    while row.find("DATA_from:") > -1:
                        row = Helpers.spacedel(f.readline())
                        while row.find("BEGIN_DATAGRID_3D") > -1:
                            row = f.readline()
                            origin = f.readline()
                            vec1 = f.readline().split()
                            vec1 = Helpers.list_str_to_float(vec1)
                            vec2 = f.readline().split()
                            vec2 = Helpers.list_str_to_float(vec2)
                            vec3 = f.readline().split()
                            vec3 = Helpers.list_str_to_float(vec3)
                            bx = vec1[0]
                            by = vec2[1]
                            bz = vec3[2]
                            f.close()

                            AllAtoms = TAtomicModel(atoms)
                            AllAtoms.box = [bx, by, bz]
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
            box = model.box
            f = open(self.filename)
            row = f.readline()
            while row != '':
                if row.find("BEGIN_BLOCK_DATAGRID_3D") > -1:
                    row = f.readline()
                    while row.find("DATA_from:") > -1:
                        datas = []
                        row = f.readline()
                        while row.find("BEGIN_DATAGRID_3D") > -1:
                            row = Helpers.spacedel(row)
                            data3D = TXSFblock(row)
                            while row.find("END_") == -1:  #END_DATAGRID_3D
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
                    row = Helpers.spacedel(f.readline()).split()
                    self.Nx = int(row[0])
                    self.Ny = int(row[1])
                    self.Nz = int(row[2])
                    self.data3D = np.zeros((1, self.Nx*self.Ny*self.Nz))

                    origin = f.readline().split()
                    origin[0] = float(origin[0])
                    origin[1] = float(origin[1])
                    origin[2] = float(origin[2])
                    self.origin = np.array(origin)
                    vec1 = float(f.readline().split()[0])
                    vec2 = float(f.readline().split()[1])
                    vec3 = float(f.readline().split()[2])
                    self.spacing = (vec1 / self.Nx, vec2 / self.Ny, vec3 / self.Nz)
                    self.box = (vec1, vec2, vec3)

                    ind = 0
                    while ind < self.Nx*self.Ny*self.Nz:
                        row = f.readline().split()
                        for data in row:
                            self.data3D[0, ind] = float(data)
                            ind += 1
                    row = f.readline()
                    row = Helpers.spacedel(f.readline())

                    for i in range(0,len(self.blocks)):
                        for j in range(0,len(self.blocks[i])):
                            if self.blocks[i][j].title.find(getChildNode) > -1:
                                self.blocks[i][j].min = np.min(self.data3D)
                                self.blocks[i][j].max = np.max(self.data3D)
                    self.data3D = self.data3D.reshape((self.Nx, self.Ny, self.Nz), order='F')
                    f.close()
                    return self.atoms, self.box
                row = f.readline()
        f.close()

    def isosurface(self, value):
        verts, faces, normals, values = marching_cubes_lewiner(self.data3D, level=value, spacing=self.spacing, gradient_direction='descent', step_size=1, allow_degenerate=True, use_classic=False)

        for i in range(0,len(verts)):
            verts[i]+=self.origin
        return verts, faces

    def contours(self, values, type_of_plane = "xy", slice = 5):
        conts = []
        #print(type_of_plane)
        spacing = self.spacing
        origin = self.origin
        if type_of_plane == "xy":
            r = self.data3D[:, :, slice]
        if type_of_plane == "xz":
            r = self.data3D[:, slice, :]
        if type_of_plane == "yz":
            r = self.data3D[ slice, :,:]
        for value in values:
            cont = find_contours(r, value)
            contours = []
            for i in range(0, len(cont)):
                contour = []
                for j in range(0, len(cont[i])):
                    if type_of_plane == "xy":
                        contour.append([ origin[0] + cont[i][j][0]*spacing[0], origin[1] + cont[i][j][1]*spacing[1], origin[2] + slice*spacing[2] ])
                    if type_of_plane == "xz":
                        contour.append([ origin[0] + cont[i][j][0]*spacing[0], origin[1] + slice*spacing[1], origin[2] + cont[i][j][1]*spacing[2] ])
                    if type_of_plane == "yz":
                        contour.append([ origin[0] + slice*spacing[0], origin[1] + cont[i][j][0]*spacing[1], origin[2] + cont[i][j][1]*spacing[2] ])
                contours.append(contour)
            conts.append(contours)
        return conts

    def plane(self, type_of_plane = "xy", slice = 5):
        origin = deepcopy(self.origin)
        if type_of_plane == "xy":
            r = self.data3D[:, :, slice]
            origin[2] = self.origin[2] + slice * self.spacing[2]
            spacing = [self.spacing[0], self.spacing[1]]

        if type_of_plane == "xz":
            r = self.data3D[:, slice, :]
            origin[1] = self.origin[1] + slice * self.spacing[1]
            spacing = [self.spacing[0], self.spacing[2]]

        if type_of_plane == "yz":
            r = self.data3D[ slice,:, :]
            origin[0] = self.origin[0] + slice * self.spacing[0]
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




    def contours_fill(self, values, type_of_plane = "xy", slice = 5):
        data = []
        origin = deepcopy(self.origin)

        if type_of_plane == "xy":
            r = self.data3D[:, :, slice]

        if type_of_plane == "xz":
            r = self.data3D[:, slice, :]

        if type_of_plane == "yz":
            r = self.data3D[ slice,:, :]

        r1 = deepcopy(r)
        Nx = len(r1)
        Ny = len(r1[0])
        for i in range(0, Nx):
            for j in range(0, Ny):
                for k in range(0,len(values)-1):
                    if (r1[i][j] > values[k]) and (r1[i][j] <= values[k+1]):
                        r1[i][j] = values[k]

        Nz = 4
        r2 = np.zeros((Nx,Ny,Nz))
        for i in range(0,Nx):
                for j in range(0,Ny):
                    for k in range(0,Nz):
                        if (k == 0) or (k == Nz-1):
                            r2[i][j][k] = 0
                        else:
                            r2[i][j][k] = r1[i][j]

        r2 = np.ascontiguousarray(r2, np.float32)

        minv = np.min(r2)
        maxv = np.max(r2)
        vl = 0

        for value in values:
            vl+=1
            if (value>=minv) and (value<=maxv):
                if type_of_plane == "xy":
                    spacing = (self.spacing[0], self.spacing[1], (4e-3)*(vl+1))
                    origin[2] = self.origin[2] + slice * self.spacing[2] - 1.5 * (4e-3) * (vl + 1)

                if type_of_plane == "xz":
                    spacing = (self.spacing[0], self.spacing[2], (4e-3) * (vl + 1))
                    origin[1] = self.origin[1] + slice * self.spacing[1] - 1.5 * (4e-3) * (vl + 1)

                if type_of_plane == "yz":
                    spacing = (self.spacing[0], self.spacing[2], (4e-3) * (vl + 1))
                    origin[0] = self.origin[0] + slice * self.spacing[0] - 1.5 * (4e-3) * (vl + 1)

                verts, faces, normals, values = marching_cubes_lewiner(r2, level=value, spacing=spacing,
                                                                   gradient_direction='descent', step_size=1,
                                                                   allow_degenerate=True, use_classic=False)

                for i in range(0, len(verts)):
                    if type_of_plane == "xz":
                            verts[i][0], verts[i][1], verts[i][2] = verts[i][0], verts[i][2], verts[i][1]
                    if type_of_plane == "yz":
                        verts[i][0], verts[i][1], verts[i][2] = verts[i][2], verts[i][0],  verts[i][1]
                    verts[i] += origin
                data.append( [verts, faces, value] )
        return data

class AtomsIdentifier(QtWidgets.QDialog):
    def __init__(self, problemAtoms):
        super(AtomsIdentifier, self).__init__()
        self.ui = Ui_Dialog_Atoms()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui.okButton.clicked.connect(self.okButtonClick)
        self.ansv = []

        self.ui.TheTable.setColumnCount(2)
        self.ui.TheTable.setHorizontalHeaderLabels(["Atom Type", "Species"])
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
            data_cell = QtWidgets.QTableWidgetItem(str(problem-199))
            data_cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.ui.TheTable.setItem(self.ui.TheTable.rowCount() - 1, 0, data_cell)
            atom_cell = QtWidgets.QComboBox()

            atom_cell.setModel(model)
            atom_cell.setCurrentIndex(0)
            self.ui.TheTable.setCellWidget(self.ui.TheTable.rowCount() - 1, 1,atom_cell )

    def okButtonClick(self):
        self.ansv = []
        for i in range(0, self.ui.TheTable.rowCount()):
            at_type = self.ui.TheTable.cellWidget(i, 1).currentText()
            if at_type != "select":
                self.ansv.append([200+i, at_type])
        if len(self.ansv) == self.ui.TheTable.rowCount():
            self.close()


class Image3Dexporter(QtWidgets.QMainWindow):
    def __init__(self, windowsWidth, windowsHeight):
            super(Image3Dexporter, self).__init__()
            self.ui = Ui_image3D()
            self.ui.setupUi(self)
            self.setFixedSize(QSize(windowsWidth, windowsHeight))

            self.MainForm = GuiOpenGL(self.ui.openGLWidget, None)
            self.MainForm.filter = None
            #self.ui.openGLWidget.initializeGL()
            #self.openGLWidget.paintGL = self.MainForm.paintGL
            #self.openGLWidget.initializeGL = self.MainForm.initializeGL

            self.show()
