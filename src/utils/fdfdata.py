# -*- coding: utf-8 -*-

import os
from copy import deepcopy


##################################################################
# TFDFfile
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

    def fdf_parser(self, data, filename):
        i = 0
        while i < len(data):
            if not data[i].lstrip().startswith('#'):
                if data[i].find("%include") >= 0:
                    new_f = data[i].split()[1]
                    dirname = os.path.dirname(filename)
                    print(dirname + "/" + new_f)
                    self.from_fdf_file(dirname + "/" + new_f)
                    i += 1
                elif data[i].find("%block") >= 0:
                    new_block = Block(data[i].split()[1])
                    i += 1
                    while data[i].find("%endblock") == -1:
                        new_block.add_row(data[i])
                        i += 1
                    self.add_block(new_block)
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
            self.fdf_parser(lines, filename)
            return self

    def from_out_file(self, filename):
        if os.path.exists(filename):
            fdf = TFDFFile.fdf_data_dump(filename)
            self.fdf_parser(fdf, filename)
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
            if prop.lower().find("numberofatoms") >= 0:
                f = False
            if prop.lower().find("numberofspecies") >= 0:
                f = False
            if prop.lower().find("atomiccoordinatesformat") >= 0:
                f = False
            if prop.lower().find("latticeconstant") >= 0:
                f = False
            if f:
                st += prop

        for block in self.blocks:
            f = True
            if block.name.lower().find("zmatrix") >= 0:
                f = False
            if block.name.lower().find("chemicalspecieslabel") >= 0:
                f = False
            if block.name.lower().find("latticeparameters") >= 0:
                f = False
            if block.name.lower().find("latticevectors") >= 0:
                f = False
            if block.name.lower().find("atomiccoordinatesandatomicspecies") >= 0:
                f = False

            if f:
                st += "%block "+block.name+"\n"
                for row in block.value:
                    st += row
                st += "%endblock "+block.name+"\n"
        return st
