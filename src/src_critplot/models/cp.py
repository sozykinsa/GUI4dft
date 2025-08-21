# -*- coding: utf-8 -*-

from core_atomistic.atom import Atom
from core_atomistic.helpers import list_str_to_float, spacedel
import numpy as np


class CriticalPoint(Atom):
    """The atom class with bond paths."""

    def __init__(self, at_data):
        """Constructor"""
        self.xyz = at_data[0]
        self.let = at_data[1]
        self.cp_type: str = at_data[2]
        self.charge = 0
        self.is_visible: bool = True
        self.selected: bool = False
        self.active: bool = False
        self.fragment1: bool = False
        self.properties = {}
        self.visible_property = ""
        self.tag = ""
        self.bonds = {}

    def properties_to_string(self):
        text = " properties: "
        text += str(len(self.properties))
        text += self.dictionary_to_str(self.properties)
        return text

    @staticmethod
    def dictionary_to_str(my_dict):
        text = ""
        for key, value in my_dict.items():
            if str(key) != "text":
                text += " property: " + str(key) + " value: " + str(value)
        return text

    def properties_from_string(self, props):
        items = props.split("property:")
        items.pop(0)
        for item in items:
            data = item.split("value:")
            data[0] = data[0].strip()
            if data[0] == 'cp_bp_len':
                self.properties[data[0]] = float(spacedel(data[1]))
            elif (data[0] == 'atom1') or (data[0] == 'atom2'):
                self.properties[data[0]] = int(spacedel(data[1]))
            elif (data[0] == 'atom1_translation') or (data[0] == 'atom2_translation'):
                data[1] = data[1][2:-2]
                data[1] = data[1].split()
                self.properties[data[0]] = np.array(list_str_to_float(data[1]))
            else:
                self.properties[data[0]] = spacedel(data[1])
