# This file is a part of GUI4dft programm.

from typing import Callable

import OpenGL.GL as gl
from copy import deepcopy
import numpy as np

from core_atomistic_qt.opengl_base import GuiOpenGLBase
from core_atomistic.atomic_model import AtomicModel
from src_gui4dft.utils.calculators import VoronoiAnalisis


class GuiOpenGL(GuiOpenGLBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        # opengl lists
        self.list_for_voronoi: int = 1
        self.list_for_surface: int = 4
        self.list_for_contour: int = 5
        self.list_for_contours_fill: int = 6

        self.is_view_surface: bool = False
        self.is_view_contour: bool = False
        self.is_view_contour_fill: bool = False
        self.is_view_voronoi: bool = False
        self.is_atomic_numbers_visible: bool = False
        self.selected_atom = -1
        self.selected_fragment_mode = False
        self.SelectedFragmentAtomsListView = None
        self.SelectedFragmentAtomsTransp = 1.0

        self.color_of_voronoi = [0, 0, 0]

        self.orientation_model_changed: Callable = None
        self.selected_atom_position: Callable = None
        self.selected_atom_callback: Callable = None

        self.contour_width = 2

        self.main_model = AtomicModel()

    def set_selected_fragment_mode(self, selected_fragment_atoms_list_view, selected_fragment_atoms_transp):
        if selected_fragment_atoms_list_view is None:
            if self.selected_fragment_mode:
                self.SelectedFragmentAtomsListView.clear()
            self.SelectedFragmentAtomsListView = None
            self.selected_fragment_mode = False
        else:
            self.selected_fragment_mode = True
            self.SelectedFragmentAtomsListView = selected_fragment_atoms_list_view
            self.SelectedFragmentAtomsTransp = selected_fragment_atoms_transp
            self.atoms_of_selected_fragment_to_form()

    def atoms_of_selected_fragment_to_form(self):
        self.SelectedFragmentAtomsListView.clear()
        self.SelectedFragmentAtomsListView.addItems(['Atoms'])
        for i in range(0, len(self.main_model.atoms)):
            if (self.main_model.atoms[i]).fragment1:
                self.SelectedFragmentAtomsListView.addItems([str(i)])

    def init_params(self, the_object) -> None:
        self.is_orthographic = the_object.is_orthographic
        self.is_view_atoms = the_object.is_view_atoms
        self.is_atomic_numbers_visible = the_object.is_atomic_numbers_visible
        self.background_color = the_object.background_color
        self.is_view_box = the_object.is_view_box
        self.is_view_bonds = the_object.is_view_bonds
        self.is_view_surface = the_object.is_view_surface
        self.is_view_contour = the_object.is_view_contour
        self.is_view_contour_fill = the_object.is_view_contour_fill
        self.is_view_voronoi = the_object.is_view_voronoi
        self.property_x_shift = the_object.property_x_shift
        self.property_y_shift = the_object.property_y_shift
        self.font_size = the_object.font_size
        self.active = the_object.active
        self.scale_factor = the_object.scale_factor
        self.bond_width = the_object.bond_width
        self.x_scr_old = the_object.x_scr_old
        self.y_scr_old = the_object.y_scr_old
        self.x_scene = the_object.x_scene
        self.y_scene = the_object.y_scene
        self.camera_position = the_object.camera_position
        self.rotation_angles[:] = the_object.rotation_angles
        self.selected_atom = the_object.selected_atom
        self.prop = the_object.prop
        self.selected_fragment_mode = the_object.selected_fragment_mode
        self.SelectedFragmentAtomsListView = the_object.SelectedFragmentAtomsListView
        self.SelectedFragmentAtomsTransp = the_object.SelectedFragmentAtomsTransp
        self.main_model = the_object.main_model
        self.color_of_atoms = the_object.color_of_atoms
        self.color_of_bonds = the_object.color_of_bonds
        self.color_of_bonds_by_atoms = the_object.color_of_bonds_by_atoms
        self.color_of_box = the_object.color_of_box
        self.is_view_axes = the_object.is_view_axes
        self.perspective_angle = the_object.perspective_angle

    def copy_state(self, ogl_model):
        self.init_params(ogl_model)
        self.add_all_elements()
        if self.is_view_voronoi:
            self.color_of_voronoi = ogl_model.color_of_voronoi
            self.add_voronoi(self.color_of_voronoi)
        if self.is_view_contour:
            self.add_contour(ogl_model.data_contour)
        if self.is_view_contour_fill:
            self.add_colored_plane(ogl_model.data_contour_fill)
        if self.is_view_surface:
            self.add_surface(ogl_model.data_surface)
        self.update()

    def set_atomic_structure(self, structure, atoms_colors, is_view_atoms, is_view_atom_numbers, is_view_box, box_color,
                             is_view_bonds, bonds_color, bond_width, bonds_by_atoms, is_view_axes, axes_color,
                             contour_width):
        self.clean()
        self.selected_atom = -1
        self.main_model = deepcopy(structure)
        self.coord0 = -self.main_model.get_center_of_mass()
        self.main_model.move(self.coord0)
        # print("initial atomic structure 0: ")
        # print(self.main_model.atoms[0].xyz)
        self.is_view_surface = False
        self.is_view_contour = False
        self.is_view_contour_fill = False
        self.active = False
        self.auto_zoom()
        self.main_model.find_bonds_fast()
        self.set_structure_parameters(atoms_colors, is_view_atoms, is_view_atom_numbers, is_view_box, box_color,
                                     is_view_bonds, bonds_color, bond_width, bonds_by_atoms, is_view_axes, axes_color,
                                     contour_width)

    def auto_zoom(self):
        super().auto_zoom()
        self.model_orientation_to_form()

    def set_color_of_voronoi(self, color):
        self.add_voronoi(color)

    def set_contour_width(self, width):
        self.contour_width = width
        self.update()

    def set_atoms_numbered(self, state):
        self.is_atomic_numbers_visible = state
        self.update()

    def scale(self, wheel):
        if super().scale(wheel):
            self.model_orientation_to_form()
            return True
        return False

    def move_atom(self, x, y):
        if super().move_atom(x, y):
            self.is_view_voronoi = False
            self.is_view_surface = False
            self.is_view_contour_fill = False
            self.is_view_contour = False
            return True

    def add_surface(self, data):
        self.data_surface = data
        gl.glNewList(self.object + 4, gl.GL_COMPILE)
        for surf in data:
            verts = surf[0]
            faces = surf[1]
            color = surf[2]
            normals = surf[3]
            gl.glColor4f(*color)
            for face in faces:
                gl.glBegin(gl.GL_TRIANGLES)
                for point in face:
                    gl.glNormal3f(*(-normals[point]))
                    gl.glVertex3f(*verts[point])
                gl.glEnd()
        gl.glEndList()
        self.is_view_surface = True
        self.update()

    def add_contour(self, params):
        self.data_contour = params
        gl.glDeleteLists(self.object + 5, 1)
        gl.glNewList(self.object + 5, gl.GL_COMPILE)
        for param in params:
            conts = param[1]
            colors = param[2]
            it = 0
            for cont in conts:
                color = colors[it]
                it += 1
                gl.glColor3f(color[0], color[1], color[2])
                for contour in cont:
                    for i in range(0, len(contour)-1):
                        p1 = contour[i]
                        p2 = contour[i+1]
                        self.add_bond(p1, p2, self.contour_width)
        gl.glEndList()
        self.is_view_contour = True
        self.update()

    def add_colored_plane(self, data):
        self.data_contour_fill = data
        gl.glDeleteLists(self.object + 6, 1)
        gl.glNewList(self.object + 6, gl.GL_COMPILE)
        for plane in data:
            points = plane[0]
            colors = plane[1]
            normal = plane[2]
            nx = len(points)
            ny = len(points[0])
            gl.glNormal3f(*normal)
            gl.glBegin(gl.GL_TRIANGLES)
            for i in range(0, nx - 1):
                for j in range(0, ny - 1):
                    gl.glColor3f(*colors[i][j])
                    gl.glVertex3f(*points[i][j][0:3])
                    gl.glColor3f(*colors[i+1][j])
                    gl.glVertex3f(*points[i+1][j][0:3])
                    gl.glColor3f(*colors[i][j+1])
                    gl.glVertex3f(*points[i][j+1][0:3])
                    gl.glColor3f(*colors[i][j+1])
                    gl.glVertex3f(*points[i][j+1][0:3])
                    gl.glColor3f(*colors[i + 1][j])
                    gl.glVertex3f(*points[i + 1][j][0:3])
                    gl.glColor3f(*colors[i + 1][j+1])
                    gl.glVertex3f(*points[i + 1][j+1][0:3])
            gl.glEnd()
        gl.glEndList()
        self.is_view_contour_fill = True
        self.update()

    def add_voronoi(self, color, max_dist=5):
        self.color_of_voronoi = color
        volume = np.inf
        if self.selected_atom >= 0:
            list_of_poligons, volume = VoronoiAnalisis(self.main_model, self.selected_atom, max_dist)
            gl.glNewList(self.object + 1, gl.GL_COMPILE)
            gl.glColor4f(color[0], color[1], color[2], 0.7)
            for poligon in list_of_poligons:
                gl.glBegin(gl.GL_POLYGON)
                for point in poligon:
                    gl.glVertex3f(point[0], point[1], point[2])
                gl.glEnd()
            gl.glEndList()
            self.is_view_voronoi = True
            self.update()
        return self.selected_atom, volume

    def paintGL(self):
        self.makeCurrent()
        try:
            self.prepere_scene()
            self.light_prepare()
            if self.active:
                self.prepare_orientation()
                if self.is_view_atoms:
                    gl.glCallList(self.object + self.list_for_atoms)  # atoms

                if self.can_atom_search:
                    self.get_atom_on_screen()

                if self.is_view_bonds and (len(self.main_model.bonds) > 0):
                    gl.glCallList(self.object + 2)  # find_bonds_exact

                if self.is_view_voronoi:
                    gl.glCallList(self.object + 1)  # Voronoi

                if self.is_view_box:
                    gl.glCallList(self.object + 3)  # lattice_parameters_abc_angles

                if self.is_view_surface:
                    gl.glCallList(self.object + 4)  # Surface

                if self.is_view_contour:
                    gl.glCallList(self.object + 5)  # Contour

                if self.is_view_contour_fill:
                    gl.glCallList(self.object + 6)  # ContourFill

                if self.is_view_axes:
                    gl.glCallList(self.object + 7)  # Axes

                text_to_render = []
                if self.is_atomic_numbers_visible:
                    # print("text 0: ")
                    # print(self.main_model.atoms[0].xyz)
                    for i in range(0, len(self.main_model.atoms)):
                        at = self.main_model.atoms[i]
                        text_to_render.append([self.scale_factor * at.x, self.scale_factor * at.y,
                                               self.scale_factor * at.z, at.let + str(i + 1)])

                if self.is_atomic_numbers_visible:
                    self.render_text(text_to_render)
        except Exception as exc:
            print(exc)
            pass

    def get_atom_on_screen(self):
        # print("-----> ")
        # print("self.x_scene, self.y_scene: ", self.x_scene, self.y_scene)
        point = self.get_point_in_3d(self.x_scene, self.y_scene)
        # print("self.selected_atom ", self.selected_atom)
        old_selected = self.selected_atom
        # print("self.scale_factor ", self.scale_factor)
        ind, min_r = self.nearest_point(self.scale_factor, self.main_model.atoms, point)
        self.update_selected_atom(ind, min_r)
        # print("int, min_r ", ind, min_r)

        if min_r < 1.4:
            if self.selected_atom >= 0:
                self.is_view_voronoi = False

        self.can_atom_search = False
        if old_selected != self.selected_atom:
            self.selected_atom_changed()
            self.add_atoms()
            self.update()
