# -*- coding: utf-8 -*-
import math
import os
import re
from copy import deepcopy
import numpy as np
from core_atomistic import helpers
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel


def vectors_from_pwout(f_name):
    """Lattice vectors from output file of PWscf.
    f_name: PWscf output file
    """
    vectors = np.eye(3, dtype=float)
    f = open(f_name)
    str1 = f.readline()

    while str1:
        if str1.find("celldm(1)=") >= 0:
            """ cell
            celldm(1)=  10.200000  celldm(2)=   0.000000  celldm(3)=   0.000000
            celldm(4)=   0.000000  celldm(5)=   0.000000  celldm(6)=   0.000000

            crystal axes: (cart. coord. in units of alat)
                a(1) = (  -0.500000   0.000000   0.500000 )  
                a(2) = (   0.000000   0.500000   0.500000 )  
                a(3) = (  -0.500000   0.500000   0.000000 ) 
            """
            params = str1.split()
            a = float(params[1]) * 0.52917720859
            b = float(params[3]) * 0.52917720859
            c = float(params[5]) * 0.52917720859
            # print(a, b, c)
            if (b == 0) and (c == 0):
                b = deepcopy(a)
                c = deepcopy(a)
            elif (b != 0) and (c == 0):
                c = deepcopy(b)
                b = deepcopy(a)
            # print(a, b, c)
            f.readline()
            f.readline()
            str1 = f.readline()
            if str1.find("crystal axes: (cart. coord. in units of alat)") >= 0:
                a1_tmp = f.readline().split()
                vectors[0] = a * np.array([a1_tmp[3], a1_tmp[4], a1_tmp[5]], dtype=float)
                a2_tmp = f.readline().split()
                vectors[1] = b * np.array([a2_tmp[3], a2_tmp[4], a2_tmp[5]], dtype=float)
                a3_tmp = f.readline().split()
                vectors[2] = c * np.array([a3_tmp[3], a3_tmp[4], a3_tmp[5]], dtype=float)
                # print(vectors)
                f.close()
                return vectors
        str1 = f.readline()
    f.close()
    return vectors


def alats_from_pwout(f_name):
    """Lattice parameters from output file of PWscf.
    f_name: PWscf output file
    """
    f = open(f_name)
    str1 = f.readline()

    while str1:
        """ cell
            celldm(1)=  10.200000  celldm(2)=   0.000000  celldm(3)=   0.000000
            celldm(4)=   0.000000  celldm(5)=   0.000000  celldm(6)=   0.000000
            """
        if str1.find("celldm(1)=") >= 0:
            params = str1.split()
            a = float(params[1]) * 0.52917720859
            b = float(params[3]) * 0.52917720859
            c = float(params[5]) * 0.52917720859
            # print(a, b, c)
            if (b == 0) and (c == 0):
                b = deepcopy(a)
                c = deepcopy(a)
            elif (b != 0) and (c == 0):
                c = deepcopy(b)
                b = deepcopy(a)
            # print(a, b, c)
            params = str1.split()
            alp = float(params[1])
            bet = float(params[3])
            gam = float(params[5])

            f.close()
            return a, b, c, alp, bet, gam
        str1 = f.readline()
    f.close()
    return 0, 0, 0, 0, 0, 0


