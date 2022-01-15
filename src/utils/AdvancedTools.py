# -*- coding: utf-8 -*-

import math
import os
import random
from copy import deepcopy

import numpy as np
from numpy import polyfit
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi

from utils.helpers import Helpers
from utils.atomic_model import TAtom, TAtomicModel


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
                if len(Models) == 0:
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
        return E0 + 9*V0*B0/16*(((alpha-1)**3)*BP + (alpha-1)**2*(6-4*alpha))

    def objectiveMurnaghan(pars, y, x):
        err = y - TCalculators.fMurnaghan(pars, x)
        return err

    def objectiveBirchMurnaghan(pars, y, x):
        err = y - TCalculators.fBirchMurnaghan(pars, x)
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

        x0 = np.array([e0, b0, bP, v0])
        murnpars, ier = leastsq(TCalculators.objectiveBirchMurnaghan, x0, args=(e, v))
        return murnpars, vfit.tolist(), TCalculators.fMurnaghan(murnpars, vfit).tolist()

    @staticmethod
    def VoronoiAnalisis(Molecula, selectedAtom, maxDist):
        newMolecula = Molecula.grow()
        newMolecula.move_atoms_to_cell()
        atoms_to_analise = newMolecula.indexes_of_atoms_in_ball(range(0, len(newMolecula.atoms)), selectedAtom, maxDist)
        points = np.empty((len(atoms_to_analise), 3))
        k = 0
        for i in atoms_to_analise:
            points[k][0] = newMolecula[i].x
            points[k][1] = newMolecula[i].y
            points[k][2] = newMolecula[i].z
            k += 1

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
            if (len(list(set(ridge) - set(regions[0]))) == 0) and (len(ridge) > 0):
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

    def add_block(self, block):
        self.blocks.append(block)

    def add_property(self, row):
        self.properties.append(row)

    def fdf_parser(self, data):
        i = 0
        while i < len(data):
            if not data[i].lstrip().startswith('#'):
                if data[i].find("%block") >= 0:
                    newBlock = Block(data[i].split()[1])
                    i += 1
                    while data[i].find("%endblock") == -1:
                        newBlock.add_row(data[i])
                        i += 1
                    self.add_block(newBlock)
                    i += 1
                else:
                    if data[i] != "" and data[i] != "\n":
                        self.add_property(data[i])
                    i += 1
            else:
                i += 1

    def from_fdf_file(self, filename):
        if os.path.exists(filename):
            f = open(filename)
            lines = f.readlines()
            f.close()
            self.fdf_parser(lines)
            return self

    def from_out_file(self, filename):
        if os.path.exists(filename):
            fdf = TFDFFile.fdf_data_dump(filename)
            self.fdf_parser(fdf)
            return self

    @staticmethod
    def fdf_data_dump(filename):
        MyFile = open(filename)
        str1 = MyFile.readline()
        while str1.find("Dump of input data file") == -1:
            str1 = MyFile.readline()
        str1 = MyFile.readline()
        fdf = []
        while str1.find("End of input data file") == -1:
            if str1 != "":
                fdf.append(str1)
            str1 = MyFile.readline()
        MyFile.close()
        return fdf

    def get_property(self, prop):
        val = ""
        prop = prop.lower()
        for pr in self.properties:
            pos = pr.lower().find(prop)
            if pos >= 0:
                val = ""
                for i in range(pos + len(prop), len(pr)):
                    val += pr[i]
                val = val.replace('=', ' ')
                val = val.strip()
                return val
        print("property '" + prop + "' not found\n")
        return val

    def get_block(self, prop):
        val = ""
        prop = prop.lower()
        for pr in self.blocks:
            pos = pr.name.lower().find(prop)
            if pos >= 0:
                val = pr.value
                return val
        print("block '" + prop + "' not found\n")
        return val

    def get_all_data(self, _structure, coordType, lattType):
        structure = deepcopy(_structure)

        st = structure.toSIESTAfdfdata(coordType, lattType)

        for prop in self.properties:
            f = True
            if prop.lower().find("numberofatoms") >= 0: f = False
            if prop.lower().find("numberofspecies") >= 0: f = False
            if prop.lower().find("atomiccoordinatesformat") >= 0: f = False
            if prop.lower().find("latticeconstant") >= 0: f = False
            if f:
                st += prop

        for block in self.blocks:
            f = True
            if (block.name).lower().find("zmatrix") >= 0: f = False
            if (block.name).lower().find("chemicalspecieslabel") >= 0: f = False
            if (block.name).lower().find("latticeparameters") >=0: f = False
            if (block.name).lower().find("latticevectors") >=0: f = False
            if (block.name).lower().find("atomiccoordinatesandatomicspecies") >= 0: f = False

            if f:
                st += "%block "+block.name+"\n"
                for row in block.value:
                    st += row
                st += "%endblock "+block.name+"\n"
        return st

    @staticmethod
    def updateAtominSIESTAfdf(filename, model):
        """ заменяет атомы во входном файле SIESTA """
        NumberOfAtoms = Helpers.fromFileProperty(filename, 'NumberOfAtoms')
        f = open(filename)
        lines = f.readlines()
        i = 0
        newlines = []

        while i < len(lines):
            if lines[i].find("%block Zmatrix") >= 0:
                newlines.append(lines[i])
                i += 1
                if lines[i].find("cartesian") >= 0:
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
        f = open(filename)
        lines = f.readlines()
        f.close()

        f = open(filename, 'w')
        for j in range(0, len(lines)):
            field = lines[j]
            if lines[j].find(property) >= 0:
                field = property + "  " + str(newvalue) + "  " + str(units) + "\n"
            f.write(field)
        f.close()

    @staticmethod
    def updateBlockinSIESTAfdf(filename, blockname, newvalue):
        """ изменяет один из блоков во входном файле """
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
                    if flag == 0:
                        f.write(lines[j])
        f.close()
