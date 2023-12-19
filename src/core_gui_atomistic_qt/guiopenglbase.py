# This file is a part of GUI4dft programm.
from typing import Callable

import OpenGL.GL as gl
import OpenGL.GLU as glu
from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtCore import QEvent
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPainter, QFont
from copy import deepcopy
from core_gui_atomistic.periodic_table import TPeriodTable
from core_gui_atomistic.atom import Atom
import math
import numpy as np


class GuiOpenGLBase(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_model = None
        self.perspective_angle: int = 35
        self.background_color = np.array((1.0, 1.0, 1.0), dtype=float)
        self.is_check_atom_selection: bool = False
        self.quality: int = 1
        # opengl lists
        self.object = None
        self.NLists = 8
        self.list_for_atoms: int = 0
        self.list_for_bonds: int = 2
        self.list_for_box: int = 3
        self.list_for_axes: int = 7

        self.can_atom_search = False
        self.x_scr_old = 0
        self.y_scr_old = 0
        self.coord0 = np.zeros(3, dtype=float)
        self.is_orthographic: bool = False
        self.is_view_atoms: bool = True
        self.is_view_box: bool = False
        self.is_view_bonds: bool = True
        self.is_gl_cull_face: bool = False
        self.active: bool = False
        self.scale_factor = 1
        self.bond_width = 20
        self.x_scene = 0
        self.y_scene = 0
        self.camera_position = np.array([0.0, 0.0, -20.0])
        self.rotation_angles = np.zeros(3, dtype=float)
        self.color_of_bonds = (0, 0, 0)
        self.color_of_axes = (0, 0, 0)
        self.color_of_box = (0, 0, 0)

        self.selected_fragment_mode = False
        self.SelectedFragmentAtomsListView = None
        self.SelectedFragmentAtomsTransp = 1.0

        self.prop = "charge"
        self.property_precision: int = 5
        self.font_size: int = 8
        self.property_x_shift: int = 0
        self.property_y_shift: int = 0

        self.is_atomic_numbers_visible: bool = False
        self.selected_atom: int = -1

        # lighting
        self.light0_position = np.array((0.0, 0.0, 100.0, 1))
        self.light_color_ambient = (0.2, 0.2, 0.2, 1.0)
        self.light_color_diffuse = (0.7, 0.7, 0.7, 1.0)
        self.light_color_specular = (1, 1, 1, 1)
        self.material_diffuse = (1.0, 1.0, 1.0, 1)
        self.material_specular = (0.2, 0.2, 0.2, 1)
        self.material_shininess = 12

        self.is_view_axes = False

        self.orientation_model_changed: Callable = None
        self.selected_atom_position: Callable = None
        self.selected_atom_callback: Callable = None

    def is_atom_selected(self):
        return self.selected_atom >= 0

    def wheelEvent(self, event: QEvent):
        self.scale(event.angleDelta().y())

    def mouseMoveEvent(self, event: QEvent):
        if event.buttons() == Qt.LeftButton:
            self.rotat(event.x(), event.y(), self.width(), self.height())
            self.set_xy(event.x(), event.y())

        elif event.buttons() == Qt.RightButton:
            if self.is_atom_selected():
                self.move_atom(event.x(), event.y())
            else:
                if not self.is_check_atom_selection.isChecked():
                    self.pan(event.x(), event.y())
            self.set_xy(event.x(), event.y())

    def mousePressEvent(self, event: QEvent):
        if event.type() == QEvent.MouseButtonPress:
            if self.is_check_atom_selection.isChecked() and event.buttons() == Qt.LeftButton:
                self.can_atom_search = True
            self.set_xy(event.x(), event.y())

    def init_params(self, the_object) -> None:
        self.is_orthographic = the_object.is_orthographic
        self.is_view_atoms = the_object.is_view_atoms
        self.is_atomic_numbers_visible = the_object.is_atomic_numbers_visible
        self.background_color = the_object.background_color
        self.is_view_box = the_object.is_view_box
        self.is_view_bonds = the_object.is_view_bonds
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
        self.update()

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

    @property
    def is_camera_ortho(self) -> bool:
        return self.is_orthographic

    @is_camera_ortho.setter
    def is_camera_ortho(self, is_orthographic):
        self.is_orthographic = is_orthographic
        if len(self.main_model.atoms) == 0:
            return
        self.auto_zoom()
        self.add_all_elements()
        self.model_orientation_to_form()

    def set_perspective_angle(self, perspective_angle: int) -> None:
        self.perspective_angle = perspective_angle

    def is_active(self):
        return self.active

    def screen2space(self, x, y, width, height):
        radius = min(width, height) * float(self.scale_factor)
        return (2.0 * x - width)/radius, -(2.0 * y - height)/radius

    def set_atoms_numbered(self, state):
        self.is_atomic_numbers_visible = state
        self.update()

    def rotate_vector(self, vect, al, bet, gam):
        mx, my, mz = self.rotation_matrix_elements(al, bet, gam)
        vect = mx.dot(vect)
        vect = my.dot(vect)
        vect = mz.dot(vect)
        return vect

    def rotate_un_vector(self, vect, al, bet, gam):
        mx, my, mz = self.rotation_matrix_elements(al, bet, gam)
        vect = mz.dot(vect)
        vect = my.dot(vect)
        vect = mx.dot(vect)
        return vect

    def clean(self):
        if self.active:
            gl.glDeleteLists(self.object, self.NLists)
        self.object = gl.glGenLists(self.NLists)

    def update_view(self):
        self.clean()
        self.add_all_elements()
        self.update()

    def prepare_orientation(self):
        gl.glTranslated(*self.camera_position)
        gl.glRotate(self.rotation_angles[0], 1, 0, 0)
        gl.glRotate(self.rotation_angles[1], 0, 1, 0)
        gl.glRotate(self.rotation_angles[2], 0, 0, 1)

    def prepere_scene(self):
        gl.glClearColor(*self.background_color, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if self.is_gl_cull_face:
            gl.glEnable(gl.GL_CULL_FACE)
        else:
            gl.glDisable(gl.GL_CULL_FACE)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        x, y, width, height = gl.glGetDoublev(gl.GL_VIEWPORT)
        if not self.is_orthographic:
            glu.gluPerspective(
                self.perspective_angle,  # field of view in degrees
                width / float(height or 1),  # aspect ratio
                .25,  # near clipping plane
                200)  # far clipping plane
        else:
            radius = .5 * min(width, height)
            w, h = width / radius, height / radius

            gl.glOrtho(-2 * w,  # GLdouble left
                       2 * w,   # GLdouble right
                       -2 * h,  # GLdouble bottom
                       2 * h,   # GLdouble top
                       -0.25,   # GLdouble near
                       200.0)   # GLdouble far
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def get_point_in_3d(self, x, y):
        model = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
        proj = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
        view = gl.glGetIntegerv(gl.GL_VIEWPORT)
        win_y = int(float(view[3]) - float(y))
        z = gl.glReadPixels(x, win_y, 1, 1, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT)
        point = glu.gluUnProject(x, y, z, model, proj, view)
        al = math.pi * self.rotation_angles[0] / 180
        # !!! Why ????
        bet = 0  # math.pi * self.rotation_angles[1] / 180
        gam = math.pi * self.rotation_angles[2] / 180
        point = self.rotate_un_vector(np.array(point), al, bet, gam)
        point = self.rotate_vector(np.array(point), al, bet, gam)
        return point

    @staticmethod
    def get_screen_coords(x, y, z):
        model = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
        proj = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
        view = gl.glGetIntegerv(gl.GL_VIEWPORT)
        win_x, win_y, win_z = glu.gluProject(x, y, z, model, proj, view)
        return win_x, win_y, win_z

    def initializeGL(self):
        self.makeCurrent()
        self.configure_gl()
        self.object = gl.glGenLists(self.NLists)
        gl.glNewList(self.object, gl.GL_COMPILE)
        gl.glEndList()

    def configure_gl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(1)
        gl.glDepthFunc(gl.GL_LEQUAL)

    def set_color_of_box(self, color):
        self.color_of_box = color
        self.add_box()
        self.update()

    def set_color_of_axes(self, color):
        self.color_of_axes = color
        self.add_axes()
        self.update()

    def set_bond_width(self, width):
        self.bond_width = width
        self.add_bonds()
        self.update()

    def set_bond_color(self, bonds_type):
        self.color_of_bonds_by_atoms = bonds_type
        self.add_bonds()
        self.update()

    def set_color_of_atoms(self, colors):
        self.color_of_atoms = colors
        self.add_atoms()
        self.add_bonds()
        self.update()

    def set_color_of_bonds(self, color):
        self.color_of_bonds = color
        self.add_bonds()

    def set_color_of_background(self, color):
        self.background_color = color
        self.update()

    def set_box_visible(self, state):
        self.is_view_box = state
        self.update()

    def set_bonds_visible(self, state):
        self.is_view_bonds = state
        self.update()

    def set_axes_visible(self, state):
        self.is_view_axes = state
        self.update()

    def rotation_angle_change(self, delta_fi):
        self.rotation_angles += delta_fi
        self.model_orientation_to_form()

    def set_atoms_visible(self, state):
        self.is_view_atoms = state
        self.update()

    def pan(self, x: int, y: int) -> None:
        """Move camera by (x,y)."""
        if self.active:
            xs, ys = self.screen2space(x, y, self.width(), self.height())
            self.camera_position_change(np.array([xs - self.x_scr_old, ys - self.y_scr_old, 0.0]))
            self.x_scr_old = xs
            self.y_scr_old = ys

    def camera_position_change(self, delta_r):
        if self.active:
            self.camera_position += delta_r
            self.model_orientation_to_form()

    def set_xy(self, x, y):
        if self.active:
            self.x_scr_old, self.y_scr_old = self.screen2space(x, y, self.width(), self.height())
            self.x_scene, self.y_scene = x, y
            self.update()
            return True

    def move_atom(self, x, y):
        if self.active:
            dx = x - self.x_scene
            dy = y - self.y_scene
            mult = 0.01 * self.scale_factor
            vect = mult * np.array([-dx, dy, 0])
            al, bet, gam = -math.pi * self.rotation_angles / 180.0
            vect = self.rotate_vector(vect, al, bet, gam)
            self.x_scene, self.y_scene = x, y
            self.main_model.atoms[self.selected_atom].x -= vect[0]
            self.main_model.atoms[self.selected_atom].y -= vect[1]
            self.main_model.atoms[self.selected_atom].z -= vect[2]
            self.selected_atom_changed()

            self.add_atoms()
            self.main_model.find_bonds_fast()
            self.add_bonds()
            return True

    def rotat(self, x, y, width, height):
        if self.active:
            x_speed = 180.0 / width
            y_speed = 180.0 / height
            self.rotation_angle_change(np.array([y_speed * (y - self.y_scene), x_speed * (x - self.x_scene),  0.0]))
            return True
        return False

    @staticmethod
    def rotation_matrix_elements(al, bet, gam):
        cos = math.cos(al)
        sin = math.sin(al)
        mx = np.array([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
        cos = math.cos(bet)
        sin = math.sin(bet)
        my = np.array([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
        cos = math.cos(gam)
        sin = math.sin(gam)
        mz = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        return mx, my, mz

    def add_all_elements(self):
        self.add_atoms()
        self.add_bonds()
        self.add_box()
        self.add_axes()

    def color_atoms_with_property(self, prop: str = "charge"):
        self.clean()
        self.prop = prop
        self.add_all_elements()

    def add_atoms(self):
        prop = self.prop
        mendeley = TPeriodTable()
        gl.glNewList(self.object + self.list_for_atoms, gl.GL_COMPILE)

        min_val = 0
        max_val = 0
        mean_val = 0

        if (len(prop) > 0) and (prop != "charge"):
            min_val = self.main_model.atoms[0].properties[prop]
            max_val = self.main_model.atoms[0].properties[prop]
            mean_val = self.main_model.atoms[0].properties[prop]
            for at in self.main_model.atoms:
                val = at.properties[prop]
                if min_val > val:
                    min_val = val
                if max_val < val:
                    max_val = val
                mean_val += val
            mean_val /= self.main_model.n_atoms()

        for at in self.main_model.atoms:
            gl.glPushMatrix()
            gl.glTranslatef(*(at.xyz * self.scale_factor))
            rad = mendeley.Atoms[at.charge].radius / mendeley.Atoms[6].radius * self.scale_factor

            color = np.array((0.0, 0.0, 0.0, 1.0))
            rad_scale = 0.3

            if not at.is_selected():
                if (len(prop) > 0) and (prop != "charge"):
                    val = at.properties[prop]
                    if val > mean_val:
                        color = (color[0], math.fabs((val-mean_val)/(max_val-mean_val)), color[2], color[3])
                    else:
                        color = (color[0], color[1], math.fabs((val-mean_val)/(min_val-mean_val)), color[3])
                else:
                    color = self.color_of_atoms[at.charge]
                    if self.selected_fragment_mode and at.fragment1:
                        color = (color[0], color[1], color[2], self.SelectedFragmentAtomsTransp)
            else:
                color[0] = 1
                rad_scale = 0.35

            gl.glColor4f(*color)
            #gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, color)
            #gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, np.array((*self.material_diffuse[0:3], color[3])))

            glu.gluSphere(glu.gluNewQuadric(), rad_scale * rad, self.quality * 70, self.quality * 70)
            gl.glPopMatrix()
        gl.glEndList()
        self.active = True

    def add_bonds(self):
        gl.glNewList(self.object + 2, gl.GL_COMPILE)
        gl.glColor3f(self.color_of_bonds[0], self.color_of_bonds[1], self.color_of_bonds[2])
        for bond in self.main_model.bonds:
            x1 = self.main_model.atoms[bond[0]].x
            y1 = self.main_model.atoms[bond[0]].y
            z1 = self.main_model.atoms[bond[0]].z
            x2 = self.main_model.atoms[bond[1]].x
            y2 = self.main_model.atoms[bond[1]].y
            z2 = self.main_model.atoms[bond[1]].z

            if not self.color_of_bonds_by_atoms:
                x3 = (self.main_model.atoms[bond[1]].x + self.main_model.atoms[bond[0]].x) / 2
                y3 = (self.main_model.atoms[bond[1]].y + self.main_model.atoms[bond[0]].y) / 2
                z3 = (self.main_model.atoms[bond[1]].z + self.main_model.atoms[bond[0]].z) / 2
                coords = ([self.scale_factor * np.array([x1, y1, z1]), self.scale_factor * np.array([x3, y3, z3]),
                           self.color_of_atoms[self.main_model.atoms[bond[0]].charge]],
                          [self.scale_factor * np.array([x3, y3, z3]), self.scale_factor * np.array([x2, y2, z2]),
                           self.color_of_atoms[self.main_model.atoms[bond[1]].charge]])
            else:
                coords = [[self.scale_factor * np.array([x1, y1, z1]), self.scale_factor * np.array([x2, y2, z2]),
                           np.array(self.color_of_bonds)]]

            for coord in coords:
                if self.selected_fragment_mode and \
                        (self.main_model.atoms[bond[0]].fragment1 or self.main_model.atoms[bond[1]].fragment1):
                    gl.glColor4f(*coord[2][0:3], self.SelectedFragmentAtomsTransp)
                else:
                    gl.glColor4f(*coord[2][0:3], 1)
                self.add_bond(coord[0], coord[1], self.scale_factor * self.bond_width)
        gl.glEndList()

    def add_box(self):
        gl.glNewList(self.object + 3, gl.GL_COMPILE)
        gl.glColor3f(*self.color_of_box[0:3])

        v1 = self.main_model.lat_vector1 * self.scale_factor
        v2 = self.main_model.lat_vector2 * self.scale_factor
        v3 = self.main_model.lat_vector3 * self.scale_factor

        origin = - (v1 + v2 + v3) / 2

        p1 = origin
        p2 = origin + v1
        p3 = origin + v2
        p4 = p2 + v2
        p5 = origin + v3
        p6 = p2 + v3
        p7 = p3 + v3
        p8 = p4 + v3
        width = 0.03 * self.scale_factor
        self.add_bond(p1, p2, width)
        self.add_bond(p1, p3, width)
        self.add_bond(p1, p5, width)
        self.add_bond(p2, p4, width)
        self.add_bond(p2, p6, width)
        self.add_bond(p3, p4, width)
        self.add_bond(p3, p7, width)
        self.add_bond(p4, p8, width)
        self.add_bond(p5, p6, width)
        self.add_bond(p5, p7, width)
        self.add_bond(p6, p8, width)
        self.add_bond(p7, p8, width)
        gl.glEndList()

    def add_axes(self):
        gl.glNewList(self.object + 7, gl.GL_COMPILE)
        gl.glColor3f(*self.color_of_axes)
        size = 2 * self.scale_factor
        size_cone = 0.2 * self.scale_factor
        letter_height = size_cone
        letter_width = 0.6 * size_cone
        width = 0.06 * self.scale_factor
        glu.gluSphere(glu.gluNewQuadric(), 2 * width, 70, 70)
        p0 = np.array([0, 0, 0])
        p1 = np.array([size, 0, 0])
        p1cone = np.array([size + size_cone, 0, 0])
        p2 = np.array([0, size, 0])
        p2cone = np.array([0, size + size_cone, 0])
        p3 = np.array([0, 0, size])
        p3cone = np.array([0, 0, size + size_cone])
        self.add_bond(p0, p1, width)
        self.add_bond(p1, p1cone, 2 * width, 'conus')
        self.add_bond(p0, p2, width)
        self.add_bond(p2, p2cone, 2 * width, 'conus')
        self.add_bond(p0, p3, width)
        self.add_bond(p3, p3cone, 2 * width, 'conus')
        # lets drow "X"
        p_x = p1cone + np.array([0, 1.5 * size_cone, 0])
        p_x1 = p_x + np.array([-0.5 * letter_width, -0.5 * letter_height, 0])
        p_x2 = p_x + np.array([+0.5 * letter_width, +0.5 * letter_height, 0])
        p_x3 = p_x + np.array([-0.5 * letter_width, +0.5 * letter_height, 0])
        p_x4 = p_x + np.array([+0.5 * letter_width, -0.5 * letter_height, 0])
        self.add_bond(p_x1, p_x2, 0.5 * width)
        self.add_bond(p_x3, p_x4, 0.5 * width)
        # lets drow "Y"
        p_y = p2cone + np.array([0, 1.5 * size_cone,  0])
        p_y1 = p_y
        p_y2 = p_y + np.array([0, +0.5 * letter_height, +0.5 * letter_width])
        p_y3 = p_y + np.array([0, -0.5 * letter_height, +0.5 * letter_width])
        p_y4 = p_y + np.array([0, +0.5 * letter_height, -0.5 * letter_width])
        self.add_bond(p_y1, p_y2, 0.5 * width)
        self.add_bond(p_y3, p_y4, 0.5 * width)
        # lets drow "Z"
        p_z = p3cone + np.array([1.5 * size_cone, 0, 0])
        p_z1 = p_z + np.array([-0.5 * letter_height, 0, -0.5 * letter_width])
        p_z2 = p_z + np.array([+0.5 * letter_height, 0, +0.5 * letter_width])
        p_z3 = p_z + np.array([-0.5 * letter_height, 0, +0.5 * letter_width])
        p_z4 = p_z + np.array([+0.5 * letter_height, 0, -0.5 * letter_width])
        self.add_bond(p_z1, p_z3, 0.5 * width)
        self.add_bond(p_z1, p_z2, 0.5 * width)
        self.add_bond(p_z2, p_z4, 0.5 * width)
        gl.glEndList()

    def add_bond(self, atom1_pos, atom2_pos, radius=0.1, shape='cylinder'):
        radius2 = radius
        if shape == 'conus':
            radius2 = 0
        rel = [atom2_pos[0] - atom1_pos[0], atom2_pos[1] - atom1_pos[1], atom2_pos[2] - atom1_pos[2]]
        binding_len = math.sqrt(math.pow(rel[0], 2) + math.pow(rel[1], 2) + math.pow(rel[2], 2))
        if binding_len != 0:
            fall = 180.0 / math.pi * math.acos(rel[2] / binding_len)
            yaw = 180.0 / math.pi * math.atan2(rel[1], rel[0])

            gl.glPushMatrix()
            gl.glTranslated(atom1_pos[0], atom1_pos[1], atom1_pos[2])
            gl.glRotated(yaw, 0, 0, 1)
            gl.glRotated(fall, 0, 1, 0)
            glu.gluCylinder(glu.gluNewQuadric(),
                            radius,  # /*baseRadius:*/
                            radius2,  # /*topRadius:*/
                            binding_len,  # /*height:*/
                            self.quality * 15,  # /*slices:*/
                            1)  # /*stacks:*/
            gl.glPopMatrix()

    def add_selected_atom(self):
        gl.glNewList(self.object+7, gl.GL_COMPILE)
        for at in self.main_model.atoms:
            if at.is_selected():
                gl.glPushMatrix()
                gl.glTranslatef(at.x, at.y, at.z)
                gl.glColor3f(1, 0, 0)
                glu.gluSphere(glu.gluNewQuadric(), 0.35, 70, 70)
                gl.glPopMatrix()
        gl.glEndList()

    def light_prepare(self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, self.material_diffuse)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, self.material_specular)
        gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, self.material_shininess)
        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        # gl.glDisable(gl.GL_COLOR_MATERIAL)

        # Determine the current lighting model
        gl.glLightModelf(gl.GL_LIGHT_MODEL_TWO_SIDE, gl.GL_TRUE)  # two-side lighting calculation

        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.light0_position)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, self.light_color_ambient)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.light_color_diffuse)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, self.light_color_specular)

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

                if self.is_view_box:
                    gl.glCallList(self.object + 3)  # lattice_parameters_abc_angles

                if self.is_view_axes:
                    gl.glCallList(self.object + 7)  # Axes
        except Exception as exc:
            print(exc)
            pass

    def render_text(self, text_to_render, font=QFont()):
        height = self.height()
        font_color = QColor.fromRgbF(0.0, 0.0, 0.0, 1)

        text_to_render.sort(key=lambda i: i[2], reverse=True)
        used_space = []

        # Render text
        font.setPointSize(self.font_size * self.quality)

        painter = QPainter(self)
        painter.setPen(font_color)
        
        painter.setFont(font)
        for row in text_to_render:
            fl = True
            x, y, z, st = row[0], row[1], row[2], row[3]
            if z > self.camera_position[2]:
                pos_x, pos_y, pos_z = self.get_screen_coords(x, y, z)
                pos_y = height - pos_y  # y is inverted
                for old in used_space:
                    if ((pos_x - old[0]) * (pos_x - old[0]) < 250) and ((pos_y - old[1]) * (pos_y - old[1]) < 250):
                        fl = False
                if fl:
                    used_space.append([pos_x, pos_y])
                    painter.drawText(pos_x - self.property_x_shift, pos_y - self.property_y_shift, st)
        painter.end()

    @staticmethod
    def nearest_point(scale_factor, ats, point):
        min_r1 = 10000
        ind1 = -1
        for at in range(0, len(ats)):
            rx2 = (point[0] - scale_factor * ats[at].x) ** 2
            ry2 = (-point[1] - scale_factor * ats[at].y) ** 2
            rz2 = (point[2] - scale_factor * ats[at].z) ** 2
            r = math.sqrt(rx2 + ry2 + rz2)
            if r < min_r1:
                min_r1 = r
                ind1 = at
        return ind1, min_r1

    def get_atom_on_screen(self):
        point = self.get_point_in_3d(self.x_scene, self.y_scene)
        old_selected = self.selected_atom
        ind, min_r = self.nearest_point(self.scale_factor, self.main_model.atoms, point)
        self.update_selected_atom(ind, min_r)

        self.can_atom_search = False
        if old_selected != self.selected_atom:
            self.selected_atom_changed()
            self.add_atoms()
            self.add_bonds()
            self.update()

    def update_selected_atom(self, ind, min_r):
        if min_r < 1.4:
            if self.selected_atom != ind:
                if self.selected_atom >= 0:
                    self.main_model.atoms[self.selected_atom].set_selected(False)
                self.selected_atom = ind
                self.main_model.atoms[self.selected_atom].set_selected(True)
            else:
                if self.selected_atom >= 0:
                    self.main_model.atoms[self.selected_atom].set_selected(False)
                self.selected_atom = -1

    def new_atom_for_model(self, charge, let, position):
        xyz = position + self.coord0
        return Atom([xyz[0], xyz[1], xyz[2], let, charge])

    def scale(self, wheel):
        if self.active:
            if self.is_orthographic:
                self.scale_factor -= 0.05 * (wheel / 120)
                self.add_all_elements()
            else:
                self.camera_position[2] -= 0.5 * (wheel / 120)
            self.update()
            self.model_orientation_to_form()
            return True
        return False

    def set_gl_cull_face(self, state):
        self.is_gl_cull_face = state
        self.update()

    def get_model(self):
        model = deepcopy(self.main_model)
        model.move(-self.coord0)
        model.translated_atoms_remove()
        return model

    def property_precision_changed(self, precision):
        self.property_precision = precision

    def set_property_font_size(self, size):
        self.font_size = size

    def set_property_shift(self, dx, dy):
        self.property_x_shift = -dx
        self.property_y_shift = dy

    def set_orientation(self, rotation, camera_pos, scale):
        if self.scale_factor != scale:
            self.scale_factor = scale
            self.scale(0)
        self.camera_position = np.array(camera_pos)
        self.rotation_angles = np.array(rotation)
        self.update()

    def auto_zoom(self):
        self.scale_factor = 1.0
        model_size = max(self.main_model.size_x(), self.main_model.size_y()) + 0.2
        if model_size < 1:
            model_size = 1
        aspect = min(self.width() / self.height(), 1)

        if self.is_orthographic:
            self.scale_factor = aspect * 6.0 / model_size
        else:
            x_max = self.main_model.maxX()
            y_max = self.main_model.maxY()
            z_max = self.main_model.maxZ()
            rad = self.main_model.get_covalent_radii().max()
            h, w = self.height(), self.width()
            size = x_max + rad if h > w else y_max + rad
            dist = size / math.tan(math.radians(self.perspective_angle / 2))
            dist *= h / w
            y_dist = (y_max + rad) / math.tan(math.radians(self.perspective_angle / 2))
            dist = max(dist, y_dist)
            self.camera_position[:] = np.array([0, 0, -z_max - dist / 10])
            self.light0_position[2] = z_max + 2 * dist
        if self.scale_factor < 1e-2:
            self.scale_factor = 1e-2

    def image3d_to_file(self, f_name):
        self.grabFramebuffer().save(f_name)

    def set_form_elements(self, check_atom_selection=None, orientation_model_changed: Callable = None,
                          selected_atom_position: Callable = None, selected_atom_changed: Callable = None,
                          quality=1):
        """Set pointers for Form update.
            Args:
                check_atom_selection: ...
                orientation_model_changed: pointer to MainForm.orientation_model_changed();
                selected_atom_position: pointer to MainForm.selected_atom_position();
                selected_atom_changed: pointer to MainForm.selected_atom_changed();
                quality: ... .
        """
        self.is_check_atom_selection = check_atom_selection
        self.orientation_model_changed = orientation_model_changed
        self.selected_atom_position = selected_atom_position
        self.selected_atom_callback = selected_atom_changed
        self.quality = quality

    def selected_atom_data_to_form(self, a, b, c, d):
        self.selected_atom_position(a, np.array((b, c, d)))

    def model_orientation_to_form(self):
        self.orientation_model_changed(self.rotation_angles, self.camera_position, self.scale_factor)

    def selected_atom_properties_to_form(self):
        self.selected_atom_callback([self.selected_atom])

    def selected_atom_changed(self):
        if self.selected_atom >= 0:
            xyz = self.main_model[self.selected_atom].xyz - self.coord0
            self.selected_atom_data_to_form(self.main_model[self.selected_atom].charge, xyz[0], xyz[1], xyz[2])
            if self.selected_fragment_mode:
                self.main_model[self.selected_atom].fragment1 = not self.main_model[self.selected_atom].fragment1
                self.atoms_of_selected_fragment_to_form()
        else:
            self.selected_atom_data_to_form(0, 0, 0, 0)
        self.selected_atom_properties_to_form()

    def set_structure_parameters(self, atoms_colors, is_view_atoms, is_view_atom_numbers, is_view_box, box_color,
                                 is_view_bonds, bonds_color, bond_width, bonds_by_atoms, is_view_axes, axes_color,
                                 contour_width: int = 8):
        self.prop = "charge"
        self.is_view_box = is_view_box
        self.is_view_atoms = is_view_atoms
        self.is_atomic_numbers_visible = is_view_atom_numbers
        self.is_view_bonds = is_view_bonds
        self.color_of_bonds_by_atoms = bonds_by_atoms
        self.bond_width = bond_width
        self.is_view_axes = is_view_axes
        self.color_of_axes = axes_color
        self.color_of_atoms = atoms_colors
        self.color_of_bonds = bonds_color
        self.color_of_box = box_color
        self.contour_width = contour_width
        self.add_all_elements()
        self.update()

    def set_atomic_structure(self, structure):
        self.clean()
        self.selected_atom = -1
        self.main_model = deepcopy(structure)
        self.coord0 = -self.main_model.get_center_of_mass()
        self.main_model.move(self.coord0)
        self.active = False
        self.auto_zoom()
        self.main_model.find_bonds_fast()
        self.add_all_elements()
        self.update()
