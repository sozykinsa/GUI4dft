# -*- coding: utf-8 -*-
from typing import List

import math
import numpy as np
from copy import deepcopy
from numpy.linalg import inv

from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from core_atomistic import helpers

from src_critplot.models.cp import CriticalPoint


class AtomicModelCP(AtomicModel):
    def __init__(self, new_atoms: List[Atom] = []):
        super().__init__(new_atoms)
        self.cps: List[CriticalPoint] = []

    def n_cps(self):
        return len(self.cps)

    def n_bcp(self):
        n = 0
        for cp in self.cps:
            if cp.cp_type == "(3,-1)":
                n += 1
        return n

    def n_ccp(self):
        n = 0
        for cp in self.cps:
            if cp.cp_type == "(3,+3)":
                n += 1
        return n

    def n_rcp(self):
        n = 0
        for cp in self.cps:
            if cp.cp_type == "(3,+1)":
                n += 1
        return n

    def n_ncp(self):
        n = 0
        for cp in self.cps:
            if cp.cp_type == "(3,-3)":
                n += 1
        return n

    def poincare_hoff_rule(self):
        rule_text = str(self.n_ncp()) + "(3,-3) - " + str(self.n_bcp()) + "(3,-1) + " + str(self.n_rcp()) + \
                    "(3,+1) - " + str(self.n_ccp()) + "(3,+3)"
        rule_int = self.n_ncp() - self.n_bcp() + self.n_rcp() - self.n_ccp()
        return rule_text, rule_int

    def equivalent_titles(self, cp):
        atom1 = cp.get_property("atom1")
        atom2 = cp.get_property("atom2")
        if (atom1 is not None) and (atom2 is not None):
            let1 = self.atoms[atom1 - 1].let
            let2 = self.atoms[atom2 - 1].let
            title1 = let1 + "-" + let2
            title2 = let2 + "-" + let1
            return title1, title2
        else:
            return None, None

    def bond_path_points_optimize(self) -> None:
        """Remove redundant points from all bond paths."""
        for cp in self.cps:
            if cp.let == "xb":
                bond1 = cp.bonds.get("bond1")
                bond2 = cp.bonds.get("bond2")
                if (bond1 is not None) and (bond2 is not None):
                    self.critical_path_simplifier("bond1", cp)
                    self.critical_path_simplifier("bond2", cp)

    @staticmethod
    def critical_path_simplifier(b, cp) -> None:
        """Remove redundant points on bond path (they lie on the same straight line).
        b: name of bond path (bond1 or bond2)
        cp: critical point
        """
        bond = deepcopy(cp.bonds.get(b))
        if bond is None:
            return

        if len(bond) > 2:
            k = 3
            i = 0
            while (i < len(bond)) and (len(bond) > 1):
                for j in range(1, k):
                    if i + 1 < len(bond):
                        bond.pop(i + 1)
                for j in range(k):
                    if i + 2 < len(bond):
                        bond.pop(i + 2)
                i += 2
        cp.bonds[b + "opt"] = bond

    def get_cp_types(self):
        cp_types = ["All"]
        for cp in self.cps:
            atom1 = cp.get_property("atom1")
            atom2 = cp.get_property("atom2")
            if not (atom1 is None) and not (atom2 is None) and cp.cp_type == "(3,-1)" and cp.is_visible:
                if (atom1 > 0) and (atom1 <= self.n_atoms()) and (atom2 > 0) and (atom2 <= self.n_atoms()):
                    atom1 = self.atoms[atom1 - 1].let
                    atom2 = self.atoms[atom2 - 1].let
                    str1 = atom1 + "-" + atom2
                    str2 = atom2 + "-" + atom1
                    if (str1 not in cp_types) and (str2 not in cp_types):
                        cp_types.append(str1)
        return cp_types

    def move(self, dl: np.ndarray):
        """Move model by the vector."""
        super().move(dl)
        for cp in self.cps:
            self.move_cp(cp, dl)
        return self.atoms

    def move_cp(self, cp, dl):
        cp.xyz += dl
        self.move_bond_path(dl, cp.bonds.get("bond1"))
        self.move_bond_path(dl, cp.bonds.get("bond2"))
        self.move_bond_path(dl, cp.bonds.get("bond1opt"))
        self.move_bond_path(dl, cp.bonds.get("bond2opt"))

    def translate_cp(self, selected_cp, step_x, step_y, step_z):
        cp = self.cps[selected_cp]
        self.move_cp(cp, step_x * self.lat_vector1 + step_y * self.lat_vector2 + step_z * self.lat_vector3)

    @staticmethod
    def move_bond_path(dl, bond):
        if bond:
            for bp in bond:
                bp.xyz += dl

    def go_to_positive_coordinates_translate(self):
        self.translated_atoms_remove()
        self.go_to_positive_array_translate(self.atoms)
        self.find_bonds_fast()
        self.go_to_positive_array_translate(self.cps)
        self.bond_path_opt_update()

    def bond_path_opt_update(self):
        for i in range(len(self.cps)):
            if self.cps[i].let == "xb":
                if "bond1" not in self.cps[i].bonds:
                    print("strange bcp: ", self.cps[i])
                else:
                    self.cps[i].bonds.pop("bond1")
                    self.cps[i].bonds.pop("bond2")
                    self.cps[i].bonds.pop("bond1opt")
                    self.cps[i].bonds.pop("bond2opt")

                    ind1 = self.cps[i].get_property("atom1")
                    ind2 = self.cps[i].get_property("atom2")
                    if (ind1 <= len(self.atoms)) and (ind2 <= len(self.atoms)):
                        p1 = CriticalPoint([self.atoms[ind1 - 1].xyz, "xz", "bp"])
                        p2 = CriticalPoint([self.cps[i].xyz, "xz", "bp"])
                        p3 = CriticalPoint([self.atoms[ind2 - 1].xyz, "xz", "bp"])

                        self.add_bond_path_point([p2, p1])
                        self.add_bond_path_point([p2, p3])
        self.bond_path_points_optimize()

    def move_atoms_to_cell(self):
        a_inv = inv(self.lat_vectors)
        self.move_object_to_cell(self.atoms, a_inv)
        self.move_object_to_cell(self.cps, a_inv)
        for cp in self.cps:
            bond1 = cp.bonds.get("bond1")
            bond2 = cp.bonds.get("bond2")
            if bond1 is not None and bond2 is not None:
                bond1opt = cp.bonds.get("bond1opt")
                bond2opt = cp.bonds.get("bond2opt")
                self.move_object_to_cell(bond1, a_inv)
                self.move_object_to_cell(bond2, a_inv)
                self.move_object_to_cell(bond1opt, a_inv)
                self.move_object_to_cell(bond2opt, a_inv)

    def go_to_positive_coordinates(self):
        dr = np.array([self.minX(), self.minY(), self.minZ()])
        self.go_to_positive_array(self.atoms, dr)
        self.go_to_positive_array(self.cps, dr)
        for cp in self.cps:
            bond1 = cp.bonds.get("bond1")
            bond2 = cp.bonds.get("bond2")
            if bond1 is not None and bond2 is not None:
                bond1opt = cp.bonds.get("bond1opt")
                bond2opt = cp.bonds.get("bond2opt")
                self.go_to_positive_array(bond1, dr)
                self.go_to_positive_array(bond2, dr)
                self.go_to_positive_array(bond1opt, dr)
                self.go_to_positive_array(bond2opt, dr)

    def convert_from_direct_to_cart(self):
        super().convert_from_direct_to_cart()
        for cp in self.cps:
            cp.xyz = np.dot(cp.xyz, self.lat_vectors)

    def add_critical_point(self, cp):
        self.cps.append(deepcopy(cp))

    def delete_all_bond_paths(self):
        for cp in self.cps:
            cp.bonds["bond1"] = None
            cp.bonds["bond2"] = None

    def add_bond_path_point(self, points):
        for cp in self.cps:
            distance = math.dist(cp.xyz, points[0].xyz)
            if distance < 1e-4:
                if cp.bonds.get("bond1") is None:
                    cp.bonds["bond1"] = deepcopy(points)
                else:
                    cp.bonds["bond2"] = deepcopy(points)

    @staticmethod
    def atoms_of_bond_path(cp):
        ind1 = cp.get_property("atom1")
        ind2 = cp.get_property("atom2")
        return ind1, ind2

    def create_csv_file_cp(self, cp_list, show_bcp, show_ccp, show_rcp, show_ncp, show_nnatr, delimiter: str = ";"):
        text = ""

        if show_bcp:
            cp_type = "xb"
            data, title = self.csv_for_cp_type(cp_list, cp_type, delimiter)
            text += title + "\n" + data + "\n"

        if show_ccp:
            cp_type = "xc"
            data, title = self.csv_for_cp_type(cp_list, cp_type, delimiter)
            text += title + "\n" + data + "\n"

        if show_rcp:
            cp_type = "xr"
            data, title = self.csv_for_cp_type(cp_list, cp_type, delimiter)
            text += title + "\n" + data + "\n"

        if show_nnatr:
            cp_type = "nn"
            data, title = self.csv_for_cp_type(cp_list, cp_type, delimiter)
            text += title + "\n" + data + "\n"

        if show_ncp:
            cp_type = "nucleus"
            data, title = self.csv_for_cp_type(cp_list, cp_type, delimiter)
            text += title + "\n" + data + "\n"
        return text

    def csv_for_cp_type(self, cp_list, cp_type, delimiter):
        data = ""
        title = ""
        # print(cp_type)
        for ind in cp_list:
            cp = self.cps[ind - 1]
            if (cp.let == cp_type) or (cp_type == "nucleus") and (cp.let not in ["xb", "xc", "xr", "nn"]):
                title = "CP" + delimiter
                data += str(ind) + delimiter
                prop_list = ["rho", "grad", "lap"]
                for prop in prop_list:
                    title += prop + delimiter
                    data += cp.get_property(prop) + delimiter

                title += "atoms" + delimiter + "dist" + delimiter
                atom_to_atom = cp.get_property("atom_to_atom")
                if atom_to_atom is None:
                    data += '" ' + "-" + ' "' + delimiter + '" ' + "-" + ' "' + delimiter
                else:
                    data += atom_to_atom + delimiter
                    cp_bp_len = cp.get_property("cp_bp_len")
                    dist_line = round(cp_bp_len, 4)
                    data += '" ' + str(dist_line) + ' "' + delimiter
                data_list = cp.get_property("text")
                if data_list:
                    data = self.text_field_to_csv(data, data_list, delimiter, title)
                    title = self.text_field_to_csv_title(data_list, delimiter, title)
        return data, title

    @staticmethod
    def text_field_to_csv(data, data_list, delimiter, title):
        data_list = data_list.split("\n")
        i = 0
        while i < len(data_list):
            if (data_list[i].find("Hessian") < 0) and (len(data_list[i]) > 0):
                col_data = data_list[i].split(":")[1].split()
                for k in range(len(col_data)):
                    data += '"' + col_data[k] + '"' + delimiter
                i += 1
            else:
                i += 4
        data += '\n'
        return data

    @staticmethod
    def text_field_to_csv_title(data_list, delimiter, title):
        data_list = data_list.split("\n")
        i = 0
        while i < len(data_list):
            if (data_list[i].find("Hessian") < 0) and (len(data_list[i]) > 0):
                col_title = helpers.spacedel(data_list[i].split(":")[0])
                col_data = data_list[i].split(":")[1].split()
                for k in range(len(col_data)):
                    title += '"' + col_title
                    if len(col_data) > 1:
                        title += "_" + str(k + 1)
                    title += '"' + delimiter
                i += 1
            else:
                i += 4
        return title

    def create_critic2_xyz(self, bcp, bcp_seleсted, is_with_selected):
        if is_with_selected:
            text = self.model_to_critic_xyz_file(bcp_seleсted)
        else:
            for b in bcp_seleсted:
                for cp in bcp:
                    if cp.to_string() == b.to_string():
                        bcp.remove(cp)
            text = self.model_to_critic_xyz_file(bcp)
        return text

    def model_to_critic_xyz_file(self, cps):
        """Returns data for *.xyz file with CP and BCP.
        model
        cps
        """
        text = ""

        n_atoms = self.n_atoms()
        for i in range(0, n_atoms):
            text += self.atoms[i].to_string() + "\n"

        n_cp = len(cps)
        for cp in cps:
            text += cp.to_string() + "\n"

        n_bcp = 0
        for cp in cps:
            bond1 = cp.bonds.get("bond1")
            bond2 = cp.bonds.get("bond2")

            for i in range(0, len(bond1)):
                n_bcp += 1
                text += bond1[i].to_string() + "\n"

            for i in range(0, len(bond2)):
                n_bcp += 1
                text += bond2[i].to_string() + "\n"

        header = "   " + str(n_atoms + n_cp + n_bcp) + "\n\n"
        return header + text

    def create_cri_file(self, cp_list, extra_points, is_form_bp, text_prop):
        """Create input file for ... caclulation with Critic2."""
        sys_coord = np.array([self.lat_vector1, self.lat_vector2, self.lat_vector3])
        obr = np.linalg.inv(sys_coord).transpose()
        text = ""
        te = ""
        lines = ""
        textl = "crystal model.BADER.cube\n"
        textl += "WRITE model.xyz\n"
        textl += "load model.BADER.cube\n"
        textl += "load model.VT.DN.cube\n"
        textl += "load model.VT.UP.cube\n"
        textl += 'LOAD AS "-$2-$3"\n'
        textl += 'LOAD AS LAP 1\n'
        textl += "REFERENCE 1\n"

        for ind in cp_list:
            cp = self.cps[ind]
            text += "Bond Critical Point: " + str(ind) + "  :  "
            ind1 = cp.get_property("atom1")
            ind2 = cp.get_property("atom2")
            atom1 = self.atoms[ind1].let + str(ind1 + 1)
            atom2 = self.atoms[ind2].let + str(ind2 + 1)
            title = atom1 + "-" + atom2
            text += title + "\n"

            if is_form_bp:
                """ bond path """
                bond1 = cp.get_property("bond1")
                bond2 = cp.get_property("bond2")

                path_low = []
                for i in range(0, len(bond1)):
                    index = len(bond1) - i
                    coord = np.array([bond1[index - 1].x, bond1[index - 1].y, bond1[index - 1].z])
                    res = obr.dot(coord)
                    path_low.append(np.array([float(res[0]), float(res[1]), float(res[2])]))

                from_to = "{0:14.10} {1:14.10} {2:14.10} {3:14.10} {4:14.10} {5:14.10} ".format(path_low[0][0],
                                                                                                path_low[0][1],
                                                                                                path_low[0][2],
                                                                                                path_low[-1][0],
                                                                                                path_low[-1][1],
                                                                                                path_low[-1][2])

                lines += "# " + title + "\n"
                lines += "REFERENCE 1\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-charge.txt\n"
                lines += "REFERENCE 4\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-totpot.txt\n"
                lines += "REFERENCE 5\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-elpot.txt\n"

                first = "{0:14.10} {1:14.10} {2:14.10} ".format(path_low[-1][0], path_low[-1][1], path_low[-1][2])

                for i in range(1, len(bond2)):
                    coord = np.array([bond2[i].x, bond2[i].y, bond2[i].z])
                    res = obr.dot(coord)
                    path_low.append(np.array([float(res[0]), float(res[1]), float(res[2])]))

                last = "{0:14.10} {1:14.10} {2:14.10} ".format(path_low[-1][0], path_low[-1][1], path_low[-1][2])
                lines += "REFERENCE 1\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-charge.txt\n"
                lines += "REFERENCE 4\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-totpot.txt\n"
                lines += "REFERENCE 5\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-elpot.txt\n"

                path_fine = [path_low[0]]
                for i in range(1, len(path_low)):
                    dv = (path_low[i] - path_low[i - 1]) / extra_points
                    for j in range(0, extra_points):
                        path_fine.append(path_fine[-1] + dv)

                for i in range(0, len(path_fine)):
                    text += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(path_fine[i][0], path_fine[i][1],
                                                                        path_fine[i][2])
                    te += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(path_fine[i][0], path_fine[i][1], path_fine[i][2])
            else:
                """ critical points only """
                res = obr.dot(np.array([cp.x, cp.y, cp.z]))
                text += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(float(res[0]), float(res[1]), float(res[2]))
                te += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(float(res[0]), float(res[1]), float(res[2]))
        textl += "# bond path information\n" + text_prop
        textl += 'POINTPROP elpot "$4"\n'
        textl += 'POINTPROP lapl "$5"\n'
        textl += "POINT ./POINTS.txt\n"
        lines += "UNLOAD ALL\nEND"
        return textl, lines, te, text
