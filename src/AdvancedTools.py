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
from pylab import polyfit
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi


##################################################################
############################ Helpers  ############################
############################ 17.11.19 ############################
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
    def RoundToPlane(atom, R):
        """ RoundToPlane  """
        z  = atom[2]
        fi = math.asin(atom[0]/R)
        if (atom[1]<=-1e-3):
            fi = 3.14 - fi
        x = -R*fi
        return [x,z]    

            
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
    def AddLinesToFile(filename1, filename2, string):                
        f2 = open(filename2, 'w')

        with open(filename1) as openfileobject:
            for line in openfileobject:
                f2.write(line)
        
        f2.write(string)
        f2.close()

        
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
    def LSM(TheList):
        """ Метод наименьших квадратов для аппроксимации полиномом второй степени вида A + Bx + Cx^2. Возвращает список коэффициентов [A,B,C] """                        
        ans = [0,0,0]
        
        x4 = 0
        x3 = 0
        x2 = 0
        x1 = 0
        x0 = len(TheList)
        x2y=0
        x1y=0
        x0y=0
        
        for i in range(0,len(TheList)):
            x4 += math.pow(float(TheList[i][0]),4)
            x3 += math.pow(float(TheList[i][0]),3)
            x2 += math.pow(float(TheList[i][0]),2)
            x1 += float(TheList[i][0])
            x2y+= math.pow(float(TheList[i][0]),2)*float(TheList[i][1])
            x1y+= float(TheList[i][0])*float(TheList[i][1])
            x0y+= float(TheList[i][1])
        
        alpha1 = x2 - x3*x3/x4
        alpha2 = x1 - x2*x3/x4
        alpha3 = x1y - x3*x2y/x4
        
        betta1 = x1 - x3*x2/x4
        betta2 = x0 - x2*x2/x4
        betta3 = x0y - x2*x2y/x4
        
        ans[0] = (betta3 - betta1*alpha3/alpha1)/(betta2 - betta1*alpha2/alpha1)
        ans[1] = (alpha3-alpha2*ans[0])/alpha1
        ans[2] = (x2y-x2*ans[0] - x3*ans[1])/x4
        return ans    

    @staticmethod
    def LSM2(TheList):
        """ Метод наименьших квадратов для аппроксимации полиномом второй степени вида Cx^2. Возвращает коэффициент C """                        

        x4 = 0
        x2y=0
        
        for i in range(0,len(TheList)):
            x4 += math.pow(float(TheList[i][0]),4)
            x2y+= math.pow(float(TheList[i][0]),2)*float(TheList[i][1])
        
        return x2y / x4    
        
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
                            """property = int(re.sub(r'\s', '', str1))"""
                        if (type == 'float'):
                            property = float(prop1)
                            """property = float(re.sub(r'\s', '', str1))"""    
                        
                    if (k == count):
                        return property
                    k+=1
                
                str1 = MyFile.readline()
            MyFile.close()
        return property            
        
        
    @staticmethod
    def List2DToFile(filename,Title,List):
        """ Записывает двумерный список List в файл filename с заголовком Title в начале файла """
        f = open(filename, 'w')
        if (len(Title)>0):
            line = ''
            for k in range(0,len(Title)):
                line += str(Title[k]) + '    '
            f.write(line+'\n')
        for i in range(0,len(List)):
            line = ''
            for k in range(0,len(List[i])):
                line += str(List[i][k]) + '    '
            f.write(line+'\n')
        f.close()

        
    @staticmethod
    def List2DToMonitor(self,Title,List):
        """Puts 2D list to the monitor"""
        line = ''
        for k in range(0,len(Title)):
            line += str(Title[k]) + '    '
            print(line)
        for i in range(0,len(List)):
            line = ''
            for k in range(0,len(List[i])):
                line += str(List[i][k]) + '    '
            print(line)
    
    def deltaBonds(self,B1,B2):
        """Not documented"""
        max = B1[0][2]-B2[0][2]
        min = B1[0][2]-B2[0][2]
        avr = 0
        
        for i in range(0,len(B1)):
            delta = math.fabs(B1[i][2]-B2[i][2])
            if (delta > max):
                max = delta
            if (delta < min):
                min = delta
            avr += delta
            
        avr /= len(B1)    
        return max
        
    
    def dev(self,model1, model2):
        """Not documented"""
        res = []    
        k = 6    
        for i in range(0,len(model1)):
            rx = round( model2[i][0] - model1[i][0] , k)
            ry = round( model2[i][1] - model1[i][1] , k)
            rz = round( model2[i][2] - model1[i][2] , k)
            r = round( math.sqrt(rx*rx+ry*ry+rz*rz) , k)
            res.append([rx,ry,rz,model1[i][3],model1[i][4],r])
        return res
        
    @staticmethod    
    def List3DAverage(list3D):
        """Not documented"""
        list2D = []
        firstDim = len(list3D)
        secondDim = len(list3D[0])
        therdDim = len(list3D[0][0])
        
        for item in list3D:
            if (len(item)<secondDim):
                secondDim = len(item)
            if (len(item[0])<therdDim):
                therdDim= len(item[0])
        print  ('list ' + firstDim + 'x' + secondDim + 'x' + therdDim)
        
        for i in range(0, secondDim):
            row = []
            for j in range(0, therdDim):
                row.append(0)
            list2D.append(row)
        
        for i in range(0, secondDim):
            for j in range(0, therdDim):
                for k in range(0, firstDim):
                    list2D[i][j] += list3D[k][i][j]
                list2D[i][j] = list2D[i][j]/len(list3D)    
        return list2D
        
    
    def Disp(self,model1,model2):
        """Not documented"""
        result = []
        if (len(model1)==len(model2)):
            for i in range(0,len(model1)-1):
                result.append([i, model2[i][0] - model1[i][0], model2[i][1] - model1[i][1], model2[i][2] - model1[i][2], model1[i][3], model1[i][4]])
        return result

##################################################################
######################## TPeriodTable ############################
################# The class needs to be rewrite ##################
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
        self.table_size = 110
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

        for i in range(37,self.table_size):
            self.Atoms.append(TPeriodTableAtom(i, self.default_radius, 'C', self.default_color))

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
###################### The molecula class ########################
##################################################################
    
