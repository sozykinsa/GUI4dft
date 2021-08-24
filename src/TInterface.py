# -*- coding: utf-8 -*-

from copy import deepcopy
import os
from AdvancedTools import TAtomicModel
from AdvancedTools import TVASP
from AdvancedTools import TFDFFile
from AdvancedTools import TSIESTA
from AdvancedTools import TPeriodTable
from AdvancedTools import Helpers
import numpy as np
import math
import skimage
if skimage.__version__ >= '0.17.2':
    from skimage.measure import marching_cubes
else:
    from skimage.measure import marching_cubes_lewiner
from skimage.measure import find_contours
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from image3D import Ui_MainWindow as Ui_image3D
from atomsidentify import Ui_Dialog as Ui_Dialog_Atoms
from TGui import GuiOpenGL


class Importer(object):

    @staticmethod
    def check_format(filename):
        """check file format"""
        if filename.endswith(".fdf") or filename.endswith(".FDF"):
            return "SIESTAfdf"

        if (filename.lower()).endswith(".out"):
            return "SIESTAout"

        if filename.endswith(".ani") or filename.endswith(".ANI"):
            return "SIESTAANI"

        if (filename.lower()).endswith(".xyz"):
            f = open(filename)
            f.readline()
            str1 = Helpers.spacedel(f.readline())
            if len(str1.split()) > 4:
                return "XMolXYZ"
            if len(str1.split()) == 0:
                return "SiestaXYZ"
            return "unknown"

        if filename.endswith(".STRUCT_OUT"):
            return "SIESTASTRUCT_OUT"

        if filename.endswith(".MD_CAR"):
            return "SIESTAMD_CAR"

        if filename.endswith(".XSF"):
            return "SIESTAXSF"

        if filename.endswith(".cube"):
            return "GAUSSIAN_cube"

        if filename.endswith("POSCAR") or filename.endswith("CONTCAR"):
            return "VASPposcar"

        return "unknown"

    @staticmethod
    def Import(filename, fl='all', prop=False):
        """import file"""
        models = []
        fdf = TFDFFile()
        if os.path.exists(filename):
            fileFormat = Importer.check_format(filename)
            print("File " + str(filename) + " : " +str(fileFormat) )

            if fileFormat == "SIESTAfdf":
                models = TAtomicModel.atoms_from_fdf(filename)
                fdf.from_fdf_file(filename)

            if fileFormat == "SIESTAout":
                type_of_run = (TSIESTA.type_of_run(filename).split())[0].lower()
                models = []
                if type_of_run != "sp":
                        if fl != 'opt':
                            models = TAtomicModel.atoms_from_output_cg(filename)
                            if len(models) == 0:
                                models = TAtomicModel.atoms_from_output_md(filename)
                        modelsopt = TAtomicModel.atoms_from_output_optim(filename)
                else:
                        modelsopt = TAtomicModel.atoms_from_output_sp(filename)
                if len(modelsopt) == 1:
                        models.append(modelsopt[0])
                if prop and (len(models) > 0):
                        try:
                            charge_mulliken = TSIESTA.get_charges_mulliken_for_atoms(filename)
                            if len(charge_mulliken[0]) > 0:
                                models[-1].add_atoms_property("charge Mulliken", charge_mulliken)
                            charge_voronoi = TSIESTA.get_charges_voronoi_for_atoms(filename)
                            if len(charge_voronoi[0]) > 0:
                                models[-1].add_atoms_property("charge Voronoi", charge_voronoi)
                            charge_hirshfeld = TSIESTA.get_charges_hirshfeld_for_atoms(filename)
                            if len(charge_hirshfeld[0]) > 0:
                                models[-1].add_atoms_property("charge Hirshfeld", charge_hirshfeld)
                        except Exception:
                            print("Properties failed")
                fdf.from_out_file(filename)

            if fileFormat == "SIESTAANI":
                models = TAtomicModel.atoms_from_ani(filename)

            if fileFormat == "SIESTASTRUCT_OUT":
                models = TAtomicModel.atoms_from_struct_out(filename)

            if fileFormat == "SIESTAMD_CAR":
                models = TAtomicModel.atoms_from_md_car(filename)

            if fileFormat == "SIESTAXSF":
                models = TXSF.get_atoms(filename)

            if fileFormat == "GAUSSIAN_cube":
                models = TGaussianCube.get_atoms(filename)

            if fileFormat == "SiestaXYZ":
                models = TAtomicModel.atoms_from_xyz(filename)

            if fileFormat == "XMolXYZ":
                models = TAtomicModel.atoms_from_XMOLxyz(filename)

            if fileFormat == "VASPposcar":
                models = TAtomicModel.atoms_from_POSCAR(filename)

        return models, fdf

    @staticmethod
    def check_dos_file(filename):
        if filename.endswith("DOSCAR"):
            eFermy = TVASP.fermi_energy_from_doscar(filename)
            return filename, eFermy

        """Check DOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".DOS"
        if os.path.exists(file):
            eFermy = TSIESTA.FermiEnergy(filename)
            return file, eFermy
        else:
            return False, 0

    @staticmethod
    def check_pdos_file(filename):
        """Check PDOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".PDOS"
        if os.path.exists(file):
            return file
        else:
            return False

    @staticmethod
    def check_bands_file(filename):
        """Check PDOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".bands"
        if os.path.exists(file):
            return file
        else:
            return False

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
        Helpers.spacedel(f.readline())

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
        return verts, faces

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
                        row = Helpers.spacedel(f.readline())
                        while row.find("BEGIN_DATAGRID") > -1:
                            row = f.readline()
                            origin = f.readline()
                            vec1 = f.readline().split()
                            vec1 = Helpers.list_str_to_float(vec1)
                            vec2 = f.readline().split()
                            vec2 = Helpers.list_str_to_float(vec2)
                            vec3 = f.readline().split()
                            vec3 = Helpers.list_str_to_float(vec3)
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
                            row = Helpers.spacedel(row)
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
                row = Helpers.spacedel(f.readline()).split()
                self.Nx = int(row[0])
                self.Ny = int(row[1])
                self.Nz = int(row[2])
                self.data3D = np.zeros((1, self.Nx*self.Ny*self.Nz))

                origin = Helpers.list_str_to_float(f.readline().split())
                self.origin = np.array(origin)
                self.origin_to_export = deepcopy(self.origin)
                tmp_model = TAtomicModel(self.atoms)
                center_mass = tmp_model.centr_mass()
                self.origin -= np.array([center_mass[0], center_mass[1], 0])
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
            self.origin -= np.array([center_mass[0], center_mass[1], 0])
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
