# -*- coding: utf-8 -*-

import math

from models.atom import Atom
from models.atomic_model import TAtomicModel


class BiNT(TAtomicModel):

    def __init__(self, n, m, leng=1, tubetype="BN"):
        super().__init__()
        #TAtomicModel.__init__(self)
        a = 1.43
        atom1 = ["C", 6]
        atom2 = ["C", 6]

        if tubetype == "BN":
            a = 1.434
            atom1 = ["B", 5]
            atom2 = ["N", 7]

        if tubetype == "BC":
            a = 1.4
            atom1 = ["B", 5]
            atom2 = ["C", 6]

        z = 0

        df = 180 / n
        dfi = 0
        row = 0

        if (n > 0) and (m == 0):
            rad = math.sqrt(3) / (2 * math.pi) * a * n

            while z <= leng:
                if (row % 2) == 0:
                    dfi += df
                if row % 2:
                    let = atom1[0]
                    charge = atom1[1]
                else:
                    let = atom2[0]
                    charge = atom2[1]

                for i in range(0, n):
                    x = rad * math.cos(math.radians(i * 360 / n + dfi))
                    y = rad * math.sin(math.radians(i * 360 / n + dfi))
                    self.add_atom(Atom([x, y, z, let, charge]))

                row += 1
                if row % 2:
                    z += a
                else:
                    z += a / 2

        if (n == m) and (n > 0):
            rad = 3 * n * a / (2 * math.pi)
            while z <= leng:

                dfi += df
                for i in range(0, n):
                    x = rad * math.cos(math.radians(i * 360 / n + dfi))
                    y = rad * math.sin(math.radians(i * 360 / n + dfi))
                    self.add_atom(Atom([x, y, z, atom1[0], atom1[1]]))

                    x = rad * math.cos(math.radians(i * 360 / n + 120 / n + dfi))
                    y = rad * math.sin(math.radians(i * 360 / n + 120 / n + dfi))
                    self.add_atom(Atom([x, y, z, atom2[0], atom2[1]]))
                row += 1
                z += math.sqrt(3) / 2 * a


