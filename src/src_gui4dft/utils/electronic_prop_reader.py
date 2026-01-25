# -*- coding: utf-8 -*-
import os
import re
import numpy as np
from core_atomistic import helpers

# Conversion factor: 1 Hartree = 27.21138602 eV (according to CODATA)
HARTREE_TO_EV = 27.21138602


def dos_from_file(filename, n=2, n_lines=0):
    energy = []
    spin_up = []
    spin_down = []
    if os.path.exists(filename):
        dos_file = open(filename)
        str_dos = dos_file.readline()

        if n_lines > 0:
            for i in range(0, 6):
                str_dos = dos_file.readline()

            for i in range(0, n_lines):
                str_dos = read_row_of_dos_file(dos_file, energy, n, spin_down, spin_up, str_dos)

        if n_lines == 0:
            while str_dos != '':
                str_dos = read_row_of_dos_file(dos_file, energy, n, spin_down, spin_up, str_dos)
    return np.array(spin_up), np.array(spin_down), np.array(energy)


def dos_from_crystal_file(filename):
    """
    Reads the DOS data from a Crystal DOSS.DAT file.
    Assumes NSPIN=2 (spin-polarized): first block for spin-up (positive DOS),
    second block for spin-down (negative DOS, which we invert to positive).
    Returns lists: spin_up, spin_down, energy (in Hartree, relative to E_FERMI).
    """
    spin_up = []
    spin_down = []
    energy = []

    with open(filename, 'r') as f:
        line = f.readline().strip().split()
        nlines = int(line[2])
        NPROJ = int(line[4])
        nspin = int(line[6])

        # Read first block: nlines lines of E DOS_up (positive)
        # The loop will automatically skip intervening # and @ lines
        for _ in range(nlines + 10):  # +10 to account for header skips (safe upper bound)
            line = f.readline().strip()
            if len(spin_up) >= nlines:
                break
            if line and not line.startswith('#') and not line.startswith('@'):
                parts = line.split()
                e = float(parts[0])
                dos_up = float(parts[1])
                energy.append(e)
                spin_up.append(dos_up)

        if nspin == 2:
            # Skip # EFERMI line
            f.readline()
            # Skip & separator unconditionally
            # f.readline()

            # Read second block: nlines lines of E DOS_down (negative, invert sign)
            for _ in range(nlines + 5):  # +5 for any extra skips
                line = f.readline().strip()
                if len(spin_down) >= nlines:
                    break
                if line and not line.startswith('#') and line != '&':
                    parts = line.split()
                    # e = float(parts[0])  # Matches energy from first block, no need to append
                    dos_down = -float(parts[1])  # Invert to make positive, like VASP
                    spin_down.append(dos_down)
        else:
            # For nspin=1, no second block to read
            pass

        # Skip final # EFERMI line if present (only for nspin=2)
        if nspin == 2:
            try:
                f.readline()
            except:
                pass

    if nspin == 1:
        # For non-spin-polarized, return total DOS as spin_up, empty spin_down
        spin_down = [0.0] * len(spin_up)

    # Validation
    if len(spin_up) != nlines:
        raise ValueError(f"Expected {nlines} points for spin-up, but read {len(spin_up)}")

    if nspin == 2 and len(spin_down) != nlines:
        raise ValueError(f"Expected {nlines} points for spin-down, but read {len(spin_down)}")

    return np.array(spin_up), np.array(spin_down), np.array(energy) * HARTREE_TO_EV


def read_row_of_dos_file(dos_file, energy, n, spin_down, spin_up, str_dos):
    line = str_dos.split(' ')
    line1 = []
    for i in range(0, len(line)):
        if line[i] != '':
            line1.append(line[i])
    energy.append(float(line1[0]))
    spin_up.append(float(line1[1]))
    if len(line1) > n:
        spin_down.append(float(line1[n]))
    else:
        spin_down.append(0)
    str_dos = dos_file.readline()
    return str_dos


def dos_siesta_vert(filename, e_f=0):
    """DOS Vertical. Spin up only"""
    if os.path.exists(filename):
        dos_file = open(filename)
        str_dos = dos_file.readline()
        dos = []
        while str_dos != '':
            line = str_dos.split(' ')
            line1 = []
            for i in range(0, len(line)):
                if line[i] != '':
                    line1.append(line[i])
            dos.append([float(line1[1]), round(float(line1[0]) - e_f, 5)])
            str_dos = dos_file.readline()
        return dos
    return None


def fermi_energy_from_crystal_dos(file_path):
    """
        Extracts the Fermi energy from the DOSS.DAT file specified by the path.
        Assumes the line with the energy has the format '# EFERMI (HARTREE) <value>'.
        If there are multiple lines (for spin-polarized calculation), returns the first one found.
        Returns the value in electronvolts (eV).
        """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    pattern = r'# EFERMI \(HARTREE\)\s*([-+]?\d+\.?\d*[eE]?-?\d*)'
    match = re.search(pattern, content)
    if match:
        fermi_hartree = float(match.group(1))
        fermi_ev = fermi_hartree * HARTREE_TO_EV
        return fermi_ev
    else:
        raise ValueError("Fermi energy not found in the file.")


def read_siesta_bands(file, is_check_bands_spin):
    f = open(file)
    e_fermi = float(f.readline())
    f.readline()
    str1 = f.readline().split()
    str1 = helpers.list_str_to_float(str1)
    e_min, e_max = float(str1[0]), float(str1[1])
    str1 = f.readline().split()
    str1 = helpers.list_str_to_int(str1)
    n_bands, n_spins = int(str1[0]), int(str1[1])
    n_k_points = int(str1[2])
    k_mesh = np.zeros((str1[2]))
    bands = np.zeros((n_bands * n_spins, n_k_points))
    for i in range(0, str1[2]):
        str2 = f.readline().split()
        str2 = helpers.list_str_to_float(str2)
        k_mesh[i] = str2[0]
        for j in range(1, len(str2)):
            bands[j - 1][i] = float(str2[j]) - e_fermi
        kol = len(str2) - 1
        while kol < n_bands * n_spins:
            str2 = f.readline().split()
            str2 = helpers.list_str_to_float(str2)
            for j in range(0, len(str2)):
                bands[kol + j][i] = float(str2[j]) - e_fermi
            kol += len(str2)
    if is_check_bands_spin:
        bands = bands[:n_bands]
    else:
        bands = bands[n_bands:]
    f.close()
    return bands, e_max, e_min, k_mesh


def siesta_homo_lumo(bands, e_max, e_min):
    # e_min, e_max = np.min(bands, 1), np.max(bands, 1)
    homo = e_min * np.ones(len(bands[0]))
    lumo = e_max * np.ones(len(bands[0]))
    for i in range(0, len(bands)):
        for j in range(0, len(bands[0])):
            tm = float(bands[i][j])
            if (tm > homo[j]) and (tm <= 0):
                homo[j] = tm
            if (tm < lumo[j]) and (tm > 0):
                lumo[j] = tm
    return homo, lumo
