# -*- coding: utf-8 -*-
from core_gui_atomistic import helpers
import numpy as np
import os


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


def read_siesta_bands(file, is_check_bands_spin, k_max, k_min):
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
    homo = e_min * np.ones(n_k_points)
    lumo = e_max * np.ones(n_k_points)
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
    for i in range(0, n_bands):
        for j in range(0, len(bands[0])):
            tm = float(bands[i][j])
            if (tm > homo[j]) and (tm <= 0):
                homo[j] = tm
            if (tm < lumo[j]) and (tm > 0):
                lumo[j] = tm
    n_sticks = int(f.readline())
    x_ticks = []
    x_tick_labels = []
    for i in range(0, n_sticks):
        str3 = f.readline().split()
        value = float(str3[0])
        if (round(value, 2) >= k_min) and (round(value, 2) <= k_max):
            x_ticks.append(value)
            letter = helpers.utf8_letter(str3[1][1:-1])
            x_tick_labels.append(letter)
    f.close()
    return bands, e_max, e_min, homo, k_mesh, lumo, x_tick_labels, x_ticks
