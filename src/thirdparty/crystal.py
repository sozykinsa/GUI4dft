# -*- coding: utf-8 -*-
import sys
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
