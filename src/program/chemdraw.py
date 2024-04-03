# -*- coding: utf-8 -*-
# Python 3
from typing import List
import copy
import math
import os
import re
from datetime import date
from copy import deepcopy

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm

from core_atomistic import helpers
from core_atomistic.periodic_table import TPeriodTable
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from scipy.spatial.distance import cdist
from scipy.optimize import fmin
import scipy


def model_from_ct(name) -> AtomicModel:
    """Get atoms with bonds from ct file."""
    data = open(name, 'r')
    data.readline()
    row1 = data.readline().split()
    n_atoms = int(row1[0])
    n_bonds = int(row1[1])
    atoms = []
    mendeley = TPeriodTable()
    new_model = AtomicModel()
    for i1 in range(0, n_atoms):
        row = data.readline()
        str1 = helpers.spacedel(row)
        s = str1.split(' ')
        xyz = np.array([float(s[0]), float(s[1]), float(s[2])], dtype=np.float32)
        let = s[3]
        charge = mendeley.get_charge_by_letter(let)
        new_model.add_atom_with_data(xyz, charge)

    bonds = []
    for j1 in range(n_bonds):
        row = data.readline()
        str1 = helpers.spacedel(row)
        s = str1.split(' ')
        new_model.add_bond([int(s[0]) - 1, int(s[1]) - 1])
    new_model.set_lat_vectors_default()
    new_model.dynamic_bonds = False
    return [new_model]