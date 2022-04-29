# -*- coding: utf-8 -*-

from utils import helpers


class Atom(object):
    """The atom class."""

    def __init__(self, at_data):
        """Constructor"""
        self.x = at_data[0]
        self.y = at_data[1]
        self.z = at_data[2]
        self.let = at_data[3]
        self.charge = int(at_data[4])
        self.selected = False
        self.fragment1 = False
        self.properties = {}

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
