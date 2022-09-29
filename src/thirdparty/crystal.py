# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
from utils import helpers
from utils.periodic_table import TPeriodTable
from models.atomic_model import TAtomicModel, Atom
from copy import deepcopy
sys.path.append('.')


def model_1d_to_d12(model):
    text = "crystal\n"
    text += "POLYMER\n"
    model1 = deepcopy(model)
    model2 = deepcopy(model)
    model2.convert_from_cart_to_direct()
    nat = model1.n_atoms()
    text += "1\n"
    text += str(model1.get_LatVect3_norm()) + "\n"
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model1.atoms[i].charge
        x = str(model2.atoms[i].z)
        y = str(model1.atoms[i].x)
        z = str(model1.atoms[i].y)
        text += str(ch) + "   " + x + "   " + y + "   " + z + "\n"
    return text


def model_2d_to_d12(model):
    text = "crystal\n"
    text += "SLAB\n"
    model1 = deepcopy(model)
    model2 = deepcopy(model)
    model2.convert_from_cart_to_direct()
    nat = model1.n_atoms()
    text += "1\n"
    text += str(model1.get_LatVect1_norm()) + " " + str(model1.get_LatVect2_norm()) + " 90.0\n"
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model1.atoms[i].charge
        x = str(model2.atoms[i].x)
        y = str(model2.atoms[i].y)
        z = str(model1.atoms[i].z)
        text += str(ch) + "   " + x + "   " + y + "   " + z + "\n"
    return text


def number_of_atoms_from_outp(filename):
    """Number of atoms in TOPOND output."""
    n_atoms = 0
    if os.path.exists(filename):
        result = helpers.from_file_property(filename, 'N. OF ATOMS PER CELL', prop_type='string')
        n_atoms = int(result.split()[0])
    return n_atoms


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
                        lat_vectors[3-k] = np.array(data)
                    k -= 1
                if line.find("DIRECT LATTICE VECTOR COMPONENTS (ANGSTROM)") >= 0:
                    k = 3
                    out = 1
                if (k == 0) and (out == 1):
                    return lat_vectors
    return None


def get_atoms(filename):
    """Atoms positions."""
    model = TAtomicModel()
    period_table = TPeriodTable()
    if os.path.exists(filename):
        number_of_atoms = number_of_atoms_from_outp(filename)
        file1 = open(filename)
        row = file1.readline()
        while row and (row.find("ATOM N.AT.  SHELL    X(A)      Y(A)      Z(A)      EXAD       N.ELECT.") < 0):
            row = file1.readline()
        if row:
            file1.readline()
            for n in range(number_of_atoms):
                data = file1.readline().split()
                charge = period_table.get_charge_by_letter(data[2])
                model.add_atom(Atom([float(data[4]), float(data[5]), float(data[6]), data[2], charge]))
    return model


def parse_cp_data(filename: str, model: TAtomicModel):
    """Get critical points data."""
    if os.path.exists(filename):
        file1 = open(filename)
        row = file1.readline()
        while row:
            while row and (row.find("CP N.") < 0):
                row = file1.readline()
            row1 = row.split()

            file1.readline()
            file1.readline()
            data1 = file1.readline().split(":")
            data = helpers.spacedel(data1[1])

            """CP TYPE                        :  (3,-1)"""
            if data == "(3,-1)":
                text = "Type : (3,-1)\n"
                row = file1.readline()
                text += helpers.spacedel(row) + "\n"
                """COORD(AU)  (X  Y  Z)           :  3.3821E+00  2.2164E+00 -3.7940E-16"""
                data = row.split(":")[1].split()
                x = float(data[0]) * 0.52917720859
                y = float(data[1]) * 0.52917720859
                z = float(data[2]) * 0.52917720859
                cp = Atom([x, y, z, "xb", 1])
                ind1, ind2 = int(row1[5]) - 1, int(row1[8]) - 1
                cp.setProperty("atom1", ind1)
                cp.setProperty("atom2", ind2)
                text += helpers.spacedel(file1.readline()) + "\n"
                """COORD FRACT. CONV. CELL        :  2.5000E-01  2.5000E-01 -2.0484E-17"""
                row = helpers.spacedel(file1.readline()) + "\n"
                """PROPERTIES (RHO,GRHO,LAP)      :  3.1585E-03  2.9929E-18  1.3881E-02"""
                data = row.split(":")[1].split()
                cp.setProperty("field", data[0])
                text += "field : " + data[0] + "\n"
                cp.setProperty("grad", data[1])
                text += "grad : " + data[1] + "\n"
                cp.setProperty("lap", data[2])
                text += "lap : " + data[2] + "\n"
                row = file1.readline()
                """KINETIC ENERGY DENSITIES (G,K) :  2.4448E-03 -1.0254E-03"""
                text += "KINETIC ENERGY DENSITIES (G) : " + row.split()[5] + "\n"
                text += "KINETIC ENERGY DENSITIES (K) : " + row.split()[6] + "\n"
                row = helpers.spacedel(file1.readline())
                """VIRIAL DENSITY                 : -1.4194E-03"""
                text += row + "\n"
                row = helpers.spacedel(file1.readline()) + "\n"
                """ELF(PAA)                       :  6.3365E-03"""
                text += helpers.spacedel(row) + "\n"
                for i in range(8):
                    file1.readline()
                row = file1.readline()
                """ELLIPTICITY                    :  1.4410E-01"""
                text += helpers.spacedel(row)

                cp.setProperty("text", text)

                ind1 = cp.getProperty("atom1")
                ind2 = cp.getProperty("atom2")
                p1 = Atom([*model.atoms[ind1].xyz, "xz", 1])
                p2 = Atom([*cp.xyz, "xz", 1])
                p3 = Atom([*model.atoms[ind2].xyz, "xz", 1])

                model.add_critical_point_bond(cp)
                model.add_bond_path_point([p2, p1])
                model.add_bond_path_point([p2, p3])
            else:
                row = file1.readline()
            while (row.find("NUMBER OF UNIQUE CRI. POINT FOUND") < 0) and (row.find("CP N.") < 0):
                row = file1.readline()
            if row.find("NUMBER OF UNIQUE CRI. POINT FOUND") > 0:
                row = ""
        model.bond_path_points_optimize()


def atomic_data_from_output(filename):
    """import lattice and positions from TOPOND output."""
    model = TAtomicModel()
    if os.path.exists(filename):
        lat_vectors = get_cell(filename)
        model = get_atoms(filename)
        model.set_lat_vectors(lat_vectors[0], lat_vectors[1], lat_vectors[2])
        parse_cp_data(filename, model)
    return [model]
