# -*- coding: utf-8 -*-

from copy import deepcopy
import os
from core_gui_atomistic.atomic_model import AtomicModel as TAtomicModel
from src_gui4dft.models.volumericdatablock import VolumericDataBlock
from src_gui4dft.models.volumericdata import VolumericData
from core_gui_atomistic.periodic_table import TPeriodTable
from core_gui_atomistic import helpers
import numpy as np


class XSF(VolumericData):
    def __init__(self):
        VolumericData.__init__(self)
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
                            f.readline()
                            f.readline()
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
            res = XSF.get_atoms(self.filename)
            if len(res) == 0:
                return False
            model = res[0]
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
                            data3D = VolumericDataBlock(row)
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
        if not os.path.exists(self.filename):
            return False
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
                center_mass = tmp_model.center_mass()
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
