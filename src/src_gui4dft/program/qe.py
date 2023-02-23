# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
from core_gui_atomistic import helpers
from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel


def vectors_from_pwout(f_name):
    vectors = np.eye(3, dtype=float)
    f = open(f_name)
    str1 = f.readline()

    while str1:
        """ cell
            celldm(1)=  10.200000  celldm(2)=   0.000000  celldm(3)=   0.000000
            celldm(4)=   0.000000  celldm(5)=   0.000000  celldm(6)=   0.000000

            crystal axes: (cart. coord. in units of alat)
                       a(1) = (  -0.500000   0.000000   0.500000 )  
                       a(2) = (   0.000000   0.500000   0.500000 )  
                       a(3) = (  -0.500000   0.500000   0.000000 ) 
            """
        if str1.find("celldm(1)=") >= 0:
            params = str1.split()
            a = float(params[1])
            print(a)
            str1 = f.readline()


    str1 = f.readline()
    f.close()
    return vectors


def atoms_from_pwout(f_name):
    print("PW out")
    models = []
    f = open(f_name)
    str1 = f.readline()
    while str1:
        if str1.find("Crystallographic axes") >= 0:
            str1 = f.readline()

    """ atoms
    Crystallographic axes

    site n.     atom                  positions (cryst. coord.)
         1           Si  tau(   1) = (  0.0000000  0.0000000  0.0000000  )
         2           Si  tau(   2) = ( -0.2500000  0.7500000 -0.2500000  )
    """
    while str1:
        if str1.find("DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)") >= 0:
            str1 = f.readline()
            vec1 = np.array(f.readline().split(), dtype=float)
            vec2 = np.array(f.readline().split(), dtype=float)
            vec3 = np.array(f.readline().split(), dtype=float)
            for i in range(6):
                f.readline()
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
