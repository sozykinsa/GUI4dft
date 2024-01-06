# -*- coding: utf-8 -*-
import numpy as np
from core_atomistic.atomic_model import AtomicModel


def atoms_trajectory_step(f_name):
    model = AtomicModel()
    n_atoms = 0
    vectors = np.eye(3, dtype=float)
    f = open(f_name)
    str1 = f.readline()

    while str1.find("ITEM:") >= 0:
        print(str1)
        if str1.find("TIMESTEP") >= 0:
            """ ITEM: TIMESTEP
                60
            """
            str1 = f.readline()
        if str1.find("NUMBER OF ATOMS") >= 0:
            """ ITEM: NUMBER OF ATOMS
                101
            """
            str1 = f.readline()
            n_atoms = int(str1)
            print("n_atoms ", n_atoms)
        if str1.find("BOX BOUNDS xy xz yz") >= 0:
            """ BOX BOUNDS xy xz yz pp pp pp
                -2.5087731568532379e-01 2.4742556201637154e+01 3.1858779527327193e-02
                -1.9912872452207075e-01 2.4711044698882301e+01 -5.1584195075493292e-02
                -9.8252636271176641e-02 1.2182513668271181e+01 2.0731030960224744e-02
                xlo_bound xhi_bound xy
                ylo_bound yhi_bound xz
                zlo_bound zhi_bound yz
            """
            str1 = f.readline()
            # a1_tmp = str1.split()
            # vectors[0] = np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)
            str1 = f.readline()
            # a2_tmp = str1.split()
            # vectors[1] = np.array([a2_tmp[0], a2_tmp[1], a2_tmp[2]], dtype=float)
            str1 = f.readline()
            # a3_tmp = str1.split()
            # vectors[2] = np.array([a3_tmp[0], a3_tmp[1], a3_tmp[2]], dtype=float)

        if str1.find("ITEM: ATOMS id type x y z fx fy fz") >= 0:
            """ ITEM: ATOMS id type x y z fx fy fz
                4 2 8.82271 11.9265 0.510165 0.672909 -0.0384503 0.37825
            """
            for i in range(n_atoms):
                str1 = f.readline()
                data = str1.split()
                xyz = np.array((data[2], data[3], data[4]), dtype=float)
                charge = int(data[1])
                tag = "type"
                model.add_atom_with_data(xyz, charge, tag)
                # print(str1)
            # model.set_lat_vectors(vectors[0], vectors[1], vectors[2])
        str1 = f.readline()
    f.close()
    return [model]
