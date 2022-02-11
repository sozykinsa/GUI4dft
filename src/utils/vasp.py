# -*- coding: utf-8 -*-
# Python 3
import copy
import math
import os
import random
import re
from copy import deepcopy

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm
from numpy import polyfit
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi

from utils import helpers
from utils.periodic_table import TPeriodTable
from utils.atomic_model import TAtom, TAtomicModel
from utils.siesta import TSIESTA


##################################################################
####################  The VASP properties class  #################
##################################################################


class TVASP:

    def __init__(self):
        """Not documented"""

    @staticmethod
    def fermi_energy_from_doscar(filename):
        if os.path.exists(filename):
            MyFile = open(filename)
            str1 = MyFile.readline()
            for i in range(0,5):
                str1 = MyFile.readline()
            MyFile.close()
            eFermy = float(str1.split()[3])
            return eFermy

    @staticmethod
    def DOS(filename):
        """DOS"""
        MyFile = open(filename)
        str1 = MyFile.readline()
        for i in range(0, 5):
            str1 = MyFile.readline()
        MyFile.close()
        nlines = int(str1.split()[2])
        if os.path.exists(filename):
            energy, spinDown, spinUp = helpers.dos_from_file(filename, 3, nlines)
            return np.array(spinUp), np.array(spinDown), np.array(energy)
