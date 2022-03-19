# -*- coding: utf-8 -*-

from copy import deepcopy
import os
from models.atomic_model import TAtomicModel
from models.volumericdatablock import VolumericDataBlock
from models.volumericdata import VolumericData
from utils.periodic_table import TPeriodTable
import numpy as np
import math


class GaussianCube(VolumericData):
    def __init__(self):
        VolumericData.__init__(self)
        self.type = "TGaussianCube"

    @staticmethod
    def get_atoms(filename):
        periodTable = TPeriodTable()
        Molecules = []
        if os.path.exists(filename):
            f = open(filename)
            f.readline()
            f.readline()
            row = f.readline().split()
            n_atoms = int(row[0])
            # origin = (float(row[1]), float(row[2]), float(row[3]))

            nx, vec1, mult = GaussianCube.local_get_N_vect(f.readline().split())
            ny, vec2, mult = GaussianCube.local_get_N_vect(f.readline().split())
            nz, vec3, mult = GaussianCube.local_get_N_vect(f.readline().split())

            atoms = []

            for i in range(0, n_atoms):
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
            model = GaussianCube.get_atoms(self.filename)[0]
            self.atoms = model.atoms

            f = open(self.filename)
            row = f.readline()
            data3D = VolumericDataBlock(row)
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

            self.Nx, vec1, mult = GaussianCube.local_get_N_vect(f.readline().split())
            self.Ny, vec2, mult = GaussianCube.local_get_N_vect(f.readline().split())
            self.Nz, vec3, mult = GaussianCube.local_get_N_vect(f.readline().split())

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
