# -*- coding: utf-8 -*-
# Python 3
from typing import List
import copy
import math
import os
import re
from datetime import date
from copy import deepcopy

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm

from core_atomistic import helpers
from core_atomistic.periodic_table import TPeriodTable
from core_atomistic.atom import Atom
from scipy.spatial.distance import cdist
from scipy.optimize import fmin
import scipy


class AtomicModel(object):
    def __init__(self, new_atoms: list = [], mendeley: TPeriodTable = None):
        self.atoms: List[Atom] = []
        self.bonds = []
        self.bonds_per = []  # for exact calculation in form
        self.dynamic_bonds: bool = True

        self.name = ""
        self.lat_vectors = 100 * np.eye(3)
        self.lat_constant: float = 1.0
        if mendeley is not None:
            self.mendeley = mendeley
        else:
            self.mendeley = TPeriodTable()

        for at in new_atoms:
            if isinstance(at, Atom):
                atom = deepcopy(at)
            else:
                atom = Atom(at)
            self.add_atom(atom)

        self.selected_atom = -1

    def __getitem__(self, i):
        return self.atoms[i]

    def add_atom_with_data(self, xyz: np.ndarray, charge: int, let: str = "", tag: str = "") -> None:
        """
        xyz: coords
        charge: atomic number
        tag: additional information
        """
        if let == "":
            let = self.mendeley.get_let(charge)
        atom = Atom([*xyz, let, charge])
        atom.tag = tag
        self.atoms.append(atom)

    def set_mendeley(self, mendeley):
        self.mendeley = mendeley

    @property
    def lat_const(self) -> float:
        return self.lat_constant

    @lat_const.setter
    def lat_const(self, lat=1.0):
        self.lat_constant = lat

    @property
    def lat_vector1(self) -> float:
        return self.lat_vectors[0]

    @lat_vector1.setter
    def lat_vector1(self, value):
        self.lat_vectors[0] = value

    @property
    def lat_vector2(self) -> float:
        return self.lat_vectors[1]

    @lat_vector2.setter
    def lat_vector2(self, value):
        self.lat_vectors[1] = value

    @property
    def lat_vector3(self) -> float:
        return self.lat_vectors[2]

    @lat_vector3.setter
    def lat_vector3(self, value):
        self.lat_vectors[2] = value

    def get_positions(self):
        pos = np.zeros((len(self.atoms), 3))
        for i in range(len(self.atoms)):
            pos[i, :] = self.atoms[i].x, self.atoms[i].y, self.atoms[i].z
        return pos

    def get_atomic_numbers(self):
        numb = np.zeros(len(self.atoms))
        for i in range(len(self.atoms)):
            numb[i] = self.atoms[i].charge
        return numb

    def get_covalent_radii(self):
        ind = list(set(self.get_atomic_numbers()))
        ind.sort()
        return self.mendeley.get_covalent_radii(ind)

    def get_center_of_mass(self):
        return np.array(self.center_mass())

    def get_tags(self):
        tags = []
        for at in self.atoms:
            tags.append(at.tag)
        return tags

    def get_cell(self):
        return self.lat_vectors

    def get_atoms_property(self, key):
        n = self.n_atoms()
        props = np.zeros(n, dtype=float)
        for i in range(n):
            props[i] = self.atoms[i].properties.get(key, 0.0)
        return props

    def get_fragment_selected(self):
        n = self.n_atoms()
        props = np.zeros(n, dtype=int)
        for i in range(n):
            props[i] = self.atoms[i].fragment1
        return props

    def twist_z(self, alpha):
        cm = self.center_mass()
        self.move(-cm)
        z0 = self.min_z()
        z1 = np.linalg.norm(self.lat_vector3)

        for i in range(0, len(self.atoms)):
            alpha1 = (self.atoms[i].z - z0) / z1 * alpha
            xnn = float(self.atoms[i].x) * math.cos(alpha1) - float(self.atoms[i].y) * math.sin(alpha1)
            ynn = float(self.atoms[i].x) * math.sin(alpha1) + float(self.atoms[i].y) * math.cos(alpha1)
            self.atoms[i].x = xnn
            self.atoms[i].y = ynn

    @staticmethod
    def atoms_from_xyz(filename):
        """Import from *.xyz file."""
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            number_of_atoms = int(math.fabs(int(f.readline())))
            new_model = AtomicModel.atoms_from_xyz_structure(number_of_atoms, f)
            molecules.append(new_model)
        return molecules

    def move(self, dl: np.ndarray) -> None:
        """Move model by the vector."""
        for atom in self.atoms:
            atom.xyz += dl

    def translate_atom(self, selected_atom, step_x, step_y, step_z):
        atom = self.atoms[selected_atom]
        atom.xyz += step_x * self.lat_vector1 + step_y * self.lat_vector2 + step_z * self.lat_vector3

    @staticmethod
    def atoms_from_xmol_xyz(filename: str):
        """Import from XMOL xyz file."""
        molecules = []
        if os.path.exists(filename):
            f = open(filename)
            number_of_atoms = int(math.fabs(int(f.readline())))
            molecules.append(AtomicModel.atoms_from_xyz_structure(number_of_atoms, f, [1, 2, 3, 4]))
        return molecules

    @staticmethod
    def atoms_from_xyz_structure(number_of_atoms: int, ani_file, indexes=[0, 1, 2, 3],
                                 is_allow_charge_incorrect: bool = False):
        """Get atoms from xyz file.
        number_of_atoms - number if data lines
        ani_file -
        indexes -
        is_only_charge_correct - check the charge for correctness
        """
        str2 = ani_file.readline()
        row = str2.split()
        if len(row) > 0:
            if not row[0].isnumeric():
                str2 = ani_file.readline()
        else:
            str2 = ani_file.readline()
        new_model = AtomicModel()
        mendeley = TPeriodTable()
        reg = re.compile('[^a-zA-Z ]')
        for i1 in range(0, number_of_atoms):
            str1 = helpers.spacedel(str2)
            s = str1.split(' ')
            xyz = np.array([s[indexes[1]], s[indexes[2]], s[indexes[3]]], dtype=float)
            if max(indexes) < len(s) - 1:
                tag = s[max(indexes) + 1]
            else:
                tag = ""
            c = s[indexes[0]]
            if c.isnumeric():
                charge = int(c)
                c = mendeley.get_let(charge)
            else:
                c = reg.sub('', s[indexes[0]])
                charge = mendeley.get_charge_by_letter(c)
            if (charge > 0) or is_allow_charge_incorrect:
                new_model.add_atom_with_data(xyz, charge, let=c, tag=tag)
            if i1 < number_of_atoms -1:
                str2 = ani_file.readline()
        new_model.set_lat_vectors_default()
        return new_model

    def get_angle_alpha(self):
        a = norm(self.lat_vector2)
        b = norm(self.lat_vector3)
        ab = self.lat_vector2[0] * self.lat_vector3[0] + self.lat_vector2[1] * self.lat_vector3[1] + \
            self.lat_vector2[2] * self.lat_vector3[2]
        angle = math.acos(ab / (a * b))
        return 180 * angle / math.pi

    def get_angle_beta(self):
        a = norm(self.lat_vector1)
        b = norm(self.lat_vector3)
        ab = self.lat_vector1[0] * self.lat_vector3[0] + self.lat_vector1[1] * self.lat_vector3[1] + \
            self.lat_vector1[2] * self.lat_vector3[2]
        angle = math.acos(ab / (a * b))
        return 180 * angle / math.pi

    def get_angle_gamma(self):
        a = norm(self.lat_vector2)
        b = norm(self.lat_vector1)
        ab = self.lat_vector2[0] * self.lat_vector1[0] + self.lat_vector2[1] * self.lat_vector1[1] + \
            self.lat_vector2[2] * self.lat_vector1[2]
        angle = math.acos(ab / (a * b))
        return 180 * angle / math.pi

    def cell_params(self):
        a = np.linalg.norm(self.lat_vector1)
        b = np.linalg.norm(self.lat_vector2)
        c = np.linalg.norm(self.lat_vector3)
        al = self.get_angle_alpha()
        bet = self.get_angle_beta()
        gam = self.get_angle_gamma()
        return a, b, c, al, bet, gam

    def set_lat_vectors(self, vectors, lat_const=1.0):
        v1, v2, v3 = vectors[0], vectors[1], vectors[2]
        self.lat_const = lat_const
        if (len(v1) == 3) and (len(v2) == 3) and (len(v3) == 3):
            self.lat_vector1 = np.array(v1)
            self.lat_vector2 = np.array(v2)
            self.lat_vector3 = np.array(v3)
        else:
            print("Wrong vectors")

    def set_lat_vectors_default(self):
        sx = self.size_x()
        if sx < 0.3:
            sx = 5
        sy = self.size_y()
        if sy < 0.3:
            sy = 5
        sz = self.size_z()
        if sz < 0.3:
            sz = 5
        self.lat_vectors = 1.4 * np.eye(3) * np.array((sx, sy, sz))

    def delete_atom(self, ind: int) -> None:
        """Remove atom from model."""
        if (ind >= 0) and (ind < self.n_atoms()):
            self.selected_atom = -1
            self.atoms.pop(ind)
            self.find_bonds_fast()

    def add_atom(self, atom, min_dist=0) -> bool:
        """Adds atom to the molecule is minimal distance to other atoms more then minDist.
        Return value: True if atom was added
        """
        dist = 10000
        if min_dist > 0:
            model = AtomicModel(self.atoms)
            model.set_lat_vectors(self.lat_vectors)
            model.add_atom(atom)
            for ind in range(0, len(self.atoms)):
                r = model.atom_atom_distance(ind, -1)  # len(model.atoms) - 1)
                if r < dist:
                    dist = r

        if min_dist < 0:
            model = AtomicModel(self.atoms)
            model.add_atom(atom)
            for ind in range(0, len(self.atoms)):
                xyz1 = model.atoms[ind].xyz
                xyz2 = model.atoms[-1].xyz
                r = np.linalg.norm(xyz1 - xyz2)
                if r < dist:
                    dist = r

        if dist > math.fabs(min_dist):
            new_at = deepcopy(atom)
            self.atoms.append(new_at)
            return True
        return False

    def add_atomic_model(self, atomic_model, min_dist=0):
        for at in atomic_model:
            self.add_atom(at, min_dist)

    def edit_atom(self, ind, new_atom):
        if (ind >= 0) and (ind < self.n_atoms()):
            self.atoms[ind] = new_atom

    def add_atoms_property(self, prop, value):
        if self.n_atoms() == len(value):
            for i in range(0, self.n_atoms()):
                self.atoms[i].set_property(prop, value[i][1])

    def add_bond(self, bond):
        self.bonds.append(bond)

    def n_bonds(self):
        return len(self.bonds)

    def modify_atoms_types(self, changes):
        for change in changes:
            let = change[1]
            charge = self.mendeley.get_charge_by_letter(let)

            old_charge = change[0]

            for atom in self.atoms:
                if atom.charge == old_charge:
                    atom.charge = charge
                    atom.let = let

    def n_atoms(self):
        return len(self.atoms)

    def translated_atoms_remove(self):
        new_atoms = []
        for atom in self.atoms:
            if atom.tag != "translated":
                new_atoms.append(atom)
        self.atoms = new_atoms

    def center_mass(self, charge=0):
        """The method returns the center of mass of the molecule."""
        cxyz = np.zeros(3)
        n = 0
        tags = self.get_tags()

        if charge == 0:
            for j in range(0, len(self.atoms)):
                if tags[j] != "translated":
                    m = self.mendeley.Atoms[self.atoms[j].charge].mass
                    cxyz += self.atoms[j].xyz * m
                    n += m
        else:
            for j in range(0, len(self.atoms)):
                if int(self.atoms[j].charge) == int(charge):
                    cxyz += self.atoms[j].xyz
                    n += 1
        if n == 0:
            res = [0, 0, 0]
        else:
            res = cxyz / n
        return np.array(res)

    def rotate_x(self, alpha):
        """The method rotates the AtList on alpha Angle."""
        alpha *= math.pi / 180
        # ox
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].y) * math.cos(alpha) - float(self.atoms[i].z) * math.sin(alpha)
            ynn = float(self.atoms[i].y) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].y = xnn
            self.atoms[i].z = ynn

    def rotate_y(self, alpha):
        """The method rotates the AtList on alpha Angle."""
        alpha *= math.pi / 180
        # oy
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) + float(self.atoms[i].z) * math.sin(alpha)
            ynn = -float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].z) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].z = ynn

    def rotate_z(self, alpha):
        """The method rotates the AtList on alpha Angle."""
        alpha *= math.pi / 180
        # oz
        for i in range(0, len(self.atoms)):
            xnn = float(self.atoms[i].x) * math.cos(alpha) - float(self.atoms[i].y) * math.sin(alpha)
            ynn = float(self.atoms[i].x) * math.sin(alpha) + float(self.atoms[i].y) * math.cos(alpha)
            self.atoms[i].x = xnn
            self.atoms[i].y = ynn

    def rotate(self, alpha, betta, gamma) -> None:
        self.rotate_x(alpha)
        self.rotate_y(betta)
        self.rotate_z(gamma)

    def sub_model(self, inds):
        new_model_atoms = []
        for i in inds:
            new_model_atoms.append(self.atoms[i])
        return AtomicModel(new_model_atoms)

    def projection_to_cylinder(self, atomslist, radius):
        """This method returns projections on cylinder with radius for atom at."""
        row = []
        for at in range(0, len(atomslist)):
            x = float(self.atoms[atomslist[at]].x)
            y = float(self.atoms[atomslist[at]].y)
            z = float(self.atoms[atomslist[at]].z)
            ro = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
            fi = math.atan(x / y)
            row.append([atomslist[at], x * radius / ro, y * radius / ro, z, ro, fi])
        return row

    def indexes_of_atoms_with_charge(self, charge):
        """ IndexesOfAtomsWithCharge """
        indexes = []
        for j in range(0, len(self.atoms)):
            if int(self.atoms[j].charge) == int(charge):
                indexes.append(j)
        return indexes

    def indexes_of_atoms_in_sphere(self, ats, atom, r):
        """Indexes of atoms in the ball of radius R with center on atom 'atom'.
        Args:
            ats: list of indexes;
            atom: index of atom in the center of ball;
            r: sphere radius.
        """
        newatoms = [atom]
        for at in ats:
            if at != atom:
                if self.atom_atom_distance(at, atom) < r:
                    newatoms.append(at)
        return newatoms

    def convert_from_scaled_to_cart(self):
        for atom in self.atoms:
            atom.xyz *= self.lat_const

    def convert_from_cart_to_scaled(self):
        for atom in self.atoms:
            atom.xyz /= self.lat_const

    def convert_from_direct_to_cart(self):
        for atom in self.atoms:
            atom.xyz = np.dot(atom.xyz, self.lat_vectors)

    def convert_from_cart_to_direct(self):
        obr = np.linalg.inv(self.lat_vectors).transpose()
        for atom in self.atoms:
            atom.xyz = obr.dot(atom.xyz)

    def to_cif(self, f_name=""):
        cif_text = "data_GUI4dft_Data\n"
        a, b, c, al, bet, gam = self.cell_params()
        cif_text += "_cell_length_a {0:11.5f}\n".format(a)
        cif_text += "_cell_length_b {0:11.5f}\n".format(b)
        cif_text += "_cell_length_c {0:11.5f}\n".format(c)
        cif_text += "_cell_angle_alpha {0:11.6f}\n".format(al)
        cif_text += "_cell_angle_beta {0:12.6f}\n".format(bet)
        cif_text += "_cell_angle_gamma {0:11.6f}\n".format(gam)
        cif_text += "_symmetry_space_group_name_H-M         'P1     '\n"
        cif_text += "_symmetry_space_group_number    1\n"
        cif_text += "_refine_date  '" + str(date.today()) + "'\n"
        cif_text += "_refine_method 'generated from GUI4dft code'\n"
        cif_text += "_refine_special_details\n;\nStructure converted from\nFile Name "
        cif_text += f_name + "\n"
        cif_text += "Title '" + str(self.formula()) + "'\n;\n\n"
        cif_text += "loop_\n"
        cif_text += "_symmetry_equiv_pos_as_xyz\n"
        cif_text += "   +x,+y,+z\n"
        cif_text += "loop_\n_atom_site_label\n_atom_site_type_symbol\n"
        cif_text += "_atom_site_fract_x\n_atom_site_fract_y\n_atom_site_fract_z\n"

        new_model = deepcopy(self)
        new_model.convert_from_cart_to_direct()
        new_model.sort_atoms_by_type()
        i = 0
        let_prev = ""
        for at in new_model.atoms:
            let = at.let
            if let == let_prev:
                i += 1
            else:
                i = 1
            let_prev = deepcopy(let)
            cif_text +="{0}{1:03d}\t{2}\t{3:10.8f}\t{4:10.8f}\t{5:10.8f}\n".format(let, i, let, at.x, at.y, at.z)

        """
        Fe001	Fe	0.00000000	0.00000000	0.00000000
        Fe002	Fe	0.50000000	0.00000000	0.00000000
        Fe022	Fe	0.00000000	0.33333333	0.33333333
        Fe095	Fe	0.41666666	0.83333333	0.83333333
        Fe096	Fe	0.91666666	0.83333333	0.83333333
        V0001	V	0.50000000	0.66666667	0.00000000
        V0012	V	0.25000000	0.83333333	0.83333333 
        """
        cif_text += "\n\n\n\n#End data_GUI4dft_Data\n\n\n"
        return cif_text

    def min_x(self):
        """Minimum X-coordinate."""
        minx = self.atoms[0].x
        for atom in self.atoms:
            if float(atom.x) < float(minx):
                minx = atom.x
        return float(minx)

    def max_x(self):
        """Maximum X-coordinate."""
        maxx = self.atoms[0].x
        for atom in self.atoms:
            if atom.x > maxx:
                maxx = atom.x
        return maxx

    def size_x(self):
        """The length of the molecule along the X axis."""
        return self.max_x() - self.min_x()

    def min_y(self):
        """Minimum Y-coordinate."""
        miny = self.atoms[0].y

        for atom in self.atoms:
            if float(atom.y) < float(miny):
                miny = atom.y
        return float(miny)

    def max_y(self):
        """Maximum Y-coordinate."""
        maxy = self.atoms[0].y

        for atom in self.atoms:
            if float(atom.y) > float(maxy):
                maxy = atom.y
        return float(maxy)

    def size_y(self):
        """The length of the molecule along the Y axis."""
        return self.max_y() - self.min_y()

    def min_z(self):
        """Minimum Z-coordinate."""
        minz = self.atoms[0].z

        for atom in self.atoms:
            if float(atom.z) < float(minz):
                minz = atom.z
        return float(minz)

    def max_z(self):
        """Maximum Z-coordinate."""
        maxz = self.atoms[0].z

        for atom in self.atoms:
            if float(atom.z) > float(maxz):
                maxz = atom.z
        return float(maxz)

    def size_z(self):
        """The length of the molecule along the Z axis."""
        return self.max_z() - self.min_z()

    def set_cluster(self, cluster, k):
        for atom in cluster:
            self.atoms[atom].cluster = k

    def sort_atoms_by_type(self):
        for i in range(0, self.n_atoms()):
            for j in range(0, self.n_atoms() - i - 1):
                if self.atoms[j].charge > self.atoms[j + 1].charge:
                    atom = self.atoms[j]
                    self.atoms[j] = self.atoms[j + 1]
                    self.atoms[j + 1] = atom

    def angle_to_center_of_atoms(self, atomslist):
        """The method returns the Angle To Center Of atoms_from_fdf list atomslist in the molecule."""
        angle = 0

        for at in range(0, len(atomslist)):
            x = self.atoms[atomslist[at]].x
            y = self.atoms[atomslist[at]].y
            fi = math.atan(x / y)
            angle += fi
        angle /= len(atomslist)
        return angle

    def atom_atom_distance(self, at1, at2):
        """ atom_atom_distance
        All atoms MUST be in the Cell!!!"""
        pos1 = self.atoms[at1].xyz
        pos2 = self.atoms[at2].xyz
        ro = self.point_point_distance(pos1, pos2)
        return ro

    def point_point_distance(self, pos1, pos2):
        delta_pos = pos2 - pos1
        values = [-1, 0, 1]
        ros = [[[norm(delta_pos + i * self.lat_vectors[0] + j * self.lat_vectors[1] + k * self.lat_vectors[2])
                 for i in values] for j in values] for k in values]
        return np.array(ros).min()

    def move_object_to_cell(self, arr, a_inv):
        for at in arr:
            pos = at.xyz
            b = pos.transpose()
            total = a_inv.dot(b)
            pos -= math.trunc(total[0] + 0.5) * self.lat_vectors[0] + math.trunc(total[1] + 0.5) * self.lat_vectors[1] +\
                   math.trunc(total[2] + 0.5) * self.lat_vectors[2]
            at.xyz = pos

    def neighbors(self, atom, col, charge):
        """Look for number of neighbors of atom "atom" with a charge "charge"."""
        neighbor = []
        for at in range(0, len(self.atoms)):
            if (at != atom) and (int(self.atoms[at].charge) == int(charge)):
                r = self.atom_atom_distance(atom, at)
                neighbor.append([at, r])
        fl = 1
        while fl == 1:
            fl = 0
            for i in range(len(neighbor) - 1, 0, -1):
                if neighbor[i - 1][1] > neighbor[i][1]:
                    at = copy.deepcopy(neighbor[i])
                    neighbor[i] = copy.deepcopy(neighbor[i - 1])
                    neighbor[i - 1] = copy.deepcopy(at)
                    fl = 1
        neighbo = [neighbor[0][0]]
        for i in range(1, col):
            neighbo.append(neighbor[i][0])
        return neighbo

    def find_clusters(self):
        clusters = []  # list of lists
        # inds = range(0, len(self.atoms))  # list of indices of atoms in model
        bonds = deepcopy(self.bonds)
        while len(bonds) > 0:
            cluster = [bonds[0][0], bonds[0][1]]
            bonds.remove(bonds[0])
            len_cluster = 2
            len_cluster_old = 0
            while (len_cluster_old != len_cluster) and (len(bonds) > 0):
                for ind in cluster:
                    for bond in bonds:
                        if (bond[0] == ind) or (bond[1] == ind):
                            if bond[0] not in cluster:
                                cluster.append(bond[0])
                            if bond[1] not in cluster:
                                cluster.append(bond[1])
                            bonds.remove(bond)  # remove bond from list
                len_cluster_old = len_cluster  # update length of cluster
                len_cluster = len(cluster)
            clusters.append(cluster)
        return clusters

    def find_clusters_by_tag(self):
        clusters = []
        tags = np.array(self.get_tags(), dtype=int)
        size = max(tags)
        for i in range(0, size):
            clusters.append([])
        for i in range(0, len(self.atoms)):
            clusters[tags[i] - 1].append(i)
        return clusters

    def find_bonds_exact(self):
        """The method returns list of bonds of the molecule."""
        if self.bonds_per:
            return self.bonds_per
        for i in range(0, len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                length = round(self.atom_atom_distance(i, j), 4)
                t1 = int(self.atoms[i].charge)
                t2 = int(self.atoms[j].charge)
                if (length > 1e-4) and (length < 1.2 * self.mendeley.Bonds[t1][t2]):
                    self.bonds_per.append([t1, t2, length, self.atoms[i].let, i, self.atoms[j].let, j])
        return self.bonds_per

    def find_bonds_fast(self):
        """The method returns list of bonds of the molecule."""
        if not (self.dynamic_bonds or len(self.bonds) == 0):
            return

        self.bonds = []
        for i in range(0, len(self.atoms)):
            for j in range(i + 1, len(self.atoms)):
                r = norm(self.atoms[i].xyz - self.atoms[j].xyz)
                r_tab = self.mendeley.Bonds[self.atoms[i].charge][self.atoms[j].charge]
                if (r > 1e-4) and (r < 1.2 * r_tab):
                    self.bonds.append([i, j])
        return self.bonds

    def get_bonds_for_charges(self, c1, c2):
        """The bonds of atoms with charges"""
        bonds = self.find_bonds_exact()
        bonds_len = []
        bonds_ok = []
        for bond in bonds:
            if ((c1 == 0) or (c2 == 0)) or ((c1 == bond[0]) and (c2 == bond[1])) or (
                    (c1 == bond[1]) and (c2 == bond[2])):
                bonds_ok.append(bond)
                bonds_len.append(bond[2])
        bonds_mean = round(np.average(bonds_len), 5)
        bonds_err = round((max(bonds_len) - min(bonds_len)) / 2.0, 5)
        return bonds_ok, bonds_mean, bonds_err

    def delta(self, molecula):
        """ maximum distance from atoms in self to the atoms in the newMolecula"""
        delta_molecula1 = 0
        r1 = norm(self.lat_vector1) + norm(self.lat_vector2) + norm(self.lat_vector3)
        for at2 in molecula.atoms:
            model = AtomicModel(self.atoms)
            model.add_atom(at2)
            for ind in range(0, len(self.atoms)):
                r = model.atom_atom_distance(ind, len(model.atoms) - 1)
                if r < r1:
                    r1 = r
            if r1 > delta_molecula1:
                delta_molecula1 = r1
        return delta_molecula1

    def move_array(self, arr, dr):
        for i in range(len(arr)):
            arr[i].xyz -= dr

    def go_to_positive_array(self, arr):
        for i in range(len(arr)):
            arr[i].x = self.minus0(arr[i].x)
            arr[i].y = self.minus0(arr[i].y)
            arr[i].z = self.minus0(arr[i].z)

    def go_to_positive_x_array_translate(self, arr):
        if np.linalg.norm(self.lat_vectors[0]) >= 500:
            return
        for i in range(len(arr)):
            if arr[i].x < 0:
                arr[i].xyz += self.lat_vectors[0]

    def go_to_positive_y_array_translate(self, arr):
        if np.linalg.norm(self.lat_vectors[1]) >= 500:
            return
        for i in range(len(arr)):
            if arr[i].y < 0:
                arr[i].xyz += self.lat_vectors[1]

    def go_to_positive_z_array_translate(self, arr):
        if np.linalg.norm(self.lat_vectors[2]) >= 500:
            return
        for i in range(len(arr)):
            if arr[i].z < 0:
                arr[i].xyz += self.lat_vectors[2]

    def go_to_positive_array_translate(self, arr):
        self.go_to_positive_x_array_translate(arr)
        self.go_to_positive_y_array_translate(arr)
        self.go_to_positive_z_array_translate(arr)

    def minus0(self, fl):
        return 0 if fl < 0 else fl

    def grow(self):
        """The model is translated in three dimensions and becomes 27 times larger."""
        new_at_list = deepcopy(self.atoms)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    if abs(i) + abs(j) + abs(k) != 0:
                        vect = i * self.lat_vector1 + j * self.lat_vector2 + k * self.lat_vector3
                        copy_of_model = AtomicModel(self.atoms)
                        copy_of_model.move(vect)
                        for atom in copy_of_model.atoms:
                            new_at_list.append(atom)
        new_model = AtomicModel(new_at_list)
        new_model.set_lat_vectors(3 * self.lat_vectors)
        return new_model

    def grow_x(self, n: int = 1):
        """Translate model in X direction.
        n: number of translations """
        new_at_list = deepcopy(self.atoms)
        for i in range(n):
            copy_of_model = AtomicModel(self.atoms)
            copy_of_model.move(((1 + i) * self.lat_vector1))
            for atom in copy_of_model.atoms:
                new_at_list.append(atom)
        new_model = AtomicModel(new_at_list)
        new_lat_vectors = deepcopy(self.lat_vectors)
        new_lat_vectors[0] = (1 + n) * self.lat_vectors[0]
        new_model.set_lat_vectors(new_lat_vectors)
        return new_model

    def grow_y(self, n: int = 1):
        """Translate model in Y direction.
        n: number of translations"""
        new_at_list = deepcopy(self.atoms)
        for i in range(n):
            copy_of_model = AtomicModel(self.atoms)
            copy_of_model.move(((1 + i) * self.lat_vector2))
            for atom in copy_of_model.atoms:
                new_at_list.append(atom)
        new_model = AtomicModel(new_at_list)
        new_lat_vectors = deepcopy(self.lat_vectors)
        new_lat_vectors[1] = (1 + n) * self.lat_vectors[1]
        new_model.set_lat_vectors(new_lat_vectors)
        return new_model

    def grow_z(self, n: int = 1):
        """Translate model in Z direction.
        n: number of translations"""
        new_at_list = deepcopy(self.atoms)
        for i in range(n):
            copy_of_model = AtomicModel(self.atoms)
            copy_of_model.move(((1 + i) * self.lat_vector3))
            for atom in copy_of_model.atoms:
                new_at_list.append(atom)
        new_model = AtomicModel(new_at_list)
        new_lat_vectors = deepcopy(self.lat_vectors)
        new_lat_vectors[2] = (1 + n) * self.lat_vectors[2]
        new_model.set_lat_vectors(new_lat_vectors)
        return new_model

    def types_of_atoms(self):
        elements = np.zeros(200)
        for atom in self.atoms:
            elements[atom.charge] += 1
        types = []
        for i in range(0, 200):
            if elements[i] > 0:
                types.append([i, elements[i]])
        return types

    def get_charge_to_type_array(self):
        per_tab = self.mendeley
        text = ""
        types = self.types_of_atoms()
        charge_to_type = np.zeros(200, dtype=int)
        for i in range(0, len(types)):
            text += ' ' + str(per_tab.get_let(int(types[i][0])))
            charge_to_type[int(types[i][0])] = i + 1
        return charge_to_type, text

    def formula(self):
        text = ""
        charges = self.types_of_atoms()
        for charge in charges:
            ind = self.indexes_of_atoms_with_charge(charge[0])
            let = self.mendeley.get_let(self.atoms[ind[0]].charge)
            text += let + str(len(ind))
        return text

    def move_atoms_to_zero(self):
        cm = self.center_mass()
        self.move(cm)

    def move_atoms_to_center(self):
        cm = self.center_mass()
        cc = 0.5 * (self.lat_vectors[0] + self.lat_vectors[1] + self.lat_vectors[2])
        self.move(cc - cm)

    def move_atoms_to_cell(self):
        a_inv = inv(self.lat_vectors)
        self.move_object_to_cell(self.atoms, a_inv)

    def go_to_positive_coordinates_translate(self):
        self.go_to_positive_array_translate(self.atoms)

    def go_to_positive_coordinates(self):
        d_vec = np.array([self.min_x(), self.min_y(), self.min_z()])
        self.move_array(self.atoms, d_vec)
        self.go_to_positive_array(self.atoms)

    def coords_for_export(self, coord_style, units="Ang", is_freez=False):
        data = ""
        types = self.types_of_atoms()
        if coord_style == "Cartesian":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                data += self.xyz_string(i, units) + str1 + "\n"

        if coord_style == "Fractional":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                data += self.xyz_string(i) + str1 + "\n"

        if coord_style == "POSCAR":
            for i in range(0, len(self.atoms)):
                fr = ""
                if is_freez:
                    if self.atoms[i].fragment1:
                        fr = " F F F"
                    else:
                        fr = " T T T"
                data += ' ' + self.xyz_string(i) + fr + "\n"

        if coord_style == "Zmatrix Cartesian":
            for i in range(0, len(self.atoms)):
                str1 = ' '
                for j in range(0, len(types)):
                    if types[j][0] == self.atoms[i].charge:
                        str1 = ' ' + str(j + 1)
                str2 = '    ' + self.xyz_string(i)
                if self.atoms[i].selected:
                    str3 = '      0  0  0'
                else:
                    str3 = '      1  1  1'
                data += str1 + str2 + str3 + "\n"

        if coord_style == "FireflyINP":
            for i in range(0, len(self.atoms)):
                str1 = ' ' + str(self.atoms[i].let) + '   ' + str(self.atoms[i].charge) + '.0  '
                str2 = '    ' + self.xyz_string(i)
                data += str1 + str2 + "\n"
            data += ' $END'
        return data

    def coords_to_ang(self):
        for at in self.atoms:
            at.xyz /= 0.52917720859

    def coords_to_bohr(self):
        for at in self.atoms:
            at.xyz *= 0.52917720859

    def xyz_string(self, i, units="Ang"):
        mult = 1.0
        if units == "Bohr":
            mult = 1.0 / 0.52917720859
        sx = helpers.float_to_string(self.atoms[i].x * mult)
        sy = helpers.float_to_string(self.atoms[i].y * mult)
        sz = helpers.float_to_string(self.atoms[i].z * mult)
        str2 = '  ' + sx + '  ' + sy + '  ' + sz
        return str2

    # Best fit a circle to these points
    def err_cylinder(self, par):
        w, v, r = par[0], par[1], par[2]
        pts = [np.linalg.norm([x - w, y - v]) - r for x, y in zip(self.x, self.y)]
        return (np.array(pts) ** 2).sum()

    def fit_with_cylinder(self):
        positions = self.get_positions()
        self.x = positions[:, 0]
        self.y = positions[:, 1]

        # Choose the inital center of fit circle as the CM
        xm = self.x.mean()
        ym = self.y.mean()

        # Choose the inital radius as the average distance to the CM
        cm = np.array([xm, ym]).reshape(1, 2)
        rm = cdist(cm, np.array([self.x, self.y]).T).mean()

        xf, yf, rf = scipy.optimize.fmin(self.err_cylinder, [xm, ym, rm])
        return xf, yf, rf
