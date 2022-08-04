# -*- coding: utf-8 -*-

from utils import helpers
import numpy as np


class Atom(object):
    """The atom class."""

    def __init__(self, at_data):
        """Constructor"""
        self.xyz = np.array([at_data[0], at_data[1], at_data[2]])
        self.let = at_data[3]
        self.charge = int(at_data[4])
        self.selected = False
        self.fragment1 = False
        self.properties = {}

    @property
    def x(self) -> float:
        return self.xyz[0]

    @x.setter
    def x(self, value):
        self.xyz[0] = value

    @property
    def y(self) -> float:
        return self.xyz[1]

    @y.setter
    def y(self, value):
        self.xyz[1] = value

    @property
    def z(self) -> float:
        return self.xyz[2]

    @z.setter
    def z(self, value):
        self.xyz[2] = value

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
