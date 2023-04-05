# -*- coding: utf-8 -*-
import os
import numpy as np

from core_gui_atomistic import helpers
from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel

from core_gui_atomistic.periodic_table import TPeriodTable
from src_gui4dft.utils.electronic_prop_reader import dos_from_file

import vasprun
from vasprun import vasprun as Vasprun


class VaspDataFromXml(Vasprun):
    def __init__(self, vasp_file='vasprun.xml'):
        super().__init__(vasp_file, verbosity=0)
        self.get_band_gap()
        print(self.values['gap'])
        self.get_dos_data()

    def get_dos_data(self, smear=None, styles='t', xlim=[-3, 3]):
        """Get all data for DOS figure

        Args:
            styles: string (`t` or `s` or `t+spd`)
            xlim: list, the range of energy values on the x-axis, e.g. [-5, 3]
            smear: float (the width of smearing, defult: None)

        Returns:
            A data for DOS figure
        """
        efermi = self.values['calculation']['efermi']
        tdos = np.array(self.values['calculation']['tdos'][0])
        tdos[:, 0] -= efermi
        e = tdos[:, 0]
        rows = (e > xlim[0]) & (e < xlim[1])
        e = e[rows]
        plt_obj = {}
        for option in styles.split('+'):
            if option == 'spd':
                option = ['s', 'p', 'd']
            else:
                option = [option]
            for style in option:
                mydos, labels = self.get_dos(rows, style)
                for data, label in zip(mydos, labels):
                    plt_obj[label] = data

        for label in plt_obj.keys():
            e = np.reshape(e, [len(e), 1])
            data = np.reshape(plt_obj[label], [len(e), 1])
            if smear is not None:
                data = np.hstack((e, data))
                data = vasprun.smear_data(data, smear)
                data = data[:, 1]
            print(data)


def atoms_from_POSCAR(filename):
    """Import structure from POSCAR file."""
    periodTable = TPeriodTable()
    molecules = []
    if os.path.exists(filename):
        struct_file = open(filename)
        helpers.spacedel(struct_file.readline())
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
            new_str = AtomicModel()
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
        my_file = open(filename)
        str1 = my_file.readline()
        for i in range(5):
            str1 = my_file.readline()
        my_file.close()
        e_fermy = float(str1.split()[3])
        return e_fermy


def vasp_dos(filename):
    """DOS"""
    my_file = open(filename)
    str1 = my_file.readline()
    for i in range(5):
        str1 = my_file.readline()
    my_file.close()
    nlines = int(str1.split()[2])
    if os.path.exists(filename):
        spin_up, spin_down, energy = dos_from_file(filename, 2, nlines)
        return np.array(spin_up), np.array(spin_down), np.array(energy)


def model_to_vasp_poscar(model):
    """Create file in VASP POSCAR format."""
    data = ""
    data += "model \n"
    data += ' 1.0 \n'

    data += '  ' + str(model.lat_vector1[0]) + '  ' + str(model.lat_vector1[1]) + '  ' + \
        str(model.lat_vector1[2]) + '\n'
    data += '  ' + str(model.lat_vector2[0]) + '  ' + str(model.lat_vector2[1]) + '  ' + \
        str(model.lat_vector2[2]) + '\n'
    data += '  ' + str(model.lat_vector3[0]) + '  ' + str(model.lat_vector3[1]) + '  ' + \
        str(model.lat_vector3[2]) + '\n'

    per_tab = TPeriodTable()

    types = model.types_of_atoms()
    for i in range(0, len(types)):
        data += ' ' + str(per_tab.get_let(int(types[i][0])))
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
    model.go_to_positive_coordinates()
    model.convert_from_cart_to_direct()
    data += model.coords_for_export("FractionalPOSCAR")
    return data
