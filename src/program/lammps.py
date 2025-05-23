# -*- coding: utf-8 -*-
import numpy as np
from core_atomistic.atomic_model import AtomicModel


def model_to_lammps_input(model: AtomicModel, charge=False):
    """
     # Comment

        4577  atoms
           3  atom types

      0.000000000000      36.920000000000  xlo xhi
      0.000000000000      36.920000000000  ylo yhi
      0.000000000000      36.920000000000  zlo zhi

     Masses

            1   55.84500000             # Fe
            2   50.94150000             # V
            3   12.01100000             # C

     Atoms # atomic

         1    1       35.499999943200       4.260000170400      24.139999858000
         2    1        0.000000000000       5.679999858000      22.720000170400
         3    1       24.139999858000       4.260000170400      24.139999858000
         4    1       34.079999886400       2.840000113600      22.720000170400
         5    1        8.519999971600       5.679999858000      22.720000170400
         6    1        4.260000170400       7.099999914800      24.139999858000
         7    1        2.840000113600       5.679999858000      22.720000170400
    """

    text = "# Comment\n"
    n_atoms = model.n_atoms()
    text += "box          tilt large\n"
    text += "change_box   all triclinic\n"
    text += str(n_atoms) + " atoms\n"
    types = model.types_of_atoms()
    text += str(len(types)) + " atom types\n"
    a, b, c, al, bt, gm = model.cell_params()
    lx, ly, lz, xy, xz, yz = cellparams_to_lammps_cell(a, b, c, al, bt, gm)

    text += "0.000000000000      " + str(lx) + "  xlo xhi\n"
    text += "0.000000000000      " + str(ly) + "  ylo yhi\n"
    text += "0.000000000000      " + str(lz) + "  zlo zhi\n"
    text += str(round(xy, 12)) + " " + str(round(xz, 12)) + " " + str(round(yz, 12)) + " xy xz yz\n\n"

    text += "Masses\n\n"
    for i in range(len(types)):
        item = model.mendeley.Atoms[types[i][0]]
        text += str(i + 1) + " " + str(item.mass) + "  #" + item.let + "\n"

    text += "\nAtoms # atomic\n\n"
    charge_to_type, text1 = model.get_charge_to_type_array()

    ch = " 0.0 " if charge else ""
    for i in range(n_atoms):
        xyz_st = model[i].xyz_string
        text += str(i + 1) + "  " + str(charge_to_type[model[i].charge]) + ch + " " + xyz_st + "\n"
    return text


def cellparams_to_lammps_cell(a, b, c, al, bt, gm):
    lx = a
    xy = b * np.cos(gm * np.pi / 180)
    xz = c * np.cos(bt * np.pi / 180)
    ly = np.sqrt(b * b - xy * xy)
    yz = (b * c * np.cos(al * np.pi / 180) - xy * xz) / ly
    lz = np.sqrt(c * c - xz * xz - yz * yz)
    return lx, ly, lz, xy, xz, yz


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
