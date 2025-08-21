# -*- coding: utf-8 -*-
from typing import List
import copy
import os
import numpy as np
from core_atomistic import helpers
from core_atomistic.periodic_table import TPeriodTable
from core_atomistic.atom import Atom
from src_critplot.models.cp import CriticalPoint
from src_critplot.models.cp_model import AtomicModelCP


class TopondModelCP(AtomicModelCP):
    def __init__(self, filename, is_add_translations=False):
        """Import lattice and positions from TOPOND output."""
        super().__init__()
        self.cps: List[CriticalPoint] = []
        self.model_type = "topond"

        if os.path.exists(filename):
            lat_vectors = self.get_cell(filename)
            self.add_atoms(filename)
            if lat_vectors is not None:
                self.set_lat_vectors([lat_vectors[0], lat_vectors[1], lat_vectors[2]])
            else:
                self.set_lat_vectors_default()
            self.parse_cp_data(filename, is_add_translations)

    def add_atoms(self, filename):
        """Atoms positions."""
        period_table = TPeriodTable()
        if os.path.exists(filename):
            number_of_atoms = self.number_of_atoms_from_outp(filename)
            file1 = open(filename)
            row = file1.readline()
            while row and (row.find("ATOM N.AT.  SHELL    X(A)      Y(A)      Z(A)      EXAD       N.ELECT.") < 0):
                row = file1.readline()
            if row:
                file1.readline()
                for n in range(number_of_atoms):
                    data = file1.readline().split()
                    charge = period_table.get_charge_by_letter(data[2])
                    self.add_atom(Atom([float(data[4]), float(data[5]), float(data[6]), data[2], charge]))

    def parse_cp_data(self, filename: str, is_add_translations=False):
        """Get critical points data."""
        if os.path.exists(filename):
            file1 = open(filename)
            row = file1.readline()
            while row:
                while row and (row.find("CP N.") < 0):
                    row = file1.readline()
                if (not row) or (row.find("CP N.  X") >= 0):
                    return
                title = row.split("CP N.")[1].split()[0]
                n_brackets = row.count("(")
                row = row.replace("(", "")
                row = row.replace(")", "")
                row1 = row.split()

                row1.insert(10, "(")
                if n_brackets == 1:
                    row1.insert(11, "0")
                    row1.insert(12, "0")
                    row1.insert(13, "0")
                row1.insert(14, ")")

                file1.readline()
                file1.readline()
                data1 = file1.readline().split(":")
                data = helpers.spacedel(data1[1])

                if data == "(3,-1)":
                    """
                    variant # 1
                    CP N.      8  NON-EQUIV. ATOM      3 C  ---    199 H (     1      1      0 )  DISTANCE(ANG)= 1.0859
                    *********

                    CP TYPE                        :  (3,-1)
                    COORD(AU)  (X  Y  Z)           :  1.8343E+00  7.5829E+00  2.5685E+01
                    COORD FRACT. CONV. CELL        :  3.5525E-02  1.4686E-01  4.9744E-01
                    PROPERTIES (RHO,GRHO,LAP)      :  2.7486E-01  1.2022E-15 -8.2652E-01
                    KINETIC ENERGY DENSITIES (G,K) :  3.7054E-02  2.4369E-01
                    VIRIAL DENSITY                 : -2.8074E-01
                    ELF(PAA)                       :  9.8781E-01

                    variant # 2                
                    CP N.      3
                    *********

                    CP TYPE                        :  (3,-1)
                    COORD(AU)  (X  Y  Z)           : -2.5571E-16 -4.5448E+00 -4.5448E+00
                    COORD FRACT. CONV. CELL        : -2.8133E-17  5.0000E-01  5.0000E-01
                    PROPERTIES (RHO,GRHO,LAP)      :  1.6510E-03  2.5625E-19  8.5997E-03   

                    variant # 3
                    CP N.      1  NON-EQUIV. ATOM      1 SI ---      2 O      DISTANCE (ANG)     1.687
                    *********

                    CP TYPE                        :  (3,-1)
                    COORD(AU)  (X  Y  Z)           :  1.9421E+00 -2.4949E-01  9.4204E+00
                    PROPERTIES (RHO,GRHO,LAP)      :  1.2029E-01  7.3282E-16  7.1917E-01                            
                    """
                    # print("bcp (3,-1) ----->")
                    text = "Type : (3,-1)\n"
                    cp_type = "(3,-1)"
                    title = "b" + title
                    let = "xb"
                    cp, row = self.parse_cp_point(file1, let, cp_type, text, title)
                    self.add_assotiated_atom_from_row(cp, row1)
                elif data == "(3,-3)":
                    """
                    CP N.      9
                    **********

                    ATTRACTOR CP TYPE              :  (3,-3)
                    COORD(AU)  (X  Y  Z)           :  2.2737E+00  7.4470E+00  2.6232E+01
                    COORD FRACT. CONV. CELL        :  4.4035E-02  1.4423E-01 -4.9195E-01
                    PROPERTIES (RHO,GRHO,LAP)      :  4.3196E-01  3.5396E-14 -2.1931E+01
                    TRAJECTORY LENGTH(ANG)         :  3.7842E-01
                    INTEGRATION STEPS              :      21
                    """
                    # print("nucleus (3,-3) ----->")
                    text = "Type : (3,-3)\n"
                    cp_type = "(3,-3)"
                    title = "A" + title
                    let = "nn"
                    cp, row = self.parse_cp_point(file1, let, cp_type, text, title)
                    self.add_critical_point(cp)
                elif data == "(3,+1)":
                    """ CP TYPE                        :  (3,+1) """
                    """
                    CP N.      7  NON-EQUIV. ATOM      2 O  ---     31 O (     0      0      0 )  DISTANCE(ANG)= 2.3736
                    *********

                    CP TYPE                        :  (3,+1)
                    COORD(AU)  (X  Y  Z)           : -1.7694E+00  1.7694E+00 -2.4047E+01
                    COORD FRACT. CONV. CELL        : -3.4268E-02  3.4268E-02 -4.6573E-01
                    PROPERTIES (RHO,GRHO,LAP)      :  2.7570E-02  1.4387E-16  1.3993E-01
                    KINETIC ENERGY DENSITIES (G,K) :  3.4069E-02 -9.1500E-04
                    VIRIAL DENSITY                 : -3.3154E-02
                    ELF(PAA)                       :  4.3030E-02
                    """
                    # print("ring (3,+1) ----->")
                    text = "Type : (3,+1)\n"
                    cp_type = "(3,+1)"
                    title = "r" + title
                    let = "xr"
                    cp, row = self.parse_cp_point(file1, let, cp_type, text, title)
                    self.add_assotiated_atom_from_row(cp, row1)
                elif data == "(3,+3)":
                    """ CP TYPE                        :  (3,+3) """
                    # print("cage (3,+3) ----->")
                    text = "Type : (3,+3)\n"
                    cp_type = "(3,+3)"
                    title = "c" + title
                    let = "xc"
                    cp, row = self.parse_cp_point(file1, let, cp_type, text, title)
                    self.add_critical_point(cp)
                elif data == "DEGENE":
                    """ CP TYPE                        :  DEGENE """
                    text = "Type : DEGENE\n"
                    cp_type = "DEGENE"
                    title = "d" + title
                    let = "dg"
                    cp, row = self.parse_cp_point(file1, let, cp_type, text, title)
                    self.add_critical_point(cp)
                else:
                    row = file1.readline()
                while (row.find("NUMBER OF UNIQUE CRI. POINT FOUND") < 0) and \
                        (row.find("NUMBER OF CRITICAL POINTS FOUND") < 0) and (row.find("CP N.") < 0):
                    row = file1.readline()
                if ((row.find("NUMBER OF UNIQUE CRI. POINT FOUND") > 0) or
                        (row.find("NUMBER OF CRITICAL POINTS FOUND") > 0)):
                    """ correction """
                    n_cp = int(helpers.spacedel(row.split(":")[1]))
                    row = file1.readline()
                    while len(row) < 10:
                        row = file1.readline()
                    row = file1.readline()
                    while len(row) < 10:
                        row = file1.readline()
                    """CP N.  X(AU)   Y(AU)   Z(AU)   TYPE      RHO    LAPL   L1(V1) L2(V2) L3(V3) ELLIP"""
                    while row.find("*************************************") < 0:
                        row = file1.readline()
                    for i in range(n_cp):
                        file1.readline()
                        row1 = file1.readline()
                        if len(row1) < 2:
                            row1 = file1.readline().split()
                            row2 = file1.readline().split()
                            atom1, atom2 = int(row1[2]), int(row2[2])
                            b_len = round((float(row1[6]) + float(row2[6])) * 0.52917720859, 4)
                            cp = self.cps[i]

                            if (atom1 is not None) and (atom2 is not None):
                                is_atom1_cor = (atom1 > 0) and (atom1 <= len(self.atoms))
                                if is_atom1_cor and (atom2 > 0) and (atom2 <= len(self.atoms)):
                                    correction = "-"
                                    atom1_old = cp.get_property("atom1")
                                    atom2_old = cp.get_property("atom2")
                                    text_new = cp.get_property("text")
                                    f1 = (atom1_old == atom1) and (atom2_old == atom2)
                                    if not (f1 or (atom1_old == atom2) and (atom2_old == atom1)):
                                        cp.set_property("atom1", atom1)
                                        cp.set_property("atom2", atom2)
                                        translation1 = np.zeros(3)
                                        translation2 = np.zeros(3)
                                        if len(row1) > 9:
                                            translation1 = int(row1[3]) * self.lat_vector1 + \
                                                           int(row1[4]) * self.lat_vector2 + \
                                                           int(row1[5]) * self.lat_vector3
                                        if len(row2) > 9:
                                            translation2 = int(row2[3]) * self.lat_vector1 + \
                                                           int(row2[4]) * self.lat_vector2 + \
                                                           int(row2[5]) * self.lat_vector3
                                        cp.set_property("atom1_translation", translation1)
                                        cp.set_property("atom2_translation", translation2)

                                        let1 = "None"
                                        let2 = "None"
                                        dist_line = "None"
                                        if atom1_old is not None:
                                            let1 = self.atoms[atom1_old - 1].let + str(atom1_old)
                                        if atom2_old is not None:
                                            let2 = self.atoms[atom2_old - 1].let + str(atom2_old)
                                        if (atom1_old is not None) and (atom2_old is not None):
                                            dist_line = round(self.atom_atom_distance(atom1_old - 1, atom2_old - 1), 4)
                                        let1n = self.atoms[atom1 - 1].let + str(atom1)
                                        let2n = self.atoms[atom2 - 1].let + str(atom2)
                                        correction = "(" + let1 + "-" + let2 + ")r=" + str(dist_line) + "->(" + \
                                                     let1n + "-" + let2n + ")" + "r=" + str(b_len)
                                    text_new += "\ncorrections : " + correction
                                    cp.set_property("text", text_new)
                                else:
                                    print("strange critical point: ", cp.to_string())
                            for j in range(3):
                                file1.readline()

                        else:
                            for j in range(4):
                                file1.readline()
                    row = ""

            for cp in self.cps:
                ind1 = cp.get_property("atom1")
                ind2 = cp.get_property("atom2")
                if (ind1 is not None) and (ind2 is not None):
                    trans1 = np.array(cp.get_property("atom1_translation"))
                    trans2 = np.array(cp.get_property("atom2_translation"))
                    p1 = CriticalPoint([self.atoms[ind1 - 1].xyz + trans1, "xz", "bp"])
                    p2 = CriticalPoint([cp.xyz, "xz", "bp"])
                    p3 = CriticalPoint([self.atoms[ind2 - 1].xyz + trans2, "xz", "bp"])
                    if is_add_translations:
                        if np.linalg.norm(trans1) > 0:
                            atom = copy.deepcopy(self.atoms[ind1 - 1])
                            atom.xyz += trans1
                            atom.tag = "translated"
                            self.add_atom(atom, min_dist=-0.01)
                        if np.linalg.norm(trans2) > 0:
                            atom = copy.deepcopy(self.atoms[ind2 - 1])
                            atom.xyz += trans2
                            atom.tag = "translated"
                            self.add_atom(atom, min_dist=-0.01)
                    self.add_bond_path_point([p2, p1])
                    self.add_bond_path_point([p2, p3])
                    atom_to_atom = self.atoms[ind1 - 1].let + str(ind1) + "-" + self.atoms[ind2 - 1].let + str(ind2)
                    cp.set_property("atom_to_atom", atom_to_atom)
                    bond_len = np.linalg.norm(self.atoms[ind2 - 1].xyz + trans2 - self.atoms[ind1 - 1].xyz - trans1)
                    cp.set_property("cp_bp_len", bond_len)
            self.bond_path_points_optimize()

    def add_assotiated_atom_from_row(self, cp, row1):
        if len(row1) > 8:
            if (row1[5] is not None) and (row1[8] is not None):
                self.add_associated_atoms(cp, row1)
        self.add_critical_point(cp)

    def add_associated_atoms(self, cp, row1):
        ind1, ind2 = int(row1[5]), int(row1[8])
        cp.set_property("atom1", ind1)
        cp.set_property("atom2", ind2)
        translation1 = np.zeros(3, dtype=float)
        translation2 = int(row1[11]) * self.lat_vector1 + int(row1[12]) * self.lat_vector2 + \
                       int(row1[13]) * self.lat_vector3
        cp.set_property("atom1_translation", translation1)
        cp.set_property("atom2_translation", translation2)

    @staticmethod
    def get_cell(filename):
        """Lattice vectors."""
        if os.path.exists(filename):
            k = -1
            out = 0
            with open(filename, "r") as file1:
                lat_vectors = 500 * np.eye(3)
                for line in file1:
                    if k >= 0:
                        data = line.split()
                        if len(data) == 3:
                            lat_vectors[3 - k] = np.array(data)
                        k -= 1
                    if line.find("DIRECT LATTICE VECTOR COMPONENTS (ANGSTROM)") >= 0:
                        k = 3
                        out = 1
                    if (k == 0) and (out == 1):
                        return lat_vectors
        return None

    @staticmethod
    def number_of_atoms_from_outp(filename):
        """Number of atoms in TOPOND output."""
        n_atoms = 0
        if os.path.exists(filename):
            result = helpers.from_file_property(filename, 'N. OF ATOMS PER CELL', prop_type='string')
            n_atoms = int(result.split()[0])
        return n_atoms

    @staticmethod
    def parse_cp_point(file1, let, cp_type, text, title):
        row = file1.readline()
        text += helpers.spacedel(row) + "\n"
        """COORD(AU)  (X  Y  Z)           :  3.3821E+00  2.2164E+00 -3.7940E-16"""
        xyz = np.array(row.split(":")[1].split(), dtype=float) * 0.52917720859
        cp = CriticalPoint([xyz, let, cp_type])
        cp.set_property("title", title)
        tmp_row = file1.readline()
        if tmp_row.find("COORD FRACT.") >= 0:
            text += helpers.spacedel(tmp_row) + "\n"
            """COORD FRACT. CONV. CELL        :  2.5000E-01  2.5000E-01 -2.0484E-17"""
            tmp_row = file1.readline()
        row = helpers.spacedel(tmp_row) + "\n"
        """PROPERTIES (RHO,GRHO,LAP)      :  3.1585E-03  2.9929E-18  1.3881E-02"""
        data = row.split(":")[1].split()
        cp.set_property("rho", data[0])
        text += "rho : " + data[0] + "\n"
        cp.set_property("grad", data[1])
        text += "grad : " + data[1] + "\n"
        cp.set_property("lap", data[2])
        text += "lap : " + data[2] + "\n"
        row = file1.readline()
        if row.find("RHOA,SPIN DENSITY") >= 0:
            """RHOA,SPIN DENSITY                 :  1.0000E+00  0.0000E+00"""
            text += "RHOA : " + row.split()[3] + "\n"
            text += "SPIN DENSITY : " + row.split()[4] + "\n"
            row = file1.readline()
        if len(row) > 1:
            if let in ["xb", "xr", "xc"]:
                """KINETIC ENERGY DENSITIES (G,K) :  2.4448E-03 -1.0254E-03"""
                text += "KINETIC ENERGY DENSITIES (G) : " + row.split()[5] + "\n"
                text += "KINETIC ENERGY DENSITIES (K) : " + row.split()[6] + "\n"
                row = helpers.spacedel(file1.readline())
                """VIRIAL DENSITY                 : -1.4194E-03"""
                text += row + "\n"
                row = helpers.spacedel(file1.readline()) + "\n"
                """ELF(PAA)                       :  6.3365E-03"""
                text += helpers.spacedel(row) + "\n"
                if let == "xb":
                    for i in range(8):
                        file1.readline()
                    row = file1.readline()
                    """ELLIPTICITY                    :  1.4410E-01"""
                    text += helpers.spacedel(row)
            else:
                """TRAJECTORY LENGTH(ANG)         :  7.1474E-01"""
                text += helpers.spacedel(row) + "\n"
                row = helpers.spacedel(file1.readline()) + "\n"
                """INTEGRATION STEPS              :      67"""
                text += helpers.spacedel(row) + "\n"
        cp.set_property("text", text)
        return cp, row
