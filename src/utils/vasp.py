# -*- coding: utf-8 -*-
import os
import numpy as np

from utils import helpers
from models.atom import Atom
from models.atomic_model import TAtomicModel

from utils.periodic_table import TPeriodTable
from utils.electronic_prop_reader import dos_from_file


def atoms_from_POSCAR(filename):
    """Import structure from POSCAR file."""
    periodTable = TPeriodTable()
    molecules = []
    if os.path.exists(filename):
        struct_file = open(filename)
        str1 = helpers.spacedel(struct_file.readline())
        latConst = float(helpers.spacedel(struct_file.readline()))
        lat1 = helpers.spacedel(struct_file.readline()).split()
        lat1 = np.array(helpers.list_str_to_float(lat1)) * latConst
        lat2 = helpers.spacedel(struct_file.readline()).split()
        lat2 = np.array(helpers.list_str_to_float(lat2)) * latConst
        lat3 = helpers.spacedel(struct_file.readline()).split()
        lat3 = np.array(helpers.list_str_to_float(lat3)) * latConst
        SortsOfAtoms = helpers.spacedel(struct_file.readline()).split()
        NumbersOfAtoms = helpers.spacedel(struct_file.readline()).split()
        NumbersOfAtoms = helpers.list_str_to_int(NumbersOfAtoms)
        NumberOfAtoms = 0
        for num in NumbersOfAtoms:
            NumberOfAtoms += num

        coord_type = helpers.spacedel(struct_file.readline()).lower()

        if (coord_type == "direct") or (coord_type == "cartesian"):
            new_str = TAtomicModel()
            for i in range(0, len(NumbersOfAtoms)):
                number = NumbersOfAtoms[i]
                for j in range(0, number):
                    str1 = helpers.spacedel(struct_file.readline())
                    s = str1.split(' ')
                    x = float(s[0])
                    y = float(s[1])
                    z = float(s[2])
                    charge = periodTable.get_charge_by_letter(SortsOfAtoms[i])
                    let = SortsOfAtoms[i]
                    new_str.add_atom(Atom([x, y, z, let, charge]))
            new_str.set_lat_vectors(lat1, lat2, lat3)
            if coord_type == "direct":
                new_str.convert_from_direct_to_cart()
            molecules.append(new_str)
    return molecules


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
        spinUp, spinDown, energy = dos_from_file(filename, 3, nlines)
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
