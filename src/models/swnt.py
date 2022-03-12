# -*- coding: utf-8 -*-

import math

from utils import helpers
from models.atom import Atom
from models.graphene import Graphene


class SWNT(Graphene):
    """The TSWNT class provides """
    def __init__(self, n, m, leng=0, ncell=1):
        if leng == 0:
            leng = ncell * SWNT.unitlength(n, m, 1.43)

        #Graphene.__init__(self)
        super().__init__()

        rad = self.radius(n, m)
        self.set_lat_vectors([10 * rad, 0, 0], [0, 10 * rad, 0], [0, 0, leng])
        np1, pi, px, py, leng = self.graphene_positions(n, m, leng)

        """ output """
        R = leng / (2 * math.pi)
        
        for i_par in range(0, np1):
            phi_par = px[i_par] / R
            qx = R * math.sin(phi_par)
            qy = -R * math.cos(phi_par)
            qz = py[i_par]
            self.add_atom(Atom([qx, qy, qz, "C", 6]))

    @staticmethod
    def radius(n, m):
        return math.sqrt(n * n + n * m + m * m)

    @staticmethod
    def unitlength(n, m, acc): 
        a = math.sqrt(3) * acc
        #pi = math.pi
        
        #b1x = 2 * pi / a / math.sqrt(3)
        #b1y = 2 * pi / a
        #b2x = 2 * pi / a / math.sqrt(3)
        #b2y = -2 * pi / a
        Ch = a * math.sqrt(n * n + n * m + m * m)
        #dia = Ch / pi
        #theta = math.atan((math.sqrt(3) * m / (2.0 * n + m)))
        #theta = theta * 180.0 / pi
        d = helpers.cdev(n, m)
        if (n - m) % (3 * d) != 0:
            dR = d
        else:
            dR = 3 * d
        #T1 = (2 * m + n) / dR
        #T2 = -(2 * n + m) / dR
        T = math.sqrt(3) * Ch / dR
        return T

