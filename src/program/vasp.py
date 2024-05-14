# -*- coding: utf-8 -*-
import os
import numpy as np
import re

from core_atomistic import helpers
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from core_atomistic.periodic_table import TPeriodTable
from utils.electronic_prop_reader import dos_from_file


class VASP:

    @staticmethod
    def atoms_from_poscar(filename):
        """Import structure from POSCAR file."""
        period_table = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            helpers.spacedel(struct_file.readline())
            lat_const = float(helpers.spacedel(struct_file.readline()))
            lat1 = helpers.spacedel(struct_file.readline()).split()
            lat1 = np.array(helpers.list_str_to_float(lat1)) * lat_const
            lat2 = helpers.spacedel(struct_file.readline()).split()
            lat2 = np.array(helpers.list_str_to_float(lat2)) * lat_const
            lat3 = helpers.spacedel(struct_file.readline()).split()
            lat3 = np.array(helpers.list_str_to_float(lat3)) * lat_const
            sorts_of_atoms = helpers.spacedel(struct_file.readline()).split()
            numbers_of_atoms = helpers.spacedel(struct_file.readline()).split()
            numbers_of_atoms = helpers.list_str_to_int(numbers_of_atoms)

            coord_type = helpers.spacedel(struct_file.readline()).lower()

            if (coord_type == "direct") or (coord_type == "cartesian"):
                new_str = AtomicModel()
                for i in range(0, len(numbers_of_atoms)):
                    number = numbers_of_atoms[i]
                    for j in range(0, number):
                        str1 = helpers.spacedel(struct_file.readline())
                        s = str1.split(' ')
                        x = float(s[0])
                        y = float(s[1])
                        z = float(s[2])
                        charge = period_table.get_charge_by_letter(sorts_of_atoms[i])
                        let = sorts_of_atoms[i]
                        new_str.add_atom(Atom([x, y, z, let, charge]))
                new_str.set_lat_vectors(lat1, lat2, lat3)
                if coord_type == "direct":
                    new_str.convert_from_direct_to_cart()
                molecules.append(new_str)
        return molecules

    @staticmethod
    def specieses_from_outcar(filename):
        specieses = []
        ions_per_type = ""
        types = []
        if os.path.exists(filename):
            my_file = open(filename)
            str1 = my_file.readline()
            while str1 != '':
                if str1.find("ions per type") >= 0:
                    ions_per_type = helpers.spacedel(str1.split("ions per type =")[1]).split(" ")
                if str1.find("VRHFIN") >= 0:
                    types.append(str1.split("VRHFIN =")[1].split(":")[0])
                str1 = my_file.readline()
            my_file.close()
        for n, let in zip(ions_per_type, types):
            for i in range(int(n)):
                specieses.append(let)
        return specieses

    def atoms_from_outcar(self, filename):
        molecules = []
        if os.path.exists(filename):
            period_table = TPeriodTable()
            all_vectors = self.vectors_from_outcar(filename)
            specieses = self.specieses_from_outcar(filename)
            prop = "POSITION"
            my_file = open(filename)
            str1 = my_file.readline()
            while str1 != '':
                if (str1 != '') and (str1.find(prop) >= 0):
                    my_file.readline()
                    new_str = AtomicModel()
                    for let in specieses:
                        str1 = my_file.readline()
                        data = str1.split()
                        xyz = np.array([float(data[0]), float(data[1]), float(data[2])])
                        new_str.add_atom_with_data(xyz, period_table.get_charge_by_letter(let))
                    vectors = all_vectors[len(molecules) + 1]
                    new_str.set_lat_vectors(vectors[0], vectors[1], vectors[2])
                    molecules.append(new_str)
                str1 = my_file.readline()
            my_file.close()
        return molecules

    def abc_from_outcar(self, filename):
        """direct lattice vectors"""
        model = AtomicModel()
        vecs = self.vectors_from_outcar(filename)
        if len(vecs) > 0:
            model.set_lat_vectors(vecs[-1][0], vecs[-1][1], vecs[-1][2])
        a, b, c, al, bet, gam = model.cell_params()
        return a, b, c

    @staticmethod
    def number_of_atoms(filename):
        """number_of_atoms"""
        if os.path.exists(filename):
            my_file = open(filename)
            for i in range(0, 7):
                str1 = my_file.readline()
            ns = re.findall(r"[0-9,\.,-]+", str1)  # [0]
            n = 0
            for i in range(0, len(ns)):
                n = n + int(ns[i])
            my_file.close()
        return n

    @staticmethod
    def energy_tot(filename):
        """Energy"""
        prop = "energy(sigma->0) ="
        is_conv = "false"
        iteration = ""
        property1 = ""
        if os.path.exists(filename):
            my_file = open(filename)
            str1 = my_file.readline()
            while str1 != '':
                if (str1 != '') and (str1.find("General timing and accounting informations for this job:") >= 0):
                    is_conv = "true"
                if (str1 != '') and (str1.find("-- Iteration") >= 0):
                    iteration = str1
                if (str1 != '') and (str1.find(prop) >= 0):
                    str1 = str1.replace(prop, ' ')
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[1]
                    property1 = float(prop1)

                str1 = my_file.readline()
            my_file.close()
        return property1, is_conv, iteration

    @staticmethod
    def volume(filename):
        """Cell volume"""
        prop = "volume of cell :"
        if os.path.exists(filename):
            my_file = open(filename)
            str1 = my_file.readline()
            while str1 != '':
                if (str1 != '') and (str1.find(prop) >= 0):
                    str1 = str1.replace(prop, ' ')
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                    property = float(prop1)

                str1 = my_file.readline()
            my_file.close()
        return property

    @staticmethod
    def model_to_vasp_poscar(model, coord_type="Fractional"):
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

        model.sort_atoms_by_type()
        # model.go_to_positive_coordinates()
        model.move_atoms_to_center()
        if coord_type == "Fractional":
            model.convert_from_cart_to_direct()
        if coord_type == "Fractional":
            data += "Direct\n"
        if coord_type == "Cartesian":
            data += "Cartesian\n"
        data += model.coords_for_export("POSCAR")
        return data

    @staticmethod
    def vectors_from_outcar(filename):
        prop = "direct lattice vectors"
        all_vectors = []
        vectors = np.zeros((3, 3), dtype=float)
        if os.path.exists(filename):
            my_file = open(filename)
            str1 = my_file.readline()
            while str1 != '':
                if (str1 != '') and (str1.find(prop) >= 0):
                    str1 = my_file.readline()
                    row1 = re.findall(r"[0-9,\.,-]+", str1)
                    str1 = my_file.readline()
                    row2 = re.findall(r"[0-9,\.,-]+", str1)
                    str1 = my_file.readline()
                    row3 = re.findall(r"[0-9,\.,-]+", str1)

                    vectors[0] = np.array((row1[0], row1[1], row1[2]), dtype=float)
                    vectors[1] = np.array((row2[0], row2[1], row2[2]), dtype=float)
                    vectors[2] = np.array((row3[0], row3[1], row3[2]), dtype=float)
                    all_vectors.append(vectors)
                str1 = my_file.readline()
            my_file.close()
        return all_vectors

    @staticmethod
    def vasp_latt_const(filename):
        """Lattice Constant"""
        if os.path.exists(filename):
            f_name = open(filename)
            f_name.readline()
            str1 = f_name.readline()
            lat_const = float(re.findall(r"[0-9,\.,-]+", str1)[0])
            f_name.close()
        return lat_const

    @staticmethod
    def fermi_energy_from_doscar(filename):
        if os.path.exists(filename):
            my_file = open(filename)
            str1 = my_file.readline()
            for i in range(5):
                str1 = my_file.readline()
            my_file.close()
            e_fermy = float(str1.split()[3])
            return e_fermy

    @staticmethod
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
