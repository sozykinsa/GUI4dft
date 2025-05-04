# -*- coding: utf-8 -*-

import math
import numpy as np
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel


class HexagonalPlaneHex(AtomicModel):
    """The HexagonalPlane with hexagonal cell """
    def __init__(self, ch1: int = 6, ch2: int = 6, a: float = 1.43, n=0, m=0, lattice: int = 3):
        super().__init__()
        lets = [self.mendeley.get_let(ch1), self.mendeley.get_let(ch2)]
        chs = [ch1, ch2]
        a1 = 0.5 * a * np.array([math.sqrt(3), 3, 0])
        a2 = 0.5 * a * np.array([-math.sqrt(3), 3, 0])
        atom1 = Atom([0.0, 0.0, 0.0, lets[0], chs[0]])
        atom2 = Atom([0.0, a, 0.0, lets[1], chs[1]])

        if lattice == 2:
            a1 = 0.5 * a * np.array([3, math.sqrt(3), 0])
            a2 = 0.5 * a * np.array([3, -math.sqrt(3), 0])
            atom1 = Atom([0.0, 0.0, 0.0, lets[0], chs[0]])
            atom2 = Atom([a, 0.0, 0.0, lets[1], chs[1]])

        if lattice == 3:
            a1 = a * np.array([math.sqrt(3), 0.0, 0.0])
            a2 = a * np.array([-0.5 * math.sqrt(3), 1.5, 0])
            atom1 = Atom([0.0, 0.0, 0.0, lets[0], chs[0]])
            atom2 = Atom([0.0, a, 0.0, lets[1], chs[1]])

        a3 = 500 * np.array([0.0, 0.0, 1.0])
        basis = AtomicModel()
        basis.set_lat_vectors([a1, a2, a3])
        basis.add_atom(atom1)
        basis.add_atom(atom2)
        model = basis.grow_x(n)
        model = model.grow_y(m)
        self.atoms = model.atoms
        self.lat_vectors = model.lat_vectors


class HexagonalPlane(AtomicModel):
    """The HexagonalPlane  with rectangular cell """
    def __init__(self, ch1: int = 6, ch2: int = 6, a: float = 1.43, n=0, m=0, length=0):
        super().__init__()

        self.maxMol = 200000
        self.a = a
        lets = [self.mendeley.get_let(ch1), self.mendeley.get_let(ch2)]
        chs = [ch1, ch2]

        if (n == 0) and (m == 0):
            return

        np1, px, py, p_site_type, self.length = self.hexagonal_positions(n, m, length)

        for i_par in range(0, np1):
            self.add_atom(Atom([px[i_par], py[i_par], 0, lets[p_site_type[i_par]], chs[p_site_type[i_par]]]))

    def hexagonal_positions(self, n=0, m=0, leng=0):
        px = np.zeros(self.maxMol)
        py = np.zeros(self.maxMol)
        p_site_type = np.zeros(self.maxMol, dtype=int)

        nx = 40
        ny = 100
        """ calculations """
        hx, hy, site_type = self.hexagon()
        for k_par in range(0, nx):
            hx_plus = 3 * self.a * k_par
            for ih_par in range(0, 4):
                i_par = ih_par + k_par * 4
                px[i_par] = hx[ih_par] + hx_plus
                py[i_par] = hy[ih_par]
                p_site_type[i_par] = site_type[ih_par]
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
                p_site_type[j1] = p_site_type[i_par]
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
                p_site_type[j] = p_site_type[i]
                j += 1
        np1 = j
        return np1, px, py, p_site_type, vlen

    def hexagon(self):
        """ definition of a hexagon """
        hx = np.zeros(6)
        hy = np.zeros(6)
        hx[0] = self.a
        hy[0] = 0.0
        site_type = [0, 1, 0, 1, 0, 1]
        for i in range(1, 6):
            hx[i] = hx[i - 1] * math.cos(math.pi / 3) - hy[i - 1] * math.sin(math.pi / 3)
            hy[i] = hx[i - 1] * math.sin(math.pi / 3) + hy[i - 1] * math.cos(math.pi / 3)
        return hx, hy, site_type
