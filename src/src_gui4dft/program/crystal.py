# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
from core_gui_atomistic import helpers
from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel


def model_1d_to_d12(model):
    text = "crystal\n"
    text += "POLYMER\n"
    model1 = deepcopy(model)
    model2 = deepcopy(model)
    model2.convert_from_cart_to_direct()
    nat = model1.n_atoms()
    text += "1\n"
    text += str(np.linalg.norm(model1.lat_vector3)) + "\n"
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
    text += str(np.linalg.norm(model1.lat_vector1)) + " " + str(np.linalg.norm(model1.lat_vector2)) + " 90.0\n"
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model1.atoms[i].charge
        x = str(model2.atoms[i].x)
        y = str(model2.atoms[i].y)
        z = str(model1.atoms[i].z)
        text += str(ch) + "   " + x + "   " + y + "   " + z + "\n"
    return text


def structure_of_primitive_cell(f_name):
    models = []
    f = open(f_name)
    str1 = f.readline()
    while str1:
        if str1.find("DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)") >= 0:
            str1 = f.readline()
            vec1 = np.array(f.readline().split(), dtype=float)
            vec2 = np.array(f.readline().split(), dtype=float)
            vec3 = np.array(f.readline().split(), dtype=float)
            for i in range(6):
                str1 = f.readline()
            model = AtomicModel()
            str1 = helpers.spacedel(f.readline())
            while len(str1) > 5:
                s = str1.split(' ')
                x = float(s[3])
                y = float(s[4])
                z = float(s[5])
                charge = int(s[1])
                let = s[2]
                model.add_atom(Atom([x, y, z, let, charge]))
                str1 = helpers.spacedel(f.readline())
            model.set_lat_vectors(vec1, vec2, vec3)
            models.append(model)
        str1 = f.readline()
    f.close()
    return models
