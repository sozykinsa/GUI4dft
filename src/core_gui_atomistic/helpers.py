# -*- coding: utf-8 -*-
import os
import re
import math
import numpy as np


def spacedel(row: str) -> str:
    """Removing extra spaces, line breaks."""
    row = row.replace('\n', ' ')
    row = row.replace('\r', ' ')
    row = row.strip()
    while row.find('  ') >= 0:
        row = row.replace('  ', ' ')
    return row


def clear_fdf_lines(lines):
    result = []
    for line in lines:
        tmp = spacedel(line)
        if not (tmp.startswith("#") or len(tmp) == 0):
            result.append(tmp)
    return result


def float_to_string(fl):
    res = '{0:12.8f}'.format(fl)
    if res == " -0.00000000":
        res = "  0.00000000"
    return res


def is_number(row) -> bool:
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


def lat_vectors_from_params(a, b, c, alpha, beta, gamma):
    tm = math.pow(math.cos(alpha), 2) + math.pow(math.cos(beta), 2) + math.pow(math.cos(gamma), 2)
    tmp = math.sqrt(1 + 2 * math.cos(alpha) * math.cos(beta) * math.cos(gamma) - tm)
    h = c * tmp / math.sin(gamma)
    lat_vectors = np.zeros((3, 3), dtype=float)
    lat_vectors[0] = np.array([a, 0, 0])
    lat_vectors[1] = np.array([b * math.cos(gamma), b * math.sin(gamma), 0])
    lat_vectors[2] = np.array([c * math.cos(beta), c * math.cos(alpha) * math.sin(gamma), h])
    for i in range(3):
        for j in range(3):
            if math.fabs(lat_vectors[i][j]) < 1e-8:
                lat_vectors[i][j] = 0
    return lat_vectors


def lattice_parameters_abc_angles(lattice_parameters, lat_constant):
    """..."""
    if len(lattice_parameters) > 0:
        data = spacedel(lattice_parameters[0]).split()
        a = lat_constant * float(data[0])
        b = lat_constant * float(data[1])
        c = lat_constant * float(data[2])
        alpha = math.radians(float(data[3]))
        beta = math.radians(float(data[4]))
        gamma = math.radians(float(data[5]))
        return lat_vectors_from_params(a, b, c, alpha, beta, gamma)
    else:
        return None


def list_str_to_float(x):
    return [float(item) for item in x]


def list_str_to_int(x):
    return [int(item) for item in x]


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


def list_n2_split(data):
    x = []
    y = []
    for row in data:
        x.append(row[0])
        y.append(row[1])
    return np.array(x), np.array(y)


def from_file_property(filename: str, prop: str, count: int = 1, prop_type: str = 'int'):
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


def write_text_to_file(f_name, text):  # pragma: no cover
    if len(f_name) > 0:
        with open(f_name, 'w') as f:
            f.write(text)


def property_from_sub_file(filename, k, prop, count, typen):
    property_value = None
    is_found = False
    if os.path.exists(filename):
        my_file = open(filename)
        str1 = my_file.readline()
        while str1 != '':
            if (str1 != '') and (str1.find("%include") >= 0):
                new_f = str1.split()[1]
                file = os.path.dirname(filename) + "/" + new_f
                is_found, k, property_value = property_from_sub_file(file, k, prop, count, typen)
            if (str1 != '') and (str1.find(prop) >= 0) and not str1.lstrip().startswith('#'):
                str1 = str1.replace(prop, ' ')
                if typen == "unformatted":
                    property_value = str1
                if typen == 'string':
                    property_value = spacedel(str1)
                else:
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                    if typen == 'int':
                        property_value = int(prop1)
                    if typen == 'float':
                        property_value = float(prop1)

                if k == count:
                    is_found = True

                k += 1
            if is_found:
                my_file.close()
                return is_found, k-1, property_value

            str1 = my_file.readline()
        my_file.close()
    return is_found, k, property_value


def text_between_lines(filename, line1, line2):
    file_name = open(filename)
    str1 = file_name.readline()
    while str1.find(line1) == -1:
        str1 = file_name.readline()
    str1 = file_name.readline()
    fdf = []
    while str1.find(line2) == -1:
        if str1 != "":
            fdf.append(str1)
        str1 = file_name.readline()
    file_name.close()
    return fdf


def utf8_letter(let):
    if (let == r'\Gamma') or (let == 'Gamma'):
        return '\u0393'
    if (let == r'\Delta') or (let == 'Delta'):
        return '\u0394'
    if (let == r'\Lambda') or (let == 'Lambda'):
        return '\u039B'
    if (let == r'\Pi') or (let == 'Pi'):
        return '\u03A0'
    if (let == r'\Sigma') or (let == 'Sigma'):
        return '\u03A3'
    if (let == r'\Omega') or (let == 'Omega'):
        return '\u03A9'
    return let


def check_format(filename):
    """check file format"""

    """check file format"""
    if filename.endswith(".fdf") or filename.endswith(".FDF"):
        return "SIESTAfdf"

    if (filename.lower()).endswith(".out"):
        return "SIESTAout"

    if filename.endswith(".ani") or filename.endswith(".ANI"):
        return "SIESTAANI"

    if (filename.lower()).endswith(".xyz"):
        f = open(filename)
        f.readline()
        str1 = spacedel(f.readline())
        if len(str1.split()) > 4:
            return "XMolXYZ"
        if len(str1.split()) <= 4:
            return "SiestaXYZ"
        return "unknown"

    if filename.endswith(".STRUCT_OUT"):
        return "SIESTASTRUCT_OUT"

    if filename.endswith(".MD_CAR"):
        return "SIESTAMD_CAR"

    if filename.endswith(".XSF"):
        return "SIESTAXSF"

    if filename.endswith(".cube"):
        return "GAUSSIAN_cube"

    if filename.endswith("POSCAR") or filename.endswith("CONTCAR"):
        return "VASPposcar"

    if filename.endswith("outp") or filename.endswith("OUTP"):
        return "topond_out"

    if filename.endswith("outp") or filename.endswith("OUTP"):
        return "topond_out"

    if filename.endswith("data") or filename.endswith("DATA"):
        return "project"

    if filename.endswith("cro") or filename.endswith("CRO"):
        return "critic_cro"

    return "unknown"
