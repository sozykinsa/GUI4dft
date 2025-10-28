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
        hartree_to_ev = 27.2114
        with open(file, "r") as f:
            lines = f.readlines()

        # First line: NKPT, NBND, NSPIN
        str1 = lines[0].split()
        print(f"Debug - first line parts: {str1}")

        # Find numerical values after labels
        nkpt = nbnd = nspins = None
        for i in range(len(str1)):
            if str1[i] == 'NKPT' and i + 1 < len(str1):
                nkpt = int(str1[i + 1])
            elif str1[i] == 'NBND' and i + 1 < len(str1):
                nbnd = int(str1[i + 1])
            elif str1[i] == 'NSPIN' and i + 1 < len(str1):
                nspins = int(str1[i + 1])

        if nkpt is None or nbnd is None or nspins is None:
            numbers = [int(x) for x in str1 if x.isdigit()]
            if len(numbers) >= 3:
                nkpt, nbnd, nspins = numbers[0], numbers[1], numbers[2]
            else:
                raise ValueError("Could not parse NKPT, NBND, NSPIN from first line")

        # Extract ALL energy values and k-point coordinates from band data
        all_energies = []
        kpoints = []

        # Find all band data lines (lines starting with numbers or negative numbers)
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or (line[0] == '-' and len(line) > 1 and line[1].isdigit())):
                parts = line.split()
                if parts:  # Make sure line is not empty
                    # First element is the k-point coordinate
                    try:
                        kcoord = float(parts[0].strip(','))
                        kpoints.append(kcoord)
                    except ValueError:
                        continue

                    # Parse all energy values (skip the first element)
                    for part in parts[1:]:
                        try:
                            energy = float(part.strip(','))
                            all_energies.append(energy)
                        except ValueError:
                            continue

        if not all_energies:
            raise ValueError("No band energy data found in file")

        if not kpoints:
            raise ValueError("No k-point coordinates found in file")

        emin = min(all_energies)
        emax = max(all_energies)
        kmin = min(kpoints)
        kmax = max(kpoints)

        # Parse Fermi energy
        efermi = None
        for line in reversed(lines):
            if line.strip().startswith("# EFERMI"):
                parts = line.split()
                for part in parts:
                    try:
                        cleaned_part = part.strip(',')
                        efermi = float(cleaned_part)
                        if abs(efermi) < 10.0:  # reasonable range for Fermi energy
                            break
                    except ValueError:
                        continue
                if efermi is not None:
                    break

        if efermi is None:
            raise ValueError("Could not find EFERMI value in the file")

        # Convert from Hartree to eV
        efermi_ev = efermi * hartree_to_ev
        emin_ev = emin * hartree_to_ev
        emax_ev = emax * hartree_to_ev
        return emax_ev, emin_ev, kmax, kmin, nspins, efermi_ev

    @staticmethod
    def read_bands_xlabels(file, k_max, k_min):
        """
        Parse high-symmetry point information from band structure file.
        Returns data in SIESTA-compatible format.

        Parameters:
            file (str): Path to band structure file
            k_max (float): Maximum k-point value (for filtering)
            k_min (float): Minimum k-point value (for filtering)

        Returns:
            x_tick_labels (list): List of high-symmetry point labels
            x_ticks (list): List of k-point coordinates for high-symmetry points
        """

        x_ticks = []
        x_tick_labels = []

        with open(file, "r") as f:
            lines = f.readlines()

        # Method 1: Look for high-symmetry point information in comment lines
        for line in lines:
            if line.startswith('#'):
                parts = line.split()
                # Look for lines with format like: "#      1   (0,0,0)/6"
                if len(parts) >= 3 and parts[1].isdigit():
                    kpoint_index = int(parts[1])
                    # The k-label is usually in the 3rd or later position
                    kpoint_label = ""
                    for i in range(2, len(parts)):
                        if '(' in parts[i] or '/' in parts[i]:
                            kpoint_label = parts[i].strip('"')
                            break

                    if kpoint_label:
                        # Convert label to SIESTA format (extract letter/symbol)
                        letter = helpers.utf8_letter(kpoint_label)
                        x_tick_labels.append(letter)
                        # For now, we'll get the actual k-coordinate from data parsing
                        x_ticks.append(kpoint_index)  # Temporary - will be replaced

        # Method 2: Extract actual k-coordinates from data and match with labels
        if x_tick_labels:
            # Parse actual k-point coordinates from band data
            k_coordinates = []
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or (line[0] == '-' and len(line) > 1 and line[1].isdigit())):
                    parts = line.split()
                    if parts:
                        try:
                            kcoord = float(parts[0])
                            k_coordinates.append(kcoord)
                        except ValueError:
                            continue

            # Match high-symmetry point indices with actual k-coordinates
            if len(k_coordinates) >= len(x_ticks):
                # Use the k-coordinates at the specified indices
                actual_x_ticks = []
                for idx in x_ticks:
                    if 0 <= idx - 1 < len(k_coordinates):  # Convert to 0-based index
                        k_value = k_coordinates[idx - 1]
                        # Filter by k-range (like SIESTA does)
                        if (round(k_value, 6) >= k_min) and (round(k_value, 6) <= k_max + 1e-6):
                            actual_x_ticks.append(k_value)
                        else:
                            # Remove the corresponding label if k-point is out of range
                            label_idx = x_ticks.index(idx)
                            x_tick_labels.pop(label_idx)
                    else:
                        # Remove the corresponding label if index is invalid
                        label_idx = x_ticks.index(idx)
                        x_tick_labels.pop(label_idx)

                x_ticks = actual_x_ticks

        # Method 3: If above methods didn't work, try XAXIS TICKLABEL approach
        if not x_ticks:
            current_tick_index = None
            current_tick_value = None

            for line in lines:
                if line.startswith('@ XAXIS TICK '):
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            current_tick_index = int(parts[2].replace(',', ''))
                            current_tick_value = float(parts[3].replace(',', ''))
                        except (ValueError, IndexError):
                            continue

                elif line.startswith('@ XAXIS TICKLABEL ') and current_tick_value is not None:
                    parts = line.split()
                    # Look for the label in quotes
                    for i in range(len(parts)):
                        if parts[i].startswith('"') or "'" in parts[i]:
                            kpoint_label = parts[i].strip('"\'')
                            letter = helpers.utf8_letter(kpoint_label)

                            # Filter by k-range (like SIESTA)
                            if (round(current_tick_value, 6) >= k_min) and (
                                    round(current_tick_value, 6) <= k_max + 1e-6):
                                x_ticks.append(current_tick_value)
                                x_tick_labels.append(letter)

                            current_tick_value = None
                            break

        # Ensure we have the same number of ticks and labels
        min_length = min(len(x_ticks), len(x_tick_labels))
        x_ticks = x_ticks[:min_length]
        x_tick_labels = x_tick_labels[:min_length]
        return x_tick_labels, x_ticks

    @staticmethod
    def read_crystal_bands(file_path, check_spin=True):
        """
        Reads a CRYSTAL BAND.DAT file and extracts the band structure.
        Returns data in the same format as SIESTA.

        Parameters:
            file_path (str): Path to BAND.DAT file.
            check_spin (bool):
                True  -> return spin-up (alpha) bands
                False -> return spin-down (beta) bands

        Returns:
            bands (ndarray): Band energies (eV, shifted by Fermi level), shape (n_bands, n_kpoints)
            e_max (float): Maximum energy (eV, relative to Fermi)
            e_min (float): Minimum energy (eV, relative to Fermi)
            k_mesh (ndarray): K-point coordinates along the path, shape (n_kpoints,)
        """

        # First, use bands_parser to get basic information
        emax_ev, emin_ev, kmax, kmin, nspin, efermi_ev = CRYSTAL.bands_parser(file_path)

        with open(file_path, "r") as f:
            lines = f.readlines()

        # --- Extract NKPT and NBND from header ---
        nkpt = nbnd = None
        for line in lines:
            if line.startswith("# NKPT"):
                parts = line.split()
                print(f"Debug - Header parts: {parts}")

                # Parse using label-based approach
                for i in range(len(parts)):
                    if parts[i] == 'NKPT' and i + 1 < len(parts):
                        nkpt = int(parts[i + 1])
                    elif parts[i] == 'NBND' and i + 1 < len(parts):
                        nbnd = int(parts[i + 1])

                # Alternative: find all numbers in the line
                if nkpt is None or nbnd is None:
                    numbers = [int(x) for x in parts if x.isdigit()]
                    if len(numbers) >= 2:
                        nkpt, nbnd = numbers[0], numbers[1]

                break

        if nkpt is None or nbnd is None:
            raise ValueError(f"Could not parse NKPT and NBND from file header. nkpt={nkpt}, nbnd={nbnd}")

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

        # Handle spin-polarized case - преобразуем к SIESTA-like формату
        if nspin == 2:
            # For spin-polarized case, data contains both spin channels sequentially
            total_kpoints_in_file = data.shape[0]
            if total_kpoints_in_file == 2 * nkpt:
                # Standard case: spin-up followed by spin-down
                data_up = data[:nkpt]  # First nkpt points - spin-up
                data_dn = data[nkpt:2 * nkpt]  # Next nkpt points - spin-down

                # Extract k-mesh (should be the same for both spins)
                k_mesh = data_up[:, 0]  # Use spin-up k-points

                # Extract bands and convert to SIESTA format: shape (n_bands * n_spins, n_kpoints)
                bands_up = data_up[:, 1:].T  # shape: (nbnd, nkpt)
                bands_dn = data_dn[:, 1:].T  # shape: (nbnd, nkpt)

                # Combine like SIESTA: all spin-up bands first, then all spin-down bands
                bands_combined = np.vstack([bands_up, bands_dn])  # shape: (2 * nbnd, nkpt)

                # Select spin according to check_spin parameter (like SIESTA)
                if check_spin:
                    bands = bands_up  # shape: (nbnd, nkpt) - spin-up
                else:
                    bands = bands_dn  # shape: (nbnd, nkpt) - spin-down

            else:
                raise ValueError(
                    f"Unexpected data size for spin-polarized case: expected {2 * nkpt}, got {total_kpoints_in_file}")

        else:
            # Non-spin-polarized case
            k_mesh = data[:, 0]
            bands = data[:, 1:].T  # shape: (nbnd, nkpt)

        # Convert bands to eV and shift relative to Fermi energy
        bands_ev = bands * 27.2114  # Convert to eV
        #bands_ev -= efermi_ev  # Shift to Fermi level

        # Compute energy limits relative to Fermi level (like SIESTA)
        e_min = np.min(bands_ev)
        e_max = np.max(bands_ev)

        # Return in SIESTA format: bands (n_bands, n_kpoints), e_max, e_min, k_mesh (n_kpoints,)
        return bands_ev, e_max, e_min, k_mesh


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
    vecs = np.ones((3, 3), dtype=float)
    while str1:
        f1 = str1.find("     ATOM             X(ANGSTROM)         Y(ANGSTROM)         Z(ANGSTROM)") >= 0
        f2 = str1.find("DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)") >= 0
        if f1:
            f.readline()
            start = 4
        if f2:
            f.readline()
            vecs[0] = np.array(f.readline().split(), dtype=float)
            vecs[1] = np.array(f.readline().split(), dtype=float)
            vecs[2] = np.array(f.readline().split(), dtype=float)
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
            model.set_lat_vectors(vecs)
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
