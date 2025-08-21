# This file is a part of CritPlot programm.

from typing import Callable

import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np
from core_atomistic_qt.opengl_base import GuiOpenGLBase
from core_atomistic.helpers import is_number
from src_critplot.models.cp_model import AtomicModelCP


class GuiOpenGLCP(GuiOpenGLBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        # opengl lists
        self.list_for_cp: int = 8
        self.list_for_bondpath: int = 9
        self.NLists = 10

        self.selected_cp = -1
        self.is_cp_available: bool = False
        self.is_bond_path_available: bool = False
        self.width_of_bp: int = 3

        self.is_show_bcp: bool = True
        self.is_show_ccp: bool = True
        self.is_show_rcp: bool = True
        self.is_show_ncp: bool = True
        self.is_show_nna: bool = True
        self.is_show_bond_path: bool = True

        self.is_bcp_property_visible: bool = False
        self.is_bcp_property_for_all: bool = False
        self.bcp_property: str = ""

        self.color_of_bcp = (1, 0, 0)
        self.color_of_ccp = (1, 1, 1)
        self.color_of_rcp = (1, 1, 0)
        self.color_of_nna = (1, 0, 1)
        self.color_of_bp = (0, 1, 0)

        self.selected_cp_callback: Callable = None
        self.main_model = AtomicModelCP()

    def add_all_elements(self) -> None:
        super().add_all_elements()
        self.add_critical_points()
        self.add_bond_path()

    def set_property_show_cp(self, show_bcp, show_ccp, show_rcp, show_ncp, show_nnatr) -> None:
        self.is_show_bcp = show_bcp
        self.is_show_ccp = show_ccp
        self.is_show_rcp = show_rcp
        self.is_show_ncp = show_ncp
        self.is_show_nna = show_nnatr
        self.add_critical_points()

    def set_width_of_bp(self, width_of_bp):
        self.width_of_bp = width_of_bp
        self.add_bond_path()
        self.update()

    def set_is_bcp_property_for_all(self, value):
        self.is_bcp_property_for_all = not value
        self.update()

    def set_property_bond_path(self, bond_path) -> None:
        self.is_show_bond_path = bond_path

    def show_cp_property(self, prop: str = ""):
        if prop == "":
            self.is_bcp_property_visible = False
        else:
            self.bcp_property = prop
            for bcp in self.main_model.cps:
                value = bcp.get_property(prop)
                if is_number(value):
                    value = float(value)
                    value = str(round(value, self.property_precision))
                bcp.visible_property = value
            self.is_bcp_property_visible = True
        self.update()

    def init_params(self, ogl_model) -> None:
        super().init_params(ogl_model)
        self.selected_cp = ogl_model.selected_cp
        self.width_of_bp = ogl_model.width_of_bp
        self.is_bcp_property_visible = ogl_model.is_bcp_property_visible
        self.is_bcp_property_for_all = ogl_model.is_bcp_property_for_all
        self.bcp_property = ogl_model.bcp_property
        self.is_cp_available = ogl_model.is_cp_available
        self.is_bond_path_available = ogl_model.is_bond_path_available
        self.is_show_bcp = ogl_model.is_show_bcp
        self.is_show_ccp = ogl_model.is_show_ccp
        self.is_show_rcp = ogl_model.is_show_rcp
        self.is_show_ncp = ogl_model.is_show_ncp
        self.is_show_nna = ogl_model.is_show_nna
        self.color_of_bcp = ogl_model.color_of_bcp
        self.color_of_rcp = ogl_model.color_of_rcp
        self.color_of_ccp = ogl_model.color_of_ccp
        self.color_of_bp = ogl_model.color_of_bp
        self.is_show_bond_path = ogl_model.is_show_bond_path

    def copy_state(self, ogl_model) -> None:
        super().copy_state(ogl_model)
        self.add_critical_points()
        self.add_bond_path()
        self.update()

    def set_cp_parameters(self, is_bcp_property_visible) -> None:
        self.is_bcp_property_visible = is_bcp_property_visible
        self.add_critical_points()
        self.add_bond_path()
        self.update()

    def selected_atom_properties_to_form(self) -> None:
        self.selected_atom_callback([self.selected_atom, self.selected_cp])

    def add_critical_points(self) -> None:
        gl.glNewList(self.object + self.list_for_cp, gl.GL_COMPILE)
        for cp in self.main_model.cps:
            if ((self.is_show_bcp and (cp.let == "xb")) or (self.is_show_ccp and (cp.let == "xc")) or \
                    (self.is_show_rcp and (cp.let == "xr")) or (self.is_show_nna and (cp.let == "nn")) or \
                    (self.is_show_ncp and (cp.let == "A"))) and cp.is_visible:
                gl.glPushMatrix()
                gl.glTranslatef(*(self.scale_factor * cp.xyz))
                color = (0, 0, 0)
                if cp.let == "xb":
                    color = self.color_of_bcp
                elif cp.let == "xr":
                    color = self.color_of_rcp
                elif cp.let == "xc":
                    color = self.color_of_ccp
                elif cp.let == "nn":
                    color = self.color_of_nna
                gl.glColor3f(*color)
                mult = self.scale_factor
                if cp.is_selected():
                    gl.glColor3f(0, 0, 1)
                    mult *= 1.3
                glu.gluSphere(glu.gluNewQuadric(), 0.15 * mult, self.quality * 70, self.quality * 70)
                gl.glPopMatrix()
        gl.glEndList()
        self.is_cp_available = True
        self.update()

    def set_cp_related_colors(self, color_of_bcp, color_of_rcp, color_of_ccp, color_of_bp) -> None:
        self.color_of_bcp = color_of_bcp
        self.color_of_rcp = color_of_rcp
        self.color_of_ccp = color_of_ccp
        self.color_of_bp = color_of_bp

    def set_color_of_bcp(self, color) -> None:
        self.color_of_bcp = color
        self.add_critical_points()
        self.update()

    def set_color_of_rcp(self, color) -> None:
        self.color_of_rcp = color
        self.add_critical_points()
        self.update()

    def set_color_of_ccp(self, color) -> None:
        self.color_of_ccp = color
        self.add_critical_points()
        self.update()

    def set_color_of_bp(self, color) -> None:
        self.color_of_bp = color
        self.add_bond_path()
        self.update()

    def add_bond_path(self) -> None:
        gl.glNewList(self.object + self.list_for_bondpath, gl.GL_COMPILE)

        for cp in self.main_model.cps:
            if cp.is_visible:
                self.add_critical_path(cp.bonds.get("bond1opt"))
                self.add_critical_path(cp.bonds.get("bond2opt"))
        gl.glEndList()
        self.is_bond_path_available = True
        self.update()

    def add_critical_path(self, bond) -> None:
        if not bond:
            return

        if np.linalg.norm(bond[0].xyz - bond[-1].xyz) > 4.0:
            return

        gl.glColor3f(*self.color_of_bp)
        if len(bond) > 2:
            i = 1
            while i < len(bond):
                self.add_bond(self.scale_factor * bond[i - 1].xyz,
                              self.scale_factor * bond[i].xyz,
                              self.scale_factor * 0.01 * self.width_of_bp)
                i += 2
        else:
            self.add_bond(self.scale_factor * bond[0].xyz,
                          self.scale_factor * bond[1].xyz,
                          self.scale_factor * 0.01 * self.width_of_bp)

    def paintGL(self) -> None:
        self.makeCurrent()
        self.configure_gl()
        try:
            self.prepere_scene()
            self.light_prepare()
            if self.active:
                self.prepare_orientation()
                if self.is_view_atoms:
                    gl.glCallList(self.object + self.list_for_atoms)  # atoms

                if self.is_cp_available and (self.is_show_bcp or self.is_show_ccp or self.is_show_rcp or
                                             self.is_show_ncp):
                    gl.glCallList(self.object + self.list_for_cp)  # CPS

                if self.can_atom_search:
                    self.get_atom_on_screen()

                if self.is_view_bonds and (len(self.main_model.bonds) > 0):
                    gl.glCallList(self.object + self.list_for_bonds)  # find_bonds_exact

                if self.is_view_box:
                    gl.glCallList(self.object + self.list_for_box)  # lattice_parameters_abc_angles

                if self.is_view_axes:
                    gl.glCallList(self.object + self.list_for_axes)  # Axes

                if self.is_bond_path_available and self.is_show_bond_path:
                    gl.glCallList(self.object + self.list_for_bondpath)  # Bondpath

                text_to_render = []
                if self.is_atomic_numbers_visible:
                    for i in range(0, len(self.main_model.atoms)):
                        at = self.main_model.atoms[i]
                        text_to_render.append([*(self.scale_factor * at.xyz), at.let + str(i + 1)])

                if self.is_bcp_property_visible:
                    if self.is_bcp_property_for_all:
                        for i in range(0, len(self.main_model.cps)):
                            at = self.main_model.cps[i]
                            fl = (self.is_show_bcp and (at.let == "xb")) or (self.is_show_ccp and (at.let == "xc")) or \
                                (self.is_show_rcp and (at.let == "xr")) or (self.is_show_nna and (at.let == "nn")) or \
                                (self.is_show_ncp and (at.let == "A"))
                            if fl and self.main_model.cps[i].is_visible:
                                text_to_render.append([*(self.scale_factor * at.xyz), at.visible_property])
                    else:
                        for i in range(0, len(self.main_model.cps)):
                            at = self.main_model.cps[i]
                            if at.active:
                                text_to_render.append([*(self.scale_factor * at.xyz), at.visible_property])

                if self.is_atomic_numbers_visible or self.is_bcp_property_visible:
                    self.render_text(text_to_render)
        except Exception as exc:
            print(exc)

    def get_atom_on_screen(self) -> None:
        point = self.get_point_in_3d(self.x_scene, self.y_scene)
        old_selected = self.selected_atom
        old_selected_cp = self.selected_cp

        cps_ind, cps_visible = self.cps_visible_list()
        if len(cps_ind) > 0:
            cp_ind, cp_min_r = self.nearest_point(self.scale_factor, cps_visible, point)
            cp_ind = cps_ind[cp_ind]
        else:
            cp_ind = -1
            cp_min_r = 10000

        atom_ind, atom_min_r = self.nearest_point(self.scale_factor, self.main_model.atoms, point)

        if cp_min_r < atom_min_r:
            if cp_min_r < 1.4:
                if self.selected_cp == cp_ind:
                    if self.selected_cp >= 0:
                        self.main_model.cps[self.selected_cp].set_selected(False)
                        self.selected_cp = -1
                else:
                    if self.selected_cp >= 0:
                        self.main_model.cps[self.selected_cp].set_selected(False)
                    self.selected_cp = cp_ind
                    if self.selected_atom >= 0:
                        self.main_model.atoms[self.selected_atom].set_selected(False)
                        self.selected_atom = -1
                    if self.selected_cp >= 0:
                        self.main_model.cps[self.selected_cp].set_selected(True)
        else:
            self.update_selected_atom(atom_ind, atom_min_r)

        self.can_atom_search = False
        selected_atom_was_modified = old_selected != self.selected_atom
        selected_cp_was_modified = old_selected_cp != self.selected_cp
        if selected_atom_was_modified and (self.selected_atom > 0):
            if self.selected_cp > 0:
                self.main_model.cps[self.selected_cp].set_selected(False)
                self.selected_cp = -1
        if selected_atom_was_modified or selected_cp_was_modified:
            self.add_atoms()
            self.add_critical_points()
            self.add_bonds()
            self.selected_atom_changed()
            self.update()

    def cps_visible_list(self):
        cps_visible = []
        cps_ind = []
        for ind, c_point in enumerate(self.main_model.cps):
            if (c_point.let == "xb") and self.is_show_bcp or (c_point.let == "xr") and self.is_show_rcp or \
                    (c_point.let == "xc") and self.is_show_ccp or (c_point.let == "nn") and self.is_show_nna or \
                    (c_point.let[0].isupper()) and self.is_show_ncp:  # "a" - not correct
                cps_visible.append(c_point)
                cps_ind.append(ind)
        return cps_ind, cps_visible
