# -*- coding: utf-8 -*-
# Python 3
import copy
import math
import os
import random
import re
from copy import deepcopy
from operator import itemgetter

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm
from numpy import polyfit
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi

##################################################################
############################ Helpers  ############################
##################################################################

class Helpers:
    @staticmethod
    def spacedel(stroka):
        """ Удаление лишних пробелов, перводов строк """
        stroka = stroka.replace('\n', ' ')
        stroka = stroka.replace('\r', ' ')
        stroka = stroka.strip()
        while stroka.find('  ')>=0:
            stroka = stroka.replace('  ', ' ')
        return stroka

    @staticmethod
    def list_plus_list(x, y):
        """ поэлементное сложение списков """
        return list(map(lambda a, b: a + b, x, y))

    @staticmethod
    def float_mult_list(x, y):
        """ умножение числа на список """
        return [float(x * item) for item in y]

    @staticmethod
    def list_str_to_float(x):
        return [float(item) for item in x]

    @staticmethod
    def list_str_to_int(x):
        return [int(item) for item in x]

    @staticmethod
    def nearest(latEn, nextLat):
        """ This example shows how to """
        res = abs(float(latEn[0][0]) - nextLat)
        for i in range(1, len(latEn)):
            if res > abs(float(latEn[i][0]) - nextLat):
                res = abs(float(latEn[i][0]) - nextLat)
        return res

    @staticmethod
    def NextLat(latEn, eps):
        """ This example shows how to """
        if len(latEn) == 1:
            nextLat = float(latEn[0][0]) + 0.5
        if len(latEn) == 2:
            if float(latEn[0][1]) > float(latEn[1][1]):
                nextLat = float(latEn[1][0]) + 0.5
            else:
                nextLat = float(latEn[0][0]) - 0.5
        if len(latEn) > 2:
            latEn.sort(key=lambda x: x[0])
            imin = Helpers.mini(latEn)
            tmList = []
            start = imin - 1
            if imin == 0:
                start = 0
            if imin == len(latEn) - 1:
                start = len(latEn) - 4
            k = 3
            x = []
            y = []
            for i in range(0, k):
                x.append(float(latEn[start + i][0]))
                y.append(float(latEn[start + i][1]))

            a, b, c = polyfit(x, y, 2)
            nextLat = -b / (2 * a)
            sign = 1
            st = 0
            # errxrange = AT.Helpers.errorsrange(latEn)
            while (Helpers.nearest(latEn, nextLat) < eps / 4) and (st < 5):
                if (len(latEn) <= imin + sign) or (imin + sign < 0):
                    nextLat = float(latEn[imin][0]) + sign * eps / 2
                else:
                    nextLat = (float(latEn[imin + sign][0]) + float(latEn[imin][0])) / 2
                sign = -sign
                st = st + 1
            if st == 5:
                nextLat = 0
        return nextLat
        
    @staticmethod
    def getsubs(dir):
        """ Получение списка директорий и файлов """
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
            
    @staticmethod
    def cdev(ii, jj):
        i = abs(ii)
        j = abs(jj)
        if (j > i):
            j, i = j, i
        if (j == 0):
            return i
        while (True):
            ir = i % j
            if (ir == 0):
                return j
            else:
                i = j
                j = ir

    @staticmethod    
    def mini(List2D):
        """ Сортирует список по возрастанию первого столбца и возвращает индекс минимального элемента во втором столбце """
        List2D = sorted(List2D, key=itemgetter(0))
        imin = 0
        for i in range(1,len(List2D)):
            if float(List2D[i][1]) < float(List2D[imin][1]):
                imin = i
        return imin

    @staticmethod
    def ListN2Split(DATA):
        # из списка N x 2 получаем 2 списка по N элементов
        x = []
        y = []
        for row in DATA:
            x.append(row[0])
            y.append(row[1])
        return np.array(x), np.array(y)
    
    @staticmethod    
    def errorsrange(ListLatEn):
        """ Возвращает ширину доверительного интервала при поиске оптимального параметра """
        ListLatEn = sorted(ListLatEn, key=itemgetter(0))
        if len(ListLatEn)<3:
            return 10
        ans = float(ListLatEn[len(ListLatEn)-1][0]) - float(ListLatEn[0][0])
        imin = Helpers.mini(ListLatEn)
        if imin == 0:
            ans = float(ListLatEn[1][0]) - float(ListLatEn[0][0])
        if imin == len(ListLatEn)-1:
            ans = float(ListLatEn[len(ListLatEn)-1][0]) - float(ListLatEn[len(ListLatEn)-2][0])
        if (imin != 0) and (imin != len(ListLatEn)-1):
            ans = float(ListLatEn[imin+1][0]) - float(ListLatEn[imin-1][0])
        return ans

    @staticmethod
    def fromFileProperty(filename,prop,count = 1, type = 'int'):
        """ Возвращает  значение параметра property из файла filename. Зрачене может быть целым или дробным числом с фиксированной точкой. Если в файле необходимый параметр встречается несколько раз, необходимо задать параметр count, который показывает какое по счету найденное значение должна вернуть функция. Параметр type указывает тип возвращаемого значения (int, float или string)  """
        property = None
        k = 1
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()            
            while str1!='':            
                if (str1 != '') and (str1.find(prop)>=0):
                    str1 = str1.replace(prop,' ')
                    if type == "unformatted":
                        return str1
                    if (type == 'string'):
                        property = Helpers.spacedel(str1)
                    else:
                        prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]
                        if (type == 'int'):
                            property = int(prop1)
                        if (type == 'float'):
                            property = float(prop1)
                        
                    if (k == count):
                        return property
                    k+=1
                
                str1 = MyFile.readline()
            MyFile.close()
        return property

    @staticmethod
    def RoundToPlane(atom, R):
        """ RoundToPlane  """

        z = atom.z
        fi = math.asin(atom.x/R)
        if (atom.y<=-1e-3):
            fi = 3.14 - fi
        x = -R*fi
        return [x,z]

##################################################################
######################## TPeriodTable ############################
##################################################################    

class TPeriodTableAtom:
    def __init__(self, charge, radius, let, color, mass = 1):
        self.charge = charge
        self.radius = radius
        self.let = let
        self.color = color
        self.mass = mass

