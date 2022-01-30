# -*- coding: utf-8 -*-

import math

import numpy as np

from utils import helpers
from utils.atomic_model import TAtom, TAtomicModel


##################################################################
######################### TGRAPHENE ##############################
##################################################################


class TGraphene(TAtomicModel):
    """The TGraphene class provides """
    def __init__(self, n=0, m=0, leng=0):
        TAtomicModel.__init__(self)
        self.maxMol = 200000
        self.a = 1.43

        if (n == 0) and (m == 0):
            return

        np1, pi, px, py, leng = self.graphene_positions(n, m, leng)

        for i_par in range(0, np1):
            self.add_atom(TAtom([px[i_par], py[i_par], 0, "C", 6]))

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


##################################################################
########################### TSWNT ################################
##################################################################


class TBiNT(TAtomicModel):

    def __init__(self, n, m, leng=1, tubetype="BN"):

        TAtomicModel.__init__(self)
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
                    self.add_atom(TAtom([x, y, z, let, charge]))

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
                    self.add_atom(TAtom([x, y, z, atom1[0], atom1[1]]))

                    x = rad * math.cos(math.radians(i * 360 / n + 120 / n + dfi))
                    y = rad * math.sin(math.radians(i * 360 / n + 120 / n + dfi))
                    self.add_atom(TAtom([x, y, z, atom2[0], atom2[1]]))
                row += 1
                z += math.sqrt(3) / 2 * a

##################################################################
########################### TSWNT ################################
##################################################################    


class TSWNT(TGraphene):
    """The TSWNT class provides """
    def __init__(self, n, m, leng=0, ncell=1):
        if leng == 0:
            leng = ncell * TSWNT.unitlength(n, m, 1.43)

        TGraphene.__init__(self)

        rad = TSWNT.radius(n, m)
        self.set_lat_vectors([10 * rad, 0, 0], [0, 10 * rad, 0], [0, 0, leng])
        np1, pi, px, py, leng = self.graphene_positions(n, m, leng)

        """ output """
        R = leng / (2 * math.pi)
        
        for i_par in range(0, np1):
            phi_par = px[i_par] / R
            qx = R * math.sin(phi_par)
            qy = -R * math.cos(phi_par)
            qz = py[i_par]
            self.add_atom(TAtom([qx, qy, qz, "C", 6]))

    @staticmethod
    def radius(n, m):
        return math.sqrt(n*n + n*m +m*m)

    @staticmethod
    def unitlength(n, m, acc): 
        a = math.sqrt(3) * acc
        pi = math.pi
        
        b1x = 2 * pi / a / math.sqrt(3)
        b1y = 2 * pi / a
        b2x = 2 * pi / a / math.sqrt(3)
        b2y = -2 * pi / a
        Ch = a * math.sqrt(n * n + n * m + m * m)
        dia = Ch / pi
        theta = math.atan((math.sqrt(3) * m / (2.0 * n + m)))
        theta = theta * 180.0 / pi
        d = helpers.cdev(n, m)
        if (n - m) % (3 * d) != 0:
            dR = d
        else:
            dR = 3 * d
        T1 = (2 * m + n) / dR
        T2 = -(2 * n + m) / dR
        T = math.sqrt(3) * Ch / dR
        return T

##################################################################
######################## TCap for SWNT ###########################
##################################################################