class TAtomicModel(object):
    """The TMolecula class provides basic fetches of molecules."""

    def __init__(self, newatoms=[]):
        self.atoms = []

        #from atomicmodel
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
    
    def AngleToCenterOfAtoms(self,atomslist):
        """The method AngleToCenterOfAtoms returns the Angle To Center Of atoms_from_fdf list atomslist in the molecule"""
        angle = 0
        
        for at in range(0,len(atomslist)):
            x = self.atoms[atomslist[at]].x
            y = self.atoms[atomslist[at]].y
            fi = math.atan(x/y)
            angle+=fi
        angle /= len(atomslist)
        return angle

    def RotateModel(self,alpha):
        """The method RotateAtList rotate the AtList on alpha Angle"""
        newmolecula = []
        xnn = []
        ynn = []
        
        #oz
        for i in range(0, len(self.atoms)):
            xnn.append(float(self.atoms[i].x) * math.cos(alpha) - float(self.atoms[i].y) * math.sin(alpha))
            ynn.append(float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].y) * math.cos(alpha))
        for i in range(0, len(self.atoms)):
            newmolecula.append(TAtom([xnn[i], ynn[i], self.atoms[i][2], self.atoms[i][3], self.atoms[i][4]]))
        
        return newmolecula

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
        



    def TorsionModel(self,alp):
        """ закручивает модель вокруг оси z на заданный угол на 1 нм длины модели """
        min= self.minZ()
        max= self.maxZ()
        lenghtz = max - min
        
        alfa=alp*lenghtz*0.1
    
        for at in self.atoms:
            yg = (at.z- min)*alfa/lenghtz;
            xxx = at.x*math.cos(yg) + at.y*math.sin(yg)
            yyy = at.y*math.cos(yg) - at.x*math.sin(yg)
            at.x = xxx
            at.y = yyy
        


    def CyclicShiftZ(self,boxZ,dz):
        """ Циклический сдвиг вдоль оси Z """
        for i in range(0, len(self.atoms)):
            self.atoms[i].z+=dz
            if (self.atoms[i].z>boxZ):
                self.atoms[i].z-=boxZ
        return self.atoms

    def PutAtListInTheBox(self, dx, dy, dz):
        """The method puts Molecula in the box"""

        self.SetBox(dx, dy, dz)

        for i in range(0, len(self.atoms)):
            while (self.atoms[i].x < -dx / 2):
                self.atoms[i].x += dx
            while (self.atoms[i].y < -dy / 2):
                self.atoms[i].y += dy
            while (self.atoms[i].z < -dz / 2):
                self.atoms[i].z += dz

            while (self.atoms[i].x > dx / 2):
                self.atoms[i].x -= dx
            while (self.atoms[i].y > dy / 2):
                self.atoms[i].y -= dy
            while (self.atoms[i].z > dz / 2):
                self.atoms[i].z -= dz
        return self.atoms
        
    def PutAtomsInTheBox(self,dx,dy,dz):
        """The method puts Molecula in the box"""
        
        self.PutAtListInTheBox(dx,dy,dz)
        
        model0 = TAtomicModel(self.atoms)
        modelst= TAtomicModel(self.atoms)
        compst = modelst.CompactnessC(3)
        
        N = 50
        
        for i in range(0,N):    
            model0.CyclicShiftZ(dz,dz/((1.0)*N))            
            comp = model0.CompactnessC(3)
            if (comp<compst):
                compst = comp
                modelst= TAtomicModel(model0.atoms)
        self.atoms = modelst.atoms
        return self.atoms, compst
        
        
    def SubMolecula(self,charge):
        """ возвращает часть молекулы с атмами заданного заряда """

        SubAtoms = []    
        for at in range(0, len(self.atoms)):
            if (int(self.atoms[at].charge) == int(charge)):
                SubAtoms.append(self.atoms[at])
        return TAtomicModel(SubAtoms)
        

    def NearestAtom(self,atom1,charge):
        """distanse to the nearest atom with charge "charge" and selected atom
        
        atom1 - number of atom
        
        charge - charge of atom
        
        """
        dist = 0    
        at = 0        
        
        while (dist==0) and (at<len(self.atoms)):
            if (int(self.atoms[at].charge) == int(charge)) and (int(atom1) != int(at)):
                x = self.atoms[at].x - self.atoms[atom1].x
                y = self.atoms[at].y - self.atoms[atom1].y
                z = self.atoms[at].z - self.atoms[atom1].z
                ro = math.sqrt(x*x+y*y+z*z)
                dist = ro                
            at+=1
        for at in range(0, len(self.atoms)):
            if (int(self.atoms[at].charge) == int(charge)) and (int(atom1) != int(at)):
                x = self.atoms[at].x - self.atoms[atom1].x
                y = self.atoms[at].y - self.atoms[atom1].y
                z = self.atoms[at].z - self.atoms[atom1].z
                ro = math.sqrt(x*x+y*y+z*z)
                if ro < dist:
                    dist = ro
        return dist
        
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
        
    def CompactnessC(self,charge):
        """ Function returns the average distance of atoms from the center of mass """
        length = 0
        n = 0
        cm = self.centr_mass(charge)
        for i in range(0, len(self.atoms)):
            if (int(self.atoms[i].charge) == int(charge)):
                l = math.sqrt(
                    math.pow(float(self.atoms[i].x) - float(cm[0]), 2) +
                    math.pow(float(self.atoms[i].y) - float(cm[1]), 2) +
                    math.pow(float(self.atoms[i].z) - float(cm[2]), 2) )
                length +=l
                n+=1
        if (n!=0):
            return length / n 
        else:
            return 0    
        
    
    def Compactness(self,charge):
        """ Function returns the average distance of between atoms (periodic doundaries) """
        model = self.SubMolecula(charge)
        length = 0
        n = 0        
        numbAtoms = model.nAtoms()
        for i in range(0,numbAtoms):
            rr = 100000
            for j in range(0,numbAtoms):
                if (i!=j):
                    dx = abs(float(model.atoms[i].x) - float(model.atoms[j].x))
                    dy = abs(float(model.atoms[i].y) - float(model.atoms[j].y))
                    dz = abs(float(model.atoms[i].z) - float(model.atoms[j].z))
                    if (self.boxX > 0):
                        while (dx>self.boxX):
                            dx -= self.boxX
                    if (self.boxY > 0):
                        while (dy>self.boxY):
                            dy -= self.boxY                            
                    if (self.boxZ > 0):
                        while (dz>self.boxZ):
                            dz -= self.boxZ
                    l = math.sqrt( math.pow(dx,2) + math.pow(dy,2) + math.pow(dz,2) )
                    
                    if(l<rr):
                        rr = l
        
            length += rr
            n+=1
        
        if (n!=0):
            return length / n
        else:
            return 0
    
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

    def BondsHistogram(self, charge1, charge2, rmin = 0.5, rmax = 6, full = 1):
        """ Гистограмма длин связей
        Параметры:
        charge1, charge2 - заряды атомов, между которыми нужно считать длины связей
        rmin, rmax - минимальное и максимальное расстояния
        full - значение я уже не помню, нужно подумать, нужен ли он вообще
        """
                
        TheBondsHistogram = []
        dr = 1e-2
        r = rmin
        while r<rmax:
            n = 0
            for i in range(0, len(self.atoms)):
                for j in range(i+1, len(self.atoms)):
                    if (float(self.atoms[i].charge) == float(charge1)) and (float(self.atoms[j].charge) == float(charge2)):
                        a = self.atom_atom_distance(i, j)
                        if (a >= r) and (a < r+dr):
                            n +=1
            r+=dr
            if not ((full == 0) and (n == 0)):
                TheBondsHistogram.append([r,n])
        return TheBondsHistogram
    
        
    def elongatezbyleng(self, elongbyangstr):
        """ Растягивает модель на заданное количество ангестрем на единицу длины по оси Z """
        minv = self.minZ()
        for atom in self.atoms:
            atom.z += (atom.z - minv) * elongbyangstr
        
        return self.atoms

        
    def grow(self):
        """ модель транслируется в трех измерениях и становится в 27 раз больше """
        #self.PutAtListInTheBox(Lx, Ly, Lz)

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
#################### The TMDanalysis class #######################
##################################################################
    
