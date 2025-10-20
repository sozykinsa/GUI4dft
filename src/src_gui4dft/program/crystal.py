# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
import math
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from core_atomistic import helpers


class CRYSTAL:
    @staticmethod
    def bands_parser(file):
        with open(file, "r") as f:
            # First line: NKPT, NBND, NSPIN
            str1 = f.readline().split()
            nkpt = int(str1[2])
            nbnd = int(str1[4])
            nspins = int(str1[6])

            # Skip next 4 lines (NPANEL and k-path info)
            for _ in range(4):
                f.readline()

            # Skip spin headers and band data blocks
            for _ in range(nspins):
                for _ in range(21):  # header block for each spin
                    f.readline()
                for _ in range(nkpt):
                    kp = 0
                    while kp < nbnd:
                        line = f.readline()
                        # Protect against empty lines or EOF
                        if not line:
                            break
                        kp += len(line.split())

            # After reading all bands, search for Fermi energy at the end of file
            efermi = None
            # Move to the end and read backwards until "# EFERMI" line is found
            with open(file, "r") as f2:
                for line in reversed(f2.readlines()):
                    if line.strip().startswith("# EFERMI"):
                        efermi = float(line.split()[-1])
                        break

        if efermi is None:
            raise ValueError("Could not find EFERMI line in the file")

        # Convert Fermi energy from Hartree to eV
        efermi_ev = efermi * 27.2114

        # Set approximate limits (can be refined later)
        emin, emax = -10.0, 10.0
        kmin, kmax = 0.0, float(nkpt)

        return emax, emin, kmax, kmin, nspins, efermi_ev


    def read_crystal_bands(file_path, check_spin=True):
        """
        Reads a CRYSTAL BAND.DAT file and extracts the band structure.

        Parameters:
            file_path (str): Path to BAND.DAT file.
            is_check_bands_spin (bool):
                True  -> return spin-up (alpha) bands
                False -> return spin-down (beta) bands

        Returns:
            bands (ndarray): Band energies (eV, shifted by Fermi level)
            emaxf (float): Maximum energy (eV, relative to Fermi)
            eminf (float): Minimum energy (eV, relative to Fermi)
            kmesh (ndarray): K-point coordinates along the path
        """

        hartree_to_ev = 27.2114

        with open(file_path, "r") as f:
            lines = f.readlines()

        # --- Read header ---
        for line in lines:
            if line.startswith("# NKPT"):
                parts = line.split()
                nkpt = int(parts[2])
                nbnd = int(parts[4])
                nspin = int(parts[6])
                break

        # --- Get Fermi energy (last occurrence) ---
        efermi = None
        for line in reversed(lines):
            if "EFERMI" in line:
                efermi = float(line.split()[-1]) * hartree_to_ev
                break
        if efermi is None:
            raise ValueError("EFERMI not found in file")

        # --- Extract data lines ---
        data_lines = [
            line for line in lines
            if not (line.startswith("#") or line.startswith("@") or line.strip() == "")
        ]

        # Convert to numeric array
        data = np.array([
            [float(x.replace('E', 'e')) for x in line.split()]
            for line in data_lines
        ])

        # Check that number of columns matches (1 for k + nbnd bands)
        ncol = data.shape[1]
        if ncol != nbnd + 1 and nspin == 2:
            # For spin-polarized case, both spin channels are concatenated
            half = len(data) // 2
            data_up = data[:half]
            data_dn = data[half:]
            if is_check_bands_spin:
                data = data_up
            else:
                data = data_dn
        elif ncol != nbnd + 1:
            raise ValueError(f"Unexpected number of columns: {ncol}")

        # Separate k-mesh and band energies
        kmesh = data[:, 0]
        bands = data[:, 1:].T * hartree_to_ev  # (nbnd, nkpt)

        # Shift relative to Fermi energy
        bands -= efermi

        # Compute energy limits
        emaxf = np.max(bands)
        eminf = np.min(bands)

        return bands, emaxf, eminf, kmesh


def model_0d_to_d12(model):
    text = "crystal\n"
    text += "MOLECULE\n"
    text += "1\n"
    model2 = deepcopy(model)
    nat = model2.n_atoms()
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model2.atoms[i].charge
        text += str(ch) + "   " + model2.atoms[i].xyz_string + "\n"
    return text


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
    text += str(np.linalg.norm(model1.lat_vector1)) + " " + str(np.linalg.norm(model1.lat_vector2))
    text += " " + str(model.get_angle_gamma()) + "\n"
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model1.atoms[i].charge
        x = str(model2.atoms[i].x)
        y = str(model2.atoms[i].y)
        z = str(model1.atoms[i].z)
        text += str(ch) + "   " + x + "   " + y + "   " + z + "\n"
    return text


