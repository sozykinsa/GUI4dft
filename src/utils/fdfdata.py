# -*- coding: utf-8 -*-

import os
from copy import deepcopy

from utils import helpers


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
        file_name = open(filename)
        str1 = file_name.readline()
        while str1.find("Dump of input data file") == -1:
            str1 = file_name.readline()
        str1 = file_name.readline()
        fdf = []
        while str1.find("End of input data file") == -1:
            if str1 != "":
                fdf.append(str1)
            str1 = file_name.readline()
        file_name.close()
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

    def get_all_data(self, _structure, coord_type, units_type, latt_type):
        structure = deepcopy(_structure)

        st = structure.toSIESTAfdfdata(coord_type, units_type, latt_type)

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
            if block.name.lower().find("zmatrix") >= 0: f = False
            if block.name.lower().find("chemicalspecieslabel") >= 0: f = False
            if block.name.lower().find("latticeparameters") >=0: f = False
            if block.name.lower().find("latticevectors") >=0: f = False
            if block.name.lower().find("atomiccoordinatesandatomicspecies") >= 0: f = False

            if f:
                st += "%block "+block.name+"\n"
                for row in block.value:
                    st += row
                st += "%endblock "+block.name+"\n"
        return st

    @staticmethod
    def updateAtominSIESTAfdf(filename, model):
        """ заменяет атомы во входном файле SIESTA """
        NumberOfAtoms = helpers.fromFileProperty(filename, 'NumberOfAtoms')
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
                        row = helpers.spacedel(lines[i])
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