class TMDanalysis:
    
    molecules = []    
    
    def __init__(self, s = []):
        """Not documented"""
        self.molecules = s
    
    def Rotate(self,alpha):
        """ Вращает все молекулы на угол alpha """
        for item in self.molecules:
            item = item.RotateModel(alpha)        
            
    def Lkvadrat(self,pos1=0):
        """Square of displacement. Starting with pos1 step"""
        if (len(self.molecules)<pos1):
            return []
            
        model0 = self.molecules[pos1]
        
        LKV = []    
        LKVx = [0,0,0,0,0,0,0,0,0]
        LKVy = [0,0,0,0,0,0,0,0,0]
        LKVz = [0,0,0,0,0,0,0,0,0]
        LKV3D= [0,0,0,0,0,0,0,0,0]
        Niter= [0,0,0,0,0,0,0,0,0]
        
        step = pos1
        for pos in range(pos1,len(self.molecules)):
            item = self.molecules[pos]
            iter = 0
            step += 1
            for it in range(0,len(item.AtList)):
                fl = 1
                for j in range(0,it):
                    if(item.AtList[it][3]==item.AtList[j][3]):
                        fl=0
                if(fl):
                    iter+=1
                    LKVx[iter]  = 0
                    LKVy[iter]  = 0
                    LKVz[iter]  = 0
                    LKV3D[iter] = 0
                    Niter[iter] = 0
                    for j in range(it,len(item.AtList)):
                        if(item.AtList[it][3]==item.AtList[j][3]):
                            Niter[iter]+=1
                            LKVx[iter] += math.pow(item.AtList[it][0] - model0.AtList[it][0],2)
                            LKVy[iter] += math.pow(item.AtList[it][1] - model0.AtList[it][1],2)
                            LKVz[iter] += math.pow(item.AtList[it][2] - model0.AtList[it][2],2)
                            LKV3D[iter]+= math.sqrt(math.pow(item.AtList[it][0] - model0.AtList[it][0],2) + math.pow(item.AtList[it][1] - model0.AtList[it][1],2) + math.pow(item.AtList[it][2] - model0.AtList[it][2],2))
            row = [step]
            for it in range(1,iter+1):
                #row.append(math.sqrt(LKVx[it] + LKVy[it] + LKVz[it])/Niter[it])
                row.append(LKV3D[it]/Niter[it])
            LKV.append(row)
        return LKV    
        
    def TimeBetweenHops(self,atom):
        """ Количество шагов между перепрыгиванием атома к другому гексагону """
        times = []
        kol = 0
        
        neighbors = []
        
        for mol in range(0,len(self.molecules)):
            neighbors.append([])
        for mol in range(0,len(self.molecules)):
            print(mol)
            neighbors[mol] = self.molecules[mol].nearestHexagonOfSWNT(atom)
        
        neighbor = neighbors[0]
        for mol in range(0,len(self.molecules)):
            neighbor1 = neighbors[mol]
            if (neighbor == neighbor1):
                kol+=1
            else:
                times.append([kol, neighbor1])
                kol = 0
                neighbor = neighbor1                
                
        if(kol>0):
            times.append([kol, neighbor1])
        
        return times
        
    def TrajectoryOfAtoms(self,atomslist,radius):
        """This method returns projections on cylinder with radius for atoms from atomslist"""
        res = []    
        for i in range(0,len(self.molecules)):
            res.append(self.molecules[i].ProjectionToCylinder(atomslist,radius))    
        return res
        
        
    def PutMoleculesInTheBox(self,demX,demY,demZ):
        """Not documented"""    
        for i in range(0,len(self.molecules)):
            self.molecules[i].PutAtListInTheBox(demX,demY,demZ)
        return []
        
        
    def ModelEvolution(self):
        """Not documented"""
        result = []
        S = len(self.molecules[0].AtList)
        StatFrom = 1
        StatFinish = len(self.molecules)
    
        D = []
        for i in range(0,S):
            D.append([0,0,0])
            
        Cil = []
        for i in range(0,S):
            Cil.append([0,0,0])
        
        iter=0
        disp  = [0,0,0,0,0,0,0,0]    
        dispD = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        dispC = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]  
        
        for l in range(StatFrom,StatFinish-1):    
            field0 = [l]
            
            for j in range(0,S):        
                D[j][0]=self.molecules[l+1].AtList[j][0] - self.molecules[StatFrom].AtList[j][0] 
                D[j][1]=self.molecules[l+1].AtList[j][1] - self.molecules[StatFrom].AtList[j][1] 
                D[j][2]=self.molecules[l+1].AtList[j][2] - self.molecules[StatFrom].AtList[j][2] 
    
                z1 = self.molecules[StatFrom].AtList[j][2]
                z2 = self.molecules[l+1].AtList[j][2] 
                ro1= math.sqrt(math.pow(self.molecules[StatFrom].AtList[j][0],2)+math.pow(self.molecules[StatFrom].AtList[j][1],2))
                ro2= math.sqrt(math.pow(self.molecules[l+1].AtList[j][0],2)+math.pow(self.molecules[l+1].AtList[j][1],2))
                fi1= math.atan(self.molecules[StatFrom].AtList[j][1]/self.molecules[StatFrom].AtList[j][0])
                fi2= math.atan(self.molecules[l+1].AtList[j][1]/self.molecules[l+1].AtList[j][0])
                Cil[j][0]=ro2-ro1;
                Cil[j][1]=math.fabs(fi2)-math.fabs(fi1);
                Cil[j][2]=z2-z1;            
    
            iter=0
            lk = 0
            
            for ijk in range(0, S):
                fl = 1
                for j in range(0,ijk):
                    if(self.molecules[StatFrom].AtList[ijk][3] == self.molecules[StatFrom].AtList[j][3]):
                        fl=0
                if(fl==1):
                    iter+=1
                    disp[iter] = 0
                    for lk in range(0,3):
                        dispC[iter][lk] = 0
                        dispD[iter][lk] = 0
                                    
                    cou = 0                
                    for j in range(0,S):
                        if(self.molecules[StatFrom].AtList[ijk][3] == self.molecules[StatFrom].AtList[j][3]):
                            disp[iter] +=D[j][0]*D[j][0]+D[j][1]*D[j][1]+D[j][2]*D[j][2]
                            for lk in range(0,3):
                                dispC[iter][lk] += math.fabs(Cil[j][lk])
                                dispD[iter][lk] += math.fabs(D[j][lk])
                                
                            cou+=1
                    disp[iter] /= cou
                    for lk in range(0,3):
                        dispC[iter][lk] /= cou
                        dispD[iter][lk] /= cou                    
    
            for j in range(1,iter+1): 
                field0.append("%.6f" % (math.sqrt(math.fabs(disp[j])))) 
                field0.append("%.6f" % (dispD[j][0])) 
                field0.append("%.6f" % (dispD[j][1])) 
                field0.append("%.6f" % (dispD[j][2])) 
                field0.append("%.6f" % (dispC[j][0])) 
                field0.append("%.6f" % (dispC[j][1])) 
                field0.append("%.6f" % (dispC[j][2])) 
            result.append(field0)
            
        row = "     N    "
        S = len(self.molecules[0].AtList)
        for ijk in range(0, S):
            fl = 1
            for j in range(0,ijk):
                if(self.molecules[0].AtList[ijk][3] == self.molecules[0].AtList[j][3]):
                    fl=0
            if(fl==1):
                row += str(self.molecules[1].AtList[ijk][4]) +  "_disp    "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_dispx   "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_dispy   "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_dispz   "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_cilro   "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_cilfi   "  
                row += str(self.molecules[1].AtList[ijk][4]) +  "_cilz    " 
            
        return result, row    
    
    def FromLammpsOutput(self,filename,Species, regime = 'coord'):
        """LAMMPS IMPORTER"""
        PeriodTable = TPeriodTable()
        self.molecules = []
        if os.path.exists(filename):
            MdLammpsFile = open(filename)
            #n = 0
            numberOfAtoms = 1
                    
            str1 = " "    
            while str1!='':
                str1 = MdLammpsFile.readline()
                atoms = []
                if str1 != '' and (str1.find("NUMBER OF ATOMS")>=0):
                    str1 = MdLammpsFile.readline()
                    numberOfAtoms = int(str1)
                    
                    if(regime == "coord"):
                        while str1 != '' and (str1.find('ITEM: ATOMS id type xs ys zs')<0): 
                            str1 = MdLammpsFile.readline()
                    else:                    
                        while str1 != '' and (str1.find('ITEM: ATOMS id type fx fy fz')<0): 
                            str1 = MdLammpsFile.readline()
                    
                    atoms = [1]
                    atoms *=numberOfAtoms
                    
                    if str1 != '':
                        for i in range(0,numberOfAtoms):
                            str1 = MdLammpsFile.readline() + ' '
                            
                            maxI = len(str1)
                            
                            S = ""
                            i = 0                    
        
                            while (str1[i] != ' ') and (i < maxI):
                                S += str1[i]
                                i+=1
                            
                            order = int(S)
    
                            S = ""    
                            
        
                            while (i < maxI) and (str1[i] == ' '):
                                i+=1
        
                            while (i < maxI) and (str1[i] != ' '):
                                S += str1[i]
                                i+=1
                            
                            type = float(S)
                                
                            S = ""                    
                            while str1[i] == ' ':
                                i+=1
                            while (str1[i] != ' ') and (i < maxI):
                                S += str1[i]
                                i+=1
                            
                            d1 = float(S)
                            
                            while str1[i] == ' ':
                                i+=1
                            
                            S = "";
                            while (str1[i] != ' ') and (i < maxI):
                                S += str1[i]
                                i+=1
                            d2 = float(S)
                            
                            while str1[i] == ' ':
                                i+=1
                            
                            S = ""
                            while (str1[i] != ' ') and (i < maxI):
                                S += str1[i]
                                i+=1
                            d3 = float(S)
                                                
                            Charge = str(Species[int(type)-1])
                            C = PeriodTable.get_let(Charge)
                            A = [d1,d2,d3,Charge,C]        
                            atoms[order-1] = A            
                    
                        str1 = MdLammpsFile.readline()
                        self.molecules.append(atoms)
            MdLammpsFile.close()        
        return self.molecules

        
    def fromsiestaMdCar(self,FDFfile, MdCarfile, step = 1):
        """Imports coordinates from siesta *.MD_CAR file"""
        self.molecules = []
        if os.path.exists(FDFfile) and os.path.exists(MdCarfile):
            NumberOfSpecies = Helpers.fromFileProperty(FDFfile,'number_of_species')
            NumberOfAtoms = Helpers.fromFileProperty(FDFfile,'number_of_atoms')
            Species = TSIESTA.Species(FDFfile)

            f = open(MdCarfile)
            
            i = 0
            N = 0
            atoms = []
            spec = []
            
            for line in f:
                if i==0:
                    title = line
                    atoms = []
                if i==1:
                    scale = float(line)
                if i==2:
                    vec1 = line.split()
                if i==3:
                    vec2 = line.split()
                if i==4:
                    vec3 = line.split()
                    vecs = np.array([vec1,vec2,vec3], dtype=np.float)
                if i==5:
                    spec = []
                    nAtoms = line.split()
                    for ii in range(0,len(nAtoms)):
                        for j in range(0,int(nAtoms[ii])):
                            spec.append(ii)
                if i==6:
                    direct = line
                if i>6:
                    atom = np.array(line.split(), dtype=np.float)
                    atom = vecs.dot(atom)

                    Charge = Species[spec[i-7]][1] 
                    C = Species[spec[i-7]][2]
                    A = [atom[0],atom[1],atom[2],C,Charge]
                    atoms.append(A)                    
                    
                i=(i+1)%(NumberOfAtoms+7)
                if i==0:
                    N=(N+1)%step
                    if N == 0:
                        self.molecules.append(TAtomicModel(atoms))
                
            f.close()
        return self.molecules

    
  
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


    def nearestHexagonOfSWNT(self,Natom,Hexagons):
        """ The nearest Hexagon Of SWNT if know all hexagons """
        hexagon = []
        if(len(Hexagons)!=0):
            Radius = 500
            
            for Nlist in Hexagons:
                n = len(Nlist)
                Rad = 0
                for j in range(0,n):
                    Rad += self.atom_atom_distance(Nlist[j], Natom, 9.893)
                Rad /= n

                if (Rad<Radius):
                    Radius = Rad
                    hexagon = copy.deepcopy(Nlist)

        return hexagon
        

    def nearestHexagonOfSWNTslow(self,Natom,Rout = 4.5):
        """ The nearest Hexagon Of SWNT if we don't know all hexagons """
        hexagon = []
        alist  = self.indexes_of_atoms_with_charge(6)
        atlist = self.indexes_of_atoms_in_ball(alist, Natom, Rout)
        n = len(atlist)
        neighbors = np.zeros((n,n))
        
        for i in range(0,n):
            for j in range(0,n):
                neighbors[i][j] = self.atom_atom_distance(atlist[i], atlist[j], 9.893)
        
        neighb = []
        
        for i in range(0,n):
            nb = []
            nb.append([i])
            for j in range(0,6):
                nb1 = []
                while (len(nb)>0):
                    nbr = nb.pop()
                    for k in range(0,n):
                        if (k not in set(nbr)):
                            if (neighbors[nbr[len(nbr)-1]][k]<2):
                                nbr2 = copy.deepcopy(nbr)
                                nbr2.append(k)
                                nb1.append(nbr2)
                            elif (neighbors[nbr[0]][k]<1.6):
                                nbr2 = copy.deepcopy(nbr)
                                nbr2.insert(0,k)
                                nb1.append(nbr2)
                nb = copy.deepcopy(nb1)
            for it in nb:
                if (neighbors[it[0]][it[5]]<1.6):
                    neighb.append([atlist[it[0]],atlist[it[1]],atlist[it[2]],atlist[it[3]],atlist[it[4]],atlist[it[5]]] )
        neig = []
        for it in neighb:
            set1 = set(it)
            fl = 1
            for it1 in neig:
                if(set1 == it1):
                    fl = 0
            if(fl == 1):
                neig.append(set1)
        
        if(len(neig)!=0):
            Radius = 500
            
            for it in neig:
                Nlist = list(it)
                n = len(Nlist)
                
                Rad = 0
                for j in range(0,n):
                    Rad += self.atom_atom_distance(Nlist[j], Natom, 9.893)
                Rad /= n

                if (Rad<Radius):
                    Radius = Rad
                    hexagon = copy.deepcopy(Nlist)
        else:    
            hexagon = self.nearestHexagonOfSWNT(Natom,Rout + 1)
        return hexagon
            
    def HexagonsOfSWNT(self):
        hexagon = []
        atlist = self.indexes_of_atoms_with_charge(6)
        n = len(atlist)
        neighbors = np.zeros((n,n))
        
        for i in range(0,n):
            for j in range(0,n):
                neighbors[i][j] = self.atom_atom_distance(atlist[i], atlist[j], 9.893)
        
        neighb = []
        
        for i in range(0,n):
            nb = []
            nb.append([i])
            for j in range(0,6):
                nb1 = []
                while (len(nb)>0):
                    nbr = nb.pop()
                    for k in range(0,n):
                        if (k not in set(nbr)):
                            if (neighbors[nbr[len(nbr)-1]][k]<2):
                                nbr2 = copy.deepcopy(nbr)
                                nbr2.append(k)
                                nb1.append(nbr2)
                            elif (neighbors[nbr[0]][k]<1.6):
                                nbr2 = copy.deepcopy(nbr)
                                nbr2.insert(0,k)
                                nb1.append(nbr2)
                nb = copy.deepcopy(nb1)
            for it in nb:
                if (neighbors[it[0]][it[5]]<1.6):
                    neighb.append([atlist[it[0]],atlist[it[1]],atlist[it[2]],atlist[it[3]],atlist[it[4]],atlist[it[5]]] )
        neig = []
        for it in neighb:
            set1 = set(it)
            fl = 1
            for it1 in neig:
                if(set1 == it1):
                    fl = 0
            if(fl == 1):
                neig.append(set1)
                
        for it in range(0,len(neig)):
            neig[it] = list(neig[it])
        return neig
    
    def FromSiestaOutput(self,filename):
        """    Imports coordinates from siesta output file        """
        self.molecules = TSIESTA.AtomsFromOutput(filename)
        return self.molecules
    
    
