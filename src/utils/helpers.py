# -*- coding: utf-8 -*-
import math
import os
import re
from operator import itemgetter
import numpy as np


def spacedel(row: str) -> str:
    """Removing extra spaces, line breaks."""
    row = row.replace('\n', ' ')
    row = row.replace('\r', ' ')
    row = row.strip()
    while row.find('  ') >= 0:
        row = row.replace('  ', ' ')
    return row


def float_to_string(fl):
    res = '{0:12.8f}'.format(fl)
    if res == "-0.00000000":
        res = " 0.00000000"
    return res


def is_number(row):
    try:
        float(row)
        return True
    except ValueError:
        return False


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def list_str_to_float(x):
    return [float(item) for item in x]


def list_str_to_int(x):
    return [int(item) for item in x]


def write_text_to_file(fname, text):
    f = open(fname, 'w')
    print(text, file=f)
    f.close()


def getsubs(dir):
    dirs = []
    subdirs = []
    files = []
    for dirname, dirnames, filenames in os.walk(dir):
        dirs.append(dirname)
        for subdirname in dirnames:
            subdirs.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    del dirs[0]
    dirs.sort()
    return dirs, files


def cdev(ii, jj):
    i = abs(ii)
    j = abs(jj)
    if j > i:
        j, i = j, i
    if j == 0:
        return i
    while True:
        ir = i % j
        if ir == 0:
            return j
        else:
            i = j
            j = ir


def mini(list_2d):
    """ Сортирует список по возрастанию первого столбца и возвращает индекс минимального элемента во втором столбце """
    list_2d = sorted(list_2d, key=itemgetter(0))
    imin = 0
    for i in range(1, len(list_2d)):
        if float(list_2d[i][1]) < float(list_2d[imin][1]):
            imin = i
    return imin


def ListN2Split(data):
    x = []
    y = []
    for row in data:
        x.append(row[0])
        y.append(row[1])
    return np.array(x), np.array(y)


def from_file_property(filename, prop, count=1, prop_type='int'):
    """Returns the value of the property parameter from the file filename.
    The value can be an integer or a fixed-point fractional number.
    If the required parameter occurs several times in the file, you must specify the count parameter,
    which shows what value the found value should be returned by the function.
    The type parameter specifies the type of the return value (int, float, or string)
    """
    k = 1
    is_found, k, property = property_from_sub_file(filename, k, prop, count, prop_type)
    if is_found:
        return property
    else:
        return None


def property_from_sub_file(filename, k, prop, count, typen):
    property = None
    is_found = False
    #k = 1
    if os.path.exists(filename):
        MyFile = open(filename)
        str1 = MyFile.readline()
        while str1 != '':
            if (str1 != '') and (str1.find("%include") >= 0):
                new_f = str1.split()[1]
                file = os.path.dirname(filename) + "/" + new_f
                is_found, k, property = property_from_sub_file(file, k, prop, count, typen)
            if (str1 != '') and (str1.find(prop) >= 0):
                str1 = str1.replace(prop, ' ')
                if typen == "unformatted":
                    property = str1
                if typen == 'string':
                    property = spacedel(str1)
                else:
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                    if typen == 'int':
                        property = int(prop1)
                    if typen == 'float':
                        property = float(prop1)

                if k == count:
                    is_found = True

                k += 1
            if is_found:
                MyFile.close()
                return is_found, k-1, property

            str1 = MyFile.readline()
        MyFile.close()
    return is_found, k, property


def RoundToPlane(atom, R):
    """ RoundToPlane  """
    z = atom.z
    fi = math.asin(atom.x/R)
    if atom.y <= -1e-3:
        fi = 3.14 - fi
    x = -R * fi
    return [x, z]


def dos_from_file(filename, n, n_lines=0):
    dos_file = open(filename)
    str_dos = dos_file.readline()
    energy = []
    spin_up = []
    spin_down = []

    if n_lines > 0:
        for i in range(0, 6):
            str_dos = dos_file.readline()

        for i in range(0, n_lines):
            str_dos = read_row_of_dos_file(dos_file, energy, n, spin_down, spin_up, str_dos)

    if n_lines == 0:
        while str_dos != '':
            str_dos = read_row_of_dos_file(dos_file, energy, n, spin_down, spin_up, str_dos)
    return energy, spin_down, spin_up


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


def utf8_letter(let):
    if let == r'\Gamma':
        return '\u0393'
    if let == r'\Delta':
        return '\u0394'
    if let == r'\Lambda':
        return '\u039B'
    if let == r'\Pi':
        return '\u03A0'
    if let == r'\Sigma':
        return '\u03A3'
    if let == r'\Omega':
        return '\u03A9'
    return let
