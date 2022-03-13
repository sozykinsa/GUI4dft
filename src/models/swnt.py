# -*- coding: utf-8 -*-

import math

from utils import helpers
from models.atom import Atom
from models.graphene import Graphene


class SWNT(Graphene):
    """The TSWNT class provides """
    def __init__(self, n, m, length=0, n_cell=1):
        if length == 0:
            length = n_cell * SWNT.unit_length(n, m, 1.43)

        super().__init__()

        rad = self.radius(n, m)
        self.set_lat_vectors([10 * rad, 0, 0], [0, 10 * rad, 0], [0, 0, length])
        np1, pi, px, py, length = self.graphene_positions(n, m, length)

        """ output """
        r = length / (2 * math.pi)
        
        for i_par in range(0, np1):
            phi_par = px[i_par] / r
            qx = r * math.sin(phi_par)
            qy = -r * math.cos(phi_par)
            qz = py[i_par]
            self.add_atom(Atom([qx, qy, qz, "C", 6]))

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