class TPeriodTable:
    """The TPeriodTable class provides basic fetches of Mendelevium's table. The constructor does not have arguments"""
    def __init__(self):
        self.table_size = 128
        self.Atoms = []
        self.default_color = [0.6, 0.6, 1.0]
        self.default_radius = 77
        self.Atoms.append(TPeriodTableAtom(0,    0, ' ',  [0.1, 1.0, 0.1]))
        self.Atoms.append(TPeriodTableAtom(1,   53, 'H',  [0.1, 0.6, 0.1], 1))
        self.Atoms.append(TPeriodTableAtom(2,   31, 'He', [0.5, 0.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(3,  145, 'Li', [1.0, 1.0, 0.15]))
        self.Atoms.append(TPeriodTableAtom(4,  112, 'Be', [0.3, 1.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(5,   98,  'B', [0.6, 0.3, 0.0]))
        self.Atoms.append(TPeriodTableAtom(6,   77,  'C', [0.2, 0.2, 0.8], 12))
        self.Atoms.append(TPeriodTableAtom(7,   92,  'N', [0.45, 0.3, 0.6]))
        self.Atoms.append(TPeriodTableAtom(8,   60,  'O', [1.0, 0.0, 0.5], 16))
        self.Atoms.append(TPeriodTableAtom(9,   73,  'F', self.default_color))
        self.Atoms.append(TPeriodTableAtom(10,  38, 'Ne', self.default_color))
        self.Atoms.append(TPeriodTableAtom(11, 190, 'Na', self.default_color))
        self.Atoms.append(TPeriodTableAtom(12, 160, 'Mg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(13, 143, 'Al', self.default_color))
        self.Atoms.append(TPeriodTableAtom(14, 132, 'Si', self.default_color))
        self.Atoms.append(TPeriodTableAtom(15, 128,  'P', self.default_color))
        self.Atoms.append(TPeriodTableAtom(16, 127,  'S', self.default_color))
        self.Atoms.append(TPeriodTableAtom(17,  99, 'Cl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(18,  71, 'Ar', self.default_color))
        self.Atoms.append(TPeriodTableAtom(19, 235,  'K', self.default_color))
        self.Atoms.append(TPeriodTableAtom(20, 197, 'Ca', self.default_color))
        self.Atoms.append(TPeriodTableAtom(21, 162, 'Sc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(22, 147, 'Ti', self.default_color))
        self.Atoms.append(TPeriodTableAtom(23, 134,  'V', self.default_color))
        self.Atoms.append(TPeriodTableAtom(24, 130, 'Cr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(25, 127, 'Mn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(26, 126, 'Fe', self.default_color))
        self.Atoms.append(TPeriodTableAtom(27, 125, 'Co', self.default_color))
        self.Atoms.append(TPeriodTableAtom(28, 124, 'Ni', self.default_color))
        self.Atoms.append(TPeriodTableAtom(29, 128, 'Cu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(30, 138, 'Zn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(31, 141, 'Ga', self.default_color))
        self.Atoms.append(TPeriodTableAtom(32, 123, 'Ge', self.default_color))
        self.Atoms.append(TPeriodTableAtom(33, 139, 'As', self.default_color))
        self.Atoms.append(TPeriodTableAtom(34, 140, 'Se', self.default_color))
        self.Atoms.append(TPeriodTableAtom(35, 114, 'Br', self.default_color))
        self.Atoms.append(TPeriodTableAtom(36,  88, 'Kr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(37, 248, 'Rb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(38, 215, 'Sr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(39, 178,  'Y', self.default_color))
        self.Atoms.append(TPeriodTableAtom(40, 160, 'Zr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(41, 160, 'Nb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(42, 139, 'Mo', self.default_color))
        self.Atoms.append(TPeriodTableAtom(43, 136, 'Tc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(44, 134, 'Ru', self.default_color))
        self.Atoms.append(TPeriodTableAtom(45, 134, 'Rh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(46, 137, 'Pd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(47, 144, 'Ag', self.default_color))
        self.Atoms.append(TPeriodTableAtom(48, 154, 'Cd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(49, 166, 'In', self.default_color))
        self.Atoms.append(TPeriodTableAtom(50, 162, 'Sn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(51, 159, 'Sb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(52, 160, 'Te', self.default_color))
        self.Atoms.append(TPeriodTableAtom(53, 136,  'I', self.default_color))
        self.Atoms.append(TPeriodTableAtom(54, 108, 'Xe', self.default_color))
        self.Atoms.append(TPeriodTableAtom(55, 267, 'Cs', self.default_color))
        self.Atoms.append(TPeriodTableAtom(56, 222, 'Ba', self.default_color))
        self.Atoms.append(TPeriodTableAtom(57, 187, 'La', self.default_color))
        self.Atoms.append(TPeriodTableAtom(58, 181, 'Ce', self.default_color))
        self.Atoms.append(TPeriodTableAtom(59, 182, 'Pr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(60, 182, 'Nd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(61, 183, 'Pm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(62, 181, 'Sm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(63, 199, 'Eu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(64, 179, 'Gd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(65, 180, 'Tb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(66, 180, 'Dy', self.default_color))
        self.Atoms.append(TPeriodTableAtom(67, 179, 'Ho', self.default_color))
        self.Atoms.append(TPeriodTableAtom(68, 178, 'Er', self.default_color))
        self.Atoms.append(TPeriodTableAtom(69, 177, 'Tm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(70, 194, 'Yb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(71, 175, 'Lu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(72, 167, 'Hf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(73, 149, 'Ta', self.default_color))
        self.Atoms.append(TPeriodTableAtom(74, 141,  'W', self.default_color))
        self.Atoms.append(TPeriodTableAtom(75, 137, 'Re', self.default_color))
        self.Atoms.append(TPeriodTableAtom(76, 135, 'Os', self.default_color))
        self.Atoms.append(TPeriodTableAtom(77, 136, 'Ir', self.default_color))
        self.Atoms.append(TPeriodTableAtom(78, 139, 'Pt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(79, 144, 'Au', self.default_color))
        self.Atoms.append(TPeriodTableAtom(80, 157, 'Hg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(81, 171, 'Tl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(82, 175, 'Pb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(83, 170, 'Bi', self.default_color))
        self.Atoms.append(TPeriodTableAtom(84, 176, 'Po', self.default_color))
        self.Atoms.append(TPeriodTableAtom(85, 145, 'At', self.default_color))
        self.Atoms.append(TPeriodTableAtom(86, 214, 'Rn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(87, 290, 'Fr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(88, 200, 'Ra', self.default_color))
        self.Atoms.append(TPeriodTableAtom(89, 188, 'Ac', self.default_color))
        self.Atoms.append(TPeriodTableAtom(90, 180, 'Th', self.default_color))
        self.Atoms.append(TPeriodTableAtom(91, 161, 'Pa', self.default_color))
        self.Atoms.append(TPeriodTableAtom(92, 138,  'U', self.default_color))
        self.Atoms.append(TPeriodTableAtom(93, 130, 'Np', self.default_color))
        self.Atoms.append(TPeriodTableAtom(94, 162, 'Pu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(95, 173, 'Am', self.default_color))
        self.Atoms.append(TPeriodTableAtom(96, 299, 'Cm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(97, 297, 'Bk', self.default_color))
        self.Atoms.append(TPeriodTableAtom(98, 295, 'Cf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(99, 292, 'Es', self.default_color))
        self.Atoms.append(TPeriodTableAtom(100,290, 'Fm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(101,287, 'Md', self.default_color))
        self.Atoms.append(TPeriodTableAtom(102,285, 'No', self.default_color))
        self.Atoms.append(TPeriodTableAtom(103,282, 'Lr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(104,280, 'Rf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(105,280, 'Db', self.default_color))
        self.Atoms.append(TPeriodTableAtom(106,280, 'Sg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(107,128, 'Bh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(108,140, 'Hs', self.default_color))
        self.Atoms.append(TPeriodTableAtom(109,150, 'Mt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(110,150, 'Ds', self.default_color))
        self.Atoms.append(TPeriodTableAtom(111,150, 'Rg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(112,150, 'Cn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(113,170, 'Nh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(114,170, 'Fl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(115,170, 'Mc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(116,170, 'Lv', self.default_color))
        self.Atoms.append(TPeriodTableAtom(117,170, 'Ts', self.default_color))
        self.Atoms.append(TPeriodTableAtom(118,152, 'Og', self.default_color))
        self.Atoms.append(TPeriodTableAtom(119,170, 'Uue', self.default_color))
        self.Atoms.append(TPeriodTableAtom(120,170, 'Ubn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(121,170, 'Ubu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(122,170, 'Ubb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(123,170, 'Ubt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(124,170, 'Ubq', self.default_color))
        self.Atoms.append(TPeriodTableAtom(125,170, 'Ubp', self.default_color))
        self.Atoms.append(TPeriodTableAtom(126,170, 'Ubh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(127,170, 'Ubs', self.default_color))

        self.Bonds = []
        for i in range(0, self.table_size):
            row = []
            for j in range(0,self.table_size):
                row.append(1)
            self.Bonds.append(row)

        self.Bonds[1][6] = 1.0
        self.Bonds[1][8] = 1.0
        self.Bonds[6][6] = 1.42
        self.Bonds[6][8] = 1.42
        self.Bonds[16][16] = 1.9
        self.Bonds[46][46] = 2.5
        self.Bonds[78][78] = 2.5
        self.Bonds[79][79] = 2.5


        for i in range(0, self.table_size):
            for j in range(i+1, self.table_size):
                self.Bonds[j][i] = self.Bonds[i][j]

    def get_rad(self, charge):
        if int(charge)< self.table_size:
            return self.Atoms[int(charge)].radius
        else:
            return self.default_radius

    def get_let(self, charge):
        if int(charge) < self.table_size:
            return self.Atoms[int(charge)].let
        if int(charge)>=200:
            return "Direct"

    def get_color(self, charge):
        if int(charge) < self.table_size:
            return self.Atoms[int(charge)].color
        else:
            return self.default_color

    def get_charge_by_letter(self, let):
        for atom in self.Atoms:
            if atom.let.lower() == let.lower():
                return int(atom.charge)
            if let.lower() == "Direct":
                return 200
        return -1

    def get_all_colors(self):
        colors = []
        for i in range(0, self.table_size):
            colors.append(self.Atoms[i].color)
        return colors

    def get_all_letters(self):
        lets = []
        for i in range(0, self.table_size):
            lets.append(self.Atoms[i].let)
        return lets
    
##################################################################
########################### TATOM ################################
##################################################################    
    
class TAtom(object):
    def __init__(self, atData):
        """Constructor"""
        self.x = atData[0]
        self.y = atData[1]
        self.z = atData[2]
        self.let = atData[3]
        self.charge = int(atData[4])
        self.selected = False
        self.fragment1 = False
        self.properties = {}
        pass

    def setSelected(self, fl):
        self.selected = fl

    def isSelected(self):
        return self.selected

    def setProperty(self, prop, val):
        self.properties[prop] = val

    def getProperty(self, prop):
        return self.properties.get(prop)
        
##################################################################
################### The AtomicModel class ########################
##################################################################
    
class TAtomicModel(object):
    def __init__(self, newatoms=[]):
        self.atoms = []
        self.bonds = []
        self.name = ""
        self.LatVect1 = np.array([100, 0, 0])
        self.LatVect2 = np.array([0, 100, 0])
        self.LatVect3 = np.array([0, 0, 100])

        for at in newatoms:
            if isinstance(at, TAtom):
                atom = deepcopy(at)
            else:
                atom = TAtom(at)
            self.add_atom(atom)


    @staticmethod
    def atoms_from_ani(filename):
        """import from ANI file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            ani_file = open(filename)
            NumberOfAtoms = int(ani_file.readline())
            while NumberOfAtoms>0:
                newModel = TSIESTA.atoms_from_xyz_structure(NumberOfAtoms, ani_file, periodTable)
                molecules.append(newModel)
                st = ani_file.readline()
                if st!='':
                    NumberOfAtoms = int(st)
                else:
                    NumberOfAtoms = 0
        return molecules





    @staticmethod
    def atoms_from_fdf(filename):
        """Return a AtList from fdf file"""
        NumberOfAtoms = TSIESTA.number_of_atoms(filename)
        NumberOfSpecies = TSIESTA.number_of_species(filename)
        AtomicCoordinatesFormat = TSIESTA.atomic_coordinates_format(filename)

        lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lattice_vectors(filename)
        if lat_vect_1[0] == False:
            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lattice_parameters_abc_angles(filename)

        tmp_ar = {}
        ChemicalSpeciesLabel = TSIESTA.get_block_from_siesta_fdf(filename, "ChemicalSpeciesLabel")
        for j in range(0, len(ChemicalSpeciesLabel)):
            tmp_ar[(ChemicalSpeciesLabel[j].split())[0]] = (ChemicalSpeciesLabel[j].split())[1:3]

        f = open(filename)
        lines = f.readlines()
        f.close()
        AllAtoms = TAtomicModel()
        AtList = []
        AtList1 = []
        i = 0
        isBlockAtomicCoordinates = False
        isBlockZMatrix = False

        while i < len(lines):
            if (lines[i].find("%block Zmatrix") >= 0):
                isBlockZMatrix = True
                i += 1
                AtList = []
                if (lines[i].find("cartesian") >= 0):
                    for j in range(0, NumberOfAtoms):
                        i += 1
                        Atom_full = lines[i].split()
                        AtList.append([float(Atom_full[1]), float(Atom_full[2]), float(Atom_full[3]),
                                       (tmp_ar[str(Atom_full[0])])[1], (tmp_ar[str(Atom_full[0])])[0]])
            if (lines[i].find("%block AtomicCoordinatesAndAtomicSpecies") >= 0):
                isBlockAtomicCoordinates = True
                mult = 1
                if AtomicCoordinatesFormat == "NotScaledCartesianBohr":
                    mult = 0.52917720859
                for j in range(0, NumberOfAtoms):
                    i += 1
                    Atom_full = lines[i].split()
                    AtList1.append([mult*float(Atom_full[0]), mult*float(Atom_full[1]), mult*float(Atom_full[2]),
                                   (tmp_ar[str(Atom_full[3])])[1], (tmp_ar[str(Atom_full[3])])[0]])

            i += 1

        if isBlockZMatrix == True:
            AllAtoms = TAtomicModel(AtList)
        else:
            if isBlockAtomicCoordinates == True:
                AllAtoms = TAtomicModel(AtList1)

        if lat_vect_1[0] == False:
            AllAtoms.set_lat_vectors_default()

        else:
            AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)

        if isBlockZMatrix == True:
            units = Helpers.fromFileProperty(filename, 'ZM.UnitsLength', 1, 'string')
            if units.lower() == "bohr":
                AllAtoms.convert_from_scaled_to_cart(0.52917720859)
        else:
            if isBlockAtomicCoordinates == True:
                if AtomicCoordinatesFormat == "ScaledByLatticeVectors":
                    AllAtoms.convert_from_direct_to_cart()
                if AtomicCoordinatesFormat == "ScaledCartesian":
                    lat = TSIESTA.lattice_constant(filename)
                    AllAtoms.convert_from_scaled_to_cart(lat)

        Molecules = [AllAtoms]
        return Molecules

    @staticmethod
    def atoms_from_output_cg(filename):
        """import from CG output"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            sps = TSIESTA.Species(filename)
            species_label_charges = ['null']
            for spec in sps:
                species_label_charges.append(spec[1])

            siesta_file = open(filename)
            sl = []
            isSpesF = 0
            str1 = siesta_file.readline()
            atoms = []
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (isSpesF == 0):
                    str1 = siesta_file.readline()
                    while str1.find('siesta') >= 0:
                        str1 = Helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = siesta_file.readline()
                    isSpesF = 1

                if (str1 != '') and (str1.find("outcell: Unit cell vectors (Ang):") >= 0) and (isSpesF == 1):
                    lat_vect_1 = siesta_file.readline().split()
                    lat_vect_1 = Helpers.list_str_to_float(lat_vect_1)
                    lat_vect_2 = siesta_file.readline().split()
                    lat_vect_2 = Helpers.list_str_to_float(lat_vect_2)
                    lat_vect_3 = siesta_file.readline().split()
                    lat_vect_3 = Helpers.list_str_to_float(lat_vect_3)

                    AllAtoms = TAtomicModel(atoms)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    molecules.append(AllAtoms)

                if (str1 != '') and (str1.find("zmatrix: Z-matrix coordinates: (Ang ; rad )") >= 0) and (isSpesF == 1):
                    for j in range(0, 2):
                        str1 = siesta_file.readline()
                    atoms = []

                    for i1 in range(0, number_of_atoms):
                        str1 = Helpers.spacedel(siesta_file.readline())
                        S = str1.split(' ')
                        d1 = float(S[0])
                        d2 = float(S[1])
                        d3 = float(S[2])
                        Charge = species_label_charges[sl[len(atoms)]]
                        C = periodTable.get_let(Charge)
                        A = [d1, d2, d3, C, Charge]
                        atoms.append(A)
                str1 = siesta_file.readline()
            siesta_file.close()
        return molecules

    @staticmethod
    def atoms_from_output_md(filename):
        """import from MD output """
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            NumberOfSpecies = TSIESTA.number_of_species(filename)
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)
            MdSiestaFile = open(filename)
            speciesLabel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sl = []
            isSpesFinde = 0
            isSpesF = 0
            str1 = MdSiestaFile.readline()
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (
                        isSpesF == 0):
                    str1 = MdSiestaFile.readline()
                    while str1.find('siesta') >= 0:
                        str1 = Helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = MdSiestaFile.readline()
                    isSpesF = 1
                if (str1 != '') and (str1.find("ChemicalSpeciesLabel") >= 0) and (isSpesFinde == 0):
                    for i in range(0, NumberOfSpecies):
                        str1 = Helpers.spacedel(MdSiestaFile.readline())
                        S = str.split(str1, ' ')
                        speciesLabel[int(S[0])] = S[1]
                    isSpesFinde = 1

                atoms = []

                if (str1 != '') and (str1.find("Begin CG move") >= 0 or str1.find("Begin MD step") >= 0):
                    if (str1 != '') and str1.find("Begin MD step") >= 0:
                        for j in range(0, 3):
                            MdSiestaFile.readline()
                    else:
                        if str1.find("Begin CG move") >= 0:
                            while (str1 != '') and (str1.find("block") == -1) and (str1.find("outcoor") == -1):
                                str1 = MdSiestaFile.readline()

                    atoms = []
                    for i1 in range(0, NumberOfAtoms):
                        str1 = Helpers.spacedel(MdSiestaFile.readline())
                        S = str1.split(' ')
                        d1 = float(S[0])
                        d2 = float(S[1])
                        d3 = float(S[2])
                        Charge = speciesLabel[sl[len(atoms)]]
                        C = periodTable.get_let(Charge)
                        A = [d1, d2, d3, C, Charge]
                        atoms.append(A)
                    str1 = MdSiestaFile.readline()
                    while str1.find("outcell: Unit cell vectors (Ang):")==-1:
                        str1 = MdSiestaFile.readline()
                    vec1 = MdSiestaFile.readline().split()
                    vec1 = Helpers.list_str_to_float(vec1)
                    vec2 = MdSiestaFile.readline().split()
                    vec2 = Helpers.list_str_to_float(vec2)
                    vec3 = MdSiestaFile.readline().split()
                    vec3 = Helpers.list_str_to_float(vec3)
                    AllAtoms = TAtomicModel(atoms)
                    AllAtoms.set_lat_vectors(vec1, vec2, vec3)
                    molecules.append(AllAtoms)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
        return molecules

    @staticmethod
    def atoms_from_md_car(filename):
        """import from MD_CAR output """
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            str1 = struct_file.readline()
            while str1.find("---")>=0:
                newStr = TAtomicModel()
                LatConst = float(struct_file.readline())
                lat1 = Helpers.spacedel(struct_file.readline()).split()
                lat1 = Helpers.list_str_to_float(lat1)
                lat1 = LatConst*np.array(lat1)
                lat2 = Helpers.spacedel(struct_file.readline()).split()
                lat2 = Helpers.list_str_to_float(lat2)
                lat2 = LatConst * np.array(lat2)
                lat3 = Helpers.spacedel(struct_file.readline()).split()
                lat3 = Helpers.list_str_to_float(lat3)
                lat3 = LatConst * np.array(lat3)
                NumbersOfAtoms = Helpers.spacedel(struct_file.readline()).split()
                NumbersOfAtoms = Helpers.list_str_to_int(NumbersOfAtoms)
                str1 = struct_file.readline()
                if Helpers.spacedel(str1) == "Direct":
                    for i in range(0,len(NumbersOfAtoms)):
                        for j in range(0, NumbersOfAtoms[i]):
                            row = Helpers.spacedel(struct_file.readline()).split()
                            row = Helpers.list_str_to_float(row)

                            let = "Direct"
                            charge = 200 + i
                            x = row[0]
                            y = row[1]
                            z = row[2]

                            newStr.add_atom(TAtom([x, y, z, let, charge]))
                    newStr.set_lat_vectors(lat1, lat2, lat3)
                    newStr.convert_from_direct_to_cart()
                    molecules.append(newStr)
        return molecules

    @staticmethod
    def atoms_from_output_optim(filename):
        """Return the relaxed AtList from output file"""
        NumberOfAtoms = TSIESTA.number_of_atoms(filename)
        NumberOfSpecies = TSIESTA.number_of_species(filename)
        Species = TSIESTA.Species(filename)

        AtList = []
        f1 = False
        f2 = False
        f3 = False
        n_vec = 0
        lat_vect_1 = ""
        lat_vect_2 = ""
        lat_vect_3 = ""

        for line in open(filename, 'r'):
            if (line.find("outcell: Unit cell vectors (Ang):") > -1):
                f2 = True
                n_vec = 0
            else:
                if (n_vec == 0) and (f2 == True):
                    lat_vect_1 = line.split()
                    lat_vect_1 = Helpers.list_str_to_float(lat_vect_1)
                if (n_vec == 1) and (f2 == True):
                    lat_vect_2 = line.split()
                    lat_vect_2 = Helpers.list_str_to_float(lat_vect_2)
                if (n_vec == 2) and (f2 == True):
                    lat_vect_3 = line.split()
                    lat_vect_3 = Helpers.list_str_to_float(lat_vect_3)
                    f2 = False
                if f2 == True:
                    n_vec += 1

            if (line.find("outcoor: Relaxed atomic coordinates (Ang)") > -1):
                f1 = True
            else:
                if (len(AtList) < NumberOfAtoms) and (f1 == True):
                    line1 = line.split()
                    line2 = [float(line1[0]), float(line1[1]), float(line1[2]), line1[5], Species[int(line1[3]) - 1][1]]
                    AtList.append(line2)
                if len(AtList) == NumberOfAtoms:
                    f1 = False
                    AllAtoms = TAtomicModel(AtList)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    return [AllAtoms]
            if (line.find("outcoor: Relaxed atomic coordinates (fractional)") > -1):
                f3 = True
            else:
                if (len(AtList) < NumberOfAtoms) and (f3 == True):
                    line1 = line.split()
                    line2 = [float(line1[0]), float(line1[1]), float(line1[2]), line1[5], Species[int(line1[3]) - 1][1]]
                    AtList.append(line2)
                if len(AtList) == NumberOfAtoms:
                    f3 = False
                    AllAtoms = TAtomicModel(AtList)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    AllAtoms.convert_from_direct_to_cart()
                    return [AllAtoms]
        return []

    @staticmethod
    def atoms_from_POSCAR(filename):
        """import from xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            str1 = Helpers.spacedel(struct_file.readline())
            latConst = float(Helpers.spacedel(struct_file.readline()))
            lat1 = Helpers.spacedel(struct_file.readline()).split()
            lat1 = np.array(Helpers.list_str_to_float(lat1))*latConst
            lat2 = Helpers.spacedel(struct_file.readline()).split()
            lat2 = np.array(Helpers.list_str_to_float(lat2))*latConst
            lat3 = Helpers.spacedel(struct_file.readline()).split()
            lat3 = np.array(Helpers.list_str_to_float(lat3))*latConst
            SortsOfAtoms = Helpers.spacedel(struct_file.readline()).split()
            NumbersOfAtoms = Helpers.spacedel(struct_file.readline()).split()
            NumbersOfAtoms = Helpers.list_str_to_int(NumbersOfAtoms)
            NumberOfAtoms = 0
            for number in NumbersOfAtoms:
                NumberOfAtoms+=number

            if Helpers.spacedel(struct_file.readline()).lower() == "direct":
                newStr = TAtomicModel()
                for i in range(0, len(NumbersOfAtoms)):
                    number = NumbersOfAtoms[i]
                    for j in range(0, number):
                        str1 = Helpers.spacedel(struct_file.readline())
                        S = str1.split(' ')
                        x = float(S[0])
                        y = float(S[1])
                        z = float(S[2])
                        charge = periodTable.get_charge_by_letter(SortsOfAtoms[i])
                        let = SortsOfAtoms[i]
                        newStr.add_atom(TAtom([x, y, z, let, charge]))
                newStr.set_lat_vectors(lat1, lat2, lat3)
                newStr.convert_from_direct_to_cart()
                molecules.append(newStr)
        return molecules


    @staticmethod
    def atoms_from_struct_out(filename):
        """import from STRUCT_OUT file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            lat1 = Helpers.spacedel(struct_file.readline()).split()
            lat1 = Helpers.list_str_to_float(lat1)
            lat2 = Helpers.spacedel(struct_file.readline()).split()
            lat2 = Helpers.list_str_to_float(lat2)
            lat3 = Helpers.spacedel(struct_file.readline()).split()
            lat3 = Helpers.list_str_to_float(lat3)
            NumberOfAtoms = int(struct_file.readline())

            newStr = TAtomicModel()
            for i1 in range(0, NumberOfAtoms):
                str1 = Helpers.spacedel(struct_file.readline())
                S = str1.split(' ')
                x = float(S[2])
                y = float(S[3])
                z = float(S[4])
                charge = int(S[1])
                let = periodTable.get_let(charge)
                newStr.add_atom(TAtom([x, y, z, let, charge]))
            newStr.set_lat_vectors(lat1,lat2,lat3)
            newStr.convert_from_direct_to_cart()
            molecules.append(newStr)
        return molecules

    @staticmethod
    def atoms_from_xyz(filename):
        """import from xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            NumberOfAtoms = int(f.readline())
            newModel = TAtomicModel.atoms_from_xyz_structure(NumberOfAtoms, f, periodTable)
            molecules.append(newModel)
        return molecules

    @staticmethod
    def atoms_from_XMOLxyz(filename):
        """import from XMOL xyz file"""
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            NumberOfAtoms = int(f.readline())
            newModel = TAtomicModel.atoms_from_xyz_structure(NumberOfAtoms, f, periodTable, [1,2,3,4])
            molecules.append(newModel)
        return molecules



    @staticmethod
    def atoms_from_xyz_structure(NumberOfAtoms, ani_file, periodTable, indexes = [0,1,2,3]):
        if indexes[0] == 0:
            str1 = Helpers.spacedel(ani_file.readline())
        atoms = []
        for i1 in range(0, NumberOfAtoms):
            str1 = Helpers.spacedel(ani_file.readline())
            S = str1.split(' ')
            d1 = float(S[indexes[1]])
            d2 = float(S[indexes[2]])
            d3 = float(S[indexes[3]])
            C = S[indexes[0]]
            Charge = periodTable.get_charge_by_letter(C)
            A = [d1, d2, d3, C, Charge]
            atoms.append(A)
        newModel = TAtomicModel(atoms)
        newModel.set_lat_vectors_default()
        return newModel



    def get_LatVect1_norm(self):
        return norm(self.LatVect1)

    def get_LatVect2_norm(self):
        return norm(self.LatVect2)

    def get_LatVect3_norm(self):
        return norm(self.LatVect3)

    def get_angle_alpha(self):
        a = self.get_LatVect2_norm()
        b = self.get_LatVect3_norm()
        ab = self.LatVect2[0]*self.LatVect3[0] + self.LatVect2[1]*self.LatVect3[1] + self.LatVect2[2]*self.LatVect3[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def get_angle_beta(self):
        a = self.get_LatVect1_norm()
        b = self.get_LatVect3_norm()
        ab = self.LatVect1[0]*self.LatVect3[0] + self.LatVect1[1]*self.LatVect3[1] + self.LatVect1[2]*self.LatVect3[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def get_angle_gamma(self):
        a = self.get_LatVect2_norm()
        b = self.get_LatVect1_norm()
        ab = self.LatVect2[0]*self.LatVect1[0] + self.LatVect2[1]*self.LatVect1[1] + self.LatVect2[2]*self.LatVect1[2]
        angle = math.acos(ab/(a*b))
        return 180*angle/math.pi

    def set_lat_vectors(self, v1, v2, v3):
        if (len(v1) == 3) and (len(v2) == 3) and (len(v3) == 3):
            self.LatVect1 = np.array(v1)
            self.LatVect2 = np.array(v2)
            self.LatVect3 = np.array(v3)
        else:
            print("Wrong vectors")

    def set_lat_vectors_default(self):
        self.LatVect1 = np.array([ 1.4*self.sizeX(), 0, 0 ])
        self.LatVect2 = np.array([ 0, 1.4*self.sizeY(), 0 ])
        self.LatVect3 = np.array([ 0, 0, 1.4*self.sizeZ() ])

    def delete_atom(self, ind):
        if (ind>=0) and (ind<self.nAtoms()):
            self.atoms.pop(ind)
            self.FindBonds()

    def add_atom(self, atom, minDist = 0):
        """ Adds atom to the molecule is minimal distance to other atoms more then minDist """
        Dist = 10000
        if minDist > 0:
            model = TAtomicModel(self.atoms)
            model.set_lat_vectors(self.LatVect1, self.LatVect2, self.LatVect3)
            model.add_atom(atom)
            for ind in range(0, len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms) - 1)
                if r < Dist:
                    Dist = r

        if Dist>minDist:
            newAt = deepcopy(atom)
            self.atoms.append(newAt)

    def add_atomic_model(self, atomic_model, minDist = 0):
        for at in atomic_model:
            self.add_atom(at, minDist)

    def edit_atom(self, ind, newAtom):
        if (ind>=0) and (ind<self.nAtoms()):
            self.atoms[ind] = newAtom

    def add_atoms_property(self, prop, charge_voronoi):
        if self.nAtoms() == len(charge_voronoi):
            for i in range(0, self.nAtoms()):
                self.atoms[i].setProperty(prop, charge_voronoi[i])

    def AddBond(self, bond):
        self.bonds.append(bond)

    def nBonds(self):
        return len(self.bonds)

    def FindBonds(self):
        self.bonds = []
        Mendeley = TPeriodTable()
        for i in range(0, len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                r = math.sqrt(
                    math.pow(self.atoms[i].x - self.atoms[j].x, 2) + math.pow(self.atoms[i].y - self.atoms[j].y,
                                                                              2) + math.pow(
                        self.atoms[i].z - self.atoms[j].z, 2))
                rTab = Mendeley.Bonds[self.atoms[i].charge][self.atoms[j].charge]
                if r < 1.2 * rTab:
                    self.bonds.append([i, j])

    def __getitem__(self, i):
        return self.atoms[i]

    def ModifyAtomsTypes(self, changes):
        Mendeley = TPeriodTable()
        for change in changes:
            let = change[1]
            charge = Mendeley.get_charge_by_letter(let)

            old_charge = change[0]

            for atom in self.atoms:
                if atom.charge == old_charge:
                    atom.charge = charge
                    atom.let = let

    def nAtoms(self):
        return len(self.atoms)
    
    def centr_mass(self, charge=0):
        """The method returns the center of mass of the molecule"""
        cx= 0
        cy= 0
        cz= 0
        n = 0
        
        if (charge==0):
            Mendeley = TPeriodTable()
            for j in range(0, len(self.atoms)):
                m = Mendeley.Atoms[self.atoms[j].charge].mass
                cx+=self.atoms[j].x*m
                cy+=self.atoms[j].y*m
                cz+=self.atoms[j].z*m
                n+=m
        else:
            for j in range(0, len(self.atoms)):
                if (int(self.atoms[j].charge) == int(charge)):
                    cx+=self.atoms[j].x
                    cy+=self.atoms[j].y
                    cz+=self.atoms[j].z
                    n+=1
        
        return [cx/n,cy/n,cz/n]

    def reformat(self,charge):
        """The half of molecule moves"""        
        for j in range(0, len(self.atoms)):
            if (int(self.atoms[j].charge) == int(charge)):
                if (self.atoms[j].z<0):
                    self.atoms[j].z+=self.boxZ
        return self


    def rotateX(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha*= math.pi / 180
        # ox
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].y) * math.cos(alpha) - float(self.atoms[i].z) * math.sin(alpha)
            ynn = float(self.atoms[i].y) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].y = xnn
            self.atoms[i].z = ynn

    def rotateY(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha*= math.pi / 180
        # oy
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) + float(self.atoms[i].z) * math.sin(alpha)
            ynn = -float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].z = ynn

    def rotateZ(self, alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        alpha*= math.pi / 180
        # oz
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) - float(self.atoms[i].y) * math.sin(alpha)
            ynn = float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].y) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].y = ynn
        
    def ProjectionToCylinder(self,atomslist,radius):
        """This method returns projections on cylinder with radius for atom at"""
        row = []
        for at in range(0,len(atomslist)):
            x = float(self.atoms[atomslist[at]].x)
            y = float(self.atoms[atomslist[at]].y)
            z = float(self.atoms[atomslist[at]].z)
            ro = math.sqrt(math.pow(x,2)+math.pow(y,2))
            fi = math.atan(x/y)
            row.append([atomslist[at],x*radius/ro,y*radius/ro,z,ro,fi])    
        return row

    def indexes_of_atoms_with_charge(self, charge):
        """ IndexesOfAtomsWithCharge """
        Indexes = []
        for j in range(0, len(self.atoms)):
            if (int(self.atoms[j].charge) == int(charge)):
                Indexes.append(j)
        return Indexes

    def indexes_of_atoms_in_ball(self, ats, atom, R):
        """ Indexes of atoms in the ball of radius R with center on atom 'atom'
        ats - list of indexes
        atom- index of atom in the center of ball
        """
        newatoms = [atom]
        for at in ats:
            if at!=atom:
                if self.atom_atom_distance(at, atom) < R:
                    newatoms.append(at)
        return newatoms

    def convert_from_scaled_to_cart(self, lat):
        for atom in self.atoms:
            atom.x *= lat
            atom.y *= lat
            atom.z *= lat

    def convert_from_direct_to_cart(self):
        for atom in self.atoms:
            x = atom.x * self.LatVect1[0] + atom.y * self.LatVect2[0] + atom.z * self.LatVect3[0]
            y = atom.x * self.LatVect1[1] + atom.y * self.LatVect2[1] + atom.z * self.LatVect3[1]
            z = atom.x * self.LatVect1[2] + atom.y * self.LatVect2[2] + atom.z * self.LatVect3[2]
            atom.x = x
            atom.y = y
            atom.z = z

    def convert_from_cart_to_direct(self):
        SysCoord = np.array([self.LatVect1, self.LatVect2, self.LatVect3])
        obr = np.linalg.inv(SysCoord).transpose()

        for atom in self.atoms:
            Coord = np.array([atom.x, atom.y, atom.z])
            res = obr.dot(Coord)
            atom.x = res[0]
            atom.y = res[1]
            atom.z = res[2]

    def minX(self):
        """ минимальная координата по оси X """
        minx = self.atoms[0].x
        for atom in self.atoms:
            if (float(atom.x) < float(minx)):
                minx = atom.x
        return float(minx)

    def maxX(self):
        """ максимальная координата по оси X """
        maxx = self.atoms[0].x
        for atom in self.atoms:
            if atom.x > maxx:
                maxx = atom.x
        return maxx

    def sizeX(self):
        """ длина молекулы по оси X """
        return self.maxX() - self.minX()

    def minY(self):
        """ минимальная координата по оси Y """
        miny = self.atoms[0].y

        for atom in self.atoms:
            if (float(atom.y) < float(miny)):
                miny = atom.y
        return float(miny)

    def maxY(self):
        """ максимальная координата по оси Y """
        maxy = self.atoms[0].y

        for atom in self.atoms:
            if (float(atom.y) > float(maxy)):
                maxy = atom.y
        return float(maxy)

    def sizeY(self):
        """ длина молекулы по оси Y """
        return self.maxY() - self.minY()

    def minZ(self):
        """ минимальная координата по оси Z """
        minz = self.atoms[0].z
        
        for atom in self.atoms:
            if (float(atom.z)<float(minz)):
                minz = atom.z
        return float(minz)        

    def maxZ(self):
        """ максимальная координата по оси Z """
        maxz = self.atoms[0].z
        
        for atom in self.atoms:
            if (float(atom.z)>float(maxz)):
                maxz = atom.z
        return float(maxz)
        
    def sizeZ(self):
        """ длина молекулы по оси Z """
        return self.maxZ() - self.minZ()

    def sort_atoms_by_type(self):
        #atom = TAtom()
        for i in range(0, self.nAtoms()):
            for j in range(0, self.nAtoms()-i-1):
                if self.atoms[j].charge > self.atoms[j+1].charge:
                    atom = self.atoms[j]
                    self.atoms[j] = self.atoms[j+1]
                    self.atoms[j+1] = atom

    def AngleToCenterOfAtoms(self, atomslist):
        """The method AngleToCenterOfAtoms returns the Angle To Center Of atoms_from_fdf list atomslist in the molecule"""
        angle = 0

        for at in range(0, len(atomslist)):
            x = self.atoms[atomslist[at]].x
            y = self.atoms[atomslist[at]].y
            fi = math.atan(x / y)
            angle += fi
        angle /= len(atomslist)
        return angle

        
    def atom_atom_distance(self, at1, at2):
        """ atom_atom_distance
        All atoms MUST be in the Cell!!!
        """
        pos1 = np.array([self.atoms[at1].x, self.atoms[at1].y, self.atoms[at1].z])
        pos2 = np.array([self.atoms[at2].x, self.atoms[at2].y, self.atoms[at2].z])

        ro = norm(pos2 - pos1)
        values = [-1, 0, 1]
        for i in values:
            for j in values:
                for k in values:
                    if abs(i)+abs(j)+abs(k)!=0:
                        ro1 = norm(pos2 - pos1 + i*self.LatVect1 + j*self.LatVect2 + k*self.LatVect3)
                        if ro1 < ro:
                            ro = ro1
        return ro

    def move_atoms_to_cell(self):
        """ ... """
        a = np.array([self.LatVect1, self.LatVect2, self.LatVect3])
        ainv = inv(a)

        for at in self.atoms:
            pos = np.array([at.x, at.y, at.z])
            b = pos.transpose()
            total = ainv.dot(b)
            pos -= math.trunc(total[0]) * self.LatVect1 + math.trunc(total[1]) * self.LatVect2 + math.trunc(total[2]) * self.LatVect3
            at.x = pos[0]
            at.y = pos[1]
            at.z = pos[2]

    def Neighbors(self,atom,col,charge):
        """ Look for col neighbors of atom "atom" with a charge "charge" """
        neighbor = []
        for at in range(0, len(self.atoms)):
            if ((at != atom) and (int(self.atoms[at].charge) == int(charge))):
                r = self.atom_atom_distance(atom, at)
                neighbor.append([at,r])
        fl = 1
        while (fl == 1):
            fl = 0
            for i in range(len(neighbor)-1,0,-1):
                if (neighbor[i-1][1]>neighbor[i][1]):
                    at = copy.deepcopy(neighbor[i])
                    neighbor[i] = copy.deepcopy(neighbor[i-1])
                    neighbor[i-1] = copy.deepcopy(at)
                    fl = 1
        neighbo = []                
        neighbo.append(neighbor[0][0])
        for i in range(1,col):
            neighbo.append(neighbor[i][0])
        return neighbo

    def Bonds(self):
        """The method returns list of bonds of the molecule"""
        PeriodTable = TPeriodTable()
        bond = []
        for i in range(0, len(self.atoms)):
            for j in range(i+1, len(self.atoms)):
                length = round(self.atom_atom_distance(i, j),4)
                t1 = int(self.atoms[i].charge)
                t2 = int(self.atoms[j].charge)
                if (math.fabs(length - PeriodTable.Bonds[t1][t2]) < 0.2*PeriodTable.Bonds[t1][t2]):
                    bond.append([t1, t2, length, self.atoms[i].let, i, self.atoms[j].let, j])
        return bond
    
    def Delta(self, newMolecula):
        """ maximum distance from atoms in self to the atoms in the newMolecula"""
        DeltaMolecula1 = 0
        r1 = norm(self.LatVect1) + norm(self.LatVect2) + norm(self.LatVect3)
        for at2 in newMolecula.atoms:
            model = TAtomicModel(self.atoms)
            model.add_atom(at2)
            for ind in range(0,len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms)-1)
                if r < r1:
                    r1 = r
            if r1>DeltaMolecula1:
                DeltaMolecula1 = r1
        return DeltaMolecula1

    def DeltaMin(self, newMolecula):
        """ minimum distance from atoms in self to the atoms in the newMolecula"""
        DeltaMolecula1 = 100000
        r1 = norm(self.LatVect1) + norm(self.LatVect2) + norm(self.LatVect3)
        for at2 in newMolecula.atoms:
            model = TAtomicModel(self.atoms)
            model.add_atom(at2)
            for ind in range(0,len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms)-1)
                if r < r1:
                    r1 = r
            if r1<DeltaMolecula1:
                DeltaMolecula1 = r1
        return DeltaMolecula1


    def GoToPositiveCoordinates(self):
        xm = self.minX()
        ym = self.minY()
        zm = self.minZ()
        for i in range(0, self.nAtoms()):
            self.atoms[i].x -= xm
            self.atoms[i].x += 0.1
            self.atoms[i].y -= ym
            self.atoms[i].y += 0.1
            self.atoms[i].z -= zm
            self.atoms[i].z += 0.1

    def grow(self):
        """ модель транслируется в трех измерениях и становится в 27 раз больше """
        newAtList = deepcopy(self.atoms)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if abs(i)+abs(j)+abs(k)!=0:
                        vect = i * self.LatVect1 + j * self.LatVect2 + k * self.LatVect3
                        copyOfModel = TAtomicModel(self.atoms)
                        copyOfModel.move(vect[0], vect[1], vect[2])
                        for atom in copyOfModel.atoms:
                            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        v1 = 3 * self.LatVect1
        v2 = 3 * self.LatVect2
        v3 = 3 * self.LatVect3
        newModel.set_lat_vectors(v1,v2,v3)
        return newModel

    def growX(self):
        """ модель транслируется в измерении X """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect1
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        v1 = 2 * self.LatVect1
        v2 = self.LatVect2
        v3 = self.LatVect3
        newModel.set_lat_vectors(v1,v2,v3)
        return newModel

    def growY(self):
        """ модель транслируется в измерении X """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect2
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        v1 = self.LatVect1
        v2 = 3 * self.LatVect2
        v3 = self.LatVect3
        newModel.set_lat_vectors(v1,v2,v3)
        return newModel

    def growZ(self):
        """ модель транслируется в измерении X """
        newAtList = deepcopy(self.atoms)
        vect = self.LatVect3
        copyOfModel = TAtomicModel(self.atoms)
        copyOfModel.move(vect[0], vect[1], vect[2])
        for atom in copyOfModel.atoms:
            newAtList.append(atom)
        newModel = TAtomicModel(newAtList)
        v1 = self.LatVect1
        v2 = self.LatVect2
        v3 = 3 * self.LatVect3
        newModel.set_lat_vectors(v1,v2,v3)
        return newModel
        
    def move(self, Lx, Ly, Lz):
        """ смещает модель на указанный вектор """
        for atom in self.atoms:
            atom.x+=Lx
            atom.y+=Ly
            atom.z+=Lz
        return self.atoms
    
    def typesOfAtoms(self):
        elements = np.zeros((200))
        for atom in self.atoms:
            elements[atom.charge]+=1
        types = []
        for i in range(0,200):
            if elements[i] > 0:
                types.append([i,elements[i]])            
        return types
    
    def toSIESTAfdf(self, filename):
        """ созадет входной файл для пакета SIESTA """
        f = open(filename,'w')
        text = self.toSIESTAfdfdata("Fractional", "LatticeVectors")
        print(text, file=f)
        f.close()
        
    def toSIESTAxyz(self, filename):
        """ созадет xyz файл, совместимый с XMol """
        f = open(filename,'w')
        text = self.toSIESTAxyzdata()
        print(text, file=f)
        f.close()     

    def toSIESTAfdfdata(self, coord_style, latt_style='LatticeParameters'):
        """ возвращает данные для входного файла пакета SIESTA """
        data = ""
        PerTab = TPeriodTable()
        data += 'NumberOfAtoms ' + str(len(self.atoms)) + "\n"
        types = self.typesOfAtoms()
        data += 'NumberOfSpecies ' + str(len(types)) + "\n"
        data += '%block ChemicalSpeciesLabel\n'
        for i in range(0, len(types)):
            data += ' ' + str(i + 1) + '  ' + str(types[i][0]) + '  ' + str(PerTab.get_let(int(types[i][0]))) + "\n"
        data += '%endblock ChemicalSpeciesLabel\n'

        # LatticeConstant
        data +='LatticeConstant       1.0 Ang\n'

        if latt_style=='LatticeParameters':
            data += '%block LatticeParameters\n'
            data += '  '+str(self.get_LatVect1_norm())+'  '+str(self.get_LatVect2_norm())+'  '+str(self.get_LatVect3_norm()) + '  '+str(self.get_angle_alpha())+'  '+ str(self.get_angle_beta()) +'  '+  str(self.get_angle_gamma()) +   '\n'
            data += '%endblock LatticeParameters\n'
        #or
        if latt_style=='LatticeVectors':
            data += '%block LatticeVectors\n'
            data += '  ' + str(self.LatVect1[0]) + '  ' + str(self.LatVect1[1]) + '  ' + str(self.LatVect1[2]) + '\n'
            data += '  ' + str(self.LatVect2[0]) + '  ' + str(self.LatVect2[1]) + '  ' + str(self.LatVect2[2]) + '\n'
            data += '  ' + str(self.LatVect3[0]) + '  ' + str(self.LatVect3[1]) + '  ' + str(self.LatVect3[2]) + '\n'
            data += '%endblock LatticeVectors\n'

        if coord_style == "Zmatrix Cartesian":
            data += 'AtomicCoordinatesFormat NotScaledCartesianAng\n'
            data+='%block Zmatrix\n'
            data+='cartesian\n'
            data += self.coords_for_export(coord_style)
            data+='%endblock Zmatrix\n'

        if coord_style == "Fractional":
            self.sort_atoms_by_type()
            self.GoToPositiveCoordinates()
            self.convert_from_cart_to_direct()
            data += 'AtomicCoordinatesFormat Fractional\n'
            data += '%block AtomicCoordinatesAndAtomicSpecies\n'
            data += self.coords_for_export(coord_style)
            data += '%endblock AtomicCoordinatesAndAtomicSpecies\n'
        return data

    def toXSFfile(self, fname, volumeric_data):
        f = open(fname+".XSF", 'w')
        text = "ATOMS\n"
        for atom in self.atoms:
            text += " " + str(atom.charge) + "    " + str(atom.x) + "    " + str(atom.y) + "    " + str(atom.z) + "\n"

        text += "BEGIN_BLOCK_DATAGRID_3D\n "
        text += "  DATA_from:GUI4DFT_diff\n"
        text += "  BEGIN_DATAGRID_3D_RHO:spin_1\n"
        text += " " + str(volumeric_data.Nx) + " " + str(volumeric_data.Ny) + " " + str(volumeric_data.Nz) + "\n"
        text += " " + str(volumeric_data.origin[0]) + " " + str(volumeric_data.origin[1]) + " " + str(volumeric_data.origin[2]) + "\n"

        text += " " + str(self.LatVect1[0]) + "   " + str(self.LatVect1[1]) + "   " + str(self.LatVect1[2]) + "\n"
        text += " " + str(self.LatVect2[0]) + "   " + str(self.LatVect2[1]) + "   " + str(self.LatVect2[2]) + "\n"
        text += " " + str(self.LatVect3[0]) + "   " + str(self.LatVect3[1]) + "   " + str(self.LatVect3[2]) + "\n"

        orderData = 'F'

        N = int(volumeric_data.Nx) * int(volumeric_data.Ny) * int(volumeric_data.Nz)

        data3D = np.reshape(volumeric_data.data3D, int(N), orderData)

        for i in range(0, N):
            text += str(data3D[i]) +"   "

        text += "\n"

        text += " END_DATAGRID_3D\n"
        text += "END_BLOCK_DATAGRID_3D\n"
        print(text, file=f)
        f.close()

    def coords_for_export(self, coord_style):
        data = ""
        types = self.typesOfAtoms()
        if coord_style == "Fractional":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                str2 = '    ' + str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
                data += str2 + str1 + "\n"

        if coord_style == "FractionalPOSCAR":
            for i in range(0, len(self.atoms)):
                data += '    ' + str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))+ "\n"

        if coord_style == "Zmatrix Cartesian":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0,len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j+1)
                str2 = '    ' + str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
                str3 = '      1  1  1'
                data+= str1+str2+str3+"\n"

        if coord_style == "FireflyINP":
            for i in range(0, len(self.atoms)):
                str1 = ' ' + str(self.atoms[i].let) + '   ' + str(self.atoms[i].charge) + '.0  '
                str2 = '    ' + str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
                data+= str1+str2+"\n"
            data+= ' $END'
        return data

    def toSIESTAxyzdata(self):
        """ возвращает данные для xyz файла """
        data = "  "
        nAtoms = self.nAtoms()
        data+= str(nAtoms) + "\n"
        for i in range(0, nAtoms):
            data+= "\n"+self.atoms[i].let + '       '+ str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
        return data

    def toFireflyINP(self, filename):
        """ create file in Firefly *.inp format """
        f = open(filename, 'w')
        data = ""
        data += "!model \n $DATA\njob\nCn 1\n\n"
        data += self.coords_for_export("FireflyINP")

        print(data, file=f)
        f.close()

    def toVASPposcar(self, filename):
        """ create file in VASP POSCAR format """
        f = open(filename, 'w')

        data = ""
        data += "model \n"
        data +=' 1.0 \n'

        data += '  ' + str(self.LatVect1[0]) + '  ' + str(self.LatVect1[1]) + '  ' + str(self.LatVect1[2]) + '\n'
        data += '  ' + str(self.LatVect2[0]) + '  ' + str(self.LatVect2[1]) + '  ' + str(self.LatVect2[2]) + '\n'
        data += '  ' + str(self.LatVect3[0]) + '  ' + str(self.LatVect3[1]) + '  ' + str(self.LatVect3[2]) + '\n'

        PerTab = TPeriodTable()

        types = self.typesOfAtoms()
        for i in range(0, len(types)):
            data += ' ' +  str(PerTab.get_let(int(types[i][0])))
        data += "\n"

        for i in range(0, len(types)):
            count = 0
            for atom in self.atoms:
                if atom.charge == int(types[i][0]):
                    count+=1
            data += ' ' +  str(count)
        data += "\n"

        data += "Direct\n"

        self.sort_atoms_by_type()
        self.GoToPositiveCoordinates()
        self.convert_from_cart_to_direct()
        data += self.coords_for_export("FractionalPOSCAR")

        print(data, file=f)
        f.close()
  
##################################################################
########################### TSWNT ################################
##################################################################    

class TSWNT(TAtomicModel):
    """The TSWNT class provides """
    def __init__(self, n, m, leng = 0, ncell = 1, type = 0):
        TAtomicModel.__init__(self)
        maxMol = 1000000
        pi = math.pi
        px = np.zeros(maxMol)
        py = np.zeros(maxMol)
        pz = np.zeros(maxMol)
        qx = np.zeros(maxMol)
        qy = np.zeros(maxMol)
        qz = np.zeros(maxMol)
        hx = np.zeros(6)
        hy = np.zeros(6)
        hz = np.zeros(6)
        #ifp = np.zeros(maxMol)
        a = 1.43
        nx = 40
        ny = 100

        if (leng == 0):
            leng = ncell*TSWNT.unitlength(n, m, a)

        rad = TSWNT.radius(n, m)
        self.set_lat_vectors([10*rad,0,0],[0, 10*rad, 0], [0, 0, leng])
        """ calculations """
        """ definition of a hexagon """
        hx[0] = a
        hy[0] = 0.0
        hz[0] = 0.0  
        for i in range(1, 6):
            hx[i] = hx[i - 1] * math.cos(pi/3) - hy[i - 1] * math.sin(pi/3)
            hy[i] = hx[i - 1] * math.sin(pi/3) + hy[i - 1] * math.cos(pi/3)
            hz[i] = 0.0
            
        for k_par in range(0, nx):
            hx_plus = 3 * a * k_par
            for ih_par in range(0, 4):
                i_par = ih_par + k_par * 4
                px[i_par] = hx[ih_par] + hx_plus
                py[i_par] = hy[ih_par]
                pz[i_par] = hz[ih_par]
            
        np1 = (nx - 1) * (nx - 1) + 4
        px_minus = (nx - 1.0) / 2.0 * 3 * a
        for i_par in range(0, np1):
            px[i_par] -= px_minus
            
        for k_par in range(0, ny):
            py_plus = math.sqrt(3.0) * a * k_par
            for i_par in range(0, np1):
                j1 = i_par + k_par * np1
                px[j1] = px[i_par]
                py[j1] = py[i_par] + py_plus
                pz[j1] = pz[i_par]
        np1 = np1 - 1 + (ny - 1) * np1
        
        """ centering y """
        py_minus = (ny - 0.5) / 2.0 * math.sqrt(3.0) * a
        for i_par in range(0, np1):
            py[i_par] -= py_minus 
            
        """ Rotate for (m,ch_m) vector """
        vx = (n + m) * 3.0 / 2.0 * a
        vy = (n - m) * math.sqrt(3.0) / 2.0 * a
        vlen = math.sqrt(vx * vx + vy * vy)

        """ Rotation  """
        for i_par in range(0, np1):
            tempx_par = px[i_par]
            tempy_par = py[i_par]
            px[i_par] =  tempx_par * vx / vlen + tempy_par * vy / vlen
            py[i_par] = -tempx_par * vy / vlen + tempy_par * vx / vlen
        """ Rotation is done """
            
        """ trimming """
        j = 0
            
        for i in range(0, np1):
            if (px[i] <= vlen / 2.0 * 1.00001) and (px[i] > -vlen / 2.0 * 0.99999) and (py[i] <= leng / 2.0) and (py[i] > -leng / 2.0):
                px[j] = px[i]
                py[j] = py[i]
                pz[j] = pz[i]
                j+=1
        np1 = j
        
        """ output """
        leng = vlen
        R = leng / (2 * pi)
        
        for i_par in range(0, np1):
            phi_par = px[i_par] / R
            qx[i_par] = R * math.sin(phi_par)
            qy[i_par] = -R * math.cos(phi_par)
            qz[i_par] = py[i_par]
            self.add_atom(TAtom([qx[i_par], qy[i_par], qz[i_par], "C", 6]))


    @staticmethod
    def radius(n, m):
        return math.sqrt(n*n + n*m +m*m)

    @staticmethod
    def unitlength(n, m, acc): 
        a = math.sqrt(3) * acc
        pi = math.pi
        
        b1x = 2 * pi / a / math.sqrt(3)
        b1y = 2 * pi / a
        b2x = 2 * pi / a / math.sqrt(3)
        b2y = -2 * pi / a
        Ch = a * math.sqrt(n * n + n * m + m * m)
        dia = Ch / pi
        theta = math.atan((math.sqrt(3) * m / (2.0 * n + m)))
        theta = theta * 180.0 / pi
        d = Helpers.cdev(n, m)
        if ((n - m) % (3 * d) != 0):
            dR = d
        else:
            dR = 3 * d
        T1 = (2 * m + n) / dR
        T2 = -(2 * n + m) / dR
        T = math.sqrt(3) * Ch / dR
        return T

##################################################################
#########################  The SIESTA class ######################
##################################################################
    
class TSIESTA:

    @staticmethod
    def lattice_constant(filename):
        """ Returns the LatticeConstant from SIESTA output file """
        mult = 1
        latc = Helpers.fromFileProperty(filename,'LatticeConstant',1,'unformatted')
        if latc == None:
            return 1
        property = (latc).split()
        if property[1].lower() == "bohr":
            mult = 0.52917720859
        return mult*float(property[0])

    @staticmethod
    def lattice_parameters_abc_angles(filename):
        """ returns data from LatticeParameters block of file """
        LatticeParameters = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeParameters')
        LatConstant = float(TSIESTA.lattice_constant(filename))
        if len(LatticeParameters)>0:
            data = Helpers.spacedel(LatticeParameters[0]).split()
            a = LatConstant*float(data[0])
            b = LatConstant*float(data[1])
            c = LatConstant*float(data[2])
            alpha = math.radians(float(data[3]))
            beta = math.radians(float(data[4]))
            gamma = math.radians(float(data[5]))

            tm = math.pow(math.cos(alpha), 2) + math.pow(math.cos(beta), 2) + math.pow(math.cos(gamma), 2)
            tmp = math.sqrt(1 + 2 * math.cos(alpha) * math.cos(beta) * math.cos(gamma) - tm)
            h = c * tmp / math.sin(gamma)

            lat_vect_1 = [a, 0, 0]
            lat_vect_2 = [b * math.cos(gamma), b * math.sin(gamma), 0]
            lat_vect_3 = [c * math.cos(beta), c * math.cos(alpha) * math.sin(gamma), h]

            if lat_vect_2[0] < 1e-8: lat_vect_2[0] = 0
            if lat_vect_2[1] < 1e-8: lat_vect_2[1] = 0
            if lat_vect_3[0] < 1e-8: lat_vect_3[0] = 0
            if lat_vect_3[1] < 1e-8: lat_vect_3[1] = 0
            if lat_vect_3[2] < 1e-8: lat_vect_3[2] = 0

            return lat_vect_1, lat_vect_2, lat_vect_3
        else:
            return [False, False, False], [False, False, False], [False, False, False]

    @staticmethod
    def lattice_vectors(filename):
        LatConstant = float(TSIESTA.lattice_constant(filename))
        LatticeVectors = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeVectors')
        if len(LatticeVectors) > 0:
            lat_vect_1 = Helpers.spacedel(LatticeVectors[0]).split()
            lat_vect_1 = np.array(Helpers.list_str_to_float(lat_vect_1))
            lat_vect_2 = Helpers.spacedel(LatticeVectors[1]).split()
            lat_vect_2 = np.array(Helpers.list_str_to_float(lat_vect_2))
            lat_vect_3 = Helpers.spacedel(LatticeVectors[2]).split()
            lat_vect_3 = np.array(Helpers.list_str_to_float(lat_vect_3))
            return LatConstant*lat_vect_1, LatConstant*lat_vect_2, LatConstant*lat_vect_3
        return [False, False, False], [False, False, False], [False, False, False]

    @staticmethod
    def calc_pdos(root, atom_index, species, number_l, number_m, number_n, number_z):
        pdos = np.zeros((2, 1000))
        energy = np.zeros((1, 10))
        nspin = 1
        for child in root:
            if child.tag == "nspin":
                nspin = int(child.text)
            # print(child.tag)
            if child.tag == "energy_values":
                data = (child.text).split()
                data = Helpers.list_str_to_float(data)
                energy = np.array(data)
                pdos = np.zeros((nspin, len(energy)))

            if child.tag == "orbital":
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
                    #print(child.attrib['species'])
                    for children in child:
                        data = (children.text).split()
                        data = Helpers.list_str_to_float(data)
                        data = np.array(data)
                        data = data.reshape((nspin, len(energy)), order='F')
                        pdos += data
        return pdos, energy

    @staticmethod
    def ChargesSIESTA3(filename):
        """Заряды всех атомов в выходном файле SIESTA (Милликен)"""
        charges = []
        if os.path.exists(filename):
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)
            NumberOfSpecies = TSIESTA.number_of_species(filename)
            SpinPolarized = Helpers.fromFileProperty(filename, 'redata: SpinPolarized (Up/Down) run      =     ', 1,
                                                     'string')
            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            skip = 0
            step = 0

            if (SpinPolarized == 'T'):
                NumberOfSpecies *= 2
                NumberOfAtoms *= 2

            asl = 0
            while str1 != '':
                if str1 != '' and (str1.find("mulliken: Atomic and Orbital Populations:") >= 0):
                    nsp = 0
                    step += 1
                    charge = [step]
                    while nsp < NumberOfSpecies:
                        atoms = 0
                        while (str1.find("mulliken:") >= 0 or len(str1) < 2 or str1.find("Species:") >= 0):
                            if str1.find("Species:") >= 0:
                                str1 = Helpers.spacedel(str1)
                                nsp += 1
                                AtomSort = str1.split(' ')[1]
                            str1 = MdSiestaFile.readline()
                        neutral = 3
                        if (AtomSort == "C"):
                            skip = 2
                            neutral = 4
                            if (SpinPolarized == 'T'):
                                neutral = neutral / 2.0
                        if (AtomSort == "S"):
                            skip = 2
                            neutral = 6
                            if (SpinPolarized == 'T'):
                                neutral = neutral / 2.0
                        if (AtomSort == "Li") or (AtomSort == "H"):
                            skip = 1
                            neutral = 1
                            if (SpinPolarized == 'T'):
                                neutral = neutral / 2.0

                        for i in range(0, skip):
                            str1 = MdSiestaFile.readline()
                        ch = 0

                        while (str1 != '\n'):
                            for i in range(0, skip):
                                str1 = MdSiestaFile.readline()
                            if (str1 != '\n'):
                                atoms += 1
                                str1 = Helpers.spacedel(str1)
                                print(str1)
                                ch += neutral - float(str1.split(' ')[1])
                        charge.append(ch)
                        if (SpinPolarized == 'True'):
                            if (nsp > NumberOfSpecies / 2.0):
                                charge.append(charge[nsp / 2] + ch)
                    charges.append(charge)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
        return charges

    @staticmethod
    def get_charges_for_atoms(filename, method):
        charges = []
        if os.path.exists(filename):
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)

            searchSTR = ""
            if method == "Hirshfeld":
                searchSTR = "Hirshfeld Net Atomic Populations:"

            if method == "Voronoi":
                searchSTR = "Voronoi Net Atomic Populations:"

            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()

            while str1 != '':
                if str1 != '' and (str1.find(searchSTR) >= 0):
                    str1 = MdSiestaFile.readline()
                    for i in range(0, NumberOfAtoms):
                        str1 = Helpers.spacedel(MdSiestaFile.readline())
                        charges.append(float(str1.split(' ')[1]))
                str1 = MdSiestaFile.readline()
        MdSiestaFile.close()
        return charges

    @staticmethod
    def get_charges_voronoi_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Voronoi")

    @staticmethod
    def get_charges_hirshfeld_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Hirshfeld")

    @staticmethod
    def ChargesSIESTA4(filename, method):
        """Заряды всех атомов в выходном файле SIESTA (Hirshfeld, Voronoi, Mulliken)"""
        charges = []
        if os.path.exists(filename):
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)
            NumberOfSpecies = TSIESTA.number_of_species(filename)

            if method == "Mulliken":
                """Заряды всех атомов в выходном файле SIESTA4 (Милликен)"""
                SpinPolarized = int(Helpers.fromFileProperty(filename, 'redata: Number of spin components', 1, 'string').split("=")[1])

                MdSiestaFile = open(filename)
                str1 = MdSiestaFile.readline()
                skip = 0
                step = 0

                if (SpinPolarized == 2):
                    NumberOfSpecies *= 2
                    NumberOfAtoms *= 2

                asl = 0
                while str1 != '':
                    if str1 != '' and (str1.find("mulliken: Atomic and Orbital Populations:") >= 0):
                        nsp = 0
                        step += 1
                        charge = [step]
                        while nsp < NumberOfSpecies:
                            atoms = 0
                            while (str1.find("mulliken:") >= 0 or len(str1) < 2 or str1.find("Species:") >= 0):
                                if str1.find("Species:") >= 0:
                                    str1 = Helpers.spacedel(str1)
                                    nsp += 1
                                    AtomSort = str1.split(' ')[1]
                                str1 = MdSiestaFile.readline()
                            neutral = 3

                            base = []
                            #base.append([charge, letter, skip, neutral])
                            base.append([1, "H", 1, 1])
                            base.append([3, "Li", 1, 1])
                            base.append([6, "C", 2, 4])
                            base.append([13, "Al", 2, 3])
                            base.append([16, "S", 2, 6])
                            base.append([22, "Ti", 2, 4])
                            base.append([24, "Cr", 2, 6])
                            base.append([28, "Ni", 2, 10])
                            base.append([37, "Ru", 2, 8])
                            base.append([78, "Pt", 2, 10])

                            for i in range(0,len(base)):
                                if base[i][1] == AtomSort:
                                    skip = base[i][2]
                                    neutral = base[i][3]

                                    if(SpinPolarized == 2):
                                        neutral /= 2.0

                            str1 = MdSiestaFile.readline()

                            ch = 0

                            while (str1 != '\n'):
                                for i in range(0, skip):
                                    str1 = MdSiestaFile.readline()
                                if (str1 != '\n'):
                                    atoms += 1
                                    str1 = Helpers.spacedel(str1)
                                    ch += neutral - float(str1.split(' ')[1])

                            if (SpinPolarized == 2) and (nsp > NumberOfSpecies / 2.0):
                                charge[int(nsp / 2)] += ch
                            else:
                                charge.append(ch)
                        del charge[0]
                        charges.append(charge)
                    str1 = MdSiestaFile.readline()
                MdSiestaFile.close()
                return charges

            searchSTR = ""
            if method == "Hirshfeld":
                searchSTR = "Hirshfeld Net Atomic Populations:"

            if method == "Voronoi":
                searchSTR = "Voronoi Net Atomic Populations:"

            Species = TSIESTA.Species(filename)

            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()

            step = 0

            while str1 != '':
                if str1 != '' and (str1.find(searchSTR) >= 0):
                    str1 = MdSiestaFile.readline()
                    atoms = 0

                    charge = []

                    for i in range(0, NumberOfSpecies):
                        charge.append(0)

                    while atoms < NumberOfAtoms:
                        atoms = atoms + 1
                        str1 = Helpers.spacedel(MdSiestaFile.readline())
                        AtomSort = str1.split(' ')[2]

                        ind = -1
                        for i in range(0, NumberOfSpecies):
                            if Species[i][2] == AtomSort:
                                ind = int(Species[i][0]) - 1

                        charge[ind] += float(str1.split(' ')[1])
                    charges.append(charge)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
        return charges

    @staticmethod
    def ChargesSIESTA4Hirshfeld(filename):
        """Заряды всех атомов в выходном файле SIESTA (Hirshfeld)"""
        return TSIESTA.ChargesSIESTA4(filename, "Hirshfeld")

    @staticmethod
    def ChargesSIESTA4Voronoi(filename):
        """Заряды всех атомов в выходном файле SIESTA (Voronoi)"""
        return TSIESTA.ChargesSIESTA4(filename, "Voronoi")

    @staticmethod
    def ChargesSIESTA4Mulliken(filename):
        """Заряды всех атомов в выходном файле SIESTA (Mulliken)"""
        return TSIESTA.ChargesSIESTA4(filename, "Mulliken")

    @staticmethod
    def DOSsiesta(filename):
        """DOS"""
        if os.path.exists(filename):
            DOSFile = open(filename)
            strDOS = DOSFile.readline()
            energy = []
            spinUp = []
            spinDown = []
            while strDOS!='':
                line = strDOS.split(' ')
                line1 = []
                for i in range(0, len(line)):
                    if line[i] != '':
                        line1.append(line[i])
                energy.append(float(line1[0]))
                spinUp.append(float(line1[1]))
                if len(line1)>2:
                    spinDown.append(float(line1[2]))
                else:
                    spinDown.append(0)
                strDOS = DOSFile.readline()
            return np.array(spinUp), np.array(spinDown), np.array(energy)

    @staticmethod
    def DOSsiestaV(filename,Ef = 0):
        """DOS Vertical. Spin up only"""
        if os.path.exists(filename):
            DOSFile = open(filename)
            strDOS = DOSFile.readline()            
            DOS = []
            while strDOS!='':
                line = strDOS.split(' ')
                line1 = []
                for i in range(0, len(line)):
                    if line[i] != '':
                        line1.append(line[i])                
                DOS.append([float(line1[1]),round(float(line1[0])-Ef,5)])
                strDOS = DOSFile.readline()
            return DOS

    @staticmethod
    def Etot(filename):
        """ Returns the Etot from SIESTA output file """
        if os.path.exists(filename):
            return Helpers.fromFileProperty(filename, 'siesta: Etot    =', 2, 'float')
        else:
            return None

    @staticmethod
    def Energies(filename):
        """ Energy from each step """
        return TSIESTA.ListOfValues(filename, "siesta: E_KS(eV) =")
        
    @staticmethod
    def FermiEnergy(filename):
        """ Fermy Energy from SIESTA output file """
        if os.path.exists(filename):
            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            Energy = 0
            while str1!='':
                if str1 != '' and (str1.find("siesta: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)   dDmax  Ef(eV)")>=0) or (str1.find("scf: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)    dDmax  Ef(eV)")>=0) or (str1.find("iscf     Eharris(eV)        E_KS(eV)     FreeEng(eV)     dDmax    Ef(eV) dHmax(eV)")>=0):
                    str1 = MdSiestaFile.readline()
                    while (str1.find('siesta')>=0) or (str1.find('timer')>=0) or (str1.find('elaps')>=0) or (str1.find('scf:')>=0) or (str1.find('spin moment:')>=0):
                        str1 = Helpers.spacedel(str1)
                        #print(str1)
                        if (str1.find('siesta')>=0) or (str1.find('scf:')>=0):
                            Energy = float(str1.split(' ')[6])
                        str1 = MdSiestaFile.readline()
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
            return Energy
        else:
            return None

    @staticmethod
    def number_of_atoms(filename):
        """ Returns the NumberOfAtomsfrom SIESTA output file """
        number = Helpers.fromFileProperty(filename,'NumberOfAtoms')
        if number == None:
            block = TSIESTA.get_block_from_siesta_fdf(filename, "AtomicCoordinatesAndAtomicSpecies")
            if len(block) > 0:
                return len(block)
        return number
    
    @staticmethod
    def number_of_species(filename):
        """ Returns the number_of_species from SIESTA output file """
        return Helpers.fromFileProperty(filename,'NumberOfSpecies')

    @staticmethod
    def atomic_coordinates_format(filename):
        """ Returns the AtomicCoordinatesFormat from SIESTA output file """
        format = Helpers.fromFileProperty(filename, 'AtomicCoordinatesFormat', 1, 'string')
        if format == None:
            formatlow = ""
        else:
            formatlow = format.lower()
        ans = "NotScaledCartesianBohr"
        if (formatlow == "ang") or (formatlow == "notscaledcartesianang"):
            ans = "NotScaledCartesianAng"
        if (formatlow == "fractional") or (formatlow == "scaledbylatticevectors"):
            ans = "ScaledByLatticeVectors"
        if (formatlow == "scaledcartesian"):
            ans = "ScaledCartesian"
        return ans

    @staticmethod    
    def Species(filename):
        """ Returns the LIST of Speciecies from SIESTA output or fdf file """
        
        if os.path.exists(filename):
            NumberOfSpecies = TSIESTA.number_of_species(filename)

            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
            Species = []
            
            while str1!='':
                if str1 != '' and (str1.find("block ChemicalSpeciesLabel")>=0):
                    str1 = MdSiestaFile.readline()
                    for i in range(0,NumberOfSpecies):
                        row = Helpers.spacedel(str1).split(' ')[:3]
                        row[0] = int(row[0])
                        row[1] = int(row[1])
                        Species.append(row)
                        str1 = MdSiestaFile.readline()
                    Species.sort(key = lambda line: line[0])
                    return Species
                str1 = MdSiestaFile.readline()
        Species.sort(key = lambda line: line[0])
        return Species
    
    @staticmethod
    def SystemLabel(filename):
        """ Returns the NumberOfAtomsfrom SIESTA output file """
        res = Helpers.fromFileProperty(filename,'SystemLabel',1,"string")
        if res == None:
            res = "siesta"
        return res
        
    @staticmethod
    def SpinPolarized(filename):
        """ Returns the SpinPolarized from SIESTA output file """
        return Helpers.fromFileProperty(filename,'SpinPolarized')

    @staticmethod    
    def ListOfValues(filename, prop):
        """ return all float values of prop from filename """
        ListOfVal = []
        if os.path.exists(filename):
            f = open(filename)
            for st in f:
                if st.find(prop)>=0:
                    ListOfVal.append(float(re.findall(r"[0-9,\.,-]+", st)[0]))
            f.close()
        return ListOfVal

    @staticmethod
    def Replaceatominsiestafdf(filename,atom,string):
        """ not documented """
        NumberOfAtoms = Helpers.fromFileProperty(filename,'number_of_atoms')
        NumberOfSpecies = Helpers.fromFileProperty(filename,'number_of_species')
        lines = []
        f = open(filename)
        lines = f.readlines()    
    
        i = 0        
        newlines = []
        
        while i < len(lines):    
            if (lines[i].find("%block ChemicalSpeciesLabel")>=0):
                for j in range(0,NumberOfSpecies):
                    newlines.append(lines[i])
                    i += 1
    
            if (lines[i].find("%block Zmatrix")>=0):
                newlines.append(lines[i])
                i += 1
                if (lines[i].find("cartesian")>=0):
                    for j in range(0, NumberOfAtoms):
                        if (j==atom):
                            newlines.append(string+'\n')
                        else:
                            newlines.append(lines[i])
                        i += 1    
            newlines.append(lines[i])
            i += 1
        return newlines
            

    @staticmethod
    def get_block_from_siesta_fdf(filename, blockname):
        """ возвращает содержимое блока входного файла """
        lines = []
        flag = 0
        f = open(filename)
        for line in f:
            if (line.find(blockname)<0) and (flag == 1):
                lines.append(line)
            if (line.find(blockname)>=0) and (flag == 1):
                f.close()
                return lines
            if (line.find(blockname)>=0) and (flag == 0):
                flag = 1
        return []

    @staticmethod
    def type_of_run(filename):
        """ MD or CG? """
        return Helpers.fromFileProperty(filename, 'MD.TypeOfRun', 1, 'string')

    @staticmethod
    def volume(filename):
        """ Returns cell volume from SIESTA output file """
        if os.path.exists(filename):
            return Helpers.fromFileProperty(filename, 'siesta: Cell volume = ', 2, 'float')
        else:
            return None

##################################################################
#################### The Tcalculators class ######################
##################################################################
    
class TCalculators:
    @staticmethod
    def FillTube(radTube, length, nAtoms, radAtom, delta, nPrompts, let, charge):
        """ Получение списка конфигураций из nAtoms радиусом radAtom в цилиндре радиусом radTube
        длиной length. Максимум смещения атомов в каждой из моделей не меньше delta """
        Models = []
        random.seed(a=None, version=2)
        
        for i in range(0, nPrompts):
            Molecula = TAtomicModel()
            j = 0
            
            while (j < 1000) and (len(Molecula.atoms) < nAtoms):
                x = random.uniform(-radTube, radTube) 
                a = math.sqrt(radTube*radTube - x*x)
                y = random.uniform(-a, a)
                z = random.uniform(0, length)
                Molecula.add_atom(TAtom([x, y, z, let, charge]), 2 * radAtom)
                j += 1

            if len(Molecula.atoms) < nAtoms:
                radAtom *= 0.95
                print("Radius of atom was dicreased. New value: "+str(radAtom))

            if len(Molecula.atoms) == nAtoms:
                myDelta = 4*radTube+length
                for newMolecula in Models:
                    myDelta2 = Molecula.Delta(newMolecula)
                    if myDelta2 < myDelta:
                        myDelta = myDelta2
                if myDelta > delta:
                    Models.append(Molecula)
                    print("Iter " + str(i) + "/" + str(nPrompts) + "| we found "+str(len(Models))+" structures")
                if len(Models)==0:
                    Models.append(Molecula)
        return Models


    @staticmethod
    def fParabola(x, b0, b1, b2):
        return b0 + b1 * x + b2 * x**2
    
    @staticmethod
    def ApproxParabola(DATA):
        xdata, ydata = Helpers.ListN2Split(DATA)
        # y = ax^2 + bx + c
        a, b, c = polyfit(xdata, ydata, 2)

        #beta_opt, beta_cov = curve_fit(TCalculators.fParabola, xdata, ydata)
        #print(str(a)+"  "+str(b)+"  "+str(c))

        xmin = xdata.min()
        xmax = xdata.max()

        x = np.linspace(xmin, xmax, 200)
        y = TCalculators.fParabola(x, c, b, a)

        return [c, b, a], x.tolist(), y.tolist()

    @staticmethod
    def fMurnaghan(parameters,vol):
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]
        return E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1.)

    @staticmethod
    def fBirchMurnaghan(parameters, vol):
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]
        alpha = pow(V0/vol, 2.0/3.0)
        return E0 + 9*V0*B0/16*(  ((alpha-1)**3)*BP + (alpha-1)**2*(6-4*alpha)   )

    def objectiveMurnaghan(pars, y, x):
        err = y - TCalculators.fMurnaghan(pars,x)
        return err

    def objectiveBirchMurnaghan(pars, y, x):
        err = y - TCalculators.fBirchMurnaghan(pars,x)
        return err

    @staticmethod
    def ApproxMurnaghan(DATA):
        v, e = Helpers.ListN2Split(DATA)
        vfit = np.linspace(min(v), max(v), 100)
        # y = ax^2 + bx + c
        a, b, c = polyfit(v, e, 2)

        # initial guesses
        v0 = -b/(2*a)
        e0 = a*v0**2 + b*v0 + c
        b0 = 2*a*v0
        bP = 4

        x0 = [e0, b0, bP, v0]
        murnpars, ier = leastsq(TCalculators.objectiveMurnaghan, x0, args=(e, v))
        return murnpars, vfit.tolist(), TCalculators.fMurnaghan(murnpars, vfit).tolist()

    @staticmethod
    def ApproxBirchMurnaghan(DATA):
        v, e = Helpers.ListN2Split(DATA)
        vfit = np.linspace(min(v), max(v), 100)

        ### fit a parabola to the data
        # y = ax^2 + bx + c
        a, b, c = polyfit(v, e, 2)

        # initial guesses
        v0 = -b/(2*a)
        e0 = a*v0**2 + b*v0 + c
        b0 = 2*a*v0
        bP = 4

        x0 = [e0, b0, bP, v0]
        murnpars, ier = leastsq(TCalculators.objectiveBirchMurnaghan, x0, args=(e, v))
        return murnpars, vfit.tolist(), TCalculators.fMurnaghan(murnpars, vfit).tolist()

    @staticmethod
    def VoronoiAnalisis(Molecula, selectedAtom, maxDist):
        newMolecula = Molecula.grow()
        newMolecula.move_atoms_to_cell()
        atoms_to_analise = newMolecula.indexes_of_atoms_in_ball(range(0, len(newMolecula.atoms)), selectedAtom, maxDist)
        points = np.empty((len(atoms_to_analise), 3))
        k=0
        for i in atoms_to_analise:
            points[k][0] = newMolecula[i].x
            points[k][1] = newMolecula[i].y
            points[k][2] = newMolecula[i].z
            k+=1

        vor = Voronoi(points)

        vol = 0
        indices = vor.regions[vor.point_region[0]]
        if -1 in indices:  # some regions can be opened
            vol = np.inf
        else:
            vol = ConvexHull(vor.vertices[indices]).volume

        regions = []
        for i in range(0,len(vor.point_region)):
            regions.append(vor.regions[vor.point_region[i]])

        point_ridges = []
        for ridge in vor.ridge_vertices:
            if (len(list(set(ridge) - set(regions[0]))) == 0) and (len(ridge)>0):
                point_ridges.append(ridge)

        ListOfPoligons = []

        if point_ridges.count(-1) == 0:
            for rid in point_ridges:
                poligon = []
                for ind1 in rid:
                    x = vor.vertices[ind1][0]
                    y = vor.vertices[ind1][1]
                    z = vor.vertices[ind1][2]
                    poligon.append([x, y, z])
                    ListOfPoligons.append(poligon)

        return ListOfPoligons, vol

##################################################################
########################## TFDFfile ##############################
##################################################################

class Block:
    def __init__(self, st):
        self.name = st
        self.value = []

    def add_row(self, row):
        self.value.append(row)

class TFDFFile:
    def __init__(self):
        self.properties = []
        self.blocks = []

    def add_block(self,block):
        self.blocks.append(block)

    def add_property(self, row):
        self.properties.append(row)

    def fdf_parser(self, data):
        i = 0
        while i < len(data):
            if not data[i].lstrip().startswith('#'):
                if data[i].find("%block") >= 0:
                    newBlock = Block(data[i].split()[1])
                    i+=1
                    while data[i].find("%endblock") == -1:
                        newBlock.add_row(data[i])
                        i+=1
                    self.add_block(newBlock)
                    i+=1
                else:
                    if data[i]!="" and data[i]!="\n":
                        self.add_property(data[i])
                    i+=1
            else:
                i += 1

    def from_fdf_file(self,filename):
        if os.path.exists(filename):
            f = open(filename)
            lines = f.readlines()
            f.close()
            self.fdf_parser(lines)
            return self

    def from_out_file(self, filename):
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()
            while str1.find("Dump of input data file") == -1:
                str1 = MyFile.readline()
            str1 = MyFile.readline()
            fdf = []
            while str1.find("End of input data file") == -1:
                if str1!="":
                    fdf.append(str1)
                str1 = MyFile.readline()
            MyFile.close()
            self.fdf_parser(fdf)
            return self


    def get_all_data(self, _structure, coordType, lattType):
        structure = deepcopy(_structure)

        st = structure.toSIESTAfdfdata(coordType,lattType)

        for prop in self.properties:
            f = True
            if (prop.lower().find("numberofatoms")>=0): f = False
            if (prop.lower().find("numberofspecies")>=0): f = False
            if (prop.lower().find("atomiccoordinatesformat")>=0): f = False
            if (prop.lower().find("latticeconstant") >= 0): f = False
            if f:
                st += prop

        for block in self.blocks:
            f = True
            if ((block.name).lower().find("zmatrix")>=0): f = False
            if ((block.name).lower().find("chemicalspecieslabel")>=0): f = False
            if ((block.name).lower().find("latticeparameters") >=0): f = False
            if ((block.name).lower().find("latticevectors") >=0): f = False

            if f:
                st +="%block "+block.name+"\n"
                for row in block.value:
                    st += row
                st +="%endblock "+block.name+"\n"
        return st

    @staticmethod
    def updateAtominSIESTAfdf(filename, model):
        """ заменяет атомы во входном файле SIESTA """
        NumberOfAtoms = Helpers.fromFileProperty(filename, 'NumberOfAtoms')
        lines = []
        f = open(filename)
        lines = f.readlines()

        i = 0

        newlines = []

        while i < len(lines):
            if (lines[i].find("%block Zmatrix") >= 0):
                newlines.append(lines[i])
                i += 1
                if (lines[i].find("cartesian") >= 0):
                    newlines.append(lines[i])
                    i += 1
                    for j in range(0, NumberOfAtoms):
                        row = Helpers.spacedel(lines[i])
                        ind = row.split(' ')[0]
                        dx = row.split(' ')[4]
                        dy = row.split(' ')[5]
                        dz = row.split(' ')[6]
                        newlines.append('   ' + str(ind) + '   ' + str(model.atoms[j].x) + '   ' + str(
                            model.atoms[j].y) + '   ' + str(model.atoms[j].z) + '   ' + str(dx) + '   ' + str(
                            dy) + '   ' + str(dz) + '\n')

                        i += 1
            newlines.append(lines[i])
            i += 1
        return newlines

    @staticmethod
    def updatePropertyInSIESTAfdf(filename, property, newvalue, units):
        """ изменяет один из параметров во входном файле """
        lines = []
        f = open(filename)
        lines = f.readlines()
        f.close()

        f = open(filename, 'w')
        for j in range(0, len(lines)):
            field = lines[j]
            if (lines[j].find(property) >= 0):
                field = property + "  " + str(newvalue) + "  " + str(units) + "\n"
            f.write(field)
        f.close()

    @staticmethod
    def updateBlockinSIESTAfdf(filename, blockname, newvalue):
        """ изменяет один из блоков во входном файле """
        lines = []
        f = open(filename)
        lines = f.readlines()
        f.close()

        f = open(filename, 'w')
        flag = 0
        for j in range(0, len(lines)):
            if (lines[j].find(blockname) >= 0) and (flag == 1):
                f.write(lines[j])
                flag = 0
            else:
                if (lines[j].find(blockname) >= 0) and (flag == 0):
                    f.write(lines[j])
                    flag = 1
                    f.write(str(newvalue) + "\n")
                else:
                    if (flag == 0):
                        f.write(lines[j])
        f.close()

##################################################################
######################## TCap for SWNT ###########################
##################################################################


class TCapedSWNT(TAtomicModel):

    def __init__(self, n, m, leng, cells, type, dist1, angle1, dist2, angle2):
        TAtomicModel.__init__(self)
        self.availableind = np.zeros((8))
        self.available = False

        self.n = n
        self.m = m
        self.length = leng
        self.tube = self.simpleSWNT()
        for atom in self.tube:
            self.add_atom(atom)
        # self.caps = []
        self.cap_atoms = TAtomicModel()
        self.cap_formation()

        if type == 1 or type == 2:
            # cap generation
            zaz = dist1
            Cap = self.cap_formation()  # TCap(n,m)
            if self.available:
                size1 = self.Size(n, m)
                capatoms = self.cap4SWNT_norm()
                if self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z

                minz = self.minZ()
                maxz = capatoms.maxZ()

                capatoms.move(0, 0, minz - maxz - zaz)
                capatoms.rotateZ(angle1)
                for i in range(0, capatoms.nAtoms()):
                    self.add_atom(capatoms[i])

            if type == 2:
                # second cap generation
                capatoms = self.cap4SWNT_norm()
                if not self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z
                maxz = self.maxZ()
                minz = capatoms.minZ()

                zaz = dist2

                capatoms.move(0, 0, (maxz - minz) + zaz)
                capatoms.rotateZ(angle2)
                for i in range(0, capatoms.nAtoms()):
                    self.add_atom(capatoms[i])
            # end cap generation

    def Size(self, n, m):
        for i in range(0,len(self.availableind)):
            if (n == self.availableind[0]) and (m == self.availableind[1]):
                return int(self.availableind[3])
        return -1

    def cap4SWNT_norm(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
                cap1 = TAtomicModel()
                for j in range(0,self.cap_atoms.nAtoms()):
                    cap1.add_atom(self.cap_atoms[j])
                cap1.move(- 1.0 * self.availableind[4] / 2.0, - 1.0 * self.availableind[5] / 2.0, 0)

                for j in range(0, cap1.nAtoms()):
                    xnn = cap1[j].x * math.cos(self.availableind[6] *math.pi / 180.0) - cap1[j].y * math.sin(self.availableind[6] *math.pi / 180.0)
                    ynn = cap1[j].x * math.sin(self.availableind[6] *math.pi / 180.0) + cap1[j].y * math.cos(self.availableind[6] *math.pi / 180.0)

                    cap1[j].x = xnn
                    cap1[j].y = ynn
                return cap1
        return None

    def invert(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
                return self.availableind[7]
        return -1

    def simpleSWNT(self):
        tube_atoms = TAtomicModel()
        bound = 1.433
        size = 0
        if (self.n > 0) and (self.m == 0):
            # zigzag nanotube
            bound = 1.421
            rad_nanotube = 5 * 0.246 * self.n / math.pi
            z_coord = 0 # z координата
            tem = 1
            # calculation of atoms
            while (z_coord < self.length):
                size += self.n
                tem +=1
                bound = 1.421
                if tem == 2:
                    tem=0
                    bound = 1.421 * math.cos(math.pi / 3.0)
                z_coord += bound
            # end calculation of atoms

            rotdeg = math.pi / self.n
            count = 0
            z_coord = 0
            ring_nanotube = 0

            while z_coord < self.length:
                for jk in range(0, self.n):
                    x = rad_nanotube * math.cos(2 * math.pi * jk / self.n+rotdeg)
                    y = rad_nanotube * math.sin(2 * math.pi * jk / self.n+rotdeg)
                    tube_atoms.add_atom(TAtom([x, y, z_coord, "C", 6, False]))

                tem +=1
                bound = 1.421
                if tem == 2:
                    tem=0
                    rotdeg += math.pi / self.n
                    bound = 1.421 * math.cos(math.pi / 3)
                z_coord += bound
                ring_nanotube +=1



        if (self.n == self.m) and (self.n > 0):
            # armchare nanotube
            pinan = math.pi / self.n
            rad_nanotube = math.sqrt((5 + 2 * math.sqrt(2 * (1 + math.cos(pinan)))) / (8 * (1 - math.cos(pinan)))) * bound
            alfa = math.acos(1 - bound * bound / (8 * rad_nanotube * rad_nanotube))
            betta = math.acos(1 - bound * bound / (2 * rad_nanotube * rad_nanotube))

            z_coord = 0 # z координата
            ring_nanotube = 0
            size = 0
            deltag = betta + alfa

            while z_coord < self.length:
                size += 2 * self.m
                z_coord += math.sqrt(3.0) * 0.5 * bound
                ring_nanotube+=1

                angle = 0
                sw = 0
                z_coord = 0
                ring_nanotube = 0
                deltag = betta + alfa
                count = 0

                while z_coord < self.length:
                    deltag = betta+alfa - deltag
                    for jk in range(0, 2 * self.m):
                        sw = 1-sw
                        if sw == 1:
                            angle += betta
                        else:
                            angle += pinan+alfa
                        if angle > 2 * math.pi:
                            angle = angle - 2 * math.pi
                        if angle < -2 * math.pi:
                            angle = angle + 2 * math.pi
                        x = rad_nanotube * math.cos(angle-deltag)
                        y = rad_nanotube * math.sin(angle-deltag)
                        tube_atoms.add_atom(TAtom([x, y, z_coord, "C", 6, False]))

                    z_coord += math.sqrt(3.0) * 0.5 * bound
                    ring_nanotube +=1
        return tube_atoms

    def cap_formation(self):
        # 0 - n
        # 1 - m
        # 2 - index in Cap
        # 3 - number of atoms
        # 4 - x0
        # 5 - y0
        # 6 - fi
        # 7 - bool invert or not

        if self.n == 6 and self.m == 6:
            self.available = True
            self.availableind[0] = 6
            self.availableind[1] = 6
            self.availableind[2] = 1 # cap  0
            self.availableind[3] = 36
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -40
            self.availableind[7] = 1

            self.cap_atoms = TAtomicModel()

            self.cap_atoms.add_atom(TAtom([-0.36693112712E+00, 0.14828478339E+01, 1.86168451, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.14123318617E+01, 0.42721410070E+00, 1.88297428, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.10568038810E+01, -0.10057307755E+01, 1.82796005, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.38589540659E+00, -0.13267764277E+01, 1.84106985, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.13496217634E+01, -0.28131482088E+00, 1.87047317, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.10071810608E+01, 0.10985087143E+01, 1.89193246, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.19987312467E+01, 0.30014395545E+01, 0.73606458, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([ -0.29578581189E+01, 0.19721596960E+01, 0.73632071, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.27571698247E+01, 0.71874399926E+00, 1.44108245, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.35829370629E+01,-0.24291285515E+00,0.68239008, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.32349211883E+01,-0.16206333154E+01,0.68625620, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.20047282591E+01,-0.19775980251E+01,1.40477121, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.16362756027E+01,-0.32383913803E+01,0.75524927, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.28063713290E+00,-0.36132532671E+01,0.71923701, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.70896305879E+00,-0.27408666603E+01,1.38701774, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.19888600177E+01,-0.29354589995E+01,0.70705602, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.30282933796E+01,-0.19633677080E+01,0.74070240, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.27179573531E+01,-0.64426510383E+00,1.43991810, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.36391537961E+01,0.27223176788E+00,0.72968705, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.32670313687E+01,0.16238573940E+01,0.73224586, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.20483841305E+01,0.19967370195E+01,1.37748738, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.15990133003E+01,0.32589685312E+01,0.71464324, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.23683726128E+00,0.36518477604E+01,0.74698622, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.74036797244E+00,0.28521743942E+01,1.47972432, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([4.0586,-0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([2.6474,3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.0000,4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-1.4111,3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-4.0586,0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-3.5688,-2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-2.6474,-3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.0000,-4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([1.4111,-3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([3.5688,-2.0604,-0.5264, "C", 6, False]))

        if self.n == 10 and self.m == 0:
            self.available = True
            self.availableind[0] = 10
            self.availableind[1] = 0
            self.availableind[2] = 1 # cap
            self.availableind[3] = 20
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -25
            self.availableind[7] = 0

            self.cap_atoms = TAtomicModel()

            self.cap_atoms.add_atom(TAtom([0.34216148481E+00, -0.12053675732E+01, 0.27817708814E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.29945044883E+01,-0.12353947470E+01,0.15621427500E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.31963746233E+01,0.76302077744E+00,0.15989438777E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.99585806005E+00,-0.74592960370E+00,0.38623433120E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.28372435918E+00, -0.33073880303E+01, 0.15748123961E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.20970977233E+01,0.24759817007E+01,0.15783693808E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.76620899479E+00,0.23662547380E+01,0.10756116106E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.29097152253E+00,0.31787983516E+01,0.16306217062E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.25460695924E+01,-0.12019370177E-01,0.10168833638E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.98415232530E+00,0.71949433978E+00,0.38919891314E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.12527638107E+01,-0.26556683526E-01,0.42986738706E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([ -0.20374152633E+01 , 0.15039739223E+01 , 0.10034475884E+01 , "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.16718683612E+01,-0.28065794251E+01,0.15605264317E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.78433886197E+00,-0.24167512792E+01,0.96858303258E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.31930381398E+01,-0.81568604886E+00,0.15674645057E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.39669805001E+00,0.11287767681E+01,0.46634191420E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.17123909710E+01,0.27591217116E+01,0.16091964100E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.29519974190E+01,0.12337637208E+01,0.16234022245E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.21072419022E+01, -0.24689911393E+01,0.15851545095E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.20785821822E+01,-0.15522369686E+01,0.10403308851E+01, "C", 6, False]))


"""
    class TCap{

        atom ** cap;
    public: 
        TCap();
    ~TCap()
    {};
    atom * cap4SWNT(int, int);
    atom * cap4SWNT_norm(int, int);
    int
    size(int, int);
    int
    isavailable(int, int);
    int
    invert(int, int);
    };
    TCap::TCap()
    {
        cap = new atom * [4];
    int  i;
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111


    availableind[2][0] = 10;
    availableind[2][1] = 10;
    availableind[2][2] = 2; // cap
    availableind[2][3] = 110;
    availableind[2][4] = 51;
    availableind[2][5] = -15;
    availableind[2][6] = 54;
    availableind[2][7] = 1;
    cap[2] = new atom[110];
    for (i=0;i < 110;i++){
    cap[2][i].c.SetStr("C", 1);
    cap[2][i].charge = 6;
    cap[2][i].select = 1;
    }
    cap[2][0].x = (float) 24.307116;    cap[2][0].y = (float) -8.391858;    cap[2][0].z = (float) 26.631681;
    cap[2][1].x = (float) 24.028402;    cap[2][1].y = (float) -6.999814;    cap[2][1].z = (float) 26.613461;
    cap[2][2].x = (float) 25.74894;     cap[2][2].y = (float) -8.591233;    cap[2][2].z = (float) 26.608431;
    cap[2][3].x = (float) 25.256088;    cap[2][3].y = (float) -6.25233;     cap[2][3].z = (float) 26.558006;
    cap[2][4].x = (float) 26.336517;    cap[2][4].y = (float) -7.251723;    cap[2][4].z = (float) 26.524309;
    cap[2][5].x = (float) 25.451431;    cap[2][5].y = (float) -4.952374;    cap[2][5].z = (float) 25.950344;
    cap[2][6].x = (float) 22.903727;    cap[2][6].y = (float) -6.458869;    cap[2][6].z = (float) 25.895767;
    cap[2][7].x = (float) 23.512154;    cap[2][7].y = (float) -9.253161;    cap[2][7].z = (float) 25.884455;
    cap[2][8].x = (float) 26.402281;    cap[2][8].y = (float) -9.617024;    cap[2][8].z = (float) 25.883873;
    cap[2][9].x = (float) 27.543873;    cap[2][9].y = (float) -7.03859;     cap[2][9].z = (float) 25.807861;
    cap[2][10].x = (float) 26.813923;   cap[2][10].y = (float) -4.730283;   cap[2][10].z = (float) 25.435555;
    cap[2][11].x = (float) 21.885521;   cap[2][11].y = (float) -7.384042;   cap[2][11].z = (float) 25.430565;
    cap[2][12].x = (float) 24.251844;   cap[2][12].y = (float) -4.368014;   cap[2][12].z = (float) 25.417097;
    cap[2][13].x = (float) 23.017797;   cap[2][13].y = (float) -5.112086;   cap[2][13].z = (float) 25.412504;
    cap[2][14].x = (float) 22.263638;   cap[2][14].y = (float) -8.773506;   cap[2][14].z = (float) 25.406738;
    cap[2][15].x = (float) 24.106068;   cap[2][15].y = (float) -10.451938;  cap[2][15].z = (float) 25.336063;
    cap[2][16].x = (float) 27.713478;   cap[2][16].y = (float) -9.483947;   cap[2][16].z = (float) 25.335426;
    cap[2][17].x = (float) 27.7791;     cap[2][17].y = (float) -5.737792;   cap[2][17].z = (float) 25.287855;
    cap[2][18].x = (float) 25.509258;   cap[2][18].y = (float) -10.582597;  cap[2][18].z = (float) 25.282236;
    cap[2][19].x = (float) 28.305012;   cap[2][19].y = (float) -8.159348;   cap[2][19].z = (float) 25.266905;
    cap[2][20].x = (float) 21.897963;   cap[2][20].y = (float) -4.546319;   cap[2][20].z = (float) 24.703777;
    cap[2][21].x = (float) 26.917971;   cap[2][21].y = (float) -3.495377;   cap[2][21].z = (float) 24.661104;
    cap[2][22].x = (float) 20.821575;   cap[2][22].y = (float) -6.853278;   cap[2][22].z = (float) 24.616817;
    cap[2][23].x = (float) 24.381664;   cap[2][23].y = (float) -3.221068;   cap[2][23].z = (float) 24.605165;
    cap[2][24].x = (float) 29.501595;   cap[2][24].y = (float) -7.858403;   cap[2][24].z = (float) 24.561548;
    cap[2][25].x = (float) 26.126131;   cap[2][25].y = (float) -11.722587;  cap[2][25].z = (float) 24.513506;
    cap[2][26].x = (float) 23.28396;    cap[2][26].y = (float) -11.332781;  cap[2][26].z = (float) 24.507889;
    cap[2][27].x = (float) 28.285215;   cap[2][27].y = (float) -10.485401;  cap[2][27].z = (float) 24.500849;
    cap[2][28].x = (float) 21.51675;    cap[2][28].y = (float) -9.593892;   cap[2][28].z = (float) 24.498133;
    cap[2][29].x = (float) 20.781013;   cap[2][29].y = (float) -5.421203;   cap[2][29].z = (float) 24.480793;
    cap[2][30].x = (float) 28.923557;   cap[2][30].y = (float) -5.488295;   cap[2][30].z = (float) 24.469994;
    cap[2][31].x = (float) 25.704922;   cap[2][31].y = (float) -2.690116;   cap[2][31].z = (float) 24.392683;
    cap[2][32].x = (float) 21.946112;   cap[2][32].y = (float) -10.949246;  cap[2][32].z = (float) 24.35844;
    cap[2][33].x = (float) 27.558289;   cap[2][33].y = (float) -11.695153;  cap[2][33].z = (float) 24.308565;
    cap[2][34].x = (float) 23.31764;    cap[2][34].y = (float) -2.718772;   cap[2][34].z = (float) 23.835554;
    cap[2][35].x = (float) 28.049913;   cap[2][35].y = (float) -3.287543;   cap[2][35].z = (float) 23.804535;
    cap[2][36].x = (float) 20.02154;    cap[2][36].y = (float) -7.71293;    cap[2][36].z = (float) 23.80274;
    cap[2][37].x = (float) 29.099838;   cap[2][37].y = (float) -4.276214;   cap[2][37].z = (float) 23.775066;
    cap[2][38].x = (float) 22.07427;    cap[2][38].y = (float) -3.384869;   cap[2][38].z = (float) 23.769482;
    cap[2][39].x = (float) 20.394318;   cap[2][39].y = (float) -9.130861;   cap[2][39].z = (float) 23.768671;
    cap[2][40].x = (float) 25.275475;   cap[2][40].y = (float) -12.659516;  cap[2][40].z = (float) 23.754967;
    cap[2][41].x = (float) 23.81428;    cap[2][41].y = (float) -12.399732;  cap[2][41].z = (float) 23.730297;
    cap[2][42].x = (float) 19.686266;   cap[2][42].y = (float) -4.93257;    cap[2][42].z = (float) 23.662189;
    cap[2][43].x = (float) 21.137602;   cap[2][43].y = (float) -11.810185;  cap[2][43].z = (float) 23.616472;
    cap[2][44].x = (float) 28.149002;   cap[2][44].y = (float) -12.723328;  cap[2][44].z = (float) 23.540396;
    cap[2][45].x = (float) 25.829796;   cap[2][45].y = (float) -1.545785;   cap[2][45].z = (float) 23.532829;
    cap[2][46].x = (float) 30.998842;   cap[2][46].y = (float) -6.29346;    cap[2][46].z = (float) 23.487898;
    cap[2][47].x = (float) 31.195286;   cap[2][47].y = (float) -8.674395;   cap[2][47].z = (float) 22.883595;
    cap[2][48].x = (float) 23.492815;   cap[2][48].y = (float) -1.661548;   cap[2][48].z = (float) 22.8822;
    cap[2][49].x = (float) 19.012489;   cap[2][49].y = (float) -7.228202;   cap[2][49].z = (float) 22.877794;
    cap[2][50].x = (float) 19.993397;   cap[2][50].y = (float) -11.350829;  cap[2][50].z = (float) 22.851616;
    cap[2][51].x = (float) 18.855139;   cap[2][51].y = (float) -5.81593;    cap[2][51].z = (float) 22.842537;
    cap[2][52].x = (float) 24.740768;   cap[2][52].y = (float) -0.941531;   cap[2][52].z = (float) 22.839033;
    cap[2][53].x = (float) 28.143888;   cap[2][53].y = (float) -2.214602;   cap[2][53].z = (float) 22.823023;
    cap[2][54].x = (float) 27.309549;   cap[2][54].y = (float) -13.638415;  cap[2][54].z = (float) 22.816744;
    cap[2][55].x = (float) 29.37397;    cap[2][55].y = (float) -12.497607;  cap[2][55].z = (float) 22.810347;
    cap[2][56].x = (float) 29.921804;   cap[2][56].y = (float) -11.138785;  cap[2][56].z = (float) 22.805902;
    cap[2][57].x = (float) 19.881659;   cap[2][57].y = (float) -3.716206;   cap[2][57].z = (float) 22.798765;
    cap[2][58].x = (float) 21.114313;   cap[2][58].y = (float) -3.043349;   cap[2][58].z = (float) 22.797981;
    cap[2][59].x = (float) 30.141171;   cap[2][59].y = (float) -4.090331;   cap[2][59].z = (float) 22.79162;
    cap[2][60].x = (float) 25.848095;   cap[2][60].y = (float) -13.504389;  cap[2][60].z = (float) 22.791164;
    cap[2][61].x = (float) 21.709684;   cap[2][61].y = (float) -12.907913;  cap[2][61].z = (float) 22.779915;
    cap[2][62].x = (float) 27.025219;   cap[2][62].y = (float) -1.334748;   cap[2][62].z = (float) 22.775311;
    cap[2][63].x = (float) 23.056452;   cap[2][63].y = (float) -13.112155;  cap[2][63].z = (float) 22.761112;
    cap[2][64].x = (float) 19.703302;   cap[2][64].y = (float) -9.919573;   cap[2][64].z = (float) 22.754223;
    cap[2][65].x = (float) 31.64447;    cap[2][65].y = (float) -7.360505;   cap[2][65].z = (float) 22.753363;
    cap[2][66].x = (float) 31.199718;   cap[2][66].y = (float) -5.068017;   cap[2][66].z = (float) 22.727516;
    cap[2][67].x = (float) 29.014811;   cap[2][67].y = (float) -2.2107;     cap[2][67].z = (float) 21.689016;
    cap[2][68].x = (float) 22.682739;   cap[2][68].y = (float) -1.526551;   cap[2][68].z = (float) 21.684744;
    cap[2][69].x = (float) 31.287226;   cap[2][69].y = (float) -9.44718;    cap[2][69].z = (float) 21.67403;
    cap[2][70].x = (float) 18.668207;   cap[2][70].y = (float) -7.955943;   cap[2][70].z = (float) 21.656946;
    cap[2][71].x = (float) 30.655699;   cap[2][71].y = (float) -10.736203;  cap[2][71].z = (float) 21.652979;
    cap[2][72].x = (float) 30.026033;   cap[2][72].y = (float) -3.221543;   cap[2][72].z = (float) 21.64381;
    cap[2][73].x = (float) 21.492094;   cap[2][73].y = (float) -2.250502;   cap[2][73].z = (float) 21.632978;
    cap[2][74].x = (float) 19.070688;   cap[2][74].y = (float) -9.297336;   cap[2][74].z = (float) 21.628992;
    cap[2][75].x = (float) 23.742189;   cap[2][75].y = (float) -13.624204;  cap[2][75].z = (float) 21.613325;
    cap[2][76].x = (float) 25.252064;   cap[2][76].y = (float) -0.282405;   cap[2][76].z = (float) 21.604607;
    cap[2][77].x = (float) 19.886501;   cap[2][77].y = (float) -12.067063;  cap[2][77].z = (float) 21.598923;
    cap[2][78].x = (float) 29.27622;    cap[2][78].y = (float) -13.270625;  cap[2][78].z = (float) 21.591307;
    cap[2][79].x = (float) 18.551779;   cap[2][79].y = (float) -5.17668;    cap[2][79].z = (float) 21.590588;
    cap[2][80].x = (float) 25.156328;   cap[2][80].y = (float) -13.750842;  cap[2][80].z = (float) 21.585398;
    cap[2][81].x = (float) 19.18738;    cap[2][81].y = (float) -3.879289;   cap[2][81].z = (float) 21.583361;
    cap[2][82].x = (float) 20.975973;   cap[2][82].y = (float) -13.06409;   cap[2][82].z = (float) 21.574989;
    cap[2][83].x = (float) 26.698114;   cap[2][83].y = (float) -0.632041;   cap[2][83].z = (float) 21.553831;
    cap[2][84].x = (float) 27.99502;    cap[2][84].y = (float) -13.89404;   cap[2][84].z = (float) 21.547998;
    cap[2][85].x = (float) 31.97467;    cap[2][85].y = (float) -5.319426;   cap[2][85].z = (float) 21.545002;
    cap[2][86].x = (float) 32.260117;   cap[2][86].y = (float) -6.783418;   cap[2][86].z = (float) 21.532591;
    cap[2][87].x = (float) 23.241642;   cap[2][87].y = (float) -0.886021;   cap[2][87].z = (float) 20.499775;
    cap[2][88].x = (float) 28.579681;   cap[2][88].y = (float) -1.601615;   cap[2][88].z = (float) 20.466377;
    cap[2][89].x = (float) 18.241289;   cap[2][89].y = (float) -7.256305;   cap[2][89].z = (float) 20.452448;
    cap[2][90].x = (float) 30.559538;   cap[2][90].y = (float) -11.519896;  cap[2][90].z = (float) 20.451962;
    cap[2][91].x = (float) 31.801649;   cap[2][91].y = (float) -8.87911;    cap[2][91].z = (float) 20.423489;
    cap[2][92].x = (float) 24.516485;   cap[2][92].y = (float) -0.370414;   cap[2][92].z = (float) 20.416256;
    cap[2][93].x = (float) 20.798647;   cap[2][93].y = (float) -2.429421;   cap[2][93].z = (float) 20.403654;
    cap[2][94].x = (float) 30.66143;    cap[2][94].y = (float) -3.581628;   cap[2][94].z = (float) 20.401373;
    cap[2][95].x = (float) 19.02692;    cap[2][95].y = (float) -10.045808;  cap[2][95].z = (float) 20.399921;
    cap[2][96].x = (float) 32.225246;   cap[2][96].y = (float) -7.558652;   cap[2][96].z = (float) 20.384998;
    cap[2][97].x = (float) 19.653811;   cap[2][97].y = (float) -3.306693;   cap[2][97].z = (float) 20.38278;
    cap[2][98].x = (float) 19.527115;   cap[2][98].y = (float) -11.410149;  cap[2][98].z = (float) 20.379232;
    cap[2][99].x = (float) 29.849607;   cap[2][99].y = (float) -12.757981;  cap[2][99].z = (float) 20.373478;
    cap[2][100].x = (float) 18.299751;  cap[2][100].y = (float) -5.846803;   cap[2][100].z = (float) 20.371761;
    cap[2][101].x = (float) 31.523699;  cap[2][101].y = (float) -4.676303;   cap[2][101].z = (float) 20.367992;
    cap[2][102].x = (float) 27.372185;  cap[2][102].y = (float) -0.799687;   cap[2][102].z = (float) 20.345131;
    cap[2][103].x = (float) 25.903364;  cap[2][103].y = (float) -14.031196;  cap[2][103].z = (float) 20.343964;
    cap[2][104].x = (float) 23.052832;  cap[2][104].y = (float) -13.603871;  cap[2][104].z = (float) 20.328026;
    cap[2][105].x = (float) 21.613218;  cap[2][105].y = (float) -13.354865;  cap[2][105].z = (float) 20.293333;
    cap[2][106].x = (float) 29.890324;  cap[2][106].y = (float) -6.534263;   cap[2][106].z = (float) 24.27564;
    cap[2][107].x = (float) 30.184898;  cap[2][107].y = (float) -8.9305;     cap[2][107].z = (float) 23.873917;
    cap[2][108].x = (float) 29.517391;  cap[2][108].y = (float) -10.189402;  cap[2][108].z = (float) 23.839216;
    cap[2][109].x = (float) 27.325338;  cap[2][109].y = (float) -14.219027;  cap[2][109].z = (float) 20.34614;




    availableind[3][0] = 19;
    availableind[3][1] = 0;
    availableind[3][2] = 0; // cap
    availableind[3][3] = 125; // 24;
    availableind[3][4] = 0;
    availableind[3][5] = 0;
    availableind[3][6] = 0;
    availableind[3][7] = 1;
    cap[3] = new atom[125];
    for (i=0;i < 125;i++){
    cap[3][i].c.SetStr("C", 1);
    cap[3][i].charge = 6;
    cap[3][i].select = 1;
    }

    cap[3][0].x = (float) -0.48589722322E+01;   cap[3][0].y = (float) -0.36221817094E+01;    cap[3][0].z = (float) -0.14080584970E+01;
    cap[3][1].x = (float) -0.45730216641E+01;   cap[3][1].y = (float) -0.48531400967E+01;    cap[3][1].z = (float) -0.74577774177E+00;
    cap[3][2].x = (float) -0.48843163209E+01;   cap[3][2].y = (float) -0.52449271110E+01;    cap[3][2].z = (float) 0.60148070560E+00;
    cap[3][3].x = (float) -0.41153315282E+01;   cap[3][3].y = (float) -0.61902792021E+01;    cap[3][3].z = (float) 0.14159023882E+01;
    cap[3][4].x = (float) -0.61987961664E+01;   cap[3][4].y = (float) -0.31933977619E+01;    cap[3][4].z = (float) 0.67432004891E+00;
    cap[3][5].x = (float) -0.57695614619E+01;   cap[3][5].y = (float) -0.44079622455E+01;    cap[3][5].z = (float) 0.14001309796E+01;
    cap[3][6].x = (float) -0.57357142720E+01;   cap[3][6].y = (float) -0.27426732726E+01;    cap[3][6].z = (float) -0.71670030400E+00;
    cap[3][7].x = (float) -0.30985668536E+01;   cap[3][7].y = (float) -0.39242127454E+01;    cap[3][7].z = (float) -0.31614631281E+01;
    cap[3][8].x = (float) -0.29215146165E+01;   cap[3][8].y = (float) -0.52169101055E+01;    cap[3][8].z = (float) -0.25760465958E+01;
    cap[3][9].x = (float) -0.36652796414E+01;   cap[3][9].y = (float) -0.56953921641E+01;    cap[3][9].z = (float) -0.14010441490E+01;
    cap[3][10].x = (float) -0.41562523579E+01;  cap[3][10].y = (float) -0.31814642732E+01;   cap[3][10].z = (float) -0.25769020730E+01;
    cap[3][11].x = (float) -0.53674105201E+01;  cap[3][11].y = (float) -0.11044211318E+01;   cap[3][11].z = (float) -0.26418590383E+01;
    cap[3][12].x = (float) -0.43605534094E+01;  cap[3][12].y = (float) -0.19146253022E+01;   cap[3][12].z = (float) -0.31653236139E+01;
    cap[3][13].x = (float) -0.59681628233E+01;  cap[3][13].y = (float) -0.14839249801E+01;   cap[3][13].z = (float) -0.13735951494E+01;
    cap[3][14].x = (float) -0.69403908369E+01;  cap[3][14].y = (float) -0.22370927539E+01;   cap[3][14].z = (float) 0.14908204357E+01;
    cap[3][15].x = (float) -0.67829820558E+01;  cap[3][15].y = (float) -0.56752250354E+00;   cap[3][15].z = (float) -0.66587975966E+00;
    cap[3][16].x = (float) -0.72402721042E+01;  cap[3][16].y = (float) -0.97249826495E+00;   cap[3][16].z = (float) 0.67447957321E+00;
    cap[3][17].x = (float) -0.73235299353E+00;  cap[3][17].y = (float) -0.39436611322E+01;   cap[3][17].z = (float) -0.38962171073E+01;
    cap[3][18].x = (float) -0.50780477489E+00;  cap[3][18].y = (float) -0.52145277840E+01;   cap[3][18].z = (float) -0.31315665561E+01;
    cap[3][19].x = (float) 0.73643831218E+00;   cap[3][19].y = (float) -0.54148786225E+01;   cap[3][19].z = (float) -0.25386385055E+01;
    cap[3][20].x = (float) 0.82869013696E+00;   cap[3][20].y = (float) -0.61954057298E+01;   cap[3][20].z = (float) -0.12991011496E+01;
    cap[3][21].x = (float) 0.19966654092E+01;   cap[3][21].y = (float) -0.61445332848E+01;   cap[3][21].z = (float) -0.56731734942E+00;
    cap[3][22].x = (float) -0.16482338625E+01;  cap[3][22].y = (float) -0.58617419890E+01;   cap[3][22].z = (float) -0.26446300562E+01;
    cap[3][23].x = (float) -0.20424170549E+01;  cap[3][23].y = (float) -0.33461547050E+01;   cap[3][23].z = (float) -0.39209782908E+01;
    cap[3][24].x = (float) -0.75114773645E+01;  cap[3][24].y = (float) 0.18067922075E+01;    cap[3][24].z = (float) -0.44811891889E+00;
    cap[3][25].x = (float) -0.79206146976E+01;  cap[3][25].y = (float) 0.14562264028E+01;    cap[3][25].z = (float) 0.91254016598E+00;
    cap[3][26].x = (float) -0.76685162423E+01;  cap[3][26].y = (float) 0.16980360536E+00;    cap[3][26].z = (float) 0.14605629646E+01;
    cap[3][27].x = (float) -0.68884826029E+01;  cap[3][27].y = (float) 0.80473287388E+00;    cap[3][27].z = (float) -0.11616286642E+01;
    cap[3][28].x = (float) -0.60047077999E+01;  cap[3][28].y = (float) 0.12593067284E+01;    cap[3][28].z = (float) -0.21853196867E+01;
    cap[3][29].x = (float) -0.37043207368E+01;  cap[3][29].y = (float) -0.11691464229E+00;   cap[3][29].z = (float) -0.47797936434E+01;
    cap[3][30].x = (float) -0.46955878800E+01;  cap[3][30].y = (float) 0.77138417158E+00;    cap[3][30].z = (float) -0.41973177994E+01;
    cap[3][31].x = (float) -0.54683045289E+01;  cap[3][31].y = (float) 0.30771919461E+00;    cap[3][31].z = (float) -0.30867828557E+01;
    cap[3][32].x = (float) -0.34994407953E+01;  cap[3][32].y = (float) -0.13884048701E+01;   cap[3][32].z = (float) -0.42753133052E+01;
    cap[3][33].x = (float) -0.21914963346E+01;  cap[3][33].y = (float) -0.20311739108E+01;   cap[3][33].z = (float) -0.44867260054E+01;
    cap[3][34].x = (float) 0.31811288950E+00;   cap[3][34].y = (float) -0.31560065296E+01;   cap[3][34].z = (float) -0.44548999592E+01;
    cap[3][35].x = (float) 0.15983815345E+01;   cap[3][35].y = (float) -0.36373350389E+01;   cap[3][35].z = (float) -0.40771402988E+01;
    cap[3][36].x = (float) 0.18123089400E+01;   cap[3][36].y = (float) -0.46147956852E+01;   cap[3][36].z = (float) -0.30333652860E+01;
    cap[3][37].x = (float) 0.30182632334E+01;   cap[3][37].y = (float) -0.46418994665E+01;   cap[3][37].z = (float) -0.23340010633E+01;
    cap[3][38].x = (float) 0.30822595901E+01;   cap[3][38].y = (float) -0.53692904839E+01;   cap[3][38].z = (float) -0.11553135841E+01;
    cap[3][39].x = (float) -0.44145125740E+01;  cap[3][39].y = (float) 0.30295629037E+01;    cap[3][39].z = (float) -0.30876901352E+01;
    cap[3][40].x = (float) -0.41496701086E+01;  cap[3][40].y = (float) 0.21668980992E+01;    cap[3][40].z = (float) -0.41788603341E+01;
    cap[3][41].x = (float) -0.54717214675E+01;  cap[3][41].y = (float) 0.26230229502E+01;    cap[3][41].z = (float) -0.22031862702E+01;
    cap[3][42].x = (float) -0.57452822978E+01;  cap[3][42].y = (float) 0.35183378284E+01;    cap[3][42].z = (float) -0.11100755633E+01;
    cap[3][43].x = (float) -0.69788869712E+01;  cap[3][43].y = (float) 0.31937006916E+01;    cap[3][43].z = (float) -0.40618133609E+00;
    cap[3][44].x = (float) -0.70193780544E+01;  cap[3][44].y = (float) 0.36965461800E+01;    cap[3][44].z = (float) 0.91517819913E+00;
    cap[3][45].x = (float) 0.16523352074E+00;   cap[3][45].y = (float) -0.18032304813E+01;   cap[3][45].z = (float) -0.49305142163E+01;
    cap[3][46].x = (float) -0.11573103944E+01;  cap[3][46].y = (float) -0.11893230741E+01;   cap[3][46].z = (float) -0.49714852095E+01;
    cap[3][47].x = (float) -0.12605392497E+01;  cap[3][47].y = (float) 0.22108796884E+00;    cap[3][47].z = (float) -0.52504323268E+01;
    cap[3][48].x = (float) -0.25794728950E+01;  cap[3][48].y = (float) 0.75361599776E+00;    cap[3][48].z = (float) -0.51733152286E+01;
    cap[3][49].x = (float) -0.28027074511E+01;  cap[3][49].y = (float) 0.21453478573E+01;    cap[3][49].z = (float) -0.47389600896E+01;
    cap[3][50].x = (float) 0.26644496516E+01;   cap[3][50].y = (float) -0.28435462096E+01;   cap[3][50].z = (float) -0.45123012806E+01;
    cap[3][51].x = (float) 0.22001072009E+01;   cap[3][51].y = (float) 0.13212985356E+01;    cap[3][51].z = (float) -0.42274981849E+01;
    cap[3][52].x = (float) 0.34848761367E+01;   cap[3][52].y = (float) 0.69294693172E+00;    cap[3][52].z = (float) -0.40171024281E+01;
    cap[3][53].x = (float) 0.43882121233E+01;   cap[3][53].y = (float) 0.11883035679E+01;    cap[3][53].z = (float) -0.29970595721E+01;
    cap[3][54].x = (float) 0.54077550723E+01;   cap[3][54].y = (float) 0.36060498625E+00;    cap[3][54].z = (float) -0.24476920823E+01;
    cap[3][55].x = (float) 0.61275551737E+01;   cap[3][55].y = (float) 0.80675134746E+00;    cap[3][55].z = (float) -0.12819119132E+01;
    cap[3][56].x = (float) 0.35784698679E+01;   cap[3][56].y = (float) -0.64465531335E+00;   cap[3][56].z = (float) -0.44393474850E+01;
    cap[3][57].x = (float) 0.25277602109E+01;   cap[3][57].y = (float) -0.14676089703E+01;   cap[3][57].z = (float) -0.49706567691E+01;
    cap[3][58].x = (float) 0.12410381593E+01;   cap[3][58].y = (float) -0.92156078036E+00;   cap[3][58].z = (float) -0.50694471974E+01;
    cap[3][59].x = (float) -0.39894863437E+01;  cap[3][59].y = (float) 0.58083051115E+01;    cap[3][59].z = (float) 0.14219366111E+01;
    cap[3][60].x = (float) -0.27891077023E+01;  cap[3][60].y = (float) 0.61425746567E+01;    cap[3][60].z = (float) 0.67675101993E+00;
    cap[3][61].x = (float) -0.17341355045E+01;  cap[3][61].y = (float) 0.67810476938E+01;    cap[3][61].z = (float) 0.14401766805E+01;
    cap[3][62].x = (float) -0.26416500505E+01;  cap[3][62].y = (float) 0.55000252031E+01;    cap[3][62].z = (float) -0.64803012252E+00;
    cap[3][63].x = (float) -0.36621284208E+01;  cap[3][63].y = (float) 0.47348285122E+01;    cap[3][63].z = (float) -0.12940342992E+01;
    cap[3][64].x = (float) -0.48361840605E+01;  cap[3][64].y = (float) 0.44386418572E+01;    cap[3][64].z = (float) -0.56295604184E+00;
    cap[3][65].x = (float) -0.49771198224E+01;  cap[3][65].y = (float) 0.50271444148E+01;    cap[3][65].z = (float) 0.71677155783E+00;
    cap[3][66].x = (float) -0.60934632823E+01;  cap[3][66].y = (float) 0.45909516215E+01;    cap[3][66].z = (float) 0.14564518832E+01;
    cap[3][67].x = (float) 0.62250744908E+00;   cap[3][67].y = (float) 0.31269666662E+01;    cap[3][67].z = (float) -0.37231933843E+01;
    cap[3][68].x = (float) 0.19476423274E+01;   cap[3][68].y = (float) 0.26239954193E+01;    cap[3][68].z = (float) -0.36829387134E+01;
    cap[3][69].x = (float) 0.10785602392E+01;   cap[3][69].y = (float) 0.54068473406E+00;    cap[3][69].z = (float) -0.48090614435E+01;
    cap[3][70].x = (float) -0.17393968925E+00;  cap[3][70].y = (float) 0.11055498947E+01;    cap[3][70].z = (float) -0.48995214127E+01;
    cap[3][71].x = (float) -0.44006718707E+00;  cap[3][71].y = (float) 0.24355601974E+01;    cap[3][71].z = (float) -0.43852749264E+01;
    cap[3][72].x = (float) -0.17860406639E+01;  cap[3][72].y = (float) 0.29334114802E+01;    cap[3][72].z = (float) -0.41530438557E+01;
    cap[3][73].x = (float) -0.13875948540E+01;  cap[3][73].y = (float) 0.55045018407E+01;    cap[3][73].z = (float) -0.13415237180E+01;
    cap[3][74].x = (float) -0.10816602975E+01;  cap[3][74].y = (float) 0.46780782608E+01;    cap[3][74].z = (float) -0.25314256051E+01;
    cap[3][75].x = (float) -0.21503536330E+01;  cap[3][75].y = (float) 0.39185313960E+01;    cap[3][75].z = (float) -0.31535540029E+01;
    cap[3][76].x = (float) -0.34823508771E+01;  cap[3][76].y = (float) 0.40141606547E+01;    cap[3][76].z = (float) -0.25651587619E+01;
    cap[3][77].x = (float) 0.24663823151E+00;   cap[3][77].y = (float) 0.42696137742E+01;    cap[3][77].z = (float) -0.28771473354E+01;
    cap[3][78].x = (float) 0.13087825816E+01;   cap[3][78].y = (float) 0.48739642843E+01;    cap[3][78].z = (float) -0.22172833310E+01;
    cap[3][79].x = (float) -0.30025910544E+00;  cap[3][79].y = (float) 0.60674159789E+01;    cap[3][79].z = (float) -0.59207743321E+00;
    cap[3][80].x = (float) -0.47015080754E+00;  cap[3][80].y = (float) 0.66469929056E+01;    cap[3][80].z = (float) 0.75076176236E+00;
    cap[3][81].x = (float) 0.78377067629E+00;   cap[3][81].y = (float) 0.69502445579E+01;    cap[3][81].z = (float) 0.15010993533E+01;
    cap[3][82].x = (float) 0.99428162544E+00;   cap[3][82].y = (float) 0.56735052099E+01;    cap[3][82].z = (float) -0.10902469016E+01;
    cap[3][83].x = (float) 0.29639384150E+01;   cap[3][83].y = (float) 0.31485718319E+01;    cap[3][83].z = (float) -0.28036662864E+01;
    cap[3][84].x = (float) 0.41637338162E+01;   cap[3][84].y = (float) 0.24428101575E+01;    cap[3][84].z = (float) -0.23693007584E+01;
    cap[3][85].x = (float) 0.49026698449E+01;   cap[3][85].y = (float) 0.28595856454E+01;    cap[3][85].z = (float) -0.11528240761E+01;
    cap[3][86].x = (float) 0.59058021710E+01;   cap[3][86].y = (float) 0.20209895859E+01;    cap[3][86].z = (float) -0.58885198538E+00;
    cap[3][87].x = (float) 0.25835618182E+01;   cap[3][87].y = (float) 0.42529284469E+01;    cap[3][87].z = (float) -0.20940560263E+01;
    cap[3][88].x = (float) -0.28062749705E+01;  cap[3][88].y = (float) -0.66368798173E+01;   cap[3][88].z = (float) -0.68453039179E+00;
    cap[3][89].x = (float) -0.15384587223E+01;  cap[3][89].y = (float) -0.66771218269E+01;   cap[3][89].z = (float) -0.13843873956E+01;
    cap[3][90].x = (float) -0.29903198921E+01;  cap[3][90].y = (float) -0.67557018742E+01;   cap[3][90].z = (float) 0.76541108211E+00;
    cap[3][91].x = (float) -0.17507117740E+01;  cap[3][91].y = (float) -0.71256372017E+01;   cap[3][91].z = (float) 0.14510273582E+01;
    cap[3][92].x = (float) -0.35026597295E+00;  cap[3][92].y = (float) -0.67174293764E+01;   cap[3][92].z = (float) -0.67607419775E+00;
    cap[3][93].x = (float) -0.43648129818E+00;  cap[3][93].y = (float) -0.70640163051E+01;   cap[3][93].z = (float) 0.66711274826E+00;
    cap[3][94].x = (float) -0.76842444280E+01;  cap[3][94].y = (float) 0.26369859554E+01;    cap[3][94].z = (float) 0.16679430268E+01;
    cap[3][95].x = (float) 0.32164176516E+01;   cap[3][95].y = (float) 0.47705528741E+01;    cap[3][95].z = (float) -0.90847477999E+00;
    cap[3][96].x = (float) 0.21695904656E+01;   cap[3][96].y = (float) 0.56594417519E+01;    cap[3][96].z = (float) -0.31784361562E+00;
    cap[3][97].x = (float) 0.44505915654E+01;   cap[3][97].y = (float) 0.40113313747E+01;    cap[3][97].z = (float) -0.38931257127E+00;
    cap[3][98].x = (float) 0.50890034792E+01;   cap[3][98].y = (float) 0.43596632579E+01;    cap[3][98].z = (float) 0.85785337730E+00;
    cap[3][99].x = (float) 0.20298162362E+01;   cap[3][99].y = (float) 0.63498829802E+01;    cap[3][99].z = (float) 0.89479069820E+00;
    cap[3][100].x = (float) 0.44394007870E+01;  cap[3][100].y = (float) 0.54464393035E+01;    cap[3][100].z = (float) 0.15820555980E+01;
    cap[3][101].x = (float) 0.39454420530E+01;  cap[3][101].y = (float) -0.28896679490E+01;   cap[3][101].z = (float) -0.38171379528E+01;
    cap[3][102].x = (float) 0.45441409267E+01;  cap[3][102].y = (float) -0.15543388643E+01;   cap[3][102].z = (float) -0.38380771818E+01;
    cap[3][103].x = (float) 0.41366706263E+01;  cap[3][103].y = (float) -0.37110428245E+01;   cap[3][103].z = (float) -0.26691313407E+01;
    cap[3][104].x = (float) 0.52084514909E+01;  cap[3][104].y = (float) -0.33625136282E+01;   cap[3][104].z = (float) -0.18417114013E+01;
    cap[3][105].x = (float) 0.54030082733E+01;  cap[3][105].y = (float) -0.10188536686E+01;   cap[3][105].z = (float) -0.28017308470E+01;
    cap[3][106].x = (float) 0.58097015616E+01;  cap[3][106].y = (float) -0.20774691375E+01;   cap[3][106].z = (float) -0.18719092053E+01;
    cap[3][107].x = (float) 0.61281717962E+01;  cap[3][107].y = (float) 0.34968779994E+01;    cap[3][107].z = (float) 0.14722175171E+01;
    cap[3][108].x = (float) 0.71524561940E+01;  cap[3][108].y = (float) 0.12360471500E+01;    cap[3][108].z = (float) 0.14839707629E+01;
    cap[3][109].x = (float) 0.72428511780E+01;  cap[3][109].y = (float) -0.91013542804E-02;   cap[3][109].z = (float) 0.75120937696E+00;
    cap[3][110].x = (float) 0.68820346010E+01;  cap[3][110].y = (float) -0.20913975592E+00;   cap[3][110].z = (float) -0.61688433125E+00;
    cap[3][111].x = (float) 0.65235436153E+01;  cap[3][111].y = (float) 0.23230838703E+01;    cap[3][111].z = (float) 0.66800236575E+00;
    cap[3][112].x = (float) 0.68398594782E+01;  cap[3][112].y = (float) -0.22554947714E+01;   cap[3][112].z = (float) 0.40870882145E+00;
    cap[3][113].x = (float) 0.63179898912E+01;  cap[3][113].y = (float) -0.35771173596E+01;   cap[3][113].z = (float) 0.39694371190E+00;
    cap[3][114].x = (float) 0.54329258323E+01;  cap[3][114].y = (float) -0.41879769539E+01;   cap[3][114].z = (float) -0.66390158760E+00;
    cap[3][115].x = (float) 0.66073744100E+01;  cap[3][115].y = (float) -0.15912966887E+01;   cap[3][115].z = (float) -0.82764811960E+00;
    cap[3][116].x = (float) 0.72761905274E+01;  cap[3][116].y = (float) -0.13246908678E+01;   cap[3][116].z = (float) 0.13980815612E+01;
    cap[3][117].x = (float) 0.62685425726E+01;  cap[3][117].y = (float) -0.42606948960E+01;   cap[3][117].z = (float) 0.15405588457E+01;
    cap[3][118].x = (float) 0.43168767014E+01;  cap[3][118].y = (float) -0.59536265241E+01;   cap[3][118].z = (float) 0.77014318327E+00;
    cap[3][119].x = (float) 0.32073538384E+01;  cap[3][119].y = (float) -0.67023387704E+01;   cap[3][119].z = (float) 0.14583053354E+01;
    cap[3][120].x = (float) 0.19751907838E+01;  cap[3][120].y = (float) -0.67562960649E+01;   cap[3][120].z = (float) 0.74440377661E+00;
    cap[3][121].x = (float) 0.43577056420E+01;  cap[3][121].y = (float) -0.52175801363E+01;   cap[3][121].z = (float) -0.47207558861E+00;
    cap[3][122].x = (float) 0.53510096191E+01;  cap[3][122].y = (float) -0.53990638900E+01;   cap[3][122].z = (float) 0.15576274634E+01;
    cap[3][123].x = (float) 0.32120768505E+01;  cap[3][123].y = (float) 0.63398270748E+01;    cap[3][123].z = (float) 0.16315574508E+01;
    cap[3][124].x = (float) 0.74576062711E+00;  cap[3][124].y = (float) -0.72007466769E+01;   cap[3][124].z = (float) 0.14325440011E+01;

    };

    atom * TCap::cap4SWNT(int
    n, int
    m){
        int
    id = -1;
    for (int i=0;i < 100;i++) if ((n == availableind[i][0]) & & (m == availableind[i][1])) id =availableind[i][2];
    return cap[id];
    };
    
"""