##################################################################
#########################  The SIESTA class ######################
##################################################################        
    
    
class TSIESTA:
    def __init__(self):
        """Not documented"""

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
        if lat_vect_1 == False:
            lat_vect_1, lat_vect_2, lat_vect_3 = TSIESTA.lattice_parameters_abc_angles(filename)
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
            if (lines[i].find("%block ChemicalSpeciesLabel") >= 0):
                tmp_ar = {}
                for j in range(0, NumberOfSpecies):
                    i += 1
                    tmp_ar[(lines[i].split())[0]] = (lines[i].split())[1:3]

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

        if lat_vect_1 == False:
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
            return False, False, False

    @staticmethod
    def lattice_vectors(filename):
        LatConstant = float(TSIESTA.lattice_constant(filename))
        LatticeVectors = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeVectors')
        if len(LatticeVectors) > 0:
            lat_vect_1 = Helpers.spacedel(LatticeVectors[0]).split()
            lat_vect_2 = Helpers.spacedel(LatticeVectors[1]).split()
            lat_vect_3 = Helpers.spacedel(LatticeVectors[2]).split()
            return LatConstant*lat_vect_1, LatConstant*lat_vect_2, LatConstant*lat_vect_3
        return False, False, False

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
                # print(child.attrib)
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
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
    def DOSsiesta(filename,Ef = 0):
        """DOS"""
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
                DOS.append([round(float(line1[0])-Ef,5),float(line1[1]),float(line1[2])])
                strDOS = DOSFile.readline()
            return DOS    

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
        return Helpers.fromFileProperty(filename, 'siesta: Etot    =', 2, 'float')


    @staticmethod
    def Energies(filename):
        """ Energy from each step """
        return TSIESTA.ListOfValues(filename, "siesta: E_KS(eV) =")

        
    @staticmethod
    def FermiEnergy(filename):
        """ Fermy Energy from SIESTA output file """
        Energy = 0    
        if os.path.exists(filename):
            MdSiestaFile = open(filename)
            str1 = MdSiestaFile.readline()
    
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


        
    @staticmethod    
    def Forces(filename):
        """ Forces """
        forces = []    
        PeriodTable = TPeriodTable()
        if os.path.exists(filename):
            NumberOfAtoms = Helpers.fromFileProperty(filename,'number_of_atoms')
            NumberOfSpecies = Helpers.fromFileProperty(filename,'number_of_species')
            MdSiestaFile = open(filename)        
            
            speciesLabel = [0,0,0,0,0,0,0,0,0,0]
            charges = [0,0,0,0,0,0,0,0,0,0]
            
            sl = []
            isSpesFinde = 0
            isSpesF = 0
            
            str1 = MdSiestaFile.readline()
            
            forces = []
            while str1!='':
                #tmp = ''
                if str1 != '' and (str1.find("siesta: Atomic coordinates (Bohr) and species")>=0) and (isSpesF == 0):
                    str1 = MdSiestaFile.readline()
                    while str1.find('siesta')>=0:
                        str1 = Helpers.spacedel(str1)
                        sl.append(int(str1.split(' ')[4]))
                        str1 = MdSiestaFile.readline()
                    isSpesF = 1
                
                if (str1 != '') and (str1.find("ChemicalSpeciesLabel")>=0):
                    if isSpesFinde == 0:
                        i = 1
                        while i <= NumberOfSpecies: 
                            str1 = Helpers.spacedel(MdSiestaFile.readline())
                            row = str1.split(' ')
                            speciesLabel[int(row[0])] = row[2]    
                            charges[int(row[0])] = row[1]
                            i+=1                            
                            isSpesFinde = 1    
                forc = []
                
                if (str1 != '') and (str1.find("Begin CG move")>=0 or str1.find("Begin MD step")>=0):
                    while (str1 != '') and (str1.find("siesta: Atomic forces (eV/Ang):")==-1):
                        str1 = MdSiestaFile.readline()
                        
                    forc = []
                    i1 = 0
                    while i1 < NumberOfAtoms:
                        str1 = MdSiestaFile.readline()                                        
                        d1 = (str1.split())[1]
                        d2 = (str1.split())[2]
                        d3 = (str1.split())[3]
                    
                        C = speciesLabel[sl[len(forc)]]
                        Charge = charges[sl[len(forc)]]
                        A = [d1,d2,d3,Charge,C]
                        forc.append(A)
                        i1+=1
                    forces.append(forc)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()        
        return forces

    
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
    def Updateatominsiestafdf(filename,model):
        """ заменяет атомы во входном файле SIESTA """
        NumberOfAtoms = Helpers.fromFileProperty(filename,'number_of_atoms')
        lines = []
        f = open(filename)
        lines = f.readlines()    
    
        i = 0
    
        newlines = []
        
        while i < len(lines):    
            if (lines[i].find("%block Zmatrix")>=0):
                newlines.append(lines[i])
                i += 1
                if (lines[i].find("cartesian")>=0):
                    newlines.append(lines[i])
                    i+=1
                    for j in range(0, NumberOfAtoms):
                        row = Helpers.spacedel(lines[i])
                        ind=row.split(' ')[0]
                        dx = row.split(' ')[4]
                        dy = row.split(' ')[5]
                        dz = row.split(' ')[6]
                        newlines.append('   '+str(ind) + '   ' +str(model.AtList[j].x)+ '   ' +str(model.AtList[j].y)+ '   ' +str(model.AtList[j].z)+'   '+str(dx)+'   '+str(dy)+'   '+str(dz)+'\n')
    
                        i += 1    
            newlines.append(lines[i])
            i+=1
        return newlines

    
    
    @staticmethod
    def Updatepropertyinsiestafdf(filename,property, newvalue, units):
        """ изменяет один из параметров во входном файле """
        lines = []
        f = open(filename)
        lines = f.readlines()    
        f.close()
        
        f = open(filename, 'w')        
        for j in range(0,len(lines)):
            field = lines[j]
            if (lines[j].find(property)>=0):
                field = property + "  " + str(newvalue)+"  " + str(units)+"\n"            
            f.write(field)                    
        f.close()
        
    @staticmethod
    def Updateblockinsiestafdf(filename,blockname, newvalue):
        """ изменяет один из блоков во входном файле """
        lines = []
        f = open(filename)
        lines = f.readlines()    
        f.close()
        
        f = open(filename, 'w')    
        flag = 0
        for j in range(0,len(lines)):
            if (lines[j].find(blockname)>=0) and (flag == 1):
                f.write(lines[j])
                flag = 0
            else:
                if (lines[j].find(blockname)>=0) and (flag == 0):
                    f.write(lines[j])
                    flag = 1
                    f.write(str(newvalue)+"\n")    
                else:
                    if (flag == 0):
                        f.write(lines[j])    
        f.close()

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
    def StartSWNTfile(n,m,startfile):
        """ Элементарная ячейка УНТ (n,m) будет записана во входной файл SIESTA startfile """
        model = TSWNT(n,m)
        st = model.AtList
        f1 = open(startfile,"w")
        f1.write("SystemName          nanotube ("+str(n)+","+str(m)+")\n")
        f1.write("SystemLabel         C"+str(len(st))+"\n")
        f1.write("number_of_atoms       "+str(len(st))+"\n")
        f1.write("number_of_species     1\n")
        f1.write("WriteMullikenPop    1\n")
        f1.write("%block ChemicalSpeciesLabel\n")
        f1.write(" 1  6  C\n")
        f1.write("%endblock ChemicalSpeciesLabel \n")
        f1.write("PAO.BasisSize  DZP\n")
        f1.write("PAO.EnergyShift  0.05 eV\n")
        f1.write("MeshCutoff       150.0 Ry\n\n")
        
        f1.write("%block kgrid_Monkhorst_Pack\n")
        f1.write("  1  0  0   0.5\n")
        f1.write("  0  1  0   0.5\n")
        f1.write("  0  0  32  0.5\n")
        f1.write("%endblock kgrid_Monkhorst_Pack\n\n")
        
        f1.write("MaxSCFIterations       150\n")
        f1.write("Diag.ParallelOverK   .false.\n")
        f1.write("SolutionMethod         diagon\n")
        f1.write("NetCharge     0.00\n")
        f1.write("DM.NumberPulay    4\n")
        f1.write("DM.MixingWeight   0.3\n")
        f1.write("DM.UseSaveDM      .true.\n")
        f1.write("NeglNonOverlapInt False\n")
        f1.write("AtomicCoordinatesFormat  NotScaledCartesianAng\n")
        
        f1.write("XC.functional=LDA\n")
        f1.write("XC.authors=CA\n")
        f1.write("ZM.UnitsLength = Ang\n")
        
        f1.write("%block Zmatrix\n")
        f1.write("cartesian\n")
        
        for i in range(0,len(st)):
            f1.write("  1   "+str(st[i][0])+"    "+str(st[i][1])+"    "+str(st[i][2])+"   1   1   1\n")
        f1.write("%endblock Zmatrix\n\n")
        
        tubelen = TSWNT.unitlength(n,m,1.43)
        f1.write("LatticeConstant      "+ str(tubelen) +" Ang\n\n")
        
        f1.write("%block LatticeParameters\n")
        f1.write("  10.0 10.0 1.0 90. 90. 90.  \n")
        f1.write("%endblock LatticeParameters \n")
        f1.write("\n")
        f1.write("WriteCoorXmol     True\n")
        f1.write("WriteForces .true.\n")
        f1.write("WriteMullikenPop     1\n")
        f1.write("%block ProjectedDensityOfStates\n")
        f1.write("   -24.00  15.00  0.100  1000  eV\n")
        f1.write("%endblock ProjectedDensityOfStates \n")
        f1.write("MD.type_of_run           cg               # Type of dynamics: Conjugate gradients\n")
        f1.write("MD.NumCGsteps          320              # number of CG steps\n")
        f1.write("MD.MaxCGDispl          0.15 Ang\n")
        f1.write("MD.MaxForceTol         0.04 eV/Ang\n")
        f1.write("MD.UseSaveXV           yes\n")
        f1.write("MD.VariableCell        .false.\n")
        f1.close()


    @staticmethod
    def type_of_run(filename):
        """ MD or CG? """
        return Helpers.fromFileProperty(filename, 'MD.TypeOfRun', 1, 'string')

    @staticmethod
    def volume(filename):
        """ Returns cell volume from SIESTA output file """
        return Helpers.fromFileProperty(filename, 'siesta: Cell volume = ', 2, 'float')


