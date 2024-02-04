# -*- coding: utf-8 -*-
import os
from copy import deepcopy

import numpy as np

from core_atomistic.atomic_model import AtomicModel
from core_atomistic.periodic_table import TPeriodTable
from core_atomistic import helpers


def model_to_dftb_d0(model: AtomicModel):
    """
    3 C
    O H

    1 1  0.00000000000E+00 -0.10000000000E+01  0.00000000000E+00
    2 2  0.00000000000E+00  0.00000000000E+00  0.78306400000E+00
    3 2  0.00000000000E+00  0.00000000000E+00 -0.78306400000E+00
    """

    n_atoms = model.n_atoms()
    text = str(n_atoms) + " C\n"  # C - cluster
    model1 = deepcopy(model)
    model1.sort_atoms_by_type()
    types = model1.types_of_atoms()
    charge_to_type,text1 = model1.get_charge_to_type_array()
    text += text1 + "\n\n"

    for i in range(n_atoms):
        xyz_st = model1[i].xyz_string
        text += str(i + 1) + "  " + str(charge_to_type[model1[i].charge]) + " " + xyz_st + "\n"
    return text


def atoms_from_gen(filename):
    period_table = TPeriodTable()
    molecules = []
    if os.path.exists(filename):
        struct_file = open(filename)
        info = helpers.spacedel(struct_file.readline()).split()
        numbers_of_atoms = int(info[0])
        pbc_type = info[1]
        info = helpers.spacedel(struct_file.readline()).split()
        charges = []
        for t in info:
            charges.append(period_table.get_charge_by_letter(t))
        if pbc_type.lower() == "c":
            new_str = AtomicModel()
            i = 0
            while i < numbers_of_atoms:
                s = helpers.spacedel(struct_file.readline()).split(' ')
                if len(s) > 4:
                    i += 1
                    xyz = np.array((s[2], s[3], s[4]), dtype=float)
                    new_str.add_atom_with_data(xyz, charges[int(s[1]) - 1])
            molecules.append(new_str)
    return molecules