def model_3d_to_d12(model):
    text = "crystal\n"
    text += "CRYSTAL\n"
    text += "0 0 0\n"
    text += "1\n"
    model2 = deepcopy(model)
    model2.convert_from_cart_to_direct()

    text += str(np.linalg.norm(model.lat_vector1)) + '  ' + str(np.linalg.norm(model.lat_vector2)) + '  ' + \
            str(np.linalg.norm(model.lat_vector3)) + '  ' + str(model.get_angle_alpha()) + '  ' + \
            str(model.get_angle_beta()) + '  ' + str(model.get_angle_gamma()) + '\n'
    nat = model2.n_atoms()
    text += str(nat) + "\n"
    for i in range(0, nat):
        ch = model2.atoms[i].charge
        text += str(ch) + "   " + model2.atoms[i].xyz_string + "\n"
    return text


def structure_opt_step(f_name):
    models = []
    f = open(f_name)
    f.readline()
    row1 = f.readline().split()
    row2 = f.readline().split()
    row3 = f.readline().split()
    if (len(row1) == 3) and (len(row2) == 3) and (len(row3) == 3):
        vec1 = np.array(row1, dtype=float)
        vec2 = np.array(row2, dtype=float)
        vec3 = np.array(row3, dtype=float)
        f.readline()
        row = f.readline().split()
        while len(row) > 1:
            row = f.readline().split()
        number_of_atoms = int(row[0])
        new_model = AtomicModel.atoms_from_xyz_structure(number_of_atoms, f, [0, 1, 2, 3])
        new_model.set_lat_vectors([vec1, vec2, vec3])
        models.append(new_model)
    f.close()
    return models


def optimisatioion_steps(f_name, prop=""):
    models = []
    f = open(f_name)
    str1 = f.readline()
    while str1:
        if str1.find("COORDINATE AND CELL OPTIMIZATION - POINT") >= 0:
            model = AtomicModel()
            f.readline()
            f.readline()
            f.readline()
            str1 = f.readline()
            if str1.find("A              B              C           ALPHA      BETA       GAMMA") >= 0:
                start = 4
                str1 = f.readline()
                a, b, c = float(str1.split()[0]), float(str1.split()[1]), float(str1.split()[2])
                alpha, beta = math.radians(float(str1.split()[3])), math.radians(float(str1.split()[4]))
                gamma = math.radians(float(str1.split()[5]))

                f.readline()
                f.readline()
                str1 = f.readline()

                mult_x = 1.0
                mult_y = 1.0
                mult_z = 1.0

                if str1.find("X/A") >= 0:
                    mult_x = a

                if str1.find("Y/B") >= 0:
                    mult_y = b

                if str1.find("Z/C") >= 0:
                    mult_z = c

                f.readline()
                str1 = f.readline()

                while len(str1) > 5:
                    str1 = helpers.spacedel(str1)
                    s = str1.split(' ')
                    x = float(s[start]) * mult_x
                    y = float(s[start + 1]) * mult_y
                    z = float(s[start + 2]) * mult_z
                    charge = int(s[start - 2])
                    let = s[start - 1]
                    model.add_atom(Atom([x, y, z, let, charge]))
                    str1 = helpers.spacedel(f.readline())

                model.lat_vectors = helpers.lat_vectors_from_params(a, b, c, alpha, beta, gamma)
                models.append(model)

        str1 = f.readline()
    f.close()
    return models


def structure_of_primitive_cell(f_name):
    models = []
    f = open(f_name)
    start = 3
    str1 = f.readline()
    vec1 = np.array([1.0, 0.0, 0.0], dtype=float)
    vec2 = np.array([0.0, 1.0, 0.0], dtype=float)
    vec3 = np.array([0.0, 0.0, 1.0], dtype=float)
    while str1:
        f1 = str1.find("     ATOM             X(ANGSTROM)         Y(ANGSTROM)         Z(ANGSTROM)") >= 0
        f2 = str1.find("DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)") >= 0
        if f1:
            f.readline()
            start = 4
        if f2:
            f.readline()
            vec1 = np.array(f.readline().split(), dtype=float)
            vec2 = np.array(f.readline().split(), dtype=float)
            vec3 = np.array(f.readline().split(), dtype=float)
            for i in range(6):
                f.readline()
                start = 3
        if f1 or f2:
            model = AtomicModel()
            str1 = helpers.spacedel(f.readline())
            while len(str1) > 5:
                s = str1.split(' ')
                x = float(s[start])
                y = float(s[start + 1])
                z = float(s[start + 2])
                charge = int(s[start - 2])
                let = s[start - 1]
                model.add_atom(Atom([x, y, z, let, charge]))
                str1 = helpers.spacedel(f.readline())
        if f2:
            model.set_lat_vectors(vec1, vec2, vec3)
        if f1 or f2:
            models.append(model)
        str1 = f.readline()
    f.close()
    return models


def energies(filename):
    """Energy from each step."""
    e = helpers.list_of_values(filename, "TOTAL ENERGY(HF)(AU)(", 1)
    if len(e) == 0:
        e = helpers.list_of_values(filename, "TOTAL ENERGY(DFT)(AU)(", 1)
    e_opt = helpers.from_file_property(filename, "* OPT END - CONVERGED * E(AU):", prop_type='float')
    e.append(e_opt)
    return np.array(e, dtype=float) * 27.2113961317875
