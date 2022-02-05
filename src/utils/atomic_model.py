# -*- coding: utf-8 -*-
# Python 3
import copy
import math
import os
from copy import deepcopy

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm

from utils import helpers
from utils.periodic_table import TPeriodTable
from utils.siesta import TSIESTA

    
##################################################################
########################### TATOM ################################
##################################################################    
    
class TAtom(object):
    def __init__(self, atData):
        """Constructor"""
        self.x = atData[0]
        self.y = atData[1]
        self.z = atData[2]
        self.let = atData[3]
        self.charge = int(atData[4])
        self.selected = False
        self.fragment1 = False
        self.properties = {}
        pass

    def setSelected(self, fl):
        self.selected = fl

    def isSelected(self):
        return self.selected

    def setProperty(self, prop, val):
        self.properties[prop] = val

    def getProperty(self, prop):
        return self.properties.get(prop)

    def to_string(self):
        let = self.let
        sx = helpers.float_to_string(self.x)
        sy = helpers.float_to_string(self.y)
        sz = helpers.float_to_string(self.z)
        return let + '  ' + sx + '  ' + sy + '  ' + sz
        
##################################################################
################### The AtomicModel class ########################
##################################################################


class TAtomicModel(object):
    def __init__(self, newatoms: list=[]):
        self.atoms = []
        self.bonds = []
        self.bonds_per = []  # for exact calculation in form

        self.bcp = []
        self.rcp = []
        self.ccp = []

        self.name = ""
        self.LatVect1 = np.array([100, 0, 0])
        self.LatVect2 = np.array([0, 100, 0])
        self.LatVect3 = np.array([0, 0, 100])

        for at in newatoms:
            if isinstance(at, TAtom):
                atom = deepcopy(at)
            else:
                atom = TAtom(at)
            self.add_atom(atom)

    def get_positions(self):
        pos = np.zeros((len(self.atoms), 3))
        for i in range(len(self.atoms)):
            pos[i,:] = self.atoms[i].x, self.atoms[i].y, self.atoms[i].z
        return pos

    def get_atomic_numbers(self):
        numb = np.zeros(len(self.atoms))
        for i in range(len(self.atoms)):
            numb[i] = self.atoms[i].charge
        return numb

    def get_center_of_mass(self):
        return np.array(self.centr_mass())

    def get_tags(self):
        return []

    def get_cell(self):
        cell = np.zeros((3,3))
        cell[0, :] = self.LatVect1
        cell[1, :] = self.LatVect2
        cell[2, :] = self.LatVect3

    @staticmethod
    def atoms_from_ani(filename):
        """import from ANI file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            ani_file = open(filename)
            NumberOfAtoms = int(ani_file.readline())
            while NumberOfAtoms > 0:
                newModel = TAtomicModel.atoms_from_xyz_structure(NumberOfAtoms, ani_file, periodTable)
                molecules.append(newModel)
                st = ani_file.readline()
                if st != '':
                    NumberOfAtoms = int(st)
                else:
                    NumberOfAtoms = 0
        return molecules

    @staticmethod
    def atoms_from_fdf(filename):
        """Return a AtList from fdf file"""
        AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat, lat_vect_1, lat_vect_2, lat_vect_3, units = TAtomicModel.atoms_from_fdf_prepare(
            filename)
        f = open(filename)
        lines = f.readlines()
        f.close()
        AllAtoms = TAtomicModel.atoms_from_fdf_text(AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat,
                                                    lat_vect_1, lat_vect_2, lat_vect_3, lines, units)
        return [AllAtoms]

    @staticmethod
    def atoms_from_fdf_prepare(filename):
        NumberOfAtoms = TSIESTA.number_of_atoms(filename)
        AtomicCoordinatesFormat = TSIESTA.atomic_coordinates_format(filename)
        lat = ""
        units = helpers.fromFileProperty(filename, 'ZM.UnitsLength', 1, 'string')
        if AtomicCoordinatesFormat == "ScaledCartesian":
            lat = TSIESTA.lattice_constant(filename)
            units = "ang"
        if not units:
            if AtomicCoordinatesFormat.lower().find("bohr") >= 0:
                units = "bohr"
            else:
                units = "ang"
        lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lattice_vectors(filename)
        if not lat_vect_1[0]:
            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lattice_parameters_abc_angles(filename)
        chem_spec_info = {}
        ChemicalSpeciesLabel = TSIESTA.get_block_from_siesta_fdf(filename, "ChemicalSpeciesLabel")
        for j in range(0, len(ChemicalSpeciesLabel)):
            chem_spec_info[(ChemicalSpeciesLabel[j].split())[0]] = (ChemicalSpeciesLabel[j].split())[1:3]
        return AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat, lat_vect_1, lat_vect_2, lat_vect_3, units

    @staticmethod
    def atoms_from_fdf_text(AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat, lat_vect_1, lat_vect_2,
                            lat_vect_3, lines, units):
        AllAtoms = TAtomicModel()
        AtList = []
        AtList1 = []
        i = 0
        isBlockAtomicCoordinates = False
        isBlockZMatrix = False
        while i < len(lines):
            if lines[i].find("%block Zmatrix") >= 0:
                isBlockZMatrix = True
                i += 1
                AtList = []
                if lines[i].find("cartesian") >= 0:
                    for j in range(0, NumberOfAtoms):
                        i += 1
                        Atom_full = lines[i].split()
                        AtList.append([float(Atom_full[1]), float(Atom_full[2]), float(Atom_full[3]),
                                       (chem_spec_info[str(Atom_full[0])])[1], (chem_spec_info[str(Atom_full[0])])[0]])
            if lines[i].find("%block AtomicCoordinatesAndAtomicSpecies") >= 0:
                isBlockAtomicCoordinates = True
                mult = 1
                if AtomicCoordinatesFormat == "NotScaledCartesianBohr":
                    mult = 0.52917720859
                for j in range(0, NumberOfAtoms):
                    i += 1
                    Atom_full = lines[i].split()
                    AtList1.append([mult * float(Atom_full[0]), mult * float(Atom_full[1]), mult * float(Atom_full[2]),
                                    (chem_spec_info[str(Atom_full[3])])[1], (chem_spec_info[str(Atom_full[3])])[0]])
            i += 1
        if isBlockZMatrix:
            AllAtoms = TAtomicModel(AtList)
        else:
            if isBlockAtomicCoordinates:
                AllAtoms = TAtomicModel(AtList1)
        if lat_vect_1[0] == False:
            AllAtoms.set_lat_vectors_default()
        else:
            AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
        if isBlockZMatrix:
            if units.lower() == "bohr":
                AllAtoms.convert_from_scaled_to_cart(0.52917720859)
        else:
            if isBlockAtomicCoordinates:
                if AtomicCoordinatesFormat == "ScaledByLatticeVectors":
                    AllAtoms.convert_from_direct_to_cart()
                if AtomicCoordinatesFormat == "ScaledCartesian":
                    AllAtoms.convert_from_scaled_to_cart(lat)
        return AllAtoms

    @staticmethod
    def atoms_from_output_cg(filename):
        """import from CG output"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            sps = TSIESTA.get_species(filename)
            species_label_charges = ['null']
            for spec in sps:
                species_label_charges.append(spec[1])

            siesta_file = open(filename)
            sl = []
            isSpesF = 0
            need_to_convert1 = 0
            str1 = siesta_file.readline()
            atoms = []
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (isSpesF == 0):
                    str1 = siesta_file.readline()
                    while str1.find('siesta') >= 0:
                        str1 = helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = siesta_file.readline()
                    isSpesF = 1

                if (str1 != '') and (str1.find("outcell: Unit cell vectors (Ang):") >= 0) and (isSpesF == 1):
                    lat_vect_1 = siesta_file.readline().split()
                    lat_vect_1 = helpers.list_str_to_float(lat_vect_1)
                    lat_vect_2 = siesta_file.readline().split()
                    lat_vect_2 = helpers.list_str_to_float(lat_vect_2)
                    lat_vect_3 = siesta_file.readline().split()
                    lat_vect_3 = helpers.list_str_to_float(lat_vect_3)
                    isFectF = 1

                    if len(atoms) > 0:
                        AllAtoms = TAtomicModel(atoms)
                        AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                        if need_to_convert1:
                            AllAtoms.convert_from_direct_to_cart()
                            need_to_convert1 = 0
                        molecules.append(AllAtoms)

                isFractionalfound = str1.find("outcoor: Atomic coordinates (fractional)") >= 0
                if isFractionalfound:
                    need_to_convert1 = 1

                isAngfound = str1.find("zmatrix: Z-matrix coordinates: (Ang ; rad )") >= 0
                isBohfound = str1.find("zmatrix: Z-matrix coordinates: (Bohr; rad )") >= 0
                mult = 1.0
                if isBohfound:
                    mult = 0.52917720859

                if (str1 != '') and (isAngfound or isBohfound or isFractionalfound) and (isSpesF == 1):
                    if not isFractionalfound:
                        for j in range(0, 2):
                            str1 = siesta_file.readline()
                    atoms = []

                    for i1 in range(0, number_of_atoms):
                        str1 = helpers.spacedel(siesta_file.readline())
                        S = str1.split(' ')
                        d1 = float(S[0]) * mult
                        d2 = float(S[1]) * mult
                        d3 = float(S[2]) * mult
                        Charge = species_label_charges[sl[len(atoms)]]
                        C = periodTable.get_let(Charge)
                        A = [d1, d2, d3, C, Charge]
                        atoms.append(A)
                str1 = siesta_file.readline()
            siesta_file.close()
        return molecules

    @staticmethod
    def atoms_from_output_md(filename):
        """import from MD output """
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            NumberOfSpecies = TSIESTA.number_of_species(filename)
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)
            MdSiestaFile = open(filename)
            speciesLabel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sl = []
            isSpesFinde = 0
            isSpesF = 0
            str1 = MdSiestaFile.readline()
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (
                        isSpesF == 0):
                    str1 = MdSiestaFile.readline()
                    while str1.find('siesta') >= 0:
                        str1 = helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = MdSiestaFile.readline()
                    isSpesF = 1
                if (str1 != '') and (str1.find("ChemicalSpeciesLabel") >= 0) and (isSpesFinde == 0):
                    for i in range(0, NumberOfSpecies):
                        str1 = helpers.spacedel(MdSiestaFile.readline())
                        S = str.split(str1, ' ')
                        speciesLabel[int(S[0])] = S[1]
                    isSpesFinde = 1

                atoms = []

                if (str1 != '') and (str1.find("Begin CG move") >= 0 or str1.find("Begin MD step") >= 0 or str1.find("Begin CG opt. move") >= 0):
                    if (str1 != '') and str1.find("Begin MD step") >= 0:
                        for j in range(0, 3):
                            MdSiestaFile.readline()
                    else:
                        if (str1.find("Begin CG move") >= 0) or (str1.find("Begin CG opt. move") >= 0):
                            while (str1 != '') and (str1.find("block") == -1) and (str1.find("outcoor: Atomic coordinates (Ang)") == -1):
                                str1 = MdSiestaFile.readline()

                    atoms = []
                    for i1 in range(0, NumberOfAtoms):
                        str1 = helpers.spacedel(MdSiestaFile.readline())
                        if str1 == "":
                            return []
                        S = str1.split(' ')
                        d1 = float(S[0])
                        d2 = float(S[1])
                        d3 = float(S[2])
                        Charge = speciesLabel[sl[len(atoms)]]
                        C = periodTable.get_let(Charge)
                        A = [d1, d2, d3, C, Charge]
                        atoms.append(A)
                    str1 = MdSiestaFile.readline()
                    while str1.find("outcell: Unit cell vectors (Ang):") == -1:
                        str1 = MdSiestaFile.readline()
                    vec1 = MdSiestaFile.readline().split()
                    vec1 = helpers.list_str_to_float(vec1)
                    vec2 = MdSiestaFile.readline().split()
                    vec2 = helpers.list_str_to_float(vec2)
                    vec3 = MdSiestaFile.readline().split()
                    vec3 = helpers.list_str_to_float(vec3)
                    AllAtoms = TAtomicModel(atoms)
                    AllAtoms.set_lat_vectors(vec1, vec2, vec3)
                    molecules.append(AllAtoms)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
        return molecules

    @staticmethod
    def atoms_from_md_car(filename):
        """import from MD_CAR output """
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            str1 = struct_file.readline()
            while str1.find("---") >= 0:
                newStr = TAtomicModel()
                LatConst = float(struct_file.readline())
                lat1 = helpers.spacedel(struct_file.readline()).split()
                lat1 = helpers.list_str_to_float(lat1)
                lat1 = LatConst*np.array(lat1)
                lat2 = helpers.spacedel(struct_file.readline()).split()
                lat2 = helpers.list_str_to_float(lat2)
                lat2 = LatConst * np.array(lat2)
                lat3 = helpers.spacedel(struct_file.readline()).split()
                lat3 = helpers.list_str_to_float(lat3)
                lat3 = LatConst * np.array(lat3)
                NumbersOfAtoms = helpers.spacedel(struct_file.readline()).split()
                NumbersOfAtoms = helpers.list_str_to_int(NumbersOfAtoms)
                str1 = struct_file.readline()
                if helpers.spacedel(str1) == "Direct":
                    for i in range(0,len(NumbersOfAtoms)):
                        for j in range(0, NumbersOfAtoms[i]):
                            row = helpers.spacedel(struct_file.readline()).split()
                            row = helpers.list_str_to_float(row)

                            let = "Direct"
                            charge = 200 + i
                            x = row[0]
                            y = row[1]
                            z = row[2]

                            newStr.add_atom(TAtom([x, y, z, let, charge]))
                    newStr.set_lat_vectors(lat1, lat2, lat3)
                    newStr.convert_from_direct_to_cart()
                    molecules.append(newStr)
        return molecules

    @staticmethod
    def atoms_from_output_sp(filename):
        """Return the initial AtList from single point output file"""
        AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat, lat_vect_1, lat_vect_2, lat_vect_3, units = TAtomicModel.atoms_from_fdf_prepare(
            filename)

        lines = TFDFFile.fdf_data_dump(filename)

        AllAtoms = TAtomicModel.atoms_from_fdf_text(AtomicCoordinatesFormat, NumberOfAtoms, chem_spec_info, lat,
                                                    lat_vect_1, lat_vect_2, lat_vect_3, lines, units)

        molecules = [AllAtoms]
        return molecules

    @staticmethod
    def atoms_from_output_optim(filename):
        """Return the relaxed AtList from output file"""
        NumberOfAtoms = TSIESTA.number_of_atoms(filename)
        Species = TSIESTA.get_species(filename)
        AtList = []
        f1 = False
        f2 = False
        f3 = False
        n_vec = 0
        lat_vect_1 = ""
        lat_vect_2 = ""
        lat_vect_3 = ""
        mult = 1

        for line in open(filename, 'r'):
            if (line.find("outcell: Unit cell vectors (Ang):") > -1):
                f2 = True
                n_vec = 0
            else:
                if (n_vec == 0) and f2:
                    lat_vect_1 = line.split()
                    lat_vect_1 = helpers.list_str_to_float(lat_vect_1)
                if (n_vec == 1) and f2:
                    lat_vect_2 = line.split()
                    lat_vect_2 = helpers.list_str_to_float(lat_vect_2)
                if (n_vec == 2) and f2:
                    lat_vect_3 = line.split()
                    lat_vect_3 = helpers.list_str_to_float(lat_vect_3)
                    f2 = False
                if f2:
                    n_vec += 1

            if (line.find("outcoor: Relaxed atomic coordinates (Ang)") > -1) or (line.find("outcoor: Relaxed atomic coordinates (Bohr)") > -1):
                f1 = True
                if line.find("outcoor: Relaxed atomic coordinates (Bohr)") > -1:
                    mult = 0.52917720859
            else:
                if (len(AtList) < NumberOfAtoms) and f1:
                    line1 = line.split()
                    line2 = [float(line1[0]) * mult, float(line1[1]) * mult, float(line1[2]) * mult, line1[5], Species[int(line1[3]) - 1][1]]
                    AtList.append(line2)
                if len(AtList) == NumberOfAtoms:
                    AllAtoms = TAtomicModel(AtList)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    return [AllAtoms]
            if line.find("outcoor: Relaxed atomic coordinates (fractional)") > -1:
                f3 = True
            else:
                if (len(AtList) < NumberOfAtoms) and f3:
                    line1 = line.split()
                    line2 = [float(line1[0]), float(line1[1]), float(line1[2]), line1[5], Species[int(line1[3]) - 1][1]]
                    AtList.append(line2)
                if len(AtList) == NumberOfAtoms:
                    AllAtoms = TAtomicModel(AtList)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    AllAtoms.convert_from_direct_to_cart()
                    return [AllAtoms]
        return []

    @staticmethod
    def atoms_from_POSCAR(filename):
        """import from xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            str1 = helpers.spacedel(struct_file.readline())
            latConst = float(helpers.spacedel(struct_file.readline()))
            lat1 = helpers.spacedel(struct_file.readline()).split()
            lat1 = np.array(helpers.list_str_to_float(lat1))*latConst
            lat2 = helpers.spacedel(struct_file.readline()).split()
            lat2 = np.array(helpers.list_str_to_float(lat2))*latConst
            lat3 = helpers.spacedel(struct_file.readline()).split()
            lat3 = np.array(helpers.list_str_to_float(lat3))*latConst
            SortsOfAtoms = helpers.spacedel(struct_file.readline()).split()
            NumbersOfAtoms = helpers.spacedel(struct_file.readline()).split()
            NumbersOfAtoms = helpers.list_str_to_int(NumbersOfAtoms)
            NumberOfAtoms = 0
            for number in NumbersOfAtoms:
                NumberOfAtoms += number

            if helpers.spacedel(struct_file.readline()).lower() == "direct":
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
                        new_str.add_atom(TAtom([x, y, z, let, charge]))
                new_str.set_lat_vectors(lat1, lat2, lat3)
                new_str.convert_from_direct_to_cart()
                molecules.append(new_str)
        return molecules


    @staticmethod
    def atoms_from_struct_out(filename):
        """import from STRUCT_OUT file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            lat1 = helpers.spacedel(struct_file.readline()).split()
            lat1 = helpers.list_str_to_float(lat1)
            lat2 = helpers.spacedel(struct_file.readline()).split()
            lat2 = helpers.list_str_to_float(lat2)
            lat3 = helpers.spacedel(struct_file.readline()).split()
            lat3 = helpers.list_str_to_float(lat3)
            NumberOfAtoms = int(struct_file.readline())

            newStr = TAtomicModel()
            for i1 in range(0, NumberOfAtoms):
                str1 = helpers.spacedel(struct_file.readline())
                S = str1.split(' ')
                x = float(S[2])
                y = float(S[3])
                z = float(S[4])
                charge = int(S[1])
                let = periodTable.get_let(charge)
                newStr.add_atom(TAtom([x, y, z, let, charge]))
            newStr.set_lat_vectors(lat1,lat2,lat3)
            newStr.convert_from_direct_to_cart()
            molecules.append(newStr)
        return molecules

    @staticmethod
    def atoms_from_xyz(filename, xyzcritic2):
        """import from xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            NumberOfAtoms = int(math.fabs(int(f.readline())))
            newModel = TAtomicModel.atoms_from_xyz_structure(NumberOfAtoms, f, periodTable)
            if xyzcritic2:
                fl = False
                critic_data = {"xn", "xr", "xb", "xc", "xz"}
                for atom in newModel.atoms:
                    if atom.let.lower() in critic_data:
                        fl = True

                if fl:
                    newModel2 = TAtomicModel()
                    xz_points = []

                    for atom in newModel.atoms:
                        if atom.let.lower() not in critic_data:
                            newModel2.add_atom(atom)
                        if atom.let.lower() == "xb":
                            newModel2.add_critical_point_bond(atom)
                        if atom.let.lower() == "xz":
                            xz_points.append(atom)

                    points = []

                    for i in range(0, len(xz_points)):
                        if len(points) == 0:
                            points.append(xz_points[i])
                        else:
                            px = points[-1].x
                            py = points[-1].y
                            pz = points[-1].z

                            nx = xz_points[i].x
                            ny = xz_points[i].y
                            nz = xz_points[i].z

                            d = math.sqrt((px-nx)*(px-nx)+(py-ny)*(py-ny)+(pz-nz)*(pz-nz))

                            if d < 0.09:
                                points.append(xz_points[i])
                            else:
                                newModel2.add_bond_path_point(points)
                                points = [xz_points[i]]

                    if len(points) > 0:
                        newModel2.add_bond_path_point(points)

                    newModel2.bond_path_points_optimize()

                    molecules.append(newModel2)
                    return molecules
            molecules.append(newModel)
        return molecules

    @staticmethod
    def atoms_from_XMOLxyz(filename):
        """import from XMOL xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            NumberOfAtoms = int(math.fabs(int(f.readline())))
            newModel = TAtomicModel.atoms_from_xyz_structure(NumberOfAtoms, f, periodTable, [1, 2, 3, 4])
            molecules.append(newModel)
        return molecules

    @staticmethod
    def atoms_from_xyz_structure(NumberOfAtoms, ani_file, periodTable, indexes=[0, 1, 2, 3]):
        if indexes[0] == 0:
            str1 = helpers.spacedel(ani_file.readline())
        atoms = []
        for i1 in range(0, NumberOfAtoms):
            str1 = helpers.spacedel(ani_file.readline())
            S = str1.split(' ')
            d1 = float(S[indexes[1]])
            d2 = float(S[indexes[2]])
            d3 = float(S[indexes[3]])
            C = S[indexes[0]]
            Charge = periodTable.get_charge_by_letter(C)
            A = [d1, d2, d3, C, Charge]
            atoms.append(A)
        newModel = TAtomicModel(atoms)
        newModel.set_lat_vectors_default()
        return newModel

    def get_LatVect1_norm(self):
        return norm(self.LatVect1)

    def get_LatVect2_norm(self):
        return norm(self.LatVect2)

    def get_LatVect3_norm(self):
        return norm(self.LatVect3)

    def get_angle_alpha(self):
        a = self.get_LatVect2_norm()
        b = self.get_LatVect3_norm()
        ab = self.LatVect2[0]*self.LatVect3[0] + self.LatVect2[1]*self.LatVect3[1] + self.LatVect2[2]*self.LatVect3[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def get_angle_beta(self):
        a = self.get_LatVect1_norm()
        b = self.get_LatVect3_norm()
        ab = self.LatVect1[0]*self.LatVect3[0] + self.LatVect1[1]*self.LatVect3[1] + self.LatVect1[2]*self.LatVect3[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def get_angle_gamma(self):
        a = self.get_LatVect2_norm()
        b = self.get_LatVect1_norm()
        ab = self.LatVect2[0]*self.LatVect1[0] + self.LatVect2[1]*self.LatVect1[1] + self.LatVect2[2]*self.LatVect1[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def set_lat_vectors(self, v1, v2, v3):
        if (len(v1) == 3) and (len(v2) == 3) and (len(v3) == 3):
            self.LatVect1 = np.array(v1)
            self.LatVect2 = np.array(v2)
            self.LatVect3 = np.array(v3)
        else:
            print("Wrong vectors")

    def set_lat_vectors_default(self):
        sx = self.sizeX()
        if sx < 0.3:
            sx = 5
        sy = self.sizeY()
        if sy < 0.3:
            sy = 5
        sz = self.sizeZ()
        if sz < 0.3:
            sz = 5
        self.LatVect1 = np.array([1.4*sx, 0, 0])
        self.LatVect2 = np.array([0, 1.4*sy, 0])
        self.LatVect3 = np.array([0, 0, 1.4*sz])

    def delete_atom(self, ind):
        if self.nAtoms() == 1:
            return
        if (ind >= 0) and (ind < self.nAtoms()):
            self.selected_atom = -1
            self.atoms.pop(ind)
            self.find_bonds_fast()

    def add_atom(self, atom, min_dist = 0):
        """ Adds atom to the molecule is minimal distance to other atoms more then minDist """
        Dist = 10000
        if min_dist > 0:
            model = TAtomicModel(self.atoms)
            model.set_lat_vectors(self.LatVect1, self.LatVect2, self.LatVect3)
            model.add_atom(atom)
            for ind in range(0, len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms) - 1)
                if r < Dist:
                    Dist = r

        if Dist > min_dist:
            newAt = deepcopy(atom)
            self.atoms.append(newAt)

    def add_critical_point_bond(self, atom):
        newAt = deepcopy(atom)
        self.bcp.append(newAt)

    def add_bond_path_point(self, points):
        for cp in self.bcp:
            dx = math.pow(cp.x - points[0].x, 2)
            dy = math.pow(cp.y - points[0].y, 2)
            dz = math.pow(cp.z - points[0].z, 2)
            d = math.sqrt(dx+dy+dz)
            if d < 1e-4:
                if cp.getProperty("bond1") == None:
                    cp.setProperty("bond1", deepcopy(points))
                else:
                    cp.setProperty("bond2", deepcopy(points))

    def atoms_of_bond_path(self, ind):
        atoms = self.atoms
        cp = self.bcp[ind]
        bond1 = cp.getProperty("bond1")
        bond2 = cp.getProperty("bond2")
        cpx1 = bond1[-1].x
        cpy1 = bond1[-1].y
        cpz1 = bond1[-1].z
        cpx2 = bond2[-1].x
        cpy2 = bond2[-1].y
        cpz2 = bond2[-1].z
        x1 = atoms[0].x
        y1 = atoms[0].y
        z1 = atoms[0].z
        minr1 = math.sqrt((cpx1 - x1) * (cpx1 - x1) + (cpy1 - y1) * (cpy1 - y1) + (cpz1 - z1) * (cpz1 - z1))
        minr2 = math.sqrt((cpx2 - x1) * (cpx2 - x1) + (cpy2 - y1) * (cpy2 - y1) + (cpz2 - z1) * (cpz2 - z1))
        ind1 = 0
        ind2 = 0
        for i in range(0, len(atoms)):
            x1 = atoms[i].x
            y1 = atoms[i].y
            z1 = atoms[i].z

            dx1 = cpx1 - x1
            dx2 = cpx2 - x1

            dy1 = cpy1 - y1
            dy2 = cpy2 - y1

            dz1 = cpz1 - z1
            dz2 = cpz2 - z1

            d1 = math.sqrt(dx1 * dx1 + dy1 * dy1 + dz1 * dz1)
            d2 = math.sqrt(dx2 * dx2 + dy2 * dy2 + dz2 * dz2)

            if d1 < minr1:
                minr1 = d1
                ind1 = i

            if d2 < minr2:
                minr2 = d2
                ind2 = i
        return ind1, ind2

    def bond_path_points_optimize(self):
        i = 0

        while i < len(self.bcp):
            bond1 = self.bcp[i].getProperty("bond1")
            bond2 = self.bcp[i].getProperty("bond2")
            if (bond1 is None) or (bond2 is None):
                self.bcp.pop(i)
                i -= 1
            else:
                if (bond1[-1].x == bond2[-1].x) and (bond1[-1].y == bond2[-1].y) and (bond1[-1].z == bond2[-1].z):
                    self.bcp.pop(i)
                    i -= 1
            i += 1

        for cp in self.bcp:
            self.critical_path_simplifier("bond1", cp)
            self.critical_path_simplifier("bond2", cp)

    def critical_path_simplifier(self, b, cp):
        bond = deepcopy(cp.getProperty(b))
        if bond is None:
            print(b)
            return
        i = 2
        while (i < len(bond)) and (len(bond) > 1):
            l = (bond[i].x - bond[i - 1].x) * (bond[i - 2].y - bond[i - 1].y) * (bond[i - 2].z - bond[i - 1].z)
            j = (bond[i].y - bond[i - 1].y) * (bond[i - 2].x - bond[i - 1].x) * (bond[i - 2].z - bond[i - 1].z)
            k = (bond[i].z - bond[i - 1].z) * (bond[i - 2].x - bond[i - 1].x) * (bond[i - 2].y - bond[i - 1].y)
            i += 1
            if (math.fabs(l - j) < 1e-6) and (math.fabs(l - k) < 1e-6):
                bond.pop(i - 2)
                i -= 1
        cp.setProperty(b + "opt", bond)

    def add_atomic_model(self, atomic_model, minDist = 0):
        for at in atomic_model:
            self.add_atom(at, minDist)

    def edit_atom(self, ind, newAtom):
        if (ind >= 0) and (ind < self.nAtoms()):
            self.atoms[ind] = newAtom

    def add_atoms_property(self, prop, value):
        if self.nAtoms() == len(value):
            for i in range(0, self.nAtoms()):
                self.atoms[i].setProperty(prop, value[i][1])

    def AddBond(self, bond):
        self.bonds.append(bond)

    def nBonds(self):
        return len(self.bonds)

    def __getitem__(self, i):
        return self.atoms[i]

    def ModifyAtomsTypes(self, changes):
        Mendeley = TPeriodTable()
        for change in changes:
            let = change[1]
            charge = Mendeley.get_charge_by_letter(let)

            old_charge = change[0]

            for atom in self.atoms:
                if atom.charge == old_charge:
                    atom.charge = charge
                    atom.let = let

    def nAtoms(self):
        return len(self.atoms)
    
    def centr_mass(self, charge=0):
        """The method returns the center of mass of the molecule"""
        cx = 0
        cy = 0
        cz = 0
        n = 0
        
        if charge == 0:
            mendeley = TPeriodTable()
            for j in range(0, len(self.atoms)):
                m = mendeley.Atoms[self.atoms[j].charge].mass
                cx += self.atoms[j].x * m
                cy += self.atoms[j].y * m
                cz += self.atoms[j].z * m
                n += m
        else:
            for j in range(0, len(self.atoms)):
                if int(self.atoms[j].charge) == int(charge):
                    cx += self.atoms[j].x
                    cy += self.atoms[j].y
                    cz += self.atoms[j].z
                    n += 1
        try:
            res = [cx/n, cy/n, cz/n]
        except Exception:
            print("ZeroDivisionError")
            return [0, 0, 0]
        
        return res

    def rotateX(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha *= math.pi / 180
        # ox
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].y) * math.cos(alpha) - float(self.atoms[i].z) * math.sin(alpha)
            ynn = float(self.atoms[i].y) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].y = xnn
            self.atoms[i].z = ynn

    def rotateY(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha *= math.pi / 180
        # oy
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) + float(self.atoms[i].z) * math.sin(alpha)
            ynn = -float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].z = ynn

    def rotateZ(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha *= math.pi / 180
        # oz
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) - float(self.atoms[i].y) * math.sin(alpha)
            ynn = float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].y) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].y = ynn
        
    def ProjectionToCylinder(self,atomslist,radius):
        """This method returns projections on cylinder with radius for atom at"""
        row = []
        for at in range(0,len(atomslist)):
            x = float(self.atoms[atomslist[at]].x)
            y = float(self.atoms[atomslist[at]].y)
            z = float(self.atoms[atomslist[at]].z)
            ro = math.sqrt(math.pow(x,2)+math.pow(y,2))
            fi = math.atan(x/y)
            row.append([atomslist[at],x*radius/ro,y*radius/ro,z,ro,fi])    
        return row

    def indexes_of_atoms_with_charge(self, charge):
        """ IndexesOfAtomsWithCharge """
        Indexes = []
        for j in range(0, len(self.atoms)):
            if int(self.atoms[j].charge) == int(charge):
                Indexes.append(j)
        return Indexes

    def indexes_of_atoms_in_ball(self, ats, atom, R):
        """ Indexes of atoms in the ball of radius R with center on atom 'atom'
        ats - list of indexes
        atom- index of atom in the center of ball
        """
        newatoms = [atom]
        for at in ats:
            if at != atom:
                if self.atom_atom_distance(at, atom) < R:
                    newatoms.append(at)
        return newatoms

    def convert_from_scaled_to_cart(self, lat):
        for atom in self.atoms:
            atom.x *= lat
            atom.y *= lat
            atom.z *= lat

    def convert_from_direct_to_cart(self):
        for atom in self.atoms:
            x = atom.x * self.LatVect1[0] + atom.y * self.LatVect2[0] + atom.z * self.LatVect3[0]
            y = atom.x * self.LatVect1[1] + atom.y * self.LatVect2[1] + atom.z * self.LatVect3[1]
            z = atom.x * self.LatVect1[2] + atom.y * self.LatVect2[2] + atom.z * self.LatVect3[2]
            atom.x = x
            atom.y = y
            atom.z = z

    def convert_from_cart_to_direct(self):
        SysCoord = np.array([self.LatVect1, self.LatVect2, self.LatVect3])
        obr = np.linalg.inv(SysCoord).transpose()

        for atom in self.atoms:
            Coord = np.array([atom.x, atom.y, atom.z])
            res = obr.dot(Coord)
            atom.x = res[0]
            atom.y = res[1]
            atom.z = res[2]

    def minX(self):
        """ минимальная координата по оси X """
        minx = self.atoms[0].x
        for atom in self.atoms:
            if float(atom.x) < float(minx):
                minx = atom.x
        return float(minx)

    def maxX(self):
        """ максимальная координата по оси X """
        maxx = self.atoms[0].x
        for atom in self.atoms:
            if atom.x > maxx:
                maxx = atom.x
        return maxx

    def sizeX(self):
        """ длина молекулы по оси X """
        return self.maxX() - self.minX()

    def minY(self):
        """ минимальная координата по оси Y """
        miny = self.atoms[0].y

        for atom in self.atoms:
            if float(atom.y) < float(miny):
                miny = atom.y
        return float(miny)

    def maxY(self):
        """ максимальная координата по оси Y """
        maxy = self.atoms[0].y

        for atom in self.atoms:
            if float(atom.y) > float(maxy):
                maxy = atom.y
        return float(maxy)

    def sizeY(self):
        """ длина молекулы по оси Y """
        return self.maxY() - self.minY()

    def minZ(self):
        """ минимальная координата по оси Z """
        minz = self.atoms[0].z
        
        for atom in self.atoms:
            if float(atom.z)<float(minz):
                minz = atom.z
        return float(minz)        

    def maxZ(self):
        """ максимальная координата по оси Z """
        maxz = self.atoms[0].z
        
        for atom in self.atoms:
            if float(atom.z)>float(maxz):
                maxz = atom.z
        return float(maxz)
        
    def sizeZ(self):
        """ длина молекулы по оси Z """
        return self.maxZ() - self.minZ()

    def sort_atoms_by_type(self):
        for i in range(0, self.nAtoms()):
            for j in range(0, self.nAtoms()-i-1):
                if self.atoms[j].charge > self.atoms[j+1].charge:
                    atom = self.atoms[j]
                    self.atoms[j] = self.atoms[j+1]
                    self.atoms[j+1] = atom

    def AngleToCenterOfAtoms(self, atomslist):
        """The method AngleToCenterOfAtoms returns the Angle To Center Of atoms_from_fdf list atomslist in the molecule"""
        angle = 0

        for at in range(0, len(atomslist)):
            x = self.atoms[atomslist[at]].x
            y = self.atoms[atomslist[at]].y
            fi = math.atan(x / y)
            angle += fi
        angle /= len(atomslist)
        return angle

        
    def atom_atom_distance(self, at1, at2):
        """ atom_atom_distance
        All atoms MUST be in the Cell!!!
        """
        pos1 = np.array([self.atoms[at1].x, self.atoms[at1].y, self.atoms[at1].z])
        pos2 = np.array([self.atoms[at2].x, self.atoms[at2].y, self.atoms[at2].z])
        delta_pos = pos2 - pos1

        ro = norm(delta_pos)
        values = [-1, 0, 1]
        for i in values:
            for j in values:
                for k in values:
                    if abs(i) + abs(j) + abs(k) != 0:
                        ro1 = norm(delta_pos + i*self.LatVect1 + j*self.LatVect2 + k*self.LatVect3)
                        if ro1 < ro:
                            ro = ro1
        return ro

    def move_atoms_to_cell(self):
        a = np.array([self.LatVect1, self.LatVect2, self.LatVect3])
        ainv = inv(a)

        for at in self.atoms:
            pos = np.array([at.x, at.y, at.z])
            b = pos.transpose()
            total = ainv.dot(b)
            pos -= math.trunc(total[0]) * self.LatVect1 + math.trunc(total[1]) * self.LatVect2 + math.trunc(total[2]) * self.LatVect3
            at.x = pos[0]
            at.y = pos[1]
            at.z = pos[2]

    def Neighbors(self, atom, col, charge):
        """ Look for col neighbors of atom "atom" with a charge "charge" """
        neighbor = []
        for at in range(0, len(self.atoms)):
            if (at != atom) and (int(self.atoms[at].charge) == int(charge)):
                r = self.atom_atom_distance(atom, at)
                neighbor.append([at,r])
        fl = 1
        while fl == 1:
            fl = 0
            for i in range(len(neighbor)-1,0,-1):
                if neighbor[i-1][1]>neighbor[i][1]:
                    at = copy.deepcopy(neighbor[i])
                    neighbor[i] = copy.deepcopy(neighbor[i-1])
                    neighbor[i-1] = copy.deepcopy(at)
                    fl = 1
        neighbo = []                
        neighbo.append(neighbor[0][0])
        for i in range(1,col):
            neighbo.append(neighbor[i][0])
        return neighbo

    def find_bonds_exact(self):
        """The method returns list of bonds of the molecule"""
        if self.bonds_per != []:
            return self.bonds_per
        PeriodTable = TPeriodTable()
        for i in range(0, len(self.atoms)):
            for j in range(i+1, len(self.atoms)):
                length = round(self.atom_atom_distance(i, j), 4)
                t1 = int(self.atoms[i].charge)
                t2 = int(self.atoms[j].charge)
                if math.fabs(length - PeriodTable.Bonds[t1][t2]) < 0.2*PeriodTable.Bonds[t1][t2]:
                    self.bonds_per.append([t1, t2, length, self.atoms[i].let, i, self.atoms[j].let, j])
        return self.bonds_per

    def find_bonds_fast(self):
        self.bonds = []
        Mendeley = TPeriodTable()
        for i in range(0, len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                rx2 = math.pow(self.atoms[i].x - self.atoms[j].x, 2)
                ry2 = math.pow(self.atoms[i].y - self.atoms[j].y, 2)
                rz2 = math.pow(self.atoms[i].z - self.atoms[j].z, 2)
                r = math.sqrt(rx2 + ry2 + rz2)
                r_tab = Mendeley.Bonds[self.atoms[i].charge][self.atoms[j].charge]
                if (r > 1e-4) and (r < 1.2 * r_tab):
                    self.bonds.append([i, j])

    def Delta(self, newMolecula):
        """ maximum distance from atoms in self to the atoms in the newMolecula"""
        DeltaMolecula1 = 0
        r1 = norm(self.LatVect1) + norm(self.LatVect2) + norm(self.LatVect3)
        for at2 in newMolecula.atoms:
            model = TAtomicModel(self.atoms)
            model.add_atom(at2)
            for ind in range(0,len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms)-1)
                if r < r1:
                    r1 = r
            if r1>DeltaMolecula1:
                DeltaMolecula1 = r1
        return DeltaMolecula1

    def DeltaMin(self, newMolecula):
        """ minimum distance from atoms in self to the atoms in the newMolecula"""
        DeltaMolecula1 = 100000
        r1 = norm(self.LatVect1) + norm(self.LatVect2) + norm(self.LatVect3)
        for at2 in newMolecula.atoms:
            model = TAtomicModel(self.atoms)
            model.add_atom(at2)
            for ind in range(0,len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms)-1)
                if r < r1:
                    r1 = r
            if r1<DeltaMolecula1:
                DeltaMolecula1 = r1
        return DeltaMolecula1

    def GoToPositiveCoordinates(self):
        xm = self.minX()
        ym = self.minY()
        zm = self.minZ()
        for i in range(0, self.nAtoms()):
            self.atoms[i].x -= xm
            self.atoms[i].x = self.minus0(self.atoms[i].x)
            self.atoms[i].y -= ym
            self.atoms[i].y = self.minus0(self.atoms[i].y)
            self.atoms[i].z -= zm
            self.atoms[i].z = self.minus0(self.atoms[i].z)

    def minus0(self, fl):
        res = fl

        #if math.fabs(fl) < 1e-8:
        #    print("!")
        #    res = 0
        #if str(fl) == "-0.0":
        #    res = 0
        #    print("!!")
        if fl < 0:
            res = 0

        return res

    def grow(self):
        """ модель транслируется в трех измерениях и становится в 27 раз больше """
        newAtList = deepcopy(self.atoms)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    if abs(i)+abs(j)+abs(k) != 0:
                        vect = i * self.LatVect1 + j * self.LatVect2 + k * self.LatVect3
                        copyOfModel = TAtomicModel(self.atoms)
                        copyOfModel.move(vect[0], vect[1], vect[2])
                        for atom in copyOfModel.atoms:
                            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        newModel.set_lat_vectors(3 * self.LatVect1, 3 * self.LatVect2, 3 * self.LatVect3)
        return newModel

    def growX(self):
        """ translate model in X direction """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect1
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        newModel.set_lat_vectors(2 * self.LatVect1, self.LatVect2, self.LatVect3)
        return newModel

    def growY(self):
        """ translate model in Y direction """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect2
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        newModel.set_lat_vectors(self.LatVect1, 2 * self.LatVect2, self.LatVect3)
        return newModel

    def growZ(self):
        """ translate model in Z direction """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect3
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        newModel.set_lat_vectors(self.LatVect1, self.LatVect2, 2 * self.LatVect3)
        return newModel
        
    def move(self, Lx, Ly, Lz):
        """ move model by the vector """
        for atom in self.atoms:
            atom.x += Lx
            atom.y += Ly
            atom.z += Lz

        for point in self.bcp:
            point.x += Lx
            point.y += Ly
            point.z += Lz

            self.move_bond_path(Lx, Ly, Lz, point.getProperty("bond1"))
            self.move_bond_path(Lx, Ly, Lz, point.getProperty("bond2"))

            self.move_bond_path(Lx, Ly, Lz, point.getProperty("bond1opt"))
            self.move_bond_path(Lx, Ly, Lz, point.getProperty("bond2opt"))
        return self.atoms

    def move_bond_path(self, Lx, Ly, Lz, bond):
        if bond:
            for bp in bond:
                bp.x += Lx
                bp.y += Ly
                bp.z += Lz

    def typesOfAtoms(self):
        elements = np.zeros((200))
        for atom in self.atoms:
            elements[atom.charge] += 1
        types = []
        for i in range(0, 200):
            if elements[i] > 0:
                types.append([i, elements[i]])
        return types

    def formula(self):
        mendeley = TPeriodTable()
        text = ""
        charges = self.typesOfAtoms()
        for charge in charges:
            ind = self.indexes_of_atoms_with_charge(charge[0])
            let = mendeley.get_let(self.atoms[ind[0]].charge)
            text += let + str(len(ind))
        return text
    
    def toSIESTAfdf(self, filename):
        """ созадет входной файл для пакета SIESTA """
        f = open(filename, 'w')
        text = self.toSIESTAfdfdata("Fractional", "Ang", "LatticeVectors")
        print(text, file=f)
        f.close()
        
    def toSIESTAxyz(self, filename):
        """ созадет xyz файл, совместимый с XMol """
        f = open(filename, 'w')
        text = self.toSIESTAxyzdata()
        print(text, file=f)
        f.close()     

    def toSIESTAfdfdata(self, coord_style, units_type,  latt_style='LatticeParameters'):
        """ returns data for SIESTA fdf file """
        data = ""
        PerTab = TPeriodTable()
        data += 'NumberOfAtoms ' + str(len(self.atoms)) + "\n"
        types = self.typesOfAtoms()
        data += 'NumberOfSpecies ' + str(len(types)) + "\n"
        data += '%block ChemicalSpeciesLabel\n'
        for i in range(0, len(types)):
            data += ' ' + str(i + 1) + '  ' + str(types[i][0]) + '  ' + str(PerTab.get_let(int(types[i][0]))) + "\n"
        data += '%endblock ChemicalSpeciesLabel\n'

        mult = 1
        LatticeConstant = 'LatticeConstant       1.0 Ang\n'

        if (coord_style != "Zmatrix Cartesian") and (units_type == "Bohr"):
            mult = 1.0 / 0.52917720859
            LatticeConstant = 'LatticeConstant       1.0 Bohr\n'

        data += LatticeConstant

        if latt_style == 'LatticeParameters':
            data += '%block LatticeParameters\n'
            data += '  ' + str(self.get_LatVect1_norm() * mult) + '  ' + str(self.get_LatVect2_norm() * mult) + '  ' + \
                    str(self.get_LatVect3_norm() * mult) + '  ' +str(self.get_angle_alpha()) +'  ' + \
                    str(self.get_angle_beta()) + '  ' +  str(self.get_angle_gamma()) +   '\n'
            data += '%endblock LatticeParameters\n'
        #or
        if latt_style == 'LatticeVectors':
            data += '%block LatticeVectors\n'
            data += '  ' + str(self.LatVect1[0] * mult) + '  ' + str(self.LatVect1[1] * mult) + '  ' + str(self.LatVect1[2] * mult) + '\n'
            data += '  ' + str(self.LatVect2[0] * mult) + '  ' + str(self.LatVect2[1] * mult) + '  ' + str(self.LatVect2[2] * mult) + '\n'
            data += '  ' + str(self.LatVect3[0] * mult) + '  ' + str(self.LatVect3[1] * mult) + '  ' + str(self.LatVect3[2] * mult) + '\n'
            data += '%endblock LatticeVectors\n'

        if coord_style == "Zmatrix Cartesian":
            data += 'AtomicCoordinatesFormat NotScaledCartesianAng\n'
            data += '%block Zmatrix\n'
            data += 'cartesian\n'
            data += self.coords_for_export(coord_style)
            data += '%endblock Zmatrix\n'

        if coord_style == "Fractional":
            self.sort_atoms_by_type()
            self.GoToPositiveCoordinates()
            self.convert_from_cart_to_direct()
            data += 'AtomicCoordinatesFormat Fractional\n'
            data += '%block AtomicCoordinatesAndAtomicSpecies\n'
            data += self.coords_for_export(coord_style)
            data += '%endblock AtomicCoordinatesAndAtomicSpecies\n'

        if coord_style == "Cartesian":
            self.sort_atoms_by_type()
            data += 'AtomicCoordinatesFormat ' + units_type + '\n'
            data += '%block AtomicCoordinatesAndAtomicSpecies\n'
            data += self.coords_for_export(coord_style, units_type)
            data += '%endblock AtomicCoordinatesAndAtomicSpecies\n'

        return data

    def toCUBEfile(self, fname, volumeric_data, x1, x2, y1, y2, z1, z2):
        f = open(fname+".cube", 'w')
        text = "DATA.cube\n"
        text += "DATA.cube\n"
        mult = 0.52917720859

        n_x = x2 - x1
        n_y = y2 - y1
        n_z = z2 - z1

        multx = mult * volumeric_data.Nx
        multy = mult * volumeric_data.Ny
        multz = mult * volumeric_data.Nz

        print("self.LatVect1 ", self.LatVect1)
        print("self.LatVect2 ", self.LatVect2)
        print("self.LatVect3 ", self.LatVect3)
        print("volumeric_data.origin_to_export ", volumeric_data.origin_to_export)
        print("add ", x1 * self.LatVect1/multx + y1 * self.LatVect2/multy + z1 * self.LatVect3/multz)

        origin = volumeric_data.origin_to_export + x1 * self.LatVect1/multx + y1 * self.LatVect2/multy + z1 * self.LatVect3/multz

        text += str(self.nAtoms())+"     " + str(origin[0]) + "    " + str(origin[1]) + "    " + str(origin[2]) + "\n"
        text += " " + str(n_x) + " "
        text += " " + str(self.LatVect1[0]/multx) + "   " + str(self.LatVect1[1]/multx) + "   " + str(self.LatVect1[2]/multx) + "\n"
        text += " " + str(n_y) + " "
        text += " " + str(self.LatVect2[0]/multy) + "   " + str(self.LatVect2[1]/multy) + "   " + str(self.LatVect2[2]/multy) + "\n"
        text += " " + str(n_z) + " "
        text += " " + str(self.LatVect3[0]/multz) + "   " + str(self.LatVect3[1]/multz) + "   " + str(self.LatVect3[2]/multz) + "\n"

        for atom in self.atoms:
            text += " " + str(atom.charge) + "     0.000000     " + str(atom.x/mult) + "    " + str(atom.y/mult) + "    " + str(atom.z/mult) + "\n"

        orderData = 'C'

        new_data = volumeric_data.data3D[x1:x2, y1:y2, z1:z2]
        new_n = new_data.size
        data3D = np.reshape(new_data, new_n, orderData)

        #n = int(volumeric_data.Nx) * int(volumeric_data.Ny) * int(volumeric_data.Nz)
        #data3D = np.reshape(volumeric_data.data3D, int(n), orderData)

        for i in range(0, data3D.size):
            text += str(data3D[i]) + "   "

        print(text, file=f)
        f.close()

    def toXSFfile(self, fname, volumeric_data, x1, x2, y1, y2, z1, z2):
        print("This is all DATA")
        f = open(fname+".XSF", 'w')
        text = "ATOMS\n"
        for atom in self.atoms:
            text += " " + str(atom.charge) + "    " + str(atom.x) + "    " + str(atom.y) + "    " + str(atom.z) + "\n"

        text += "BEGIN_BLOCK_DATAGRID_3D\n "
        text += "  DATA_from:GUI4DFT_diff\n"
        text += "  BEGIN_DATAGRID_3D_RHO:spin_1\n"
        text += " " + str(x2 - x1) + " " + str(y2 - y1) + " " + str(z2 - z1) + "\n"
        origin = volumeric_data.origin_to_export
        text += " " + str(origin[0]) + " " + str(origin[1]) + " " + str(origin[2]) + "\n"

        vector1 = self.LatVect1 * (x2 - x1) / volumeric_data.Nx
        vector2 = self.LatVect2 * (y2 - y1) / volumeric_data.Ny
        vector3 = self.LatVect3 * (z2 - z1) / volumeric_data.Nz

        text += " " + str(vector1[0]) + "   " + str(vector1[1]) + "   " + str(vector1[2]) + "\n"
        text += " " + str(vector2[0]) + "   " + str(vector2[1]) + "   " + str(vector2[2]) + "\n"
        text += " " + str(vector3[0]) + "   " + str(vector3[1]) + "   " + str(vector3[2]) + "\n"

        orderData = 'F'

        new_data = volumeric_data.data3D[x1:x2, y1:y2, z1:z2]
        new_n = new_data.size
        data3D = np.reshape(new_data, new_n, orderData)

        #n = int(volumeric_data.Nx) * int(volumeric_data.Ny) * int(volumeric_data.Nz)
        #data3D = np.reshape(volumeric_data.data3D, int(n), orderData)

        for i in range(0, data3D.size):
            text += str(data3D[i]) + "   "

        text += "\n"

        text += " END_DATAGRID_3D\n"
        text += "END_BLOCK_DATAGRID_3D\n"
        print(text, file=f)
        f.close()

    def coords_for_export(self, coord_style, units="Ang"):
        data = ""
        types = self.typesOfAtoms()
        if coord_style == "Cartesian":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                data += self.xyz_string(i, units) + str1 + "\n"

        if coord_style == "Fractional":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                data += self.xyz_string(i) + str1 + "\n"

        if coord_style == "FractionalPOSCAR":
            for i in range(0, len(self.atoms)):
                data += ' ' + self.xyz_string(i) + "\n"

        if coord_style == "Zmatrix Cartesian":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j+1)
                str2 = '    ' + self.xyz_string(i)
                str3 = '      1  1  1'
                data += str1+str2+str3+"\n"

        if coord_style == "FireflyINP":
            for i in range(0, len(self.atoms)):
                str1 = ' ' + str(self.atoms[i].let) + '   ' + str(self.atoms[i].charge) + '.0  '
                str2 = '    ' + self.xyz_string(i)
                data += str1+str2+"\n"
            data += ' $END'
        return data

    def xyz_string(self, i, units="Ang"):
        mult = 1.0
        if units == "Bohr":
            mult = 1.0 / 0.52917720859
        sx = helpers.float_to_string(self.atoms[i].x * mult)
        sy = helpers.float_to_string(self.atoms[i].y * mult)
        sz = helpers.float_to_string(self.atoms[i].z * mult)
        str2 = '  ' + sx + '  ' + sy + '  ' + sz
        return str2

    def toCriticXYZfile(self, cps):
        """ returns data for *.xyz file with CP and BCP """
        text = ""

        n_atoms = self.nAtoms()
        for i in range(0, n_atoms):
            text += self.atoms[i].to_string() + "\n"

        n_cp = len(cps)
        for cp in cps:
            text += cp.to_string() + "\n"

        n_bcp = 0
        for cp in cps:
            bond1 = cp.getProperty("bond1")
            bond2 = cp.getProperty("bond2")

            for i in range(0, len(bond1)):
                n_bcp += 1
                text += bond1[i].to_string() + "\n"

            for i in range(0, len(bond2)):
                n_bcp += 1
                text += bond2[i].to_string() + "\n"

        header = "   " + str(n_atoms + n_cp + n_bcp) + "\n\n"
        return header + text

    def toSIESTAxyzdata(self):
        """ returns data for *.xyz file """
        data = "  "
        nAtoms = self.nAtoms()
        data += str(nAtoms) + "\n"
        for i in range(0, nAtoms):
            data += "\n" + self.atoms[i].let + '       ' + self.xyz_string(i)
        return data

    def toFireflyINP(self, filename):
        """ create file in Firefly *.inp format """
        f = open(filename, 'w')
        data = ""
        data += "!model \n $DATA\njob\nCn 1\n\n"
        data += self.coords_for_export("FireflyINP")

        print(data, file=f)
        f.close()

    def toVASPposcar(self, filename):
        """ create file in VASP POSCAR format """
        f = open(filename, 'w')

        data = ""
        data += "model \n"
        data +=' 1.0 \n'

        data += '  ' + str(self.LatVect1[0]) + '  ' + str(self.LatVect1[1]) + '  ' + str(self.LatVect1[2]) + '\n'
        data += '  ' + str(self.LatVect2[0]) + '  ' + str(self.LatVect2[1]) + '  ' + str(self.LatVect2[2]) + '\n'
        data += '  ' + str(self.LatVect3[0]) + '  ' + str(self.LatVect3[1]) + '  ' + str(self.LatVect3[2]) + '\n'

        PerTab = TPeriodTable()

        types = self.typesOfAtoms()
        for i in range(0, len(types)):
            data += ' ' +  str(PerTab.get_let(int(types[i][0])))
        data += "\n"

        for i in range(0, len(types)):
            count = 0
            for atom in self.atoms:
                if atom.charge == int(types[i][0]):
                    count+=1
            data += ' ' +  str(count)
        data += "\n"

        data += "Direct\n"

        self.sort_atoms_by_type()
        self.GoToPositiveCoordinates()
        self.convert_from_cart_to_direct()
        data += self.coords_for_export("FractionalPOSCAR")

        print(data, file=f)
        f.close()