##################################################################
####################  The VASP properties class  #################
##################################################################        
        
        
class TVASP:    
        
    def __init__(self):
        """Not documented"""        
    
    @staticmethod
    def VaspEnergy(filename):
        """Energy"""
        prop = "energy(sigma->0) ="
        isConv = "false"
        iter = ""
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()            
            while str1!='':        
                if (str1 != '') and (str1.find("General timing and accounting informations for this job:")>=0):
                    isConv = "true"
                if (str1 != '') and (str1.find("-- Iteration")>=0):
                    iter = str1
                if (str1 != '') and (str1.find(prop)>=0):
                    str1 = str1.replace(prop,' ')
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[1]

                    property = float(prop1)
                
                str1 = MyFile.readline()
            MyFile.close()
        return property, isConv, iter    

        
    @staticmethod
    def VaspVolume(filename):
        """Cell volume"""
        prop = "volume of cell :"
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()            
            while str1!='':            
                if (str1 != '') and (str1.find(prop)>=0):
                    str1 = str1.replace(prop,' ')
                    prop1 = re.findall(r"[0-9,\.,-]+", str1)[0]

                    property = float(prop1)
                
                str1 = MyFile.readline()
            MyFile.close()
        return property        
        
    @staticmethod
    def VaspNumberOfAtoms(filename):
        """number_of_atoms"""
        if os.path.exists(filename):
            MyFile = open(filename)
            for i in range(0,7):
                str1 = MyFile.readline()            
            #print str1
            ns = re.findall(r"[0-9,\.,-]+", str1)#[0]
            n = 0
            for i in range(0,len(ns)):
                n = n+int(ns[i])

            MyFile.close()
        return n
        
    @staticmethod
    def VaspLattConst(filename):
        """Lattice Constant"""
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()
            str1 = MyFile.readline()
            print(str1)
            n = float(re.findall(r"[0-9,\.,-]+", str1)[0])
            MyFile.close()
        return n
        
    @staticmethod
    def updateLatticeConstant(newvalue):
        """ изменяет параметр решетки во входном файле POSCAR """
        lines = []
        f = open('POSCAR')
        lines = f.readlines()    
        f.close()
        
        f = open('POSCAR', 'w')        
        for j in range(0,len(lines)):
            field = lines[j]
            if (j==1):
                field = "  " + str(newvalue)+"\n"            
            f.write(field)                    
        f.close()
        
        
        
