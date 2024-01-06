# -*- coding: utf-8 -*-
import re
import math
from copy import deepcopy
import numpy as np

from src_core_atomistic.atomic_model import AtomicModel
from src_core_atomistic import helpers


def n_atoms_from_struct(f_name):
    """
    Test_file_WIEN2k9.2_Fe54
    P   LATTICE,NONEQUIV. ATOMS108
    """
    f = open(f_name)
    f.readline()
    n = f.readline()
    n = re.findall('\d+', n)[-1]
    f.close()
    return int(n)


def alats_from_struct(f_name):
    """
    Test_file_WIEN2k9.2_Fe54
    P   LATTICE,NONEQUIV. ATOMS108
    MODE OF CALC=RELA unit=bohr
     32.220000 16.110000 16.110000 90.000000 90.000000 90.000000
    """
    f = open(f_name)
    f.readline()
    f.readline()
    f.readline()  # units
    units = "bohr"
    mult = 1.0
    if units == "bohr":
        mult = 0.52917720859
    str1 = f.readline().split()
    a = mult * float(str1[0])
    b = mult * float(str1[1])
    c = mult * float(str1[2])
    alp = math.radians(float(str1[3]))
    bet = math.radians(float(str1[4]))
    gam = math.radians(float(str1[5]))
    f.close()
    return a, b, c, alp, bet, gam


def atoms_from_struct(f_name):
    model = AtomicModel()
    n_atoms = n_atoms_from_struct(f_name)
    a, b, c, alp, bet, gam = alats_from_struct(f_name)
    lattice = helpers.lat_vectors_from_params(a, b, c, alp, bet, gam)
    model.set_lat_vectors(lattice[0], lattice[1], lattice[2])
    f = open(f_name)
    for i in range(5):
        str1 = f.readline()
    k = 0

    """                      
    ATOM  -1: X=0.00000000 Y=0.00000000 Z=0.00000000
          MULT= 1          ISPLIT= 8
    Fe         NPT=  781  R0=0.00005000 RMT=    2.0000   Z: 26.0                   
    LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000
                     0.0000000 1.0000000 0.0000000
                     0.0000000 0.0000000 1.0000000    
    """
    while (k < n_atoms) and str1:
        while (str1.find("ATOM") < 0) and str1:
            str1 = f.readline()
        coord = str1  # ATOM  -1: X=0.00000000 Y=0.00000000 Z=0.00000000
        atom_coords = re.findall('\d+.\d+', coord)
        xyz = np.array([float(atom_coords[-3]), float(atom_coords[-2]), float(atom_coords[-1])], dtype=float)
        f.readline()
        str1 = f.readline()  # Fe         NPT=  781  R0=0.00005000 RMT=    2.0000   Z: 26.0
        charge = float(str1.split("Z:")[1])
        model.add_atom_with_data(xyz, charge)
        k += 1
    model.convert_from_direct_to_cart()
    return [model]


def model_to_wien_struct(model: AtomicModel):
    n_atoms = model.n_atoms()
    text = "Model " + model.formula() + "\n"
    text += "P" + "{:29}".format(n_atoms) + "\n"
    text += "MODE OF CALC=RELA unit=bohr\n"
    a, b, c, al, bet, gam = model.cell_params()
    text += "{:10.6f}".format(a / 0.52917720859)
    text += "{:10.6f}".format(b / 0.52917720859)
    text += "{:10.6f}".format(c / 0.52917720859)
    text += "{:10.6f}".format(al)
    text += "{:10.6f}".format(bet)
    text += "{:10.6f}".format(gam) + '\n'

    model1 = deepcopy(model)
    model1.convert_from_cart_to_direct()
    for i in range(n_atoms):
        """
        ATOM  -1: X=0.00000000 Y=0.00000000 Z=0.00000000
                  MULT= 1          ISPLIT= 8
        Fe         NPT=  781  R0=0.00005000 RMT=    2.0000   Z: 26.0                   
        LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000
                             0.0000000 1.0000000 0.0000000
                             0.0000000 0.0000000 1.0000000
        """
        atom_text = "ATOM" + "{:4}".format(-i - 1) + ":"
        atom_text += " X=" + "{:10.8f}".format(model1[i].x)
        atom_text += " Y=" + "{:10.8f}".format(model1[i].y)
        atom_text += " Z=" + "{:10.08f}".format(model1[i].z) + "\n"
        atom_text += "          MULT= 1          ISPLIT= 8\n"
        atom_text += "{:2}".format(model1[i].let) + "         NPT=  781  R0=0.00005000 RMT=    2.0000   Z:"
        atom_text += "{:5.1f}".format(1.0 * model1[i].charge) + "\n"
        atom_text += "LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000\n"
        atom_text += "                     0.0000000 1.0000000 0.0000000\n"
        atom_text += "                     0.0000000 0.0000000 1.0000000\n"
        text += atom_text
    text += "   1      NUMBER OF SYMMETRY OPERATIONS\n"
    text += " 1 0 0 0.00000000\n"
    text += " 0 1 0 0.00000000\n"
    text += " 0 0 1 0.00000000\n"
    text += "   1\n\n"
    return text
