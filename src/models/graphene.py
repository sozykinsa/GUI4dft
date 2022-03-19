# -*- coding: utf-8 -*-

import math

import numpy as np

from models.atom import Atom
from models.atomic_model import TAtomicModel


class Graphene(TAtomicModel):
    """The TGraphene class provides """
    def __init__(self, n=0, m=0, leng=0):
        TAtomicModel.__init__(self)
        self.maxMol = 200000
        self.a = 1.43

        if (n == 0) and (m == 0):
            return

        np1, pi, px, py, leng = self.graphene_positions(n, m, leng)

        for i_par in range(0, np1):
            self.add_atom(Atom([px[i_par], py[i_par], 0, "C", 6]))

    def graphene_positions(self, n, m, leng):
        pi = math.pi
        px = np.zeros(self.maxMol)
        py = np.zeros(self.maxMol)
        pz = np.zeros(self.maxMol)
        hx = np.zeros(6)
        hy = np.zeros(6)
        hz = np.zeros(6)
        nx = 40
        ny = 100
        """ calculations """
        """ definition of a hexagon """
        hx[0] = self.a
        hy[0] = 0.0
        hz[0] = 0.0
        for i in range(1, 6):
            hx[i] = hx[i - 1] * math.cos(pi / 3) - hy[i - 1] * math.sin(pi / 3)
            hy[i] = hx[i - 1] * math.sin(pi / 3) + hy[i - 1] * math.cos(pi / 3)
            hz[i] = 0.0
        for k_par in range(0, nx):
            hx_plus = 3 * self.a * k_par
            for ih_par in range(0, 4):
                i_par = ih_par + k_par * 4
                px[i_par] = hx[ih_par] + hx_plus
                py[i_par] = hy[ih_par]
                pz[i_par] = hz[ih_par]
        np1 = (nx - 1) * (nx - 1) + 4
        px_minus = (nx - 1.0) / 2.0 * 3 * self.a
        for i_par in range(0, np1):
            px[i_par] -= px_minus
        for k_par in range(0, ny):
            py_plus = math.sqrt(3.0) * self.a * k_par
            for i_par in range(0, np1):
                j1 = i_par + k_par * np1
                px[j1] = px[i_par]
                py[j1] = py[i_par] + py_plus
                pz[j1] = pz[i_par]
        np1 = np1 - 1 + (ny - 1) * np1

        """ centering y """
        py_minus = (ny - 0.5) / 2.0 * math.sqrt(3.0) * self.a
        for i_par in range(0, np1):
            py[i_par] -= py_minus
        """ Rotate for (m,ch_m) vector """
        vx = (n + m) * 3.0 / 2.0 * self.a
        vy = (n - m) * math.sqrt(3.0) / 2.0 * self.a
        vlen = math.sqrt(vx * vx + vy * vy)
        """ Rotation  """
        for i_par in range(0, np1):
            tempx_par = px[i_par]
            tempy_par = py[i_par]
            px[i_par] = tempx_par * vx / vlen + tempy_par * vy / vlen
            py[i_par] = -tempx_par * vy / vlen + tempy_par * vx / vlen
        """ Rotation is done """
        """ trimming """
        j = 0
        for i in range(0, np1):
            if (px[i] <= vlen / 2.0 * 1.00001) and (px[i] > -vlen / 2.0 * 0.99999) and (py[i] <= leng / 2.0) and (
                    py[i] > -leng / 2.0):
                px[j] = px[i]
                py[j] = py[i]
                pz[j] = pz[i]
                j += 1
        np1 = j
        return np1, pi, px, py, vlen
