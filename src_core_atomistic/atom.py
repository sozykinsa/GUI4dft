# -*- coding: utf-8 -*-

from src_core_atomistic import helpers
import numpy as np


class Atom(object):
    """The atom class."""

    def __init__(self, at_data):
        """Constructor"""
        self.xyz = np.array([at_data[0], at_data[1], at_data[2]])
        self.let = at_data[3]
        self.charge = int(at_data[4])
        self.is_visible: bool = True
        self.selected: bool = False
        self.active: bool = False
        self.fragment1: bool = False
        self.properties = {}
        self.visible_property = ""
        self.tag = ""

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

    @property
    def xyz_string(self) -> str:
        return "{0:12.6f}    {1:12.6f}    {2:12.6f}".format(self.xyz[0], self.xyz[1], self.xyz[2])

    def set_selected(self, fl):
        self.selected = fl

    def is_selected(self):
        return self.selected

    def set_property(self, prop, val):
        self.properties[prop] = val

    def get_property(self, prop):
        return self.properties.get(prop)

    def to_string(self):
        let = self.let
        sx = helpers.float_to_string(self.x)
        sy = helpers.float_to_string(self.y)
        sz = helpers.float_to_string(self.z)
        return let + '  ' + sx + '  ' + sy + '  ' + sz
