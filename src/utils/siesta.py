# -*- coding: utf-8 -*-
import math
import os
import re

import numpy as np

from utils.helpers import Helpers
from utils.periodic_table import TPeriodTable


##################################################################
#########################  The SIESTA class ######################
##################################################################
    
class TSIESTA:

    @staticmethod
    def lattice_constant(filename):
        """ Returns the LatticeConstant from SIESTA output file """
        mult = 1
        latc = Helpers.fromFileProperty(filename, 'LatticeConstant', 1, 'unformatted')
        if latc is None:
            return 1
        property = latc.split()
        if property[1].lower() == "bohr":
            mult = 0.52917720859
        return mult*float(property[0])

    @staticmethod
    def lattice_parameters_abc_angles(filename):
        """ returns data from LatticeParameters block of file """
        LatticeParameters = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeParameters')
        LatConstant = float(TSIESTA.lattice_constant(filename))
        if len(LatticeParameters) > 0:
            data = Helpers.spacedel(LatticeParameters[0]).split()
            a = LatConstant*float(data[0])
            b = LatConstant*float(data[1])
            c = LatConstant*float(data[2])
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
            lat_vect_1 = Helpers.spacedel(LatticeVectors[0]).split()
            lat_vect_1 = np.array(Helpers.list_str_to_float(lat_vect_1))
            lat_vect_2 = Helpers.spacedel(LatticeVectors[1]).split()
            lat_vect_2 = np.array(Helpers.list_str_to_float(lat_vect_2))
            lat_vect_3 = Helpers.spacedel(LatticeVectors[2]).split()
            lat_vect_3 = np.array(Helpers.list_str_to_float(lat_vect_3))
            return LatConstant*lat_vect_1, LatConstant*lat_vect_2, LatConstant*lat_vect_3
        return [False, False, False], [False, False, False], [False, False, False]

    @staticmethod
    def calc_pdos(root, atom_index, species, number_l, number_m, number_n, number_z):
        pdos = np.zeros((2, 1000))
        energy = np.zeros((1, 10))
        nspin = 1
        for child in root:
            if child.tag == "nspin":
                nspin = int(child.text)
            # print(child.tag)
            if child.tag == "energy_values":
                data = (child.text).split()
                data = Helpers.list_str_to_float(data)
                energy = np.array(data)
                pdos = np.zeros((nspin, len(energy)))

            if child.tag == "orbital":
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
                    for children in child:
                        data = children.text.split()
                        data = Helpers.list_str_to_float(data)
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

                is_spin_polarized = int(Helpers.fromFileProperty(filename, 'redata: Number of spin components', 1, 'string').split("=")[1])

                MdSiestaFile = open(filename)
                str1 = MdSiestaFile.readline()

                if is_spin_polarized == 2:
                    number_of_species *= 2
                    number_of_atoms *= 2

                charges_for_all_steps = []
                while str1 != '':
                    if str1 != '' and (str1.find("mulliken: Atomic and Orbital Populations:") >= 0):
                        nsp = 0

                        charges_m = []
                        for i in range(0, len(charges)):
                            charges_m.append(["",0])

                        while nsp < number_of_species:
                            atoms = 0
                            AtomSort = -1
                            while str1.find("mulliken:") >= 0 or len(str1) < 2 or str1.find("Species:") >= 0:
                                if str1.find("Species:") >= 0:
                                    str1 = Helpers.spacedel(str1)
                                    nsp += 1
                                    for i in range(0,len(species)):
                                        if str1.split(' ')[1] == species[i][2]:
                                            AtomSort = i
                                str1 = MdSiestaFile.readline()
                            neutral = pseudo_charges[AtomSort]
                            if is_spin_polarized == 2:
                                neutral /= 2.0

                            skip = 0
                            str1 = Helpers.spacedel(MdSiestaFile.readline())
                            while not Helpers.is_integer(str1.split()[0]):
                                str1 = Helpers.spacedel(MdSiestaFile.readline())
                                if len(str1) == 0:
                                    str1 = Helpers.spacedel(MdSiestaFile.readline())
                                skip += 1

                            while str1 != '\n':
                                if str1 != '\n':
                                    atoms += 1
                                    str1 = Helpers.spacedel(str1)
                                    at = int(str1.split(' ')[0])
                                    chr = float(str1.split(' ')[1])
                                    charges_m[at-1][0] = species[AtomSort][1]
                                    charges_m[at-1][1] += neutral - chr
                                for i in range(0, skip):
                                    str1 = MdSiestaFile.readline()

                        charges_for_all_steps.append(charges_m)
                    str1 = MdSiestaFile.readline()
                MdSiestaFile.close()

                charges = charges_for_all_steps[-1]
                for i in range(0, len(charges)):
                    charges[i][1] = round(charges[i][1],3)
                return charges

            searchSTR1 = ""
            searchSTR2 = ""
            if method == "Hirshfeld":
                searchSTR1 = "Hirshfeld Net Atomic Populations:"
                searchSTR2 = "Hirshfeld Atomic Populations:"

            if method == "Voronoi":
                searchSTR1 = "Voronoi Net Atomic Populations:"
                searchSTR2 = "Voronoi Atomic Populations:"

            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            mendeley = TPeriodTable()

            while str1 != '':
                if str1 != '' and ((str1.find(searchSTR1) >= 0) or (str1.find(searchSTR2) >= 0)):
                    str1 = MdSiestaFile.readline()
                    for i in range(0, number_of_atoms):
                        data = (Helpers.spacedel(MdSiestaFile.readline())).split(' ')
                        charge = float(data[1])
                        atom_sort = mendeley.get_charge_by_letter(data[-1])
                        charges[i] = [atom_sort, charge]
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
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
    def DOS(filename):
        """DOS"""
        if os.path.exists(filename):
            energy, spinDown, spinUp = Helpers.dos_from_file(filename, 2)
            return np.array(spinUp), np.array(spinDown), np.array(energy)

    @staticmethod
    def DOSsiestaV(filename, Ef=0):
        """DOS Vertical. Spin up only"""
        if os.path.exists(filename):
            DOSFile = open(filename)
            strDOS = DOSFile.readline()            
            DOS = []
            while strDOS != '':
                line = strDOS.split(' ')
                line1 = []
                for i in range(0, len(line)):
                    if line[i] != '':
                        line1.append(line[i])                
                DOS.append([float(line1[1]), round(float(line1[0]) - Ef, 5)])
                strDOS = DOSFile.readline()
            return DOS

    @staticmethod
    def Etot(filename):
        """ Returns the Etot from SIESTA output file """
        if os.path.exists(filename):
            return Helpers.fromFileProperty(filename, 'siesta: Etot    =', 2, 'float')
        else:
            return None

    @staticmethod
    def Energies(filename):
        """ Energy from each step """
        return TSIESTA.ListOfValues(filename, "siesta: E_KS(eV) =")
        
    @staticmethod
    def FermiEnergy(filename):
        """ Fermy Energy from SIESTA output file """
        if os.path.exists(filename):
            energy = 0
            try:
                energy = float(Helpers.fromFileProperty(filename, 'siesta:         Fermi =', 2, 'float'))
            except Exception:
                MdSiestaFile = open(filename)
                str1 = MdSiestaFile.readline()
                energy_string = "0 0 0 0 0 0 0"
                while str1 != '':
                    if str1 != '' and (str1.find(
                            "siesta: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)   dDmax  Ef(eV)") >= 0) or (
                            str1.find("scf: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)    dDmax  Ef(eV)") >= 0) or (
                            str1.find(
                                    "iscf     Eharris(eV)        E_KS(eV)     FreeEng(eV)     dDmax    Ef(eV) dHmax(eV)") >= 0):
                        str1 = MdSiestaFile.readline()
                        while (str1.find('siesta') >= 0) or (str1.find('timer') >= 0) or (str1.find('elaps') >= 0) or (
                                str1.find('scf:') >= 0) or (str1.find('spin moment:') >= 0):
                            str1 = Helpers.spacedel(str1)
                            if (str1.find('siesta') >= 0) or (str1.find('scf:') >= 0):
                                energy_string = str1
                            str1 = MdSiestaFile.readline()
                    str1 = MdSiestaFile.readline()
                MdSiestaFile.close()
                energy = float(energy_string.split(' ')[6])
            return energy
        else:
            return None

    @staticmethod
    def number_of_atoms(filename):
        """ Returns the NumberOfAtoms from SIESTA output file """
        number = Helpers.fromFileProperty(filename, 'NumberOfAtoms')
        if number is None:
            block = TSIESTA.get_block_from_siesta_fdf(filename, "AtomicCoordinatesAndAtomicSpecies")
            if len(block) > 0:
                return len(block)
        return number
    
    @staticmethod
    def number_of_species(filename):
        """ Returns the NumberOfSpecies from SIESTA output file """
        return Helpers.fromFileProperty(filename, 'NumberOfSpecies')

    @staticmethod
    def pseudo_charge_of_species(filename):
        """ Returns the pseudo charge from SIESTA output file (from pseudopotential file) """
        species = TSIESTA.get_species(filename)
        MdSiestaFile = open(filename)
        str1 = MdSiestaFile.readline()
        pseudo_charges = []

        while str1 != '':
            if str1 != '' and (str1.find("initatom: Reading input for the pseudopotentials and atomic orbitals") >= 0):
                for i in range(0, len(species)+1):
                    str1 = MdSiestaFile.readline()
                for j in range(0, len(species)):
                    pseudo_charges.append(0)
                    while str1.find("Ground state valence configuration:") < 0:
                        str1 = MdSiestaFile.readline()
                    states = (Helpers.spacedel(str1.split(":")[1])).split(" ")
                    n_states = len(states)
                    while str1.find("Valence configuration for pseudopotential generation") < 0:
                        str1 = MdSiestaFile.readline()
                    for i in range(0, n_states):
                        str1 = MdSiestaFile.readline()
                        pseudo_charges[j] += float(((str1).split("(")[1]).split(")")[0])
                return pseudo_charges
            str1 = MdSiestaFile.readline()
        return pseudo_charges

    @staticmethod
    def atomic_coordinates_format(filename):
        """ Returns the AtomicCoordinatesFormat from SIESTA output file """
        format = Helpers.fromFileProperty(filename, 'AtomicCoordinatesFormat', 1, 'string')
        if format == None:
            formatlow = ""
        else:
            formatlow = format.lower()
        ans = "NotScaledCartesianBohr"
        if (formatlow == "ang") or (formatlow == "notscaledcartesianang"):
            ans = "NotScaledCartesianAng"
        if (formatlow == "fractional") or (formatlow == "scaledbylatticevectors"):
            ans = "ScaledByLatticeVectors"
        if (formatlow == "scaledcartesian"):
            ans = "ScaledCartesian"
        return ans

    @staticmethod    
    def get_species(filename):
        """ Returns the LIST of Speciecies from SIESTA output or fdf file """
        Species = []
        if os.path.exists(filename):
            NumberOfSpecies = TSIESTA.number_of_species(filename)
            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            while str1!='':
                if str1 != '' and (str1.find("block ChemicalSpeciesLabel")>=0):
                    str1 = MdSiestaFile.readline()
                    for i in range(0,NumberOfSpecies):
                        row = Helpers.spacedel(str1).split(' ')[:3]
                        row[0] = int(row[0])
                        row[1] = int(row[1])
                        Species.append(row)
                        str1 = MdSiestaFile.readline()
                    Species.sort(key=lambda line: line[0])
                    return Species
                str1 = MdSiestaFile.readline()
        Species.sort(key=lambda line: line[0])
        return Species
    
    @staticmethod
    def SystemLabel(filename):
        """ Returns the NumberOfAtomsfrom SIESTA output file """
        res = Helpers.fromFileProperty(filename,'SystemLabel',1,"string")
        if res == None:
            res = "siesta"
        return res
        
    @staticmethod
    def SpinPolarized(filename):
        """ Returns the SpinPolarized from SIESTA output file """
        return Helpers.fromFileProperty(filename,'SpinPolarized')

    @staticmethod    
    def ListOfValues(filename, prop):
        """ return all float values of prop from filename """
        ListOfVal = []
        if os.path.exists(filename):
            f = open(filename)
            for st in f:
                if st.find(prop)>=0:
                    ListOfVal.append(float(re.findall(r"[0-9,\.,-]+", st)[0]))
            f.close()
        return ListOfVal

    @staticmethod
    def Replaceatominsiestafdf(filename, atom, string):
        """ not documented """
        NumberOfAtoms = Helpers.fromFileProperty(filename, 'number_of_atoms')
        NumberOfSpecies = Helpers.fromFileProperty(filename, 'number_of_species')
        #lines = []
        f = open(filename)
        lines = f.readlines()    
    
        i = 0        
        newlines = []
        
        while i < len(lines):    
            if lines[i].find("%block ChemicalSpeciesLabel") >= 0:
                for j in range(0,NumberOfSpecies):
                    newlines.append(lines[i])
                    i += 1
    
            if lines[i].find("%block Zmatrix") >= 0:
                newlines.append(lines[i])
                i += 1
                if lines[i].find("cartesian") >= 0:
                    for j in range(0, NumberOfAtoms):
                        if (j == atom):
                            newlines.append(string+'\n')
                        else:
                            newlines.append(lines[i])
                        i += 1    
            newlines.append(lines[i])
            i += 1
        return newlines

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
        steps = Helpers.fromFileProperty(filename, 'MD.NumCGsteps', 1, 'int')
        if steps == 0:
            """ single point"""
            return "sp"
        """ MD or CG? """
        res = Helpers.fromFileProperty(filename, 'MD.TypeOfRun', 1, 'string')
        if res is None:
            res = Helpers.fromFileProperty(filename, "Begin CG opt. move =", 1, 'string')
            if res == "0":
                return "cg"
            res = Helpers.fromFileProperty(filename, "Begin MD step =", 1, 'string')
            if res == "1":
                return "mg"
        return res

    @staticmethod
    def volume(filename):
        """ Returns cell volume from SIESTA output file """
        if os.path.exists(filename):
            return Helpers.fromFileProperty(filename, 'siesta: Cell volume = ', 2, 'float')
        else:
            return None