# -*- coding: utf-8 -*-

from utils import helpers


class Atom(object):
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

    def to_string(self):
        let = self.let
        sx = helpers.float_to_string(self.x)
        sy = helpers.float_to_string(self.y)
        sz = helpers.float_to_string(self.z)
        return let + '  ' + sx + '  ' + sy + '  ' + sz
