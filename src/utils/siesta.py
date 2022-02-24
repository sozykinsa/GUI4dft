# -*- coding: utf-8 -*-
import math
import os
import re

import numpy as np

from utils import helpers
import xml.etree.ElementTree as ET
from utils.periodic_table import TPeriodTable


##################################################################
#########################  The SIESTA class ######################
##################################################################

class TSIESTA:

    @staticmethod
    def lattice_constant(filename):
        """Returns the LatticeConstant from SIESTA output file."""
        mult = 1
        latc = helpers.from_file_property(filename, 'LatticeConstant', 1, 'unformatted')
        if latc is None:
            return 1
        property = latc.split()
        if property[1].lower() == "bohr":
            mult = 0.52917720859
        return mult * float(property[0])

    @staticmethod
    def lattice_parameters_abc_angles(filename):
        """Returns data from LatticeParameters block of file."""
        LatticeParameters = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeParameters')
        LatConstant = float(TSIESTA.lattice_constant(filename))
        if len(LatticeParameters) > 0:
            data = helpers.spacedel(LatticeParameters[0]).split()
            a = LatConstant * float(data[0])
            b = LatConstant * float(data[1])
            c = LatConstant * float(data[2])
            alpha = math.radians(float(data[3]))
            beta = math.radians(float(data[4]))
            gamma = math.radians(float(data[5]))

            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lat_vectors_from_params(a, b, c, alpha, beta, gamma)

            return lat_vect_1, lat_vect_2, lat_vect_3
        else:
            return [False, False, False], [False, False, False], [False, False, False]

    @staticmethod
    def lat_vectors_from_params(a, b, c, alpha, beta, gamma):
        tm = math.pow(math.cos(alpha), 2) + math.pow(math.cos(beta), 2) + math.pow(math.cos(gamma), 2)
        tmp = math.sqrt(1 + 2 * math.cos(alpha) * math.cos(beta) * math.cos(gamma) - tm)
        h = c * tmp / math.sin(gamma)
        lat_vect_1 = [a, 0, 0]
        lat_vect_2 = [b * math.cos(gamma), b * math.sin(gamma), 0]
        lat_vect_3 = [c * math.cos(beta), c * math.cos(alpha) * math.sin(gamma), h]
        if math.fabs(lat_vect_2[0]) < 1e-8:
            lat_vect_2[0] = 0
        if math.fabs(lat_vect_2[1]) < 1e-8:
            lat_vect_2[1] = 0
        if math.fabs(lat_vect_3[0]) < 1e-8:
            lat_vect_3[0] = 0
        if math.fabs(lat_vect_3[1]) < 1e-8:
            lat_vect_3[1] = 0
        if math.fabs(lat_vect_3[2]) < 1e-8:
            lat_vect_3[2] = 0
        return lat_vect_1, lat_vect_2, lat_vect_3

    @staticmethod
    def lattice_vectors(filename):
        LatConstant = float(TSIESTA.lattice_constant(filename))
        LatticeVectors = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeVectors')
        if len(LatticeVectors) > 0:
            lat_vect_1 = helpers.spacedel(LatticeVectors[0]).split()
            lat_vect_1 = np.array(helpers.list_str_to_float(lat_vect_1))
            lat_vect_2 = helpers.spacedel(LatticeVectors[1]).split()
            lat_vect_2 = np.array(helpers.list_str_to_float(lat_vect_2))
            lat_vect_3 = helpers.spacedel(LatticeVectors[2]).split()
            lat_vect_3 = np.array(helpers.list_str_to_float(lat_vect_3))
            return LatConstant * lat_vect_1, LatConstant * lat_vect_2, LatConstant * lat_vect_3
        return [False, False, False], [False, False, False], [False, False, False]

    @staticmethod
    def calc_pdos(file, atom_index, species, number_l, number_m, number_n, number_z):
        tree = ET.parse(file)
        root = tree.getroot()
        pdos = np.zeros((2, 1000))
        energy = np.zeros((1, 10))
        nspin = 1
        for child in root:
            if child.tag == "nspin":
                nspin = int(child.text)
            if child.tag == "energy_values":
                data = child.text.split()
                data = helpers.list_str_to_float(data)
                energy = np.array(data)
                pdos = np.zeros((nspin, len(energy)))

            if child.tag == "orbital":
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
                    for children in child:
                        data = children.text.split()
                        data = helpers.list_str_to_float(data)
                        data = np.array(data)
                        data = data.reshape((nspin, len(energy)), order='F')
                        pdos += data
        return pdos, energy

    @staticmethod
    def get_charges_for_atoms(filename, method):
        if os.path.exists(filename):
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            charges = []
            for i in range(0, number_of_atoms):
                charges.append([])

            if method == "Mulliken":
                pseudo_charges = TSIESTA.pseudo_charge_of_species(filename)
                number_of_species = len(pseudo_charges)
                species = TSIESTA.get_species(filename)

                is_spin_polarized = int(helpers.from_file_property(filename, 'redata: Number of spin components', 1,
                                                                   'string').split("=")[1])

                md_siesta_file = open(filename)
                str1 = md_siesta_file.readline()

                if is_spin_polarized == 2:
                    number_of_species *= 2
                    number_of_atoms *= 2

                charges_for_all_steps = []
                while str1 != '':
                    if str1 != '' and (str1.find("mulliken: Atomic and Orbital Populations:") >= 0):
                        nsp = 0

                        charges_m = []
                        for i in range(0, len(charges)):
                            charges_m.append(["", 0])

                        while nsp < number_of_species:
                            atoms = 0
                            atom_sort = -1
                            while str1.find("mulliken:") >= 0 or len(str1) < 2 or str1.find("Species:") >= 0:
                                if str1.find("Species:") >= 0:
                                    str1 = helpers.spacedel(str1)
                                    nsp += 1
                                    for i in range(0, len(species)):
                                        if str1.split(' ')[1] == species[i][2]:
                                            atom_sort = i
                                str1 = md_siesta_file.readline()
                            neutral = pseudo_charges[atom_sort]
                            if is_spin_polarized == 2:
                                neutral /= 2.0

                            skip = 0
                            str1 = helpers.spacedel(md_siesta_file.readline())
                            while not helpers.is_integer(str1.split()[0]):
                                str1 = helpers.spacedel(md_siesta_file.readline())
                                if len(str1) == 0:
                                    str1 = helpers.spacedel(md_siesta_file.readline())
                                skip += 1

                            while str1 != '\n':
                                if str1 != '\n':
                                    atoms += 1
                                    str1 = helpers.spacedel(str1)
                                    at = int(str1.split(' ')[0])
                                    chr = float(str1.split(' ')[1])
                                    charges_m[at - 1][0] = species[atom_sort][1]
                                    charges_m[at - 1][1] += neutral - chr
                                for i in range(0, skip):
                                    str1 = md_siesta_file.readline()

                        charges_for_all_steps.append(charges_m)
                    str1 = md_siesta_file.readline()
                md_siesta_file.close()

                if len(charges_for_all_steps) > 0:
                    charges = charges_for_all_steps[-1]
                    for i in range(0, len(charges)):
                        charges[i][1] = round(charges[i][1], 3)
                return charges

            searchSTR1 = ""
            searchSTR2 = ""
            if method == "Hirshfeld":
                searchSTR1 = "Hirshfeld Net Atomic Populations:"
                searchSTR2 = "Hirshfeld Atomic Populations:"

            if method == "Voronoi":
                searchSTR1 = "Voronoi Net Atomic Populations:"
                searchSTR2 = "Voronoi Atomic Populations:"

            md_siesta_file = open(filename)
            str1 = md_siesta_file.readline()
            mendeley = TPeriodTable()

            while str1 != '':
                if str1 != '' and ((str1.find(searchSTR1) >= 0) or (str1.find(searchSTR2) >= 0)):
                    str1 = md_siesta_file.readline()
                    for i in range(0, number_of_atoms):
                        data = (helpers.spacedel(md_siesta_file.readline())).split(' ')
                        charge = float(data[1])
                        atom_sort = mendeley.get_charge_by_letter(data[-1])
                        charges[i] = [atom_sort, charge]
                str1 = md_siesta_file.readline()
            md_siesta_file.close()
        return charges

    @staticmethod
    def get_charges_voronoi_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Voronoi")

    @staticmethod
    def get_charges_hirshfeld_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Hirshfeld")

    @staticmethod
    def get_charges_mulliken_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Mulliken")

    @staticmethod
    def energy_tot(filename):
        """ Returns the Etot from SIESTA output file """
        if os.path.exists(filename):
            return helpers.from_file_property(filename, 'siesta: Etot    =', 2, 'float')
        else:
            return None

    @staticmethod
    def energies(filename):
        """Energy from each step."""
        return TSIESTA.list_of_values(filename, "siesta: E_KS(eV) =")

    @staticmethod
    def FermiEnergy(filename):
        """ Fermy Energy from SIESTA output file """
        if os.path.exists(filename):
            energy = 0
            try:
                energy = float(helpers.from_file_property(filename, 'siesta:         Fermi =', 2, 'float'))
            except Exception:
                md_siesta_file = open(filename)
                str1 = md_siesta_file.readline()
                energy_string = "0 0 0 0 0 0 0"
                search1 = "siesta: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)   dDmax  Ef(eV)"
                search2 = "scf: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)    dDmax  Ef(eV)"
                search3 = "iscf     Eharris(eV)        E_KS(eV)     FreeEng(eV)     dDmax    Ef(eV) dHmax(eV)"
                while str1 != '':
                    if str1 != '' and (str1.find(search1) >= 0) or (str1.find(search2) >= 0) or \
                            (str1.find(search3) >= 0):
                        str1 = md_siesta_file.readline()
                        while (str1.find('siesta') >= 0) or (str1.find('timer') >= 0) or (str1.find('elaps') >= 0) or (
                                str1.find('scf:') >= 0) or (str1.find('spin moment:') >= 0):
                            str1 = helpers.spacedel(str1)
                            if (str1.find('siesta') >= 0) or (str1.find('scf:') >= 0):
                                energy_string = str1
                            str1 = md_siesta_file.readline()
                    str1 = md_siesta_file.readline()
                md_siesta_file.close()
                energy = float(energy_string.split(' ')[6])
            return energy
        else:
            return None

    @staticmethod
    def number_of_atoms(filename):
        """Returns the NumberOfAtoms from SIESTA output file."""
        number = helpers.from_file_property(filename, 'NumberOfAtoms')
        if number is None:
            block = TSIESTA.get_block_from_siesta_fdf(filename, "AtomicCoordinatesAndAtomicSpecies")
            if len(block) > 0:
                return len(block)
        return number

    @staticmethod
    def number_of_species(filename):
        """ Returns the NumberOfSpecies from SIESTA output file """
        return helpers.from_file_property(filename, 'NumberOfSpecies')

    @staticmethod
    def pseudo_charge_of_species(filename):
        """ Returns the pseudo charge from SIESTA output file (from pseudopotential file) """
        species = TSIESTA.get_species(filename)
        siesta_file = open(filename)
        str1 = siesta_file.readline()
        pseudo_charges = []

        while str1 != '':
            if str1 != '' and (str1.find("initatom: Reading input for the pseudopotentials and atomic orbitals") >= 0):
                for i in range(0, len(species) + 1):
                    str1 = siesta_file.readline()
                for j in range(0, len(species)):
                    pseudo_charges.append(0)
                    while str1.find("Ground state valence configuration:") < 0:
                        str1 = siesta_file.readline()
                    states = (helpers.spacedel(str1.split(":")[1])).split(" ")
                    n_states = len(states)
                    while str1.find("Valence configuration for pseudopotential generation") < 0:
                        str1 = siesta_file.readline()
                    for i in range(0, n_states):
                        str1 = siesta_file.readline()
                        pseudo_charges[j] += float(((str1).split("(")[1]).split(")")[0])
                return pseudo_charges
            str1 = siesta_file.readline()
        return pseudo_charges

    @staticmethod
    def atomic_coordinates_format(filename):
        """Returns the AtomicCoordinatesFormat from SIESTA output file."""
        format = helpers.from_file_property(filename, 'AtomicCoordinatesFormat', 1, 'string')
        if format is None:
            formatlow = ""
        else:
            formatlow = format.lower()
        ans = "NotScaledCartesianBohr"
        if (formatlow == "ang") or (formatlow == "notscaledcartesianang"):
            ans = "NotScaledCartesianAng"
        if (formatlow == "fractional") or (formatlow == "scaledbylatticevectors"):
            ans = "ScaledByLatticeVectors"
        if formatlow == "scaledcartesian":
            ans = "ScaledCartesian"
        return ans

    @staticmethod
    def get_species(filename):
        """Returns the LIST of Speciecies from SIESTA output or fdf file."""
        species = []
        if os.path.exists(filename):
            NumberOfSpecies = TSIESTA.number_of_species(filename)
            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            while str1 != '':
                if str1 != '' and (str1.find("block ChemicalSpeciesLabel") >= 0):
                    str1 = MdSiestaFile.readline()
                    for i in range(0, NumberOfSpecies):
                        row = helpers.spacedel(str1).split(' ')[:3]
                        row[0] = int(row[0])
                        row[1] = int(row[1])
                        species.append(row)
                        str1 = MdSiestaFile.readline()
                    species.sort(key=lambda line: line[0])
                    return species
                str1 = MdSiestaFile.readline()
        species.sort(key=lambda line: line[0])
        return species

    @staticmethod
    def system_label(filename):
        """Returns the SystemLabel SIESTA output file."""
        res = helpers.from_file_property(filename, 'SystemLabel', 1, "string")
        if res is None:
            res = "siesta"
        return res

    @staticmethod
    def spin_polarized(filename):
        """Returns the SpinPolarized from SIESTA output file."""
        res = helpers.from_file_property(filename, 'SpinPolarized')
        if res is None:
            res = False
        return res

    @staticmethod
    def list_of_values(filename, prop):
        """Return all float values of prop from filename."""
        list_of_val = []
        if os.path.exists(filename):
            f = open(filename)
            for st in f:
                if st.find(prop) >= 0:
                    list_of_val.append(float(re.findall(r"[0-9,\.,-]+", st)[0]))
            f.close()
        return list_of_val

    # @staticmethod
    # def Replaceatominsiestafdf(filename, atom, string):
    #    """ not documented """
    #    NumberOfAtoms = helpers.from_file_property(filename, 'number_of_atoms')
    #    NumberOfSpecies = helpers.from_file_property(filename, 'number_of_species')
    #    f = open(filename)
    #    lines = f.readlines()

    #    i = 0
    #    newlines = []

    #    while i < len(lines):
    #        if lines[i].find("%block ChemicalSpeciesLabel") >= 0:
    #            for j in range(0, NumberOfSpecies):
    #                newlines.append(lines[i])
    #                i += 1

    #        if lines[i].find("%block Zmatrix") >= 0:
    #            newlines.append(lines[i])
    #            i += 1
    #            if lines[i].find("cartesian") >= 0:
    #                for j in range(0, NumberOfAtoms):
    #                    if j == atom:
    #                        newlines.append(string+'\n')
    #                    else:
    #                        newlines.append(lines[i])
    #                    i += 1
    #        newlines.append(lines[i])
    #        i += 1
    #    return newlines

    @staticmethod
    def get_block_from_siesta_fdf(filename, blockname):
        """ возвращает содержимое блока входного файла """
        lines = []
        flag = 0
        f = open(filename)
        blockname = blockname.lower()
        for line in f:
            line1 = line.lower()
            if (line1.find(blockname) < 0) and (flag == 1):
                lines.append(line)
            if (line1.find(blockname) >= 0) and (flag == 1):
                f.close()
                return lines
            if (line1.find(blockname) >= 0) and (flag == 0):
                flag = 1
        return []

    @staticmethod
    def type_of_run(filename):
        steps = helpers.from_file_property(filename, 'MD.NumCGsteps', 1, 'int')
        if steps == 0:
            """ single point """
            return "sp"
        """ MD or CG? """
        res = helpers.from_file_property(filename, 'MD.TypeOfRun', 1, 'string')
        if res is None:
            res = helpers.from_file_property(filename, "Begin CG opt. move =", 1, 'string')
            if res == "0":
                return "cg"
            res = helpers.from_file_property(filename, "Begin MD step =", 1, 'string')
            if res == "1":
                return "mg"
            res = "cg"
        return res

    @staticmethod
    def volume(filename):
        """Returns cell volume from SIESTA output file."""
        if os.path.exists(filename):
            return helpers.from_file_property(filename, 'siesta: Cell volume = ', 1, 'float')
        else:
            return None
