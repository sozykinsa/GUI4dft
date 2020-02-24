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

##################################################################
######################## TPeriodTable ############################
##################################################################    

class TPeriodTableAtom:
    def __init__(self, charge, radius, let, color):
        self.charge = charge
        self.radius = radius
        self.let = let
        self.color = color

class TPeriodTable:
    """The TPeriodTable class provides basic fetches of Mendelevium's table. The constructor does not have arguments"""
    def __init__(self):
        self.table_size = 128
        self.Atoms = []
        self.default_color = [0.6, 0.6, 1.0]
        self.default_radius = 77
        self.Atoms.append(TPeriodTableAtom(0,    0, ' ',  [0.1, 1.0, 0.1]))
        self.Atoms.append(TPeriodTableAtom(1,   53, 'H',  [0.1, 0.6, 0.1]))
        self.Atoms.append(TPeriodTableAtom(2,   31, 'He', [0.5, 0.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(3,  145, 'Li', [1.0, 1.0, 0.15]))
        self.Atoms.append(TPeriodTableAtom(4,  112, 'Be', [0.3, 1.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(5,   98,  'B', [0.6, 0.3, 0.0]))
        self.Atoms.append(TPeriodTableAtom(6,   77,  'C', [0.2, 0.2, 0.8]))
        self.Atoms.append(TPeriodTableAtom(7,   92,  'N', [0.45, 0.3, 0.6]))
        self.Atoms.append(TPeriodTableAtom(8,   60,  'O', [1.0, 0.0, 0.5]))
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
                row.append(0)
            self.Bonds.append(row)

        self.Bonds[6][6] = 1.42
        self.Bonds[16][16] = 1.9
        self.Bonds[46][46] = 2.5
        self.Bonds[78][78] = 2.5
        self.Bonds[79][79] = 2.5

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
        pass

    def setSelected(self, fl):
        self.selected = fl

    def isSelected(self):
        return self.selected
        
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

    def get_LatVect1_norm(self):
        return norm(self.LatVect1)

    def get_LatVect2_norm(self):
        return norm(self.LatVect2)

    def get_LatVect3_norm(self):
        return norm(self.LatVect3)

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

    def edit_atom(self, ind, newAtom):
        if (ind>=0) and (ind<self.nAtoms()):
            self.atoms[ind] = newAtom

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
            for j in range(0, len(self.atoms)):
                cx+=self.atoms[j].x
                cy+=self.atoms[j].y
                cz+=self.atoms[j].z
                n+=1
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
                length = self.atom_atom_distance(i, j)
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
        text = self.toSIESTAfdfdata()
        print(text, file=f)
        f.close()
        
    def toSIESTAxyz(self, filename):
        """ созадет xyz файл, совместимый с XMol """
        f = open(filename,'w')
        text = self.toSIESTAxyzdata()
        print(text, file=f)
        f.close()     

    def toSIESTAfdfdata(self):
        """ возвращает данные для входного файла пакета SIESTA """
        data = ""
        PerTab = TPeriodTable()
        data+='NumberOfAtoms ' + str(len(self.atoms)) + "\n"
        types = self.typesOfAtoms()
        data+='NumberOfSpecies '+str(len(types))+"\n"
        data+='%block ChemicalSpeciesLabel\n'
        for i in range(0,len(types)):
            data+=' '+str(i+1)+'  '+str(types[i][0])+'  '+str(PerTab.get_let(int(types[i][0])))+"\n"
        data+='%endblock ChemicalSpeciesLabel\n'
        data+='%block Zmatrix\n'
        data+='cartesian\n'
        for i in range(0, len(self.atoms)):
            str1 = ' '
            for j in range(0,len(types)):
                if types[j][0] == self.atoms[i].charge:
                    str1 = ' ' + str(j+1)
            str2 = '    ' + str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
            str3 = '      1  1  1'
            data+= str1+str2+str3+"\n"    
        data+='%endblock Zmatrix\n'
        return data

    def toSIESTAxyzdata(self):
        """ возвращает данные для xyz файла """
        data = "  "
        nAtoms = self.nAtoms()
        data+= str(nAtoms) + "\n"
        for i in range(0, nAtoms):
            data+= "\n"+self.atoms[i].let + '       '+ str(round(self.atoms[i].x, 7)) + '     ' + str(round(self.atoms[i].y, 7)) + '      ' + str(round(self.atoms[i].z, 7))
        return data
  
##################################################################
########################### TSWNT ################################
##################################################################    

class TSWNT(TAtomicModel):
    """The TSWNT class provides """
    def __init__(self, n, m, leng = 0, ncell = 1):
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
        ifp = np.zeros(maxMol)
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
            newModel = TSIESTA.atoms_from_xyz_structure(NumberOfAtoms, f, periodTable)
            molecules.append(newModel)
        return molecules

    @staticmethod
    def atoms_from_xyz_structure(NumberOfAtoms, ani_file, periodTable):
        str1 = Helpers.spacedel(ani_file.readline())
        atoms = []
        for i1 in range(0, NumberOfAtoms):
            str1 = Helpers.spacedel(ani_file.readline())
            S = str1.split(' ')
            d1 = float(S[1])
            d2 = float(S[2])
            d3 = float(S[3])
            C = S[0]
            Charge = periodTable.get_charge_by_letter(C)
            A = [d1, d2, d3, C, Charge]
            atoms.append(A)
        newModel = TAtomicModel(atoms)
        newModel.set_lat_vectors_default()
        return newModel

    @staticmethod
    def lattice_constant(filename):
        """ Returns the LatticeConstant from SIESTA output file """
        mult = 1
        property = (Helpers.fromFileProperty(filename,'LatticeConstant',1,'unformatted')).split()
        if property[1].lower() == "bohr":
            mult = 0.52917720859
        return mult*property[0]

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
        for child in root:
            # print(child.tag)
            if child.tag == "energy_values":
                data = (child.text).split()
                data = Helpers.list_str_to_float(data)
                energy = np.array(data)
                pdos = np.zeros((2, len(energy)))

            if child.tag == "orbital":
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
                    #print(child.attrib['species'])
                    for children in child:
                        data = (children.text).split()
                        data = Helpers.list_str_to_float(data)
                        data = np.array(data)
                        data = data.reshape((2, len(energy)), order='F')
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
    def ChargesSIESTA4(filename, method):
        """Заряды всех атомов в выходном файле SIESTA (Hirshfeld, Voronoi, Mulliken)"""
        charges = []
        if os.path.exists(filename):
            NumberOfAtoms = TSIESTA.number_of_atoms(filename)
            NumberOfSpecies = TSIESTA.number_of_species(filename)

            if method == "Mulliken":
                """Заряды всех атомов в выходном файле SIESTA4 (Милликен)"""
                SpinPolarized = Helpers.fromFileProperty(filename, 'redata: Number of spin components        =', 1,
                                                         'string')
                MdSiestaFile = open(filename)
                str1 = MdSiestaFile.readline()
                skip = 0
                step = 0

                if (SpinPolarized == '2'):
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
                                if (SpinPolarized == '2'):
                                    neutral = neutral / 2.0
                            if (AtomSort == "S"):
                                skip = 2
                                neutral = 6
                                if (SpinPolarized == '2'):
                                    neutral = neutral / 2.0
                            if (AtomSort == "Li") or (AtomSort == "H"):
                                skip = 1
                                neutral = 1
                                if (SpinPolarized == '2'):
                                    neutral = neutral / 2.0

                            if (AtomSort == "C"):
                                for i in range(0, skip - 1):
                                    str1 = MdSiestaFile.readline()
                            else:
                                for i in range(0, skip):
                                    str1 = MdSiestaFile.readline()
                            ch = 0

                            while (str1 != '\n'):
                                for i in range(0, skip):
                                    str1 = MdSiestaFile.readline()
                                if (str1 != '\n'):
                                    atoms += 1
                                    str1 = Helpers.spacedel(str1)
                                    ch += neutral - float(str1.split(' ')[1])

                            if (SpinPolarized == '2') and (nsp > NumberOfSpecies / 2.0):
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
                spinDown.append(float(line1[2]))
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
        ans = "NotScaledCartesianBohr"
        if (format.lower() == "ang") or (format.lower() == "notscaledcartesianang"):
            ans = "NotScaledCartesianAng"
        if (format.lower() == "fractional") or (format.lower() == "scaledbylatticevectors"):
            ans = "ScaledByLatticeVectors"
        if (format.lower() == "scaledcartesian"):
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
        return Helpers.fromFileProperty(filename,'SystemLabel',1,"string")      
        
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
        beta_opt, beta_cov = curve_fit(TCalculators.fParabola, xdata, ydata)
        print(beta_opt)

        xmin = xdata.min()
        xmax = xdata.max()

        x = np.linspace(xmin, xmax, 200)
        y = TCalculators.fParabola(x, *beta_opt)

        return beta_opt, x.tolist(), y.tolist()

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

    def get_all_data(self, atoms):
        structure = TAtomicModel(atoms)
        st = structure.toSIESTAfdfdata()

        for prop in self.properties:
            if (prop.lower().find("numberofatoms")==-1) and (prop.lower().find("numberofspecies")==-1):
                st += prop

        for block in self.blocks:
            if (((block.name).lower().find("zmatrix")==-1) and ((block.name).lower().find("chemicalspecieslabel")==-1)):
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
                        newlines.append('   ' + str(ind) + '   ' + str(model.AtList[j].x) + '   ' + str(
                            model.AtList[j].y) + '   ' + str(model.AtList[j].z) + '   ' + str(dx) + '   ' + str(
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

