# -*- coding: utf-8 -*-
import os
import numpy as np

from utils.periodic_table import TPeriodTable
from utils.electronic_prop_reader import dos_from_file


def fermi_energy_from_doscar(filename):
    if os.path.exists(filename):
        MyFile = open(filename)
        str1 = MyFile.readline()
        for i in range(5):
            str1 = MyFile.readline()
        MyFile.close()
        eFermy = float(str1.split()[3])
        return eFermy


def vasp_dos(filename):
    """DOS"""
    MyFile = open(filename)
    str1 = MyFile.readline()
    for i in range(5):
        str1 = MyFile.readline()
    MyFile.close()
    nlines = int(str1.split()[2])
    if os.path.exists(filename):
        energy, spinDown, spinUp = dos_from_file(filename, 3, nlines)
        return np.array(spinUp), np.array(spinDown), np.array(energy)


def model_to_vasp_poscar(model, filename):
    """Create file in VASP POSCAR format."""
    f = open(filename, 'w')

    data = ""
    data += "model \n"
    data += ' 1.0 \n'

    data += '  ' + str(model.LatVect1[0]) + '  ' + str(model.LatVect1[1]) + '  ' + str(model.LatVect1[2]) + '\n'
    data += '  ' + str(model.LatVect2[0]) + '  ' + str(model.LatVect2[1]) + '  ' + str(model.LatVect2[2]) + '\n'
    data += '  ' + str(model.LatVect3[0]) + '  ' + str(model.LatVect3[1]) + '  ' + str(model.LatVect3[2]) + '\n'

    PerTab = TPeriodTable()

    types = model.typesOfAtoms()
    for i in range(0, len(types)):
        data += ' ' + str(PerTab.get_let(int(types[i][0])))
    data += "\n"

    for i in range(0, len(types)):
        count = 0
        for atom in model.atoms:
            if atom.charge == int(types[i][0]):
                count += 1
        data += ' ' + str(count)
    data += "\n"

    data += "Direct\n"

    model.sort_atoms_by_type()
    model.GoToPositiveCoordinates()
    model.convert_from_cart_to_direct()
    data += model.coords_for_export("FractionalPOSCAR")

    print(data, file=f)
    f.close()