##################################################################
#################### The Tcalculators class ######################
##################################################################
    
class TCalculators:

    @staticmethod
    def M11S11(DOS):
        """ Returns the distance between first Van-Hove singularities in DOS """
        EnergyLeft = 0
        EnergyRight= 0    
        
        ZeroPos = 0
        
        for i in range(0,len(DOS)):
            if math.fabs(DOS[i][0])<2e-2:
                ZeroPos = i
            
        EnergyRight = ZeroPos
        EnergyLeft = ZeroPos
        while (float(DOS[EnergyRight][1])-float(DOS[EnergyRight+1][1]))<=1e-1:
            EnergyRight+=1
        while (float(DOS[EnergyLeft-1][1])-float(DOS[EnergyLeft][1]))>=-1e-1:
            EnergyLeft-=1
        return DOS[EnergyRight][0] - DOS[EnergyLeft][0]
        


    @staticmethod
    def MomentSil(model,force):
        """ Момент сил """
        momentx= 0
        momenty= 0
        for j in range(0, len(model)):
            cm = TAtomicModel.CentrMass(model)
            atom = model[j]
            atom[0] -= cm[0]
            atom[1] -= cm[1]
            fi= math.atan(atom[1]/atom[0])
            r = math.sqrt(math.pow(atom[0],2) + math.pow(atom[1],2))
            momentx += r*float(force[j][0])*math.cos(fi)
            momenty += r*float(force[j][1])*math.sin(fi)
        return math.sqrt(math.pow(momentx,2) + math.pow(momenty,2))
        
            
    @staticmethod
    def ACFs(molecules):
        """The Velocity Autocorrelation Function (space)"""
        theACF = []
        StatFrom = 200
        StatFinish = len(molecules)
        S = len(molecules[1].AtList)
        
        Vsr = []
        Vsr0 = []
        ACF = []
        for ij in range(0,20):
            Vsr.append(0)    
            Vsr0.append(0) 
            ACF.append(0) 
        
        Title = []
        Title.append("N")
        
        for ij in range(0,S):
            fl = 1
            for j in range(0,ij):
                if(molecules[1].AtList[ij][3]==molecules[1].AtList[j][3]):
                    fl=0
            if(fl):
                Title.append(molecules[1].AtList[ij][4])
        
        D = []
        D0 = []
        
        for ij in range(0,S):
            D.append([0,0,0,0])
            D0.append([0,0,0,0])
            
        iter = 0
        row = []
            
        for l in range(StatFrom,StatFinish-1):
            row = []
            row.append(l)
    
            for j in range(0,S):
                D0[j][0]=molecules[StatFrom+1].AtList[j][0]-molecules[StatFrom].AtList[j][0]
                D0[j][1]=molecules[StatFrom+1].AtList[j][1]-molecules[StatFrom].AtList[j][1]
                D0[j][2]=molecules[StatFrom+1].AtList[j][2]-molecules[StatFrom].AtList[j][2]
                
                D[j][0]=molecules[l+1].AtList[j][0]-molecules[l].AtList[j][0]
                D[j][1]=molecules[l+1].AtList[j][1]-molecules[l].AtList[j][1]
                D[j][2]=molecules[l+1].AtList[j][2]-molecules[l].AtList[j][2]
            
            iter=0
            
            for ijk in range(0,S):
                fl = 1
                for j in range(0,ijk):
                    if(molecules[1].AtList[ijk][3]==molecules[1].AtList[j][3]):
                        fl=0
                if(fl):
                    iter+=1
                    Vsr[iter] = 0
                    Vsr0[iter] = 0
                    for j in range(ijk,S):
                        if(molecules[1].AtList[j][3]==molecules[1].AtList[ijk][3]):
                            Vsr0[iter]+=D0[j][0]*D0[j][0]+D0[j][1]*D0[j][1]+D0[j][2]*D0[j][2]
                            Vsr[iter] +=D[j][0] *D0[j][0]+ D[j][1]*D0[j][1]+ D[j][2]*D0[j][2]
                    ACF[iter] = Vsr[iter]/Vsr0[iter]
            
            for j in range(1,iter+1): 
                row.append(ACF[j])
            
            theACF.append(row)
        return theACF, Title
    
    
    @staticmethod            
    def ACFt(molecules):
        """The Velocity Autocorrelation Function (time)"""
        theACF = []
        
        StatFrom = 200
        StatFinish = (len(molecules) - StatFrom)/2
        S = len(molecules[0].AtList)
            
        Vsr = []
        Vsr0 = []
        ACF = []
        for ij in range(0,20):
            Vsr.append(0)    
            Vsr0.append(0) 
            ACF.append(0) 
        
        Title = []
        Title.append("N")
        
        for ij in range(0,S):
            fl = 1
            for j in range(0,ij):
                if(molecules[1].AtList[ij][3]==molecules[1].AtList[j][3]):
                    fl=0
            if(fl):
                Title.append(molecules[1].AtList[ij][4])
        
        D = []
        D0 = []
        
        for ij in range(0,S):
            D.append([0,0,0,0])
            D0.append([0,0,0,0])
                
        iter = 0
        row = []
                        
        for r in range(StatFrom,StatFinish-StatFrom-1):
            row.append(r-StatFrom)
            iter=0
            for ijk in range(0,S):
                fl = 1
                for j in range(0,ijk):
                    if(molecules[1].AtList[ijk][3]==molecules[1].AtList[j][3]):
                        fl=0
                if(fl):
                    iter+=1
                    Vsr[iter] = 0
                    Vsr0[iter] = 0
                    for j in range(ijk,S):
                        if(molecules[1].AtList[j][3]==molecules[1].AtList[ijk][3]):
                            for l in range(0,StatFinish-StatFrom-1):
                                for k in range(0,2):
                                    D0[j][k]= molecules[StatFrom+l+1].AtList[j][k]  - molecules[StatFrom+l].AtList[j][k]
                                    D[j][k] = molecules[StatFrom+l+r+1].AtList[j][k]- molecules[StatFrom+l+r].AtList[j][k]
                            Vsr0[iter]+=D0[j][0]*D0[j][0]+D0[j][1]*D0[j][1]+D0[j][2]*D0[j][2]
                            Vsr[iter] +=D[j][0] *D0[j][0]+ D[j][1]*D0[j][1]+ D[j][2]*D0[j][2]
                    ACF[iter] = Vsr[iter]/Vsr0[iter]
            
            for j in range(1,iter+1):
                row.append(ACF[j])
            
            theACF.append(row)
            row = []
        return theACF, Title

    @staticmethod        
    def DfromACF(list2D):
        """Not documented"""
        D = []
        firstDim = len(list2D)
        secondDim = len(list2D[0])
        
        for item in list2D:
            if (len(item)<secondDim):
                secondDim = len(item)
        
        print('list ' + firstDim + 'x' + secondDim)
        
        D = []
        
        for firstDimt in range (2, firstDim):
            D = []
            
            for i in range(0, secondDim):
                D.append(0)
            
            for i in range(1,firstDimt-1):
                for j in range(1, secondDim):
                    D[j] += list2D[i][j]
            
            for j in range(1,secondDim):
                D[j] += (list2D[0][j] + list2D[firstDimt][j])/2
            
            print(firstDimt + '  ' + D[1] + '  ' + D[2])
        return D
    
        
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
                    print("Iter " + str(i) + "/" + str(nPrompts) + "| we found "+str(len(Models))+"structures")
                if len(Models)==0:
                    Models.append(Molecula)
        return Models


    @staticmethod
    def fParabola(x, b0, b1, b2):
        return b0 + b1 * x + b2 * x**2
    
    @staticmethod
    def ApproxParabola(DATA):
        #beta = (0.25, 0.75, 0.5)
        xdata, ydata = Helpers.ListN2Split(DATA)
        #xdata = np.linspace(0, 5, 50)
        #y = TCalculators.fMurnagham(xdata, *beta)
        #ydata = y + 0.05 * np.random.randn(len(xdata))
        beta_opt, beta_cov = curve_fit(TCalculators.fParabola, xdata, ydata)
        print(beta_opt)

        xmin = xdata.min()
        xmax = xdata.max()

        x = np.linspace(xmin, xmax, 200)
        y = TCalculators.fParabola(x, *beta_opt)

        return beta_opt, x.tolist(), y.tolist()


    #now we have to create the equation of state function
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

    # and we define an objective function that will be minimized
    def objectiveMurnaghan(pars, y, x):
        #we will minimize this function
        err = y - TCalculators.fMurnaghan(pars,x)
        return err

    def objectiveBirchMurnaghan(pars, y, x):
        #we will minimize this function
        err = y - TCalculators.fBirchMurnaghan(pars,x)
        return err

    @staticmethod
    def ApproxMurnaghan(DATA):
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


    def from_structure(self):
        r=7

    def get_all_data(self, atoms):
        structure = TAtomicModel(atoms)
        st = structure.toSIESTAfdf()

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

