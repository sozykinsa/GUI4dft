# -*- coding: utf-8 -*-
from typing import List
import copy
import os
import math
import numpy as np
import numpy.linalg

from core_atomistic.periodic_table import TPeriodTable
from core_atomistic import helpers
from src_critplot.models.cp import CriticalPoint
from src_critplot.models.cp_model import AtomicModelCP


class Critic2ModelCP(AtomicModelCP):
    def __init__(self, filename):
        """
        * Complete CP list, bcp and rcp connectivity table
        # (cp(end)+lvec connected to bcp/rcp)
        #cp  ncp   typ        position (cryst. coords.)            end1 (lvec)      end2 (lvec)
        1      1    n   0.41201875    0.19237040    0.32843532
        """
        super().__init__()
        self.cps: List[CriticalPoint] = []
        self.model_type = "critic2"

        period_table = TPeriodTable()
        if os.path.exists(filename) and filename.endswith("cro"):
            box_ang = helpers.from_file_property(filename, "Lattice parameters (ang):", 1, 'string').split()
            box_ang = np.array(helpers.list_str_to_float(box_ang))
            box_deg = helpers.from_file_property(filename, "Lattice angles (degrees):", 1, 'string').split()
            box_deg = np.array(helpers.list_str_to_float(box_deg))

            lat_vectors = helpers.lat_vectors_from_params(box_ang[0], box_ang[1], box_ang[2],
                                                          math.radians(box_deg[0]),
                                                          math.radians(box_deg[1]),
                                                          math.radians(box_deg[2]))

            self.set_lat_vectors([lat_vectors[0], lat_vectors[1], lat_vectors[2]])

            crit_points = self.get_critical_points_info(filename)

            f = open(filename)
            str1 = f.readline()
            while str1.find("* Complete CP list, bcp and rcp connectivity table") < 0:
                str1 = f.readline()

            f.readline()
            f.readline()
            str1 = f.readline()
            while len(str1) > 5:
                str1 = str1.replace("(", "")
                str1 = str1.replace(")", "")
                data = str1.split()
                title_number = data[0]
                if data[0] != data[1]:
                    title_number += "(" + data[1] + ")"
                number = int(data[1]) - 1
                """
                #cp  ncp   typ        position (cryst. coords.)            end1 (lvec)      end2 (lvec)
                1      1    n   0.67394965    0.51875056    0.41176494  
                115    37   b   0.61261657    0.49723994    0.38722411  101  ( 0  0  0 )  76  ( 0  0  0 )
                347    108  r   0.51856128    0.51875294    0.44655967  359  ( 0  0  0 ) 359  ( 0  0  0 )
                362    116  c   0.51852061    0.51875000    0.63729618
                """
                xyz = np.array([data[3], data[4], data[5]], dtype=float)
                crit_info = crit_points[number]
                if crit_info[3] == "nucleus":
                    let = crit_info[8].replace("_", "")
                    cp_type = "(3,-3)"
                    title = let + title_number
                    new_cp = self.init_crit_point(crit_info, let, cp_type, title, xyz)
                    charge = period_table.get_charge_by_letter(let)
                    self.add_atom_with_data(xyz, charge)
                    self.add_critical_point(new_cp)

                if crit_info[3] == "nnattr":
                    let = "attr"
                    cp_type = "(3,-3)"
                    title = let + title_number
                    new_cp = self.init_crit_point(crit_info, let, cp_type, title, xyz)
                    self.add_critical_point(new_cp)

                if crit_info[3] == "bond":
                    let = "xb"
                    cp_type = "(3,-1)"
                    title = let + title_number
                    new_cp = self.init_crit_point(crit_info, let, cp_type, title, xyz)
                    self.add_atoms_to_cp(data, new_cp)
                    self.add_critical_point(new_cp)

                if crit_info[3] == "ring":
                    let = "xr"
                    cp_type = "(3,+1)"
                    title = let + title_number
                    new_cp = self.init_crit_point(crit_info, let, cp_type, title, xyz)
                    self.add_atoms_to_cp(data, new_cp)
                    self.add_critical_point(new_cp)

                if crit_info[3] == "cage":
                    let = "xc"
                    cp_type = "(3,+3)"
                    title = let + title_number
                    new_cp = self.init_crit_point(crit_info, let, cp_type, title, xyz)
                    self.add_atoms_to_cp(data, new_cp)
                    self.add_critical_point(new_cp)
                str1 = f.readline()

            f.readline()
            f.close()
            self.convert_from_direct_to_cart()

            for cp in self.cps:
                ind1 = cp.get_property("atom1")
                ind2 = cp.get_property("atom2")
                if (ind1 is not None) and (ind2 is not None):
                    trans1 = np.array(cp.get_property("atom1_translation"))
                    trans2 = np.array(cp.get_property("atom2_translation"))
                    p1 = CriticalPoint([self.cps[ind1 - 1].xyz + trans1, "xz", "bp"])
                    p2 = CriticalPoint([cp.xyz, "xz", "bp"])
                    p3 = CriticalPoint([self.cps[ind2 - 1].xyz + trans2, "xz", "bp"])
                    if (np.linalg.norm(trans1) > 0) and (ind1 < self.n_atoms()):
                        atom = copy.deepcopy(self.atoms[ind1 - 1])
                        atom.xyz += trans1
                        atom.tag = "translated"
                        self.add_atom(atom, min_dist=-0.01)
                    if (np.linalg.norm(trans2) > 0) and (ind2 < self.n_atoms()):
                        atom = copy.deepcopy(self.atoms[ind2 - 1])
                        atom.xyz += trans2
                        atom.tag = "translated"
                        self.add_atom(atom, min_dist=-0.01)
                    self.add_bond_path_point([p2, p1])
                    self.add_bond_path_point([p2, p3])
                    atom_to_atom = self.cps[ind1 - 1].let + str(ind1) + "-" + self.cps[ind2 - 1].let + str(ind2)
                    cp.set_property("atom_to_atom", atom_to_atom)
                    bond_len = np.linalg.norm(self.cps[ind2 - 1].xyz + trans2 - self.cps[ind1 - 1].xyz - trans1)
                    cp.set_property("cp_bp_len", bond_len)
            self.bond_path_points_optimize()

    @staticmethod
    def get_critical_points_info(filename: str):
        f = open(filename)
        str1 = f.readline()
        while str1.find("* Critical point list, final report (non-equivalent cps)") < 0:
            str1 = f.readline()
        f.readline()
        f.readline()
        f.readline()
        str1 = f.readline()
        crit_points = []

        while len(str1) > 5:
            """
            ncp   pg  type   CPname         position (cryst. coords.)       mult  name            f             |grad|           lap
            1    C1  (3,-3) nucleus   0.41201875   0.19237040   0.32843532    1     H_      4.02547716E+00  0.00000000E+00 -1.04730465E+02
            """
            data1 = str1.split(")")
            data2 = data1[0].split("(")
            data = data1[1].split()
            row = data2[0].split()
            row.append(data2[1])
            row += data
            crit_points.append(row)
            str1 = f.readline()

        while (str1.find("Additional properties at the critical points") < 0) and (len(str1) > 0):
            str1 = f.readline()
        str1 = f.readline()
        point = 0

        while str1.find("+ Critical point no.") >= 0:
            text = ""
            str1 = f.readline()
            while not str1.startswith("+ "):
                if len(str1) > 0:
                    text += str1
                str1 = f.readline()
            crit_points[point].append(text)
            point += 1
        f.close()
        return crit_points

    def add_atoms_to_cp(self, data, cp):
        if len(data) > 6:
            atom1 = int(data[6])
            atom2 = int(data[10])
            if (atom1 <= len(self.atoms)) and (atom2 <= len(self.atoms)):
                cp.set_property("atom1", atom1)
                cp.set_property("atom2", atom2)
                translation1 = int(data[7]) * self.lat_vector1 + int(data[8]) * self.lat_vector2 + \
                               int(data[9]) * self.lat_vector3
                translation2 = int(data[11]) * self.lat_vector1 + int(data[12]) * self.lat_vector2 + \
                               int(data[13]) * self.lat_vector3
                cp.set_property("atom1_translation", translation1)
                cp.set_property("atom2_translation", translation2)
            else:
                print("strange critical point: ", cp.to_string(), atom1, atom2)

    @staticmethod
    def init_crit_point(crit_info, let, cp_type, title, xyz):
        new_cp = CriticalPoint([xyz, let, cp_type])
        new_cp.set_property("title", title)
        new_cp.set_property("rho", crit_info[9])
        new_cp.set_property("grad", crit_info[10])
        new_cp.set_property("lap", crit_info[11])
        new_cp.set_property("text", crit_info[12])
        return new_cp

    def parse_bondpaths(self, filename: str) -> None:
        """Import bond paths from *.xyz file.
        filename - name of *.xyz file
        """
        if os.path.exists(filename):
            f = open(filename)
            number_of_atoms = int(math.fabs(int(f.readline())))
            new_model = AtomicModelCP.atoms_from_xyz_structure(number_of_atoms, f, is_allow_charge_incorrect=True)
            self.delete_all_bond_paths()

            xz_points = []

            for atom in new_model.atoms:
                if atom.let.lower() == "xz":
                    xz_points.append(atom)

            points = []

            for i in range(0, len(xz_points)):
                if len(points) == 0:
                    points.append(xz_points[i])
                else:
                    d = math.dist(points[-1].xyz, xz_points[i].xyz)
                    if d < 0.09:
                        points.append(xz_points[i])
                    else:
                        self.add_bond_path_point(points)
                        points = [xz_points[i]]

            if len(points) > 0:
                self.add_bond_path_point(points)

            self.bond_path_points_optimize()
