# -*- coding: utf-8 -*-
import math
import os
import re
from operator import itemgetter

import numpy as np


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
    def float_to_string(fl):
        res = '{0:12.8f}'.format(fl)
        if res == "-0.00000000":
            res = " 0.00000000"
        return res

    @staticmethod
    def is_number(row):
        try:
            float(row)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

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
        nextLat = 0
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

            a, b, c = np.polyfit(x, y, 2)
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
    def fromFileProperty(filename, prop, count=1, type='int'):
        """
        Возвращает  значение параметра property из файла filename.
        Значене может быть целым или дробным числом с фиксированной точкой.
        Если в файле необходимый параметр встречается несколько раз, необходимо задать параметр count,
        который показывает какое по счету найденное значение должна вернуть функция.
        Параметр type указывает тип возвращаемого значения (int, float или string)
        """
        k = 1
        is_found, k, property = Helpers.property_from_sub_file(filename, k, prop, count, type)
        if is_found:
            return property
        else:
            return None

    @staticmethod
    def property_from_sub_file(filename, k, prop, count, typen):
        property = None
        is_found = False
        k = 1
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()
            while str1 != '':
                if (str1 != '') and (str1.find("%include") >= 0):
                    new_f = str1.split()[1]
                    file = os.path.dirname(filename) + "/" + new_f
                    is_found, k, property = Helpers.property_from_sub_file(file, k, prop, count, typen)
                if (str1 != '') and (str1.find(prop) >= 0):
                    str1 = str1.replace(prop, ' ')
                    if typen == "unformatted":
                        property = str1
                    if typen == 'string':
                        property = Helpers.spacedel(str1)
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

    @staticmethod
    def RoundToPlane(atom, R):
        """ RoundToPlane  """

        z = atom.z
        fi = math.asin(atom.x/R)
        if atom.y <= -1e-3:
            fi = 3.14 - fi
        x = -R*fi
        return [x, z]

    @staticmethod
    def dos_from_file(filename, n, nlines = 0):
        DOSFile = open(filename)
        strDOS = DOSFile.readline()
        energy = []
        spinUp = []
        spinDown = []

        if nlines > 0:
            MyFile = open(filename)
            for i in range(0, 6):
                strDOS = DOSFile.readline()

            for i in range(0, nlines):
                strDOS = Helpers.read_row_of_dos_file(DOSFile, energy, n, spinDown, spinUp, strDOS)

        if nlines == 0:
            while strDOS != '':
                strDOS = Helpers.read_row_of_dos_file(DOSFile, energy, n, spinDown, spinUp, strDOS)
        return energy, spinDown, spinUp

    @staticmethod
    def read_row_of_dos_file(DOSFile, energy, n, spinDown, spinUp, strDOS):
        line = strDOS.split(' ')
        line1 = []
        for i in range(0, len(line)):
            if line[i] != '':
                line1.append(line[i])
        energy.append(float(line1[0]))
        spinUp.append(float(line1[1]))
        if len(line1) > n:
            spinDown.append(float(line1[2]))
        else:
            spinDown.append(0)
        strDOS = DOSFile.readline()
        return strDOS