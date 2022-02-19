# -*- coding: utf-8 -*-
# Python 3

##################################################################
######################## TPeriodTable ############################
##################################################################    

class TPeriodTableAtom:
    def __init__(self, charge, radius, let, color, mass=1):
        self.charge = charge
        self.radius = radius
        self.let = let
        self.color = color
        self.mass = mass


class TPeriodTable:
    """The TPeriodTable class provides basic fetches of Mendelevium's table. The constructor does not have arguments"""
    def __init__(self):
        self.table_size = 128
        self.Atoms = []
        self.default_color = [0.6, 0.6, 1.0]
        self.default_radius = 77
        self.Atoms.append(TPeriodTableAtom(0,    0, ' ',  [0.1, 1.0, 0.1]))
        self.Atoms.append(TPeriodTableAtom(1,   53, 'H',  [0.1, 0.6, 0.1], 1))
        self.Atoms.append(TPeriodTableAtom(2,   31, 'He', [0.5, 0.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(3,  145, 'Li', [1.0, 1.0, 0.15]))
        self.Atoms.append(TPeriodTableAtom(4,  112, 'Be', [0.3, 1.0, 1.0]))
        self.Atoms.append(TPeriodTableAtom(5,   98,  'B', [0.6, 0.3, 0.0]))
        self.Atoms.append(TPeriodTableAtom(6,   77,  'C', [0.2, 0.2, 0.8], 12))
        self.Atoms.append(TPeriodTableAtom(7,   92,  'N', [0.45, 0.3, 0.6]))
        self.Atoms.append(TPeriodTableAtom(8,   60,  'O', [1.0, 0.0, 0.5], 16))
        self.Atoms.append(TPeriodTableAtom(9,   73,  'F', self.default_color))
        self.Atoms.append(TPeriodTableAtom(10,  38, 'Ne', self.default_color))
        self.Atoms.append(TPeriodTableAtom(11, 190, 'Na', self.default_color))
        self.Atoms.append(TPeriodTableAtom(12, 160, 'Mg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(13, 143, 'Al', self.default_color))
        self.Atoms.append(TPeriodTableAtom(14, 132, 'Si', self.default_color))
        self.Atoms.append(TPeriodTableAtom(15, 128,  'P', self.default_color))
        self.Atoms.append(TPeriodTableAtom(16, 127,  'S', self.default_color))
        self.Atoms.append(TPeriodTableAtom(17,  99, 'Cl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(18,  71, 'Ar', self.default_color))
        self.Atoms.append(TPeriodTableAtom(19, 235,  'K', self.default_color))
        self.Atoms.append(TPeriodTableAtom(20, 197, 'Ca', self.default_color))
        self.Atoms.append(TPeriodTableAtom(21, 162, 'Sc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(22, 147, 'Ti', self.default_color))
        self.Atoms.append(TPeriodTableAtom(23, 134,  'V', self.default_color))
        self.Atoms.append(TPeriodTableAtom(24, 130, 'Cr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(25, 127, 'Mn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(26, 126, 'Fe', self.default_color))
        self.Atoms.append(TPeriodTableAtom(27, 125, 'Co', self.default_color))
        self.Atoms.append(TPeriodTableAtom(28, 124, 'Ni', self.default_color))
        self.Atoms.append(TPeriodTableAtom(29, 128, 'Cu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(30, 138, 'Zn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(31, 141, 'Ga', self.default_color))
        self.Atoms.append(TPeriodTableAtom(32, 123, 'Ge', self.default_color))
        self.Atoms.append(TPeriodTableAtom(33, 139, 'As', self.default_color))
        self.Atoms.append(TPeriodTableAtom(34, 140, 'Se', self.default_color))
        self.Atoms.append(TPeriodTableAtom(35, 114, 'Br', self.default_color))
        self.Atoms.append(TPeriodTableAtom(36,  88, 'Kr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(37, 248, 'Rb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(38, 215, 'Sr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(39, 178,  'Y', self.default_color))
        self.Atoms.append(TPeriodTableAtom(40, 160, 'Zr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(41, 160, 'Nb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(42, 139, 'Mo', self.default_color))
        self.Atoms.append(TPeriodTableAtom(43, 136, 'Tc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(44, 134, 'Ru', self.default_color))
        self.Atoms.append(TPeriodTableAtom(45, 134, 'Rh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(46, 137, 'Pd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(47, 144, 'Ag', self.default_color))
        self.Atoms.append(TPeriodTableAtom(48, 154, 'Cd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(49, 166, 'In', self.default_color))
        self.Atoms.append(TPeriodTableAtom(50, 162, 'Sn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(51, 159, 'Sb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(52, 160, 'Te', self.default_color))
        self.Atoms.append(TPeriodTableAtom(53, 136,  'I', self.default_color))
        self.Atoms.append(TPeriodTableAtom(54, 108, 'Xe', self.default_color))
        self.Atoms.append(TPeriodTableAtom(55, 267, 'Cs', self.default_color))
        self.Atoms.append(TPeriodTableAtom(56, 222, 'Ba', self.default_color))
        self.Atoms.append(TPeriodTableAtom(57, 187, 'La', self.default_color))
        self.Atoms.append(TPeriodTableAtom(58, 181, 'Ce', self.default_color))
        self.Atoms.append(TPeriodTableAtom(59, 182, 'Pr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(60, 182, 'Nd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(61, 183, 'Pm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(62, 181, 'Sm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(63, 199, 'Eu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(64, 179, 'Gd', self.default_color))
        self.Atoms.append(TPeriodTableAtom(65, 180, 'Tb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(66, 180, 'Dy', self.default_color))
        self.Atoms.append(TPeriodTableAtom(67, 179, 'Ho', self.default_color))
        self.Atoms.append(TPeriodTableAtom(68, 178, 'Er', self.default_color))
        self.Atoms.append(TPeriodTableAtom(69, 177, 'Tm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(70, 194, 'Yb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(71, 175, 'Lu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(72, 167, 'Hf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(73, 149, 'Ta', self.default_color))
        self.Atoms.append(TPeriodTableAtom(74, 141,  'W', self.default_color))
        self.Atoms.append(TPeriodTableAtom(75, 137, 'Re', self.default_color))
        self.Atoms.append(TPeriodTableAtom(76, 135, 'Os', self.default_color))
        self.Atoms.append(TPeriodTableAtom(77, 136, 'Ir', self.default_color))
        self.Atoms.append(TPeriodTableAtom(78, 139, 'Pt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(79, 144, 'Au', self.default_color))
        self.Atoms.append(TPeriodTableAtom(80, 157, 'Hg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(81, 171, 'Tl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(82, 175, 'Pb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(83, 170, 'Bi', self.default_color))
        self.Atoms.append(TPeriodTableAtom(84, 176, 'Po', self.default_color))
        self.Atoms.append(TPeriodTableAtom(85, 145, 'At', self.default_color))
        self.Atoms.append(TPeriodTableAtom(86, 214, 'Rn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(87, 290, 'Fr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(88, 200, 'Ra', self.default_color))
        self.Atoms.append(TPeriodTableAtom(89, 188, 'Ac', self.default_color))
        self.Atoms.append(TPeriodTableAtom(90, 180, 'Th', self.default_color))
        self.Atoms.append(TPeriodTableAtom(91, 161, 'Pa', self.default_color))
        self.Atoms.append(TPeriodTableAtom(92, 138,  'U', self.default_color))
        self.Atoms.append(TPeriodTableAtom(93, 130, 'Np', self.default_color))
        self.Atoms.append(TPeriodTableAtom(94, 162, 'Pu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(95, 173, 'Am', self.default_color))
        self.Atoms.append(TPeriodTableAtom(96, 299, 'Cm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(97, 297, 'Bk', self.default_color))
        self.Atoms.append(TPeriodTableAtom(98, 295, 'Cf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(99, 292, 'Es', self.default_color))
        self.Atoms.append(TPeriodTableAtom(100,290, 'Fm', self.default_color))
        self.Atoms.append(TPeriodTableAtom(101,287, 'Md', self.default_color))
        self.Atoms.append(TPeriodTableAtom(102,285, 'No', self.default_color))
        self.Atoms.append(TPeriodTableAtom(103,282, 'Lr', self.default_color))
        self.Atoms.append(TPeriodTableAtom(104,280, 'Rf', self.default_color))
        self.Atoms.append(TPeriodTableAtom(105,280, 'Db', self.default_color))
        self.Atoms.append(TPeriodTableAtom(106,280, 'Sg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(107,128, 'Bh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(108,140, 'Hs', self.default_color))
        self.Atoms.append(TPeriodTableAtom(109,150, 'Mt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(110,150, 'Ds', self.default_color))
        self.Atoms.append(TPeriodTableAtom(111,150, 'Rg', self.default_color))
        self.Atoms.append(TPeriodTableAtom(112,150, 'Cn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(113,170, 'Nh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(114,170, 'Fl', self.default_color))
        self.Atoms.append(TPeriodTableAtom(115,170, 'Mc', self.default_color))
        self.Atoms.append(TPeriodTableAtom(116,170, 'Lv', self.default_color))
        self.Atoms.append(TPeriodTableAtom(117,170, 'Ts', self.default_color))
        self.Atoms.append(TPeriodTableAtom(118,152, 'Og', self.default_color))
        self.Atoms.append(TPeriodTableAtom(119,170, 'Uue', self.default_color))
        self.Atoms.append(TPeriodTableAtom(120,170, 'Ubn', self.default_color))
        self.Atoms.append(TPeriodTableAtom(121,170, 'Ubu', self.default_color))
        self.Atoms.append(TPeriodTableAtom(122,170, 'Ubb', self.default_color))
        self.Atoms.append(TPeriodTableAtom(123,170, 'Ubt', self.default_color))
        self.Atoms.append(TPeriodTableAtom(124,170, 'Ubq', self.default_color))
        self.Atoms.append(TPeriodTableAtom(125,170, 'Ubp', self.default_color))
        self.Atoms.append(TPeriodTableAtom(126,170, 'Ubh', self.default_color))
        self.Atoms.append(TPeriodTableAtom(127,170, 'Ubs', self.default_color))

        self.Bonds = []
        rang = range(0, self.table_size)
        for i in rang:
            row = []
            for j in rang:
                tab_rad_i = self.Atoms[i].radius / 100.0
                tab_rad_j = self.Atoms[j].radius / 100.0
                row.append(tab_rad_i+tab_rad_j)
            self.Bonds.append(row)

        self.Bonds[1][6] = 1.0
        self.Bonds[1][8] = 1.0
        self.Bonds[6][6] = 1.42
        self.Bonds[6][8] = 1.42
        self.Bonds[16][16] = 1.9
        self.Bonds[46][46] = 2.5
        self.Bonds[78][78] = 2.5
        self.Bonds[79][79] = 2.5

        for i in range(0, self.table_size):
            for j in range(i+1, self.table_size):
                self.Bonds[j][i] = self.Bonds[i][j]

    def get_rad(self, charge):
        if int(charge) < self.table_size:
            return self.Atoms[int(charge)].radius
        else:
            return self.default_radius

    def get_let(self, charge):
        if int(charge) < self.table_size:
            return self.Atoms[int(charge)].let
        if int(charge) >= 200:
            return "Direct"

    def get_color(self, charge):
        if int(charge) < self.table_size:
            return self.Atoms[int(charge)].color
        else:
            return self.default_color

    def get_charge_by_letter(self, let):
        for atom in self.Atoms:
            if atom.let.lower() == let.lower():
                return int(atom.charge)
        if let.lower() == "direct":
            return 200
        return -1

    def get_all_colors(self):
        colors = []
        for i in range(0, self.table_size):
            colors.append(self.Atoms[i].color)
        return colors

    def get_all_letters(self):
        lets = []
        for i in range(0, self.table_size):
            lets.append(self.Atoms[i].let)
        return lets