class TCapedSWNT(TAtomicModel):
    def __init__(self, n, m, leng, ncell, type, dist1, angle1, dist2, angle2):
        if leng == 0:
            leng = ncell * TSWNT.unitlength(n, m, 1.43)
        TAtomicModel.__init__(self)
        self.availableind = np.zeros((8))
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
            Cap = self.cap_formation()  # TCap(n,m)
            if self.available:
                size1 = self.Size(n, m)
                capatoms = self.cap4SWNT_norm()
                if self.invert():
                    for i in range(0, size1):
                        capatoms[i].z = -capatoms[i].z

                minz = self.minZ()
                maxz = capatoms.maxZ()

                capatoms.move(0, 0, minz - maxz - zaz)
                capatoms.rotateZ(angle1)
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
                capatoms.rotateZ(angle2)
                for i in range(0, capatoms.nAtoms()):
                    self.add_atom(capatoms[i])
            # end cap generation

    def Size(self, n, m):
        for i in range(0,len(self.availableind)):
            if (n == self.availableind[0]) and (m == self.availableind[1]):
                return int(self.availableind[3])
        return -1

    def cap4SWNT_norm(self):
        if (self.n == self.availableind[0]) and (self.m == self.availableind[1]):
                cap1 = TAtomicModel()
                for j in range(0,self.cap_atoms.nAtoms()):
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
            z_coord = 0 # z координата
            tem = 1
            # calculation of atoms
            while (z_coord < self.length):
                size += self.n
                tem +=1
                bound = 1.421
                if tem == 2:
                    tem=0
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
                    tube_atoms.add_atom(TAtom([x, y, z_coord, "C", 6, False]))

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

            z_coord = 0 # z координата
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
                        tube_atoms.add_atom(TAtom([x, y, z_coord, "C", 6, False]))

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
            self.availableind[2] = 1 # cap  0
            self.availableind[3] = 36
            self.availableind[4] = 0
            self.availableind[5] = 0
            self.availableind[6] = -40
            self.availableind[7] = 1

            self.cap_atoms = TAtomicModel()

            self.cap_atoms.add_atom(TAtom([-0.36693112712E+00, 0.14828478339E+01, 1.86168451, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.14123318617E+01, 0.42721410070E+00, 1.88297428, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.10568038810E+01, -0.10057307755E+01, 1.82796005, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.38589540659E+00, -0.13267764277E+01, 1.84106985, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.13496217634E+01, -0.28131482088E+00, 1.87047317, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.10071810608E+01, 0.10985087143E+01, 1.89193246, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.19987312467E+01, 0.30014395545E+01, 0.73606458, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([ -0.29578581189E+01, 0.19721596960E+01, 0.73632071, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.27571698247E+01, 0.71874399926E+00, 1.44108245, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.35829370629E+01,-0.24291285515E+00,0.68239008, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.32349211883E+01,-0.16206333154E+01,0.68625620, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.20047282591E+01,-0.19775980251E+01,1.40477121, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.16362756027E+01,-0.32383913803E+01,0.75524927, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.28063713290E+00,-0.36132532671E+01,0.71923701, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.70896305879E+00,-0.27408666603E+01,1.38701774, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.19888600177E+01,-0.29354589995E+01,0.70705602, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.30282933796E+01,-0.19633677080E+01,0.74070240, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.27179573531E+01,-0.64426510383E+00,1.43991810, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.36391537961E+01,0.27223176788E+00,0.72968705, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.32670313687E+01,0.16238573940E+01,0.73224586, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.20483841305E+01,0.19967370195E+01,1.37748738, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.15990133003E+01,0.32589685312E+01,0.71464324, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.23683726128E+00,0.36518477604E+01,0.74698622, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.74036797244E+00,0.28521743942E+01,1.47972432, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([4.0586,-0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([2.6474,3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.0000,4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-1.4111,3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-3.5688,2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-4.0586,0.7137,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-3.5688,-2.0604,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-2.6474,-3.1580,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.0000,-4.1209,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([1.4111,-3.8717,-0.5264, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([3.5688,-2.0604,-0.5264, "C", 6, False]))

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

            self.cap_atoms.add_atom(TAtom([0.34216148481E+00, -0.12053675732E+01, 0.27817708814E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.29945044883E+01,-0.12353947470E+01,0.15621427500E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.31963746233E+01,0.76302077744E+00,0.15989438777E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.99585806005E+00,-0.74592960370E+00,0.38623433120E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.28372435918E+00, -0.33073880303E+01, 0.15748123961E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.20970977233E+01,0.24759817007E+01,0.15783693808E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.76620899479E+00,0.23662547380E+01,0.10756116106E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.29097152253E+00,0.31787983516E+01,0.16306217062E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.25460695924E+01,-0.12019370177E-01,0.10168833638E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.98415232530E+00,0.71949433978E+00,0.38919891314E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.12527638107E+01,-0.26556683526E-01,0.42986738706E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([ -0.20374152633E+01 , 0.15039739223E+01 , 0.10034475884E+01 , "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.16718683612E+01,-0.28065794251E+01,0.15605264317E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.78433886197E+00,-0.24167512792E+01,0.96858303258E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.31930381398E+01,-0.81568604886E+00,0.15674645057E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.39669805001E+00,0.11287767681E+01,0.46634191420E+00, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.17123909710E+01,0.27591217116E+01,0.16091964100E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.29519974190E+01,0.12337637208E+01,0.16234022245E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([0.21072419022E+01, -0.24689911393E+01,0.15851545095E+01, "C", 6, False]))
            self.cap_atoms.add_atom(TAtom([-0.20785821822E+01,-0.15522369686E+01,0.10403308851E+01, "C", 6, False]))


"""
    class TCap{

        atom ** cap;
    public: 
        TCap();
    ~TCap()
    {};
    atom * cap4SWNT(int, int);
    atom * cap4SWNT_norm(int, int);
    int
    size(int, int);
    int
    isavailable(int, int);
    int
    invert(int, int);
    };
    TCap::TCap()
    {
        cap = new atom * [4];
    int  i;
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111


    availableind[2][0] = 10;
    availableind[2][1] = 10;
    availableind[2][2] = 2; // cap
    availableind[2][3] = 110;
    availableind[2][4] = 51;
    availableind[2][5] = -15;
    availableind[2][6] = 54;
    availableind[2][7] = 1;
    cap[2] = new atom[110];
    for (i=0;i < 110;i++){
    cap[2][i].c.SetStr("C", 1);
    cap[2][i].charge = 6;
    cap[2][i].select = 1;
    }
    cap[2][0].x = (float) 24.307116;    cap[2][0].y = (float) -8.391858;    cap[2][0].z = (float) 26.631681;
    cap[2][1].x = (float) 24.028402;    cap[2][1].y = (float) -6.999814;    cap[2][1].z = (float) 26.613461;
    cap[2][2].x = (float) 25.74894;     cap[2][2].y = (float) -8.591233;    cap[2][2].z = (float) 26.608431;
    cap[2][3].x = (float) 25.256088;    cap[2][3].y = (float) -6.25233;     cap[2][3].z = (float) 26.558006;
    cap[2][4].x = (float) 26.336517;    cap[2][4].y = (float) -7.251723;    cap[2][4].z = (float) 26.524309;
    cap[2][5].x = (float) 25.451431;    cap[2][5].y = (float) -4.952374;    cap[2][5].z = (float) 25.950344;
    cap[2][6].x = (float) 22.903727;    cap[2][6].y = (float) -6.458869;    cap[2][6].z = (float) 25.895767;
    cap[2][7].x = (float) 23.512154;    cap[2][7].y = (float) -9.253161;    cap[2][7].z = (float) 25.884455;
    cap[2][8].x = (float) 26.402281;    cap[2][8].y = (float) -9.617024;    cap[2][8].z = (float) 25.883873;
    cap[2][9].x = (float) 27.543873;    cap[2][9].y = (float) -7.03859;     cap[2][9].z = (float) 25.807861;
    cap[2][10].x = (float) 26.813923;   cap[2][10].y = (float) -4.730283;   cap[2][10].z = (float) 25.435555;
    cap[2][11].x = (float) 21.885521;   cap[2][11].y = (float) -7.384042;   cap[2][11].z = (float) 25.430565;
    cap[2][12].x = (float) 24.251844;   cap[2][12].y = (float) -4.368014;   cap[2][12].z = (float) 25.417097;
    cap[2][13].x = (float) 23.017797;   cap[2][13].y = (float) -5.112086;   cap[2][13].z = (float) 25.412504;
    cap[2][14].x = (float) 22.263638;   cap[2][14].y = (float) -8.773506;   cap[2][14].z = (float) 25.406738;
    cap[2][15].x = (float) 24.106068;   cap[2][15].y = (float) -10.451938;  cap[2][15].z = (float) 25.336063;
    cap[2][16].x = (float) 27.713478;   cap[2][16].y = (float) -9.483947;   cap[2][16].z = (float) 25.335426;
    cap[2][17].x = (float) 27.7791;     cap[2][17].y = (float) -5.737792;   cap[2][17].z = (float) 25.287855;
    cap[2][18].x = (float) 25.509258;   cap[2][18].y = (float) -10.582597;  cap[2][18].z = (float) 25.282236;
    cap[2][19].x = (float) 28.305012;   cap[2][19].y = (float) -8.159348;   cap[2][19].z = (float) 25.266905;
    cap[2][20].x = (float) 21.897963;   cap[2][20].y = (float) -4.546319;   cap[2][20].z = (float) 24.703777;
    cap[2][21].x = (float) 26.917971;   cap[2][21].y = (float) -3.495377;   cap[2][21].z = (float) 24.661104;
    cap[2][22].x = (float) 20.821575;   cap[2][22].y = (float) -6.853278;   cap[2][22].z = (float) 24.616817;
    cap[2][23].x = (float) 24.381664;   cap[2][23].y = (float) -3.221068;   cap[2][23].z = (float) 24.605165;
    cap[2][24].x = (float) 29.501595;   cap[2][24].y = (float) -7.858403;   cap[2][24].z = (float) 24.561548;
    cap[2][25].x = (float) 26.126131;   cap[2][25].y = (float) -11.722587;  cap[2][25].z = (float) 24.513506;
    cap[2][26].x = (float) 23.28396;    cap[2][26].y = (float) -11.332781;  cap[2][26].z = (float) 24.507889;
    cap[2][27].x = (float) 28.285215;   cap[2][27].y = (float) -10.485401;  cap[2][27].z = (float) 24.500849;
    cap[2][28].x = (float) 21.51675;    cap[2][28].y = (float) -9.593892;   cap[2][28].z = (float) 24.498133;
    cap[2][29].x = (float) 20.781013;   cap[2][29].y = (float) -5.421203;   cap[2][29].z = (float) 24.480793;
    cap[2][30].x = (float) 28.923557;   cap[2][30].y = (float) -5.488295;   cap[2][30].z = (float) 24.469994;
    cap[2][31].x = (float) 25.704922;   cap[2][31].y = (float) -2.690116;   cap[2][31].z = (float) 24.392683;
    cap[2][32].x = (float) 21.946112;   cap[2][32].y = (float) -10.949246;  cap[2][32].z = (float) 24.35844;
    cap[2][33].x = (float) 27.558289;   cap[2][33].y = (float) -11.695153;  cap[2][33].z = (float) 24.308565;
    cap[2][34].x = (float) 23.31764;    cap[2][34].y = (float) -2.718772;   cap[2][34].z = (float) 23.835554;
    cap[2][35].x = (float) 28.049913;   cap[2][35].y = (float) -3.287543;   cap[2][35].z = (float) 23.804535;
    cap[2][36].x = (float) 20.02154;    cap[2][36].y = (float) -7.71293;    cap[2][36].z = (float) 23.80274;
    cap[2][37].x = (float) 29.099838;   cap[2][37].y = (float) -4.276214;   cap[2][37].z = (float) 23.775066;
    cap[2][38].x = (float) 22.07427;    cap[2][38].y = (float) -3.384869;   cap[2][38].z = (float) 23.769482;
    cap[2][39].x = (float) 20.394318;   cap[2][39].y = (float) -9.130861;   cap[2][39].z = (float) 23.768671;
    cap[2][40].x = (float) 25.275475;   cap[2][40].y = (float) -12.659516;  cap[2][40].z = (float) 23.754967;
    cap[2][41].x = (float) 23.81428;    cap[2][41].y = (float) -12.399732;  cap[2][41].z = (float) 23.730297;
    cap[2][42].x = (float) 19.686266;   cap[2][42].y = (float) -4.93257;    cap[2][42].z = (float) 23.662189;
    cap[2][43].x = (float) 21.137602;   cap[2][43].y = (float) -11.810185;  cap[2][43].z = (float) 23.616472;
    cap[2][44].x = (float) 28.149002;   cap[2][44].y = (float) -12.723328;  cap[2][44].z = (float) 23.540396;
    cap[2][45].x = (float) 25.829796;   cap[2][45].y = (float) -1.545785;   cap[2][45].z = (float) 23.532829;
    cap[2][46].x = (float) 30.998842;   cap[2][46].y = (float) -6.29346;    cap[2][46].z = (float) 23.487898;
    cap[2][47].x = (float) 31.195286;   cap[2][47].y = (float) -8.674395;   cap[2][47].z = (float) 22.883595;
    cap[2][48].x = (float) 23.492815;   cap[2][48].y = (float) -1.661548;   cap[2][48].z = (float) 22.8822;
    cap[2][49].x = (float) 19.012489;   cap[2][49].y = (float) -7.228202;   cap[2][49].z = (float) 22.877794;
    cap[2][50].x = (float) 19.993397;   cap[2][50].y = (float) -11.350829;  cap[2][50].z = (float) 22.851616;
    cap[2][51].x = (float) 18.855139;   cap[2][51].y = (float) -5.81593;    cap[2][51].z = (float) 22.842537;
    cap[2][52].x = (float) 24.740768;   cap[2][52].y = (float) -0.941531;   cap[2][52].z = (float) 22.839033;
    cap[2][53].x = (float) 28.143888;   cap[2][53].y = (float) -2.214602;   cap[2][53].z = (float) 22.823023;
    cap[2][54].x = (float) 27.309549;   cap[2][54].y = (float) -13.638415;  cap[2][54].z = (float) 22.816744;
    cap[2][55].x = (float) 29.37397;    cap[2][55].y = (float) -12.497607;  cap[2][55].z = (float) 22.810347;
    cap[2][56].x = (float) 29.921804;   cap[2][56].y = (float) -11.138785;  cap[2][56].z = (float) 22.805902;
    cap[2][57].x = (float) 19.881659;   cap[2][57].y = (float) -3.716206;   cap[2][57].z = (float) 22.798765;
    cap[2][58].x = (float) 21.114313;   cap[2][58].y = (float) -3.043349;   cap[2][58].z = (float) 22.797981;
    cap[2][59].x = (float) 30.141171;   cap[2][59].y = (float) -4.090331;   cap[2][59].z = (float) 22.79162;
    cap[2][60].x = (float) 25.848095;   cap[2][60].y = (float) -13.504389;  cap[2][60].z = (float) 22.791164;
    cap[2][61].x = (float) 21.709684;   cap[2][61].y = (float) -12.907913;  cap[2][61].z = (float) 22.779915;
    cap[2][62].x = (float) 27.025219;   cap[2][62].y = (float) -1.334748;   cap[2][62].z = (float) 22.775311;
    cap[2][63].x = (float) 23.056452;   cap[2][63].y = (float) -13.112155;  cap[2][63].z = (float) 22.761112;
    cap[2][64].x = (float) 19.703302;   cap[2][64].y = (float) -9.919573;   cap[2][64].z = (float) 22.754223;
    cap[2][65].x = (float) 31.64447;    cap[2][65].y = (float) -7.360505;   cap[2][65].z = (float) 22.753363;
    cap[2][66].x = (float) 31.199718;   cap[2][66].y = (float) -5.068017;   cap[2][66].z = (float) 22.727516;
    cap[2][67].x = (float) 29.014811;   cap[2][67].y = (float) -2.2107;     cap[2][67].z = (float) 21.689016;
    cap[2][68].x = (float) 22.682739;   cap[2][68].y = (float) -1.526551;   cap[2][68].z = (float) 21.684744;
    cap[2][69].x = (float) 31.287226;   cap[2][69].y = (float) -9.44718;    cap[2][69].z = (float) 21.67403;
    cap[2][70].x = (float) 18.668207;   cap[2][70].y = (float) -7.955943;   cap[2][70].z = (float) 21.656946;
    cap[2][71].x = (float) 30.655699;   cap[2][71].y = (float) -10.736203;  cap[2][71].z = (float) 21.652979;
    cap[2][72].x = (float) 30.026033;   cap[2][72].y = (float) -3.221543;   cap[2][72].z = (float) 21.64381;
    cap[2][73].x = (float) 21.492094;   cap[2][73].y = (float) -2.250502;   cap[2][73].z = (float) 21.632978;
    cap[2][74].x = (float) 19.070688;   cap[2][74].y = (float) -9.297336;   cap[2][74].z = (float) 21.628992;
    cap[2][75].x = (float) 23.742189;   cap[2][75].y = (float) -13.624204;  cap[2][75].z = (float) 21.613325;
    cap[2][76].x = (float) 25.252064;   cap[2][76].y = (float) -0.282405;   cap[2][76].z = (float) 21.604607;
    cap[2][77].x = (float) 19.886501;   cap[2][77].y = (float) -12.067063;  cap[2][77].z = (float) 21.598923;
    cap[2][78].x = (float) 29.27622;    cap[2][78].y = (float) -13.270625;  cap[2][78].z = (float) 21.591307;
    cap[2][79].x = (float) 18.551779;   cap[2][79].y = (float) -5.17668;    cap[2][79].z = (float) 21.590588;
    cap[2][80].x = (float) 25.156328;   cap[2][80].y = (float) -13.750842;  cap[2][80].z = (float) 21.585398;
    cap[2][81].x = (float) 19.18738;    cap[2][81].y = (float) -3.879289;   cap[2][81].z = (float) 21.583361;
    cap[2][82].x = (float) 20.975973;   cap[2][82].y = (float) -13.06409;   cap[2][82].z = (float) 21.574989;
    cap[2][83].x = (float) 26.698114;   cap[2][83].y = (float) -0.632041;   cap[2][83].z = (float) 21.553831;
    cap[2][84].x = (float) 27.99502;    cap[2][84].y = (float) -13.89404;   cap[2][84].z = (float) 21.547998;
    cap[2][85].x = (float) 31.97467;    cap[2][85].y = (float) -5.319426;   cap[2][85].z = (float) 21.545002;
    cap[2][86].x = (float) 32.260117;   cap[2][86].y = (float) -6.783418;   cap[2][86].z = (float) 21.532591;
    cap[2][87].x = (float) 23.241642;   cap[2][87].y = (float) -0.886021;   cap[2][87].z = (float) 20.499775;
    cap[2][88].x = (float) 28.579681;   cap[2][88].y = (float) -1.601615;   cap[2][88].z = (float) 20.466377;
    cap[2][89].x = (float) 18.241289;   cap[2][89].y = (float) -7.256305;   cap[2][89].z = (float) 20.452448;
    cap[2][90].x = (float) 30.559538;   cap[2][90].y = (float) -11.519896;  cap[2][90].z = (float) 20.451962;
    cap[2][91].x = (float) 31.801649;   cap[2][91].y = (float) -8.87911;    cap[2][91].z = (float) 20.423489;
    cap[2][92].x = (float) 24.516485;   cap[2][92].y = (float) -0.370414;   cap[2][92].z = (float) 20.416256;
    cap[2][93].x = (float) 20.798647;   cap[2][93].y = (float) -2.429421;   cap[2][93].z = (float) 20.403654;
    cap[2][94].x = (float) 30.66143;    cap[2][94].y = (float) -3.581628;   cap[2][94].z = (float) 20.401373;
    cap[2][95].x = (float) 19.02692;    cap[2][95].y = (float) -10.045808;  cap[2][95].z = (float) 20.399921;
    cap[2][96].x = (float) 32.225246;   cap[2][96].y = (float) -7.558652;   cap[2][96].z = (float) 20.384998;
    cap[2][97].x = (float) 19.653811;   cap[2][97].y = (float) -3.306693;   cap[2][97].z = (float) 20.38278;
    cap[2][98].x = (float) 19.527115;   cap[2][98].y = (float) -11.410149;  cap[2][98].z = (float) 20.379232;
    cap[2][99].x = (float) 29.849607;   cap[2][99].y = (float) -12.757981;  cap[2][99].z = (float) 20.373478;
    cap[2][100].x = (float) 18.299751;  cap[2][100].y = (float) -5.846803;   cap[2][100].z = (float) 20.371761;
    cap[2][101].x = (float) 31.523699;  cap[2][101].y = (float) -4.676303;   cap[2][101].z = (float) 20.367992;
    cap[2][102].x = (float) 27.372185;  cap[2][102].y = (float) -0.799687;   cap[2][102].z = (float) 20.345131;
    cap[2][103].x = (float) 25.903364;  cap[2][103].y = (float) -14.031196;  cap[2][103].z = (float) 20.343964;
    cap[2][104].x = (float) 23.052832;  cap[2][104].y = (float) -13.603871;  cap[2][104].z = (float) 20.328026;
    cap[2][105].x = (float) 21.613218;  cap[2][105].y = (float) -13.354865;  cap[2][105].z = (float) 20.293333;
    cap[2][106].x = (float) 29.890324;  cap[2][106].y = (float) -6.534263;   cap[2][106].z = (float) 24.27564;
    cap[2][107].x = (float) 30.184898;  cap[2][107].y = (float) -8.9305;     cap[2][107].z = (float) 23.873917;
    cap[2][108].x = (float) 29.517391;  cap[2][108].y = (float) -10.189402;  cap[2][108].z = (float) 23.839216;
    cap[2][109].x = (float) 27.325338;  cap[2][109].y = (float) -14.219027;  cap[2][109].z = (float) 20.34614;




    availableind[3][0] = 19;
    availableind[3][1] = 0;
    availableind[3][2] = 0; // cap
    availableind[3][3] = 125; // 24;
    availableind[3][4] = 0;
    availableind[3][5] = 0;
    availableind[3][6] = 0;
    availableind[3][7] = 1;
    cap[3] = new atom[125];
    for (i=0;i < 125;i++){
    cap[3][i].c.SetStr("C", 1);
    cap[3][i].charge = 6;
    cap[3][i].select = 1;
    }

    cap[3][0].x = (float) -0.48589722322E+01;   cap[3][0].y = (float) -0.36221817094E+01;    cap[3][0].z = (float) -0.14080584970E+01;
    cap[3][1].x = (float) -0.45730216641E+01;   cap[3][1].y = (float) -0.48531400967E+01;    cap[3][1].z = (float) -0.74577774177E+00;
    cap[3][2].x = (float) -0.48843163209E+01;   cap[3][2].y = (float) -0.52449271110E+01;    cap[3][2].z = (float) 0.60148070560E+00;
    cap[3][3].x = (float) -0.41153315282E+01;   cap[3][3].y = (float) -0.61902792021E+01;    cap[3][3].z = (float) 0.14159023882E+01;
    cap[3][4].x = (float) -0.61987961664E+01;   cap[3][4].y = (float) -0.31933977619E+01;    cap[3][4].z = (float) 0.67432004891E+00;
    cap[3][5].x = (float) -0.57695614619E+01;   cap[3][5].y = (float) -0.44079622455E+01;    cap[3][5].z = (float) 0.14001309796E+01;
    cap[3][6].x = (float) -0.57357142720E+01;   cap[3][6].y = (float) -0.27426732726E+01;    cap[3][6].z = (float) -0.71670030400E+00;
    cap[3][7].x = (float) -0.30985668536E+01;   cap[3][7].y = (float) -0.39242127454E+01;    cap[3][7].z = (float) -0.31614631281E+01;
    cap[3][8].x = (float) -0.29215146165E+01;   cap[3][8].y = (float) -0.52169101055E+01;    cap[3][8].z = (float) -0.25760465958E+01;
    cap[3][9].x = (float) -0.36652796414E+01;   cap[3][9].y = (float) -0.56953921641E+01;    cap[3][9].z = (float) -0.14010441490E+01;
    cap[3][10].x = (float) -0.41562523579E+01;  cap[3][10].y = (float) -0.31814642732E+01;   cap[3][10].z = (float) -0.25769020730E+01;
    cap[3][11].x = (float) -0.53674105201E+01;  cap[3][11].y = (float) -0.11044211318E+01;   cap[3][11].z = (float) -0.26418590383E+01;
    cap[3][12].x = (float) -0.43605534094E+01;  cap[3][12].y = (float) -0.19146253022E+01;   cap[3][12].z = (float) -0.31653236139E+01;
    cap[3][13].x = (float) -0.59681628233E+01;  cap[3][13].y = (float) -0.14839249801E+01;   cap[3][13].z = (float) -0.13735951494E+01;
    cap[3][14].x = (float) -0.69403908369E+01;  cap[3][14].y = (float) -0.22370927539E+01;   cap[3][14].z = (float) 0.14908204357E+01;
    cap[3][15].x = (float) -0.67829820558E+01;  cap[3][15].y = (float) -0.56752250354E+00;   cap[3][15].z = (float) -0.66587975966E+00;
    cap[3][16].x = (float) -0.72402721042E+01;  cap[3][16].y = (float) -0.97249826495E+00;   cap[3][16].z = (float) 0.67447957321E+00;
    cap[3][17].x = (float) -0.73235299353E+00;  cap[3][17].y = (float) -0.39436611322E+01;   cap[3][17].z = (float) -0.38962171073E+01;
    cap[3][18].x = (float) -0.50780477489E+00;  cap[3][18].y = (float) -0.52145277840E+01;   cap[3][18].z = (float) -0.31315665561E+01;
    cap[3][19].x = (float) 0.73643831218E+00;   cap[3][19].y = (float) -0.54148786225E+01;   cap[3][19].z = (float) -0.25386385055E+01;
    cap[3][20].x = (float) 0.82869013696E+00;   cap[3][20].y = (float) -0.61954057298E+01;   cap[3][20].z = (float) -0.12991011496E+01;
    cap[3][21].x = (float) 0.19966654092E+01;   cap[3][21].y = (float) -0.61445332848E+01;   cap[3][21].z = (float) -0.56731734942E+00;
    cap[3][22].x = (float) -0.16482338625E+01;  cap[3][22].y = (float) -0.58617419890E+01;   cap[3][22].z = (float) -0.26446300562E+01;
    cap[3][23].x = (float) -0.20424170549E+01;  cap[3][23].y = (float) -0.33461547050E+01;   cap[3][23].z = (float) -0.39209782908E+01;
    cap[3][24].x = (float) -0.75114773645E+01;  cap[3][24].y = (float) 0.18067922075E+01;    cap[3][24].z = (float) -0.44811891889E+00;
    cap[3][25].x = (float) -0.79206146976E+01;  cap[3][25].y = (float) 0.14562264028E+01;    cap[3][25].z = (float) 0.91254016598E+00;
    cap[3][26].x = (float) -0.76685162423E+01;  cap[3][26].y = (float) 0.16980360536E+00;    cap[3][26].z = (float) 0.14605629646E+01;
    cap[3][27].x = (float) -0.68884826029E+01;  cap[3][27].y = (float) 0.80473287388E+00;    cap[3][27].z = (float) -0.11616286642E+01;
    cap[3][28].x = (float) -0.60047077999E+01;  cap[3][28].y = (float) 0.12593067284E+01;    cap[3][28].z = (float) -0.21853196867E+01;
    cap[3][29].x = (float) -0.37043207368E+01;  cap[3][29].y = (float) -0.11691464229E+00;   cap[3][29].z = (float) -0.47797936434E+01;
    cap[3][30].x = (float) -0.46955878800E+01;  cap[3][30].y = (float) 0.77138417158E+00;    cap[3][30].z = (float) -0.41973177994E+01;
    cap[3][31].x = (float) -0.54683045289E+01;  cap[3][31].y = (float) 0.30771919461E+00;    cap[3][31].z = (float) -0.30867828557E+01;
    cap[3][32].x = (float) -0.34994407953E+01;  cap[3][32].y = (float) -0.13884048701E+01;   cap[3][32].z = (float) -0.42753133052E+01;
    cap[3][33].x = (float) -0.21914963346E+01;  cap[3][33].y = (float) -0.20311739108E+01;   cap[3][33].z = (float) -0.44867260054E+01;
    cap[3][34].x = (float) 0.31811288950E+00;   cap[3][34].y = (float) -0.31560065296E+01;   cap[3][34].z = (float) -0.44548999592E+01;
    cap[3][35].x = (float) 0.15983815345E+01;   cap[3][35].y = (float) -0.36373350389E+01;   cap[3][35].z = (float) -0.40771402988E+01;
    cap[3][36].x = (float) 0.18123089400E+01;   cap[3][36].y = (float) -0.46147956852E+01;   cap[3][36].z = (float) -0.30333652860E+01;
    cap[3][37].x = (float) 0.30182632334E+01;   cap[3][37].y = (float) -0.46418994665E+01;   cap[3][37].z = (float) -0.23340010633E+01;
    cap[3][38].x = (float) 0.30822595901E+01;   cap[3][38].y = (float) -0.53692904839E+01;   cap[3][38].z = (float) -0.11553135841E+01;
    cap[3][39].x = (float) -0.44145125740E+01;  cap[3][39].y = (float) 0.30295629037E+01;    cap[3][39].z = (float) -0.30876901352E+01;
    cap[3][40].x = (float) -0.41496701086E+01;  cap[3][40].y = (float) 0.21668980992E+01;    cap[3][40].z = (float) -0.41788603341E+01;
    cap[3][41].x = (float) -0.54717214675E+01;  cap[3][41].y = (float) 0.26230229502E+01;    cap[3][41].z = (float) -0.22031862702E+01;
    cap[3][42].x = (float) -0.57452822978E+01;  cap[3][42].y = (float) 0.35183378284E+01;    cap[3][42].z = (float) -0.11100755633E+01;
    cap[3][43].x = (float) -0.69788869712E+01;  cap[3][43].y = (float) 0.31937006916E+01;    cap[3][43].z = (float) -0.40618133609E+00;
    cap[3][44].x = (float) -0.70193780544E+01;  cap[3][44].y = (float) 0.36965461800E+01;    cap[3][44].z = (float) 0.91517819913E+00;
    cap[3][45].x = (float) 0.16523352074E+00;   cap[3][45].y = (float) -0.18032304813E+01;   cap[3][45].z = (float) -0.49305142163E+01;
    cap[3][46].x = (float) -0.11573103944E+01;  cap[3][46].y = (float) -0.11893230741E+01;   cap[3][46].z = (float) -0.49714852095E+01;
    cap[3][47].x = (float) -0.12605392497E+01;  cap[3][47].y = (float) 0.22108796884E+00;    cap[3][47].z = (float) -0.52504323268E+01;
    cap[3][48].x = (float) -0.25794728950E+01;  cap[3][48].y = (float) 0.75361599776E+00;    cap[3][48].z = (float) -0.51733152286E+01;
    cap[3][49].x = (float) -0.28027074511E+01;  cap[3][49].y = (float) 0.21453478573E+01;    cap[3][49].z = (float) -0.47389600896E+01;
    cap[3][50].x = (float) 0.26644496516E+01;   cap[3][50].y = (float) -0.28435462096E+01;   cap[3][50].z = (float) -0.45123012806E+01;
    cap[3][51].x = (float) 0.22001072009E+01;   cap[3][51].y = (float) 0.13212985356E+01;    cap[3][51].z = (float) -0.42274981849E+01;
    cap[3][52].x = (float) 0.34848761367E+01;   cap[3][52].y = (float) 0.69294693172E+00;    cap[3][52].z = (float) -0.40171024281E+01;
    cap[3][53].x = (float) 0.43882121233E+01;   cap[3][53].y = (float) 0.11883035679E+01;    cap[3][53].z = (float) -0.29970595721E+01;
    cap[3][54].x = (float) 0.54077550723E+01;   cap[3][54].y = (float) 0.36060498625E+00;    cap[3][54].z = (float) -0.24476920823E+01;
    cap[3][55].x = (float) 0.61275551737E+01;   cap[3][55].y = (float) 0.80675134746E+00;    cap[3][55].z = (float) -0.12819119132E+01;
    cap[3][56].x = (float) 0.35784698679E+01;   cap[3][56].y = (float) -0.64465531335E+00;   cap[3][56].z = (float) -0.44393474850E+01;
    cap[3][57].x = (float) 0.25277602109E+01;   cap[3][57].y = (float) -0.14676089703E+01;   cap[3][57].z = (float) -0.49706567691E+01;
    cap[3][58].x = (float) 0.12410381593E+01;   cap[3][58].y = (float) -0.92156078036E+00;   cap[3][58].z = (float) -0.50694471974E+01;
    cap[3][59].x = (float) -0.39894863437E+01;  cap[3][59].y = (float) 0.58083051115E+01;    cap[3][59].z = (float) 0.14219366111E+01;
    cap[3][60].x = (float) -0.27891077023E+01;  cap[3][60].y = (float) 0.61425746567E+01;    cap[3][60].z = (float) 0.67675101993E+00;
    cap[3][61].x = (float) -0.17341355045E+01;  cap[3][61].y = (float) 0.67810476938E+01;    cap[3][61].z = (float) 0.14401766805E+01;
    cap[3][62].x = (float) -0.26416500505E+01;  cap[3][62].y = (float) 0.55000252031E+01;    cap[3][62].z = (float) -0.64803012252E+00;
    cap[3][63].x = (float) -0.36621284208E+01;  cap[3][63].y = (float) 0.47348285122E+01;    cap[3][63].z = (float) -0.12940342992E+01;
    cap[3][64].x = (float) -0.48361840605E+01;  cap[3][64].y = (float) 0.44386418572E+01;    cap[3][64].z = (float) -0.56295604184E+00;
    cap[3][65].x = (float) -0.49771198224E+01;  cap[3][65].y = (float) 0.50271444148E+01;    cap[3][65].z = (float) 0.71677155783E+00;
    cap[3][66].x = (float) -0.60934632823E+01;  cap[3][66].y = (float) 0.45909516215E+01;    cap[3][66].z = (float) 0.14564518832E+01;
    cap[3][67].x = (float) 0.62250744908E+00;   cap[3][67].y = (float) 0.31269666662E+01;    cap[3][67].z = (float) -0.37231933843E+01;
    cap[3][68].x = (float) 0.19476423274E+01;   cap[3][68].y = (float) 0.26239954193E+01;    cap[3][68].z = (float) -0.36829387134E+01;
    cap[3][69].x = (float) 0.10785602392E+01;   cap[3][69].y = (float) 0.54068473406E+00;    cap[3][69].z = (float) -0.48090614435E+01;
    cap[3][70].x = (float) -0.17393968925E+00;  cap[3][70].y = (float) 0.11055498947E+01;    cap[3][70].z = (float) -0.48995214127E+01;
    cap[3][71].x = (float) -0.44006718707E+00;  cap[3][71].y = (float) 0.24355601974E+01;    cap[3][71].z = (float) -0.43852749264E+01;
    cap[3][72].x = (float) -0.17860406639E+01;  cap[3][72].y = (float) 0.29334114802E+01;    cap[3][72].z = (float) -0.41530438557E+01;
    cap[3][73].x = (float) -0.13875948540E+01;  cap[3][73].y = (float) 0.55045018407E+01;    cap[3][73].z = (float) -0.13415237180E+01;
    cap[3][74].x = (float) -0.10816602975E+01;  cap[3][74].y = (float) 0.46780782608E+01;    cap[3][74].z = (float) -0.25314256051E+01;
    cap[3][75].x = (float) -0.21503536330E+01;  cap[3][75].y = (float) 0.39185313960E+01;    cap[3][75].z = (float) -0.31535540029E+01;
    cap[3][76].x = (float) -0.34823508771E+01;  cap[3][76].y = (float) 0.40141606547E+01;    cap[3][76].z = (float) -0.25651587619E+01;
    cap[3][77].x = (float) 0.24663823151E+00;   cap[3][77].y = (float) 0.42696137742E+01;    cap[3][77].z = (float) -0.28771473354E+01;
    cap[3][78].x = (float) 0.13087825816E+01;   cap[3][78].y = (float) 0.48739642843E+01;    cap[3][78].z = (float) -0.22172833310E+01;
    cap[3][79].x = (float) -0.30025910544E+00;  cap[3][79].y = (float) 0.60674159789E+01;    cap[3][79].z = (float) -0.59207743321E+00;
    cap[3][80].x = (float) -0.47015080754E+00;  cap[3][80].y = (float) 0.66469929056E+01;    cap[3][80].z = (float) 0.75076176236E+00;
    cap[3][81].x = (float) 0.78377067629E+00;   cap[3][81].y = (float) 0.69502445579E+01;    cap[3][81].z = (float) 0.15010993533E+01;
    cap[3][82].x = (float) 0.99428162544E+00;   cap[3][82].y = (float) 0.56735052099E+01;    cap[3][82].z = (float) -0.10902469016E+01;
    cap[3][83].x = (float) 0.29639384150E+01;   cap[3][83].y = (float) 0.31485718319E+01;    cap[3][83].z = (float) -0.28036662864E+01;
    cap[3][84].x = (float) 0.41637338162E+01;   cap[3][84].y = (float) 0.24428101575E+01;    cap[3][84].z = (float) -0.23693007584E+01;
    cap[3][85].x = (float) 0.49026698449E+01;   cap[3][85].y = (float) 0.28595856454E+01;    cap[3][85].z = (float) -0.11528240761E+01;
    cap[3][86].x = (float) 0.59058021710E+01;   cap[3][86].y = (float) 0.20209895859E+01;    cap[3][86].z = (float) -0.58885198538E+00;
    cap[3][87].x = (float) 0.25835618182E+01;   cap[3][87].y = (float) 0.42529284469E+01;    cap[3][87].z = (float) -0.20940560263E+01;
    cap[3][88].x = (float) -0.28062749705E+01;  cap[3][88].y = (float) -0.66368798173E+01;   cap[3][88].z = (float) -0.68453039179E+00;
    cap[3][89].x = (float) -0.15384587223E+01;  cap[3][89].y = (float) -0.66771218269E+01;   cap[3][89].z = (float) -0.13843873956E+01;
    cap[3][90].x = (float) -0.29903198921E+01;  cap[3][90].y = (float) -0.67557018742E+01;   cap[3][90].z = (float) 0.76541108211E+00;
    cap[3][91].x = (float) -0.17507117740E+01;  cap[3][91].y = (float) -0.71256372017E+01;   cap[3][91].z = (float) 0.14510273582E+01;
    cap[3][92].x = (float) -0.35026597295E+00;  cap[3][92].y = (float) -0.67174293764E+01;   cap[3][92].z = (float) -0.67607419775E+00;
    cap[3][93].x = (float) -0.43648129818E+00;  cap[3][93].y = (float) -0.70640163051E+01;   cap[3][93].z = (float) 0.66711274826E+00;
    cap[3][94].x = (float) -0.76842444280E+01;  cap[3][94].y = (float) 0.26369859554E+01;    cap[3][94].z = (float) 0.16679430268E+01;
    cap[3][95].x = (float) 0.32164176516E+01;   cap[3][95].y = (float) 0.47705528741E+01;    cap[3][95].z = (float) -0.90847477999E+00;
    cap[3][96].x = (float) 0.21695904656E+01;   cap[3][96].y = (float) 0.56594417519E+01;    cap[3][96].z = (float) -0.31784361562E+00;
    cap[3][97].x = (float) 0.44505915654E+01;   cap[3][97].y = (float) 0.40113313747E+01;    cap[3][97].z = (float) -0.38931257127E+00;
    cap[3][98].x = (float) 0.50890034792E+01;   cap[3][98].y = (float) 0.43596632579E+01;    cap[3][98].z = (float) 0.85785337730E+00;
    cap[3][99].x = (float) 0.20298162362E+01;   cap[3][99].y = (float) 0.63498829802E+01;    cap[3][99].z = (float) 0.89479069820E+00;
    cap[3][100].x = (float) 0.44394007870E+01;  cap[3][100].y = (float) 0.54464393035E+01;    cap[3][100].z = (float) 0.15820555980E+01;
    cap[3][101].x = (float) 0.39454420530E+01;  cap[3][101].y = (float) -0.28896679490E+01;   cap[3][101].z = (float) -0.38171379528E+01;
    cap[3][102].x = (float) 0.45441409267E+01;  cap[3][102].y = (float) -0.15543388643E+01;   cap[3][102].z = (float) -0.38380771818E+01;
    cap[3][103].x = (float) 0.41366706263E+01;  cap[3][103].y = (float) -0.37110428245E+01;   cap[3][103].z = (float) -0.26691313407E+01;
    cap[3][104].x = (float) 0.52084514909E+01;  cap[3][104].y = (float) -0.33625136282E+01;   cap[3][104].z = (float) -0.18417114013E+01;
    cap[3][105].x = (float) 0.54030082733E+01;  cap[3][105].y = (float) -0.10188536686E+01;   cap[3][105].z = (float) -0.28017308470E+01;
    cap[3][106].x = (float) 0.58097015616E+01;  cap[3][106].y = (float) -0.20774691375E+01;   cap[3][106].z = (float) -0.18719092053E+01;
    cap[3][107].x = (float) 0.61281717962E+01;  cap[3][107].y = (float) 0.34968779994E+01;    cap[3][107].z = (float) 0.14722175171E+01;
    cap[3][108].x = (float) 0.71524561940E+01;  cap[3][108].y = (float) 0.12360471500E+01;    cap[3][108].z = (float) 0.14839707629E+01;
    cap[3][109].x = (float) 0.72428511780E+01;  cap[3][109].y = (float) -0.91013542804E-02;   cap[3][109].z = (float) 0.75120937696E+00;
    cap[3][110].x = (float) 0.68820346010E+01;  cap[3][110].y = (float) -0.20913975592E+00;   cap[3][110].z = (float) -0.61688433125E+00;
    cap[3][111].x = (float) 0.65235436153E+01;  cap[3][111].y = (float) 0.23230838703E+01;    cap[3][111].z = (float) 0.66800236575E+00;
    cap[3][112].x = (float) 0.68398594782E+01;  cap[3][112].y = (float) -0.22554947714E+01;   cap[3][112].z = (float) 0.40870882145E+00;
    cap[3][113].x = (float) 0.63179898912E+01;  cap[3][113].y = (float) -0.35771173596E+01;   cap[3][113].z = (float) 0.39694371190E+00;
    cap[3][114].x = (float) 0.54329258323E+01;  cap[3][114].y = (float) -0.41879769539E+01;   cap[3][114].z = (float) -0.66390158760E+00;
    cap[3][115].x = (float) 0.66073744100E+01;  cap[3][115].y = (float) -0.15912966887E+01;   cap[3][115].z = (float) -0.82764811960E+00;
    cap[3][116].x = (float) 0.72761905274E+01;  cap[3][116].y = (float) -0.13246908678E+01;   cap[3][116].z = (float) 0.13980815612E+01;
    cap[3][117].x = (float) 0.62685425726E+01;  cap[3][117].y = (float) -0.42606948960E+01;   cap[3][117].z = (float) 0.15405588457E+01;
    cap[3][118].x = (float) 0.43168767014E+01;  cap[3][118].y = (float) -0.59536265241E+01;   cap[3][118].z = (float) 0.77014318327E+00;
    cap[3][119].x = (float) 0.32073538384E+01;  cap[3][119].y = (float) -0.67023387704E+01;   cap[3][119].z = (float) 0.14583053354E+01;
    cap[3][120].x = (float) 0.19751907838E+01;  cap[3][120].y = (float) -0.67562960649E+01;   cap[3][120].z = (float) 0.74440377661E+00;
    cap[3][121].x = (float) 0.43577056420E+01;  cap[3][121].y = (float) -0.52175801363E+01;   cap[3][121].z = (float) -0.47207558861E+00;
    cap[3][122].x = (float) 0.53510096191E+01;  cap[3][122].y = (float) -0.53990638900E+01;   cap[3][122].z = (float) 0.15576274634E+01;
    cap[3][123].x = (float) 0.32120768505E+01;  cap[3][123].y = (float) 0.63398270748E+01;    cap[3][123].z = (float) 0.16315574508E+01;
    cap[3][124].x = (float) 0.74576062711E+00;  cap[3][124].y = (float) -0.72007466769E+01;   cap[3][124].z = (float) 0.14325440011E+01;

    };

    atom * TCap::cap4SWNT(int
    n, int
    m){
        int
    id = -1;
    for (int i=0;i < 100;i++) if ((n == availableind[i][0]) & & (m == availableind[i][1])) id =availableind[i][2];
    return cap[id];
    };
    
"""

