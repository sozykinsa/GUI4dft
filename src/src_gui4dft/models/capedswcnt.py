# -*- coding: utf-8 -*-

import math

import numpy as np
from pathlib import Path

from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel as TAtomicModel
from src_gui4dft.models.swnt import SWNT


class CapedSWNT(TAtomicModel):
    def __init__(self, n, m, leng, ncell, type, dist1, angle1, dist2, angle2):
        if leng == 0:
            leng = ncell * SWNT.unit_length(n, m, 1.43)
        TAtomicModel.__init__(self)
        self.availableind = np.zeros(8)
        self.available = False

        self.n = n
        self.m = m
        self.length = leng
        self.tube = self.simpleSWNT()
        for atom in self.tube:
            self.add_atom(atom)
        # self.caps = []
        self.cap_atoms = TAtomicModel()
        self.cap_formation()

        if type == 1 or type == 2:
            # cap generation
            zaz = dist1
            if self.available:
                size1 = self.size(n, m)
                capatoms = self.cap4swnt_norm()
                if self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z

                minz = self.min_z()
                maxz = capatoms.max_z()

                capatoms.move(np.array([0, 0, minz - maxz - zaz]))
                capatoms.rotate_z(angle1)
                for i in range(0, capatoms.n_atoms()):
                    self.add_atom(capatoms[i])

            if type == 2:
                # second cap generation
                capatoms = self.cap4swnt_norm()
                if not self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z
                maxz = self.max_z()
                minz = capatoms.min_z()

                zaz = dist2

                capatoms.move(np.array([0, 0, (maxz - minz) + zaz]))
                capatoms.rotate_z(angle2)
                for i in range(0, capatoms.n_atoms()):
                    self.add_atom(capatoms[i])
            # end cap generation

    def size(self, n, m):
        for i in range(0, len(self.availableind)):
            if (n == self.availableind[0]) and (m == self.availableind[1]):
                return int(self.availableind[3])

    def cap4swnt_norm(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
            cap1 = TAtomicModel()
            for j in range(0, self.cap_atoms.n_atoms()):
                cap1.add_atom(self.cap_atoms[j])
            cap1.move(np.array([- 1.0 * self.availableind[4] / 2.0, - 1.0 * self.availableind[5] / 2.0, 0]))

            for j in range(0, cap1.n_atoms()):
                xnn = cap1[j].x * math.cos(self.availableind[6] * math.pi / 180.0) - \
                    cap1[j].y * math.sin(self.availableind[6] * math.pi / 180.0)
                ynn = cap1[j].x * math.sin(self.availableind[6] * math.pi / 180.0) + \
                    cap1[j].y * math.cos(self.availableind[6] * math.pi / 180.0)

                cap1[j].x = xnn
                cap1[j].y = ynn
            return cap1

    def invert(self):
        return self.availableind[7]

    def simpleSWNT(self):
        tube_atoms = TAtomicModel()
        bound = 1.433
        size = 0
        if (self.n > 0) and (self.m == 0):
            # zigzag nanotube
            bound = 1.421
            rad_nanotube = 5 * 0.246 * self.n / math.pi
            z_coord = 0  # z
            tem = 1
            # calculation of atoms
            while z_coord < self.length:
                size += self.n
                tem += 1
                bound = 1.421
                if tem == 2:
                    tem = 0
                    bound = 1.421 * math.cos(math.pi / 3.0)
                z_coord += bound
            # end calculation of atoms

            rotdeg = math.pi / self.n
            z_coord = 0
            ring_nanotube = 0

            while z_coord < self.length:
                for jk in range(0, self.n):
                    x = rad_nanotube * math.cos(2 * math.pi * jk / self.n+rotdeg)
                    y = rad_nanotube * math.sin(2 * math.pi * jk / self.n+rotdeg)
                    tube_atoms.add_atom(Atom([x, y, z_coord, "C", 6, False]))

                tem += 1
                bound = 1.421
                if tem == 2:
                    tem = 0
                    rotdeg += math.pi / self.n
                    bound = 1.421 * math.cos(math.pi / 3)
                z_coord += bound
                ring_nanotube += 1

        if (self.n == self.m) and (self.n > 0):
            # armchare nanotube
            pinan = math.pi / self.n
            rad_nanotube = math.sqrt((5 + 2 * math.sqrt(2 * (1 + math.cos(pinan)))) / (8 * (1 - math.cos(pinan)))) * \
                bound
            alfa = math.acos(1 - bound * bound / (8 * rad_nanotube * rad_nanotube))
            betta = math.acos(1 - bound * bound / (2 * rad_nanotube * rad_nanotube))

            z_coord = 0  # z
            ring_nanotube = 0
            size = 0
            # deltag = betta + alfa

            while z_coord < self.length:
                size += 2 * self.m
                z_coord += math.sqrt(3.0) * 0.5 * bound
                ring_nanotube += 1

                angle = 0
                sw = 0
                z_coord = 0
                ring_nanotube = 0
                deltag = betta + alfa

                while z_coord < self.length:
                    deltag = betta+alfa - deltag
                    for jk in range(0, 2 * self.m):
                        sw = 1-sw
                        if sw == 1:
                            angle += betta
                        else:
                            angle += pinan+alfa
                        if angle > 2 * math.pi:
                            angle = angle - 2 * math.pi
                        if angle < -2 * math.pi:
                            angle = angle + 2 * math.pi
                        x = rad_nanotube * math.cos(angle-deltag)
                        y = rad_nanotube * math.sin(angle-deltag)
                        tube_atoms.add_atom(Atom([x, y, z_coord, "C", 6, False]))

                    z_coord += math.sqrt(3.0) * 0.5 * bound
                    ring_nanotube += 1
        return tube_atoms

    def cap_formation(self):
        # 0 - n
        # 1 - m
        # 2 - index in Cap
        # 3 - number of atoms
        # 4 - x0
        # 5 - y0
        # 6 - fi
        # 7 - bool invert or not

        if self.n == 6 and self.m == 6:
            self.available = True
            self.availableind[0] = 6
            self.availableind[1] = 6
            self.availableind[2] = 1  # cap  0
            self.availableind[3] = 36
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -40
            self.availableind[7] = 1

            f_name = Path(__file__).parent / "caps" / 'cap-6-6.xyz'
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name)[0]

        if self.n == 10 and self.m == 0:
            self.available = True
            self.availableind[0] = 10
            self.availableind[1] = 0
            self.availableind[2] = 1  # cap
            self.availableind[3] = 20
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -25
            self.availableind[7] = 0

            f_name = Path(__file__).parent / "caps" / 'cap-10-0.xyz'
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name)[0]

        if self.n == 19 and self.m == 0:
            self.available = True
            self.availableind[0] = 19
            self.availableind[1] = 0
            self.availableind[2] = 0
            self.availableind[3] = 125
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = 10
            self.availableind[7] = 0

            f_name = Path(__file__).parent / "caps" / 'cap-19-0.xyz'
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name)[0]

        if self.n == 10 and self.m == 10:
            self.available = True
            self.availableind[0] = 10
            self.availableind[1] = 10
            self.availableind[2] = 2
            self.availableind[3] = 110
            self.availableind[4] = 51
            self.availableind[5] = -15
            self.availableind[6] = 54
            self.availableind[7] = 1

            f_name = Path(__file__).parent / "caps" / 'cap-10-10.xyz'
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name)[0]
