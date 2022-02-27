# -*- coding: utf-8 -*-

import math

import numpy as np
from pathlib import Path

from models.atom import Atom
from models.atomic_model import TAtomicModel
from models.swnt import SWNT


class CapedSWNT(TAtomicModel):
    def __init__(self, n, m, leng, ncell, type, dist1, angle1, dist2, angle2):
        if leng == 0:
            leng = ncell * SWNT.unitlength(n, m, 1.43)
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
                size1 = self.Size(n, m)
                capatoms = self.cap4SWNT_norm()
                if self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z

                minz = self.minZ()
                maxz = capatoms.maxZ()

                capatoms.move(0, 0, minz - maxz - zaz)
                capatoms.rotate_z(angle1)
                for i in range(0, capatoms.nAtoms()):
                    self.add_atom(capatoms[i])

            if type == 2:
                # second cap generation
                capatoms = self.cap4SWNT_norm()
                if not self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z
                maxz = self.maxZ()
                minz = capatoms.minZ()

                zaz = dist2

                capatoms.move(0, 0, (maxz - minz) + zaz)
                capatoms.rotate_z(angle2)
                for i in range(0, capatoms.nAtoms()):
                    self.add_atom(capatoms[i])
            # end cap generation

    def Size(self, n, m):
        for i in range(0, len(self.availableind)):
            if (n == self.availableind[0]) and (m == self.availableind[1]):
                return int(self.availableind[3])
        return -1

    def cap4SWNT_norm(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
                cap1 = TAtomicModel()
                for j in range(0, self.cap_atoms.nAtoms()):
                    cap1.add_atom(self.cap_atoms[j])
                cap1.move(- 1.0 * self.availableind[4] / 2.0, - 1.0 * self.availableind[5] / 2.0, 0)

                for j in range(0, cap1.nAtoms()):
                    xnn = cap1[j].x * math.cos(self.availableind[6] *math.pi / 180.0) - cap1[j].y * math.sin(self.availableind[6] *math.pi / 180.0)
                    ynn = cap1[j].x * math.sin(self.availableind[6] *math.pi / 180.0) + cap1[j].y * math.cos(self.availableind[6] *math.pi / 180.0)

                    cap1[j].x = xnn
                    cap1[j].y = ynn
                return cap1
        return None

    def invert(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
            return self.availableind[7]
        return -1

    def simpleSWNT(self):
        tube_atoms = TAtomicModel()
        bound = 1.433
        size = 0
        if (self.n > 0) and (self.m == 0):
            # zigzag nanotube
            bound = 1.421
            rad_nanotube = 5 * 0.246 * self.n / math.pi
            z_coord = 0  # z координата
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
            count = 0
            z_coord = 0
            ring_nanotube = 0

            while z_coord < self.length:
                for jk in range(0, self.n):
                    x = rad_nanotube * math.cos(2 * math.pi * jk / self.n+rotdeg)
                    y = rad_nanotube * math.sin(2 * math.pi * jk / self.n+rotdeg)
                    tube_atoms.add_atom(Atom([x, y, z_coord, "C", 6, False]))

                tem +=1
                bound = 1.421
                if tem == 2:
                    tem=0
                    rotdeg += math.pi / self.n
                    bound = 1.421 * math.cos(math.pi / 3)
                z_coord += bound
                ring_nanotube +=1

        if (self.n == self.m) and (self.n > 0):
            # armchare nanotube
            pinan = math.pi / self.n
            rad_nanotube = math.sqrt((5 + 2 * math.sqrt(2 * (1 + math.cos(pinan)))) / (8 * (1 - math.cos(pinan)))) * bound
            alfa = math.acos(1 - bound * bound / (8 * rad_nanotube * rad_nanotube))
            betta = math.acos(1 - bound * bound / (2 * rad_nanotube * rad_nanotube))

            z_coord = 0  # z координата
            ring_nanotube = 0
            size = 0
            deltag = betta + alfa

            while z_coord < self.length:
                size += 2 * self.m
                z_coord += math.sqrt(3.0) * 0.5 * bound
                ring_nanotube+=1

                angle = 0
                sw = 0
                z_coord = 0
                ring_nanotube = 0
                deltag = betta + alfa
                count = 0

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
                    ring_nanotube +=1
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

            self.cap_atoms = TAtomicModel()

            self.cap_atoms.add_atom(Atom([-0.36693112712E+00, 0.14828478339E+01, 1.86168451, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.14123318617E+01, 0.42721410070E+00, 1.88297428, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.10568038810E+01, -0.10057307755E+01, 1.82796005, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.38589540659E+00, -0.13267764277E+01, 1.84106985, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.13496217634E+01, -0.28131482088E+00, 1.87047317, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.10071810608E+01, 0.10985087143E+01, 1.89193246, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.19987312467E+01, 0.30014395545E+01, 0.73606458, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([ -0.29578581189E+01, 0.19721596960E+01, 0.73632071, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.27571698247E+01, 0.71874399926E+00, 1.44108245, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.35829370629E+01,-0.24291285515E+00,0.68239008, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.32349211883E+01,-0.16206333154E+01,0.68625620, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.20047282591E+01,-0.19775980251E+01,1.40477121, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.16362756027E+01,-0.32383913803E+01,0.75524927, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.28063713290E+00,-0.36132532671E+01,0.71923701, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.70896305879E+00,-0.27408666603E+01,1.38701774, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.19888600177E+01,-0.29354589995E+01,0.70705602, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.30282933796E+01,-0.19633677080E+01,0.74070240, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.27179573531E+01,-0.64426510383E+00,1.43991810, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.36391537961E+01,0.27223176788E+00,0.72968705, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.32670313687E+01,0.16238573940E+01,0.73224586, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.20483841305E+01,0.19967370195E+01,1.37748738, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.15990133003E+01,0.32589685312E+01,0.71464324, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.23683726128E+00,0.36518477604E+01,0.74698622, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.74036797244E+00,0.28521743942E+01,1.47972432, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([4.0586,-0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([2.6474,3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.0000,4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-1.4111,3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-4.0586,0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-3.5688,-2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-2.6474,-3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.0000,-4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([1.4111,-3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([3.5688,-2.0604,-0.5264, "C", 6, False]))

        if self.n == 10 and self.m == 0:
            self.available = True
            self.availableind[0] = 10
            self.availableind[1] = 0
            self.availableind[2] = 1 # cap
            self.availableind[3] = 20
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -25
            self.availableind[7] = 0

            self.cap_atoms = TAtomicModel()

            self.cap_atoms.add_atom(Atom([0.34216148481E+00, -0.12053675732E+01, 0.27817708814E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.29945044883E+01,-0.12353947470E+01,0.15621427500E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.31963746233E+01,0.76302077744E+00,0.15989438777E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.99585806005E+00,-0.74592960370E+00,0.38623433120E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.28372435918E+00, -0.33073880303E+01, 0.15748123961E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.20970977233E+01,0.24759817007E+01,0.15783693808E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.76620899479E+00,0.23662547380E+01,0.10756116106E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.29097152253E+00,0.31787983516E+01,0.16306217062E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.25460695924E+01,-0.12019370177E-01,0.10168833638E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.98415232530E+00,0.71949433978E+00,0.38919891314E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.12527638107E+01,-0.26556683526E-01,0.42986738706E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([ -0.20374152633E+01 , 0.15039739223E+01 , 0.10034475884E+01 , "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.16718683612E+01,-0.28065794251E+01,0.15605264317E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.78433886197E+00,-0.24167512792E+01,0.96858303258E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.31930381398E+01,-0.81568604886E+00,0.15674645057E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.39669805001E+00,0.11287767681E+01,0.46634191420E+00, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.17123909710E+01,0.27591217116E+01,0.16091964100E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.29519974190E+01,0.12337637208E+01,0.16234022245E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([0.21072419022E+01, -0.24689911393E+01,0.15851545095E+01, "C", 6, False]))
            self.cap_atoms.add_atom(Atom([-0.20785821822E+01,-0.15522369686E+01,0.10403308851E+01, "C", 6, False]))

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
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name, False)[0]

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
            self.cap_atoms = TAtomicModel.atoms_from_xyz(f_name, False)[0]
