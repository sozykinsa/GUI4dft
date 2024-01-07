# -*- coding: utf-8 -*-

import math
import numpy as np

from core_atomistic import helpers
from models.graphene import Graphene


class SWNT(Graphene):
    """The TSWNT class provides """
    def __init__(self, n, m, length=0, n_cell=1):
        if length == 0:
            length = n_cell * SWNT.unit_length(n, m, 1.43)

        super().__init__(n, m, length)

        rad = self.radius(n, m)
        self.set_lat_vectors([10 * rad, 0, 0], [0, 10 * rad, 0], [0, 0, length])

        """ output """
        vx = (n + m) * 3.0 / 2.0 * self.a
        vy = (n - m) * math.sqrt(3.0) / 2.0 * self.a
        vlen = math.sqrt(vx * vx + vy * vy)
        r = vlen / (2 * math.pi)

        for i_par in range(0, self.n_atoms()):
            phi_par = self.atoms[i_par].x / r
            qx = r * math.sin(phi_par)
            qy = -r * math.cos(phi_par)
            qz = self.atoms[i_par].y
            self.atoms[i_par].xyz = np.array([qx, qy, qz])

    @staticmethod
    def radius(n, m):
        return math.sqrt(n * n + n * m + m * m)

    @staticmethod
    def unit_length(n, m, acc):
        a = math.sqrt(3) * acc
        ch = a * math.sqrt(n * n + n * m + m * m)
        d = helpers.cdev(n, m)
        if (n - m) % (3 * d) != 0:
            d_r = d
        else:
            d_r = 3 * d
        t = math.sqrt(3) * ch / d_r
        return t