def atoms_from_pwout(f_name):
    # print("PW out")
    models = []
    vectors = vectors_from_pwout(f_name)
    a, b, c, alp, bet, gam = alats_from_pwout(f_name)
    f = open(f_name)
    str1 = f.readline()
    while str1:

        if str1.find("celldm(1)=") >= 0:
            """ cell
            celldm(1)=  10.200000  celldm(2)=   0.000000  celldm(3)=   0.000000
            celldm(4)=   0.000000  celldm(5)=   0.000000  celldm(6)=   0.000000

            crystal axes: (cart. coord. in units of alat)
                a(1) = (  -0.500000   0.000000   0.500000 )  
                a(2) = (   0.000000   0.500000   0.500000 )  
                a(3) = (  -0.500000   0.500000   0.000000 ) 
            """
            params = str1.split()
            a = float(params[1]) * 0.52917720859
            b = float(params[3]) * 0.52917720859
            c = float(params[5]) * 0.52917720859
            # print(a, b, c)
            if (b == 0) and (c == 0):
                b = deepcopy(a)
                c = deepcopy(a)
            elif (b != 0) and (c == 0):
                c = deepcopy(b)
                b = deepcopy(a)
            # print(a, b, c)
            f.readline()
            f.readline()
            str1 = f.readline()
            if str1.find("crystal axes: (cart. coord. in units of alat)") >= 0:
                a1_tmp = f.readline().split()
                vectors[0] = a * np.array([a1_tmp[3], a1_tmp[4], a1_tmp[5]], dtype=float)
                a2_tmp = f.readline().split()
                vectors[1] = b * np.array([a2_tmp[3], a2_tmp[4], a2_tmp[5]], dtype=float)
                a3_tmp = f.readline().split()
                vectors[2] = c * np.array([a3_tmp[3], a3_tmp[4], a3_tmp[5]], dtype=float)

        if str1.find("CELL_PARAMETERS (angstrom)") >= 0:
            """ every vc-relax step
            CELL_PARAMETERS (angstrom)
            -2.717604706   0.006737812   2.717537544
            -0.005129402   2.719272750   2.719145955
            -2.720314497   2.720374130   0.004028022
            """
            # print("CELL_PARAMETERS (angstrom)")
            a1_tmp = f.readline().split()
            vectors[0] = np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)
            a2_tmp = f.readline().split()
            vectors[1] = np.array([a2_tmp[0], a2_tmp[1], a2_tmp[2]], dtype=float)
            a3_tmp = f.readline().split()
            vectors[2] = np.array([a3_tmp[0], a3_tmp[1], a3_tmp[2]], dtype=float)

        if str1.find("CELL_PARAMETERS (alat=") >= 0:
            """ every vc-relax step
            CELL_PARAMETERS (alat=  3.62007036)
            1.004854534  -1.740459107   0.000000000
            1.004854534   1.740459107   0.000000000
            0.000000000  -0.000000000   3.321930409
            """
            print("CELL_PARAMETERS (alat")
            a1_tmp = f.readline().split()
            vectors[0] = a * np.array([a1_tmp[0], a1_tmp[1], a1_tmp[2]], dtype=float)
            a2_tmp = f.readline().split()
            vectors[1] = a * np.array([a2_tmp[0], a2_tmp[1], a2_tmp[2]], dtype=float)
            a3_tmp = f.readline().split()
            vectors[2] = a * np.array([a3_tmp[0], a3_tmp[1], a3_tmp[2]], dtype=float)

        if str1.find("ATOMIC_POSITIONS (alat)") >= 0:
            """ every step
            ATOMIC_POSITIONS (alat)
            Si       0.002000062   0.003501432  -0.000003750
            Si       0.251999938   0.253498568   0.250003750
            """
            # print("ATOMIC_POSITIONS (alat)")
            model, str1 = get_positions(f, vectors)
            model.convert_from_scaled_to_cart(a)
            models.append(model)

        if str1.find("ATOMIC_POSITIONS (crystal)") >= 0:
            """ every step
            ATOMIC_POSITIONS (crystal)
            Si       0.001450378   0.000614400   0.000038753
            Si      -0.246450378   0.751385600  -0.250038753
            """
            # print("ATOMIC_POSITIONS (crystal)")
            model, str1 = get_positions(f, vectors)
            model.convert_from_direct_to_cart()
            models.append(model)

        if str1.find("Cartesian axes") >= 0:
            """ one ! atoms
                Cartesian axes

                site n.     atom                  positions (alat units)
                1           Si  tau(   1) = (   0.0000000   0.0000000   0.0000000  )
                2           Si  tau(   2) = (   0.2500000   0.2500000   0.2500000  )
                """
            f.readline()
            str1 = f.readline()
            if str1.find("site n.     atom                  positions (alat units)") >= 0:
                model = AtomicModel()
                str1 = helpers.spacedel(f.readline())
                # print(str1)
                while len(str1) > 5:
                    s = str1.split(' ')
                    x = a * float(s[6])
                    y = a * float(s[7])
                    z = a * float(s[8])
                    let = s[1]
                    charge = model.mendeley.get_charge_by_letter(let)
                    model.add_atom(Atom([x, y, z, let, charge]))
                    str1 = helpers.spacedel(f.readline())
                model.lat_vectors = vectors
                models.append(model)
        str1 = f.readline()
    f.close()
    return models


