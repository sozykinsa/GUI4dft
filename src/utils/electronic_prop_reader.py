# -*- coding: utf-8 -*-
from utils import helpers
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
        spin_down.append(float(line1[2]))
    else:
        spin_down.append(0)
    str_dos = dos_file.readline()
    return str_dos


def dos_siesta_vert(filename, e_f=0):
    """DOS Vertical. Spin up only"""
    if os.path.exists(filename):
        DOSFile = open(filename)
        strDOS = DOSFile.readline()
        DOS = []
        while strDOS != '':
            line = strDOS.split(' ')
            line1 = []
            for i in range(0, len(line)):
                if line[i] != '':
                    line1.append(line[i])
            DOS.append([float(line1[1]), round(float(line1[0]) - e_f, 5)])
            strDOS = DOSFile.readline()
        return DOS


def read_siesta_bands(file, is_check_bands_spin, kmax, kmin):
    f = open(file)
    e_fermi = float(f.readline())
    f.readline()
    str1 = f.readline().split()
    str1 = helpers.list_str_to_float(str1)
    eminf, emaxf = float(str1[0]), float(str1[1])
    str1 = f.readline().split()
    str1 = helpers.list_str_to_int(str1)
    nbands, nspins = int(str1[0]), int(str1[1])
    n_k_points = int(str1[2])
    kmesh = np.zeros((str1[2]))
    homo = eminf * np.ones(n_k_points)
    lumo = emaxf * np.ones(n_k_points)
    bands = np.zeros((nbands * nspins, n_k_points))
    for i in range(0, str1[2]):
        str2 = f.readline().split()
        str2 = helpers.list_str_to_float(str2)
        kmesh[i] = str2[0]
        for j in range(1, len(str2)):
            bands[j - 1][i] = float(str2[j]) - e_fermi
        kol = len(str2) - 1
        while kol < nbands * nspins:
            str2 = f.readline().split()
            str2 = helpers.list_str_to_float(str2)
            for j in range(0, len(str2)):
                bands[kol + j][i] = float(str2[j]) - e_fermi
            kol += len(str2)
    if is_check_bands_spin:
        bands = bands[:nbands]
    else:
        bands = bands[nbands:]
    for i in range(0, nbands):
        for j in range(0, len(bands[0])):
            tm = float(bands[i][j])
            if (tm > homo[j]) and (tm <= 0):
                homo[j] = tm
            if (tm < lumo[j]) and (tm > 0):
                lumo[j] = tm
    nsticks = int(f.readline())
    xticks = []
    xticklabels = []
    for i in range(0, nsticks):
        str3 = f.readline().split()
        value = float(str3[0])
        if (round(value, 2) >= kmin) and (round(value, 2) <= kmax):
            xticks.append(value)
            letter = helpers.utf8_letter(str3[1][1:-1])
            xticklabels.append(letter)
    f.close()
    return bands, emaxf, eminf, homo, kmesh, lumo, xticklabels, xticks
