# -*- coding: utf-8 -*-
import math
from copy import deepcopy
import numpy as np
from core_gui_atomistic import helpers
from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel


def parse_trajectory_step(f_name):
    n_atoms = 0
    vectors = np.eye(3, dtype=float)
    f = open(f_name)
    str1 = f.readline()

    while str1.find("ITEM:") >= 0:
        if str1.find("NUMBER OF ATOMS") >= 0:
            """ ITEM: NUMBER OF ATOMS
                101
            """
            str1 = f.readline()
            n_atoms = int(str1)
        if str1.find("BOX BOUNDS xy xz yz") >= 0:
            """ BOX BOUNDS xy xz yz pp pp pp
                -2.5087731568532379e-01 2.4742556201637154e+01 3.1858779527327193e-02
                -1.9912872452207075e-01 2.4711044698882301e+01 -5.1584195075493292e-02
                -9.8252636271176641e-02 1.2182513668271181e+01 2.0731030960224744e-02
            """
            str1 = f.readline()
            a1_tmp = str1.split()
            vectors[0] = np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)
            str1 = f.readline()
            a2_tmp = str1.split()
            vectors[1] = np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)
            str1 = f.readline()
            a3_tmp = str1.split()
            vectors[2] = np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)

        if str1.find("ITEM: ATOMS id type x y z fx fy fz") >= 0:
            """ ITEM: ATOMS id type x y z fx fy fz
                4 2 8.82271 11.9265 0.510165 0.672909 -0.0384503 0.37825
            """
            for i in range(n_atoms):
                str1 = f.readline()
                print(str1)
        str1 = f.readline()
    f.close()
    # return vectors