def get_positions(f, vectors):
    model = AtomicModel()
    str1 = helpers.spacedel(f.readline())
    # print(str1)
    while len(str1.split(' ')) > 3:
        s = str1.split(' ')
        x = float(s[1])
        y = float(s[2])
        z = float(s[3])
        let = s[0]
        charge = model.mendeley.get_charge_by_letter(let)
        model.add_atom(Atom([x, y, z, let, charge]))
        str1 = helpers.spacedel(f.readline())
    model.lat_vectors = deepcopy(vectors)
    return model, str1


def model_to_qe_pw(model: AtomicModel):
    types = model.types_of_atoms()
    text = "&system\n"
    text += "ibrav = 0, \n"
    alat = math.fabs(model.lat_vector1[0])
    text += "celldm(1) = " + str(alat / 0.52917720859) + ", \n"
    text += "nat = " + str(model.n_atoms()) + ", \n"
    text += "ntyp = " + str(len(types)) + ", \n"
    text += "/\n"
    text += "CELL_PARAMETERS { alat }\n"
    vector1 = model.lat_vector1 / alat
    vector2 = model.lat_vector2 / alat
    vector3 = model.lat_vector3 / alat
    text += str(round(vector1[0], 10)) + "   " + str(round(vector1[1], 10)) + "   " + str(round(vector1[2], 10)) + "\n"
    text += str(round(vector2[0], 10)) + "   " + str(round(vector2[1], 10)) + "   " + str(round(vector2[2], 10)) + "\n"
    text += str(round(vector3[0], 10)) + "   " + str(round(vector3[1], 10)) + "   " + str(round(vector3[2], 10)) + "\n"
    text += "ATOMIC_SPECIES\n"
    for i in range(0, len(types)):
        text += str(model.mendeley.get_let(int(types[i][0]))) + " mass  UPF_file_name\n"
    text += "ATOMIC_POSITIONS {crystal}\n"
    model1 = deepcopy(model)
    model1.convert_from_cart_to_direct()
    for atom in model1.atoms:
        text += atom.let + " " + atom.xyz_string + "\n"
    return text


def energy_tot(filename):
    """Energy"""
    prop = "!    total energy              ="
    is_conv = "false"
    iteration = ""
    property1 = ""
    if os.path.exists(filename):
        my_file = open(filename)
        str1 = my_file.readline()
        while str1 != '':
            if (str1 != '') and (str1.find("General timing and accounting informations for this job:") >= 0):
                is_conv = "true"
            if (str1 != '') and (str1.find("-- Iteration") >= 0):
                iteration = str1
            if (str1 != '') and (str1.find(prop) >= 0):
                str1 = str1.replace(prop, ' ')
                prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                property1 = float(prop1) #* 13.6056923
            str1 = my_file.readline()
        my_file.close()
    return property1, is_conv, iteration


def volume(filename):
    """Cell volume"""
    prop = "unit-cell volume          ="
    if os.path.exists(filename):
        my_file = open(filename)
        str1 = my_file.readline()
        while str1 != '':
            if (str1 != '') and (str1.find(prop) >= 0):
                str1 = str1.replace(prop, ' ')
                prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                property = float(prop1)
            str1 = my_file.readline()
        my_file.close()
    return property
