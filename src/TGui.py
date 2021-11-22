# -*- coding: utf-8 -*-

import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QFont
from copy import deepcopy
from AdvancedTools import TAtom
from AdvancedTools import TAtomicModel
from AdvancedTools import TCalculators
from AdvancedTools import TPeriodTable
import math
import numpy as np

class mouse_events_filter(QObject):
    def __init__(self, wind):
        super(mouse_events_filter, self).__init__()
        self.window = wind

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            self.window.scale(event.angleDelta().y())

        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.LeftButton:
                self.window.rotat(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())
                self.window.setXY(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())

            elif event.buttons() == Qt.RightButton:
                if self.window.isAtomSelected():
                    self.window.move_atom(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())
                else:
                    if not self.window.CheckAtomSelection.isChecked():
                        self.window.move(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())
                self.window.setXY(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())

        elif event.type() == QEvent.MouseButtonPress:
            if self.window.CheckAtomSelection.isChecked() and event.buttons() == Qt.LeftButton:
                self.window.CanSearch = True
            self.window.setXY(event.x(), event.y(), self.window.openGLWidget.width(), self.window.openGLWidget.height())
        return False


class GuiOpenGL(object):
    def __init__(self, widget, CheckAtomSelection, selected_atom_info=[], quality=1):
        self.openGLWidget = widget
        self.MainModel = TAtomicModel()
        self.CheckAtomSelection = CheckAtomSelection
        if len(selected_atom_info) == 5:
            self.selected_atom_type = selected_atom_info[0]
            self.selected_atom_X = selected_atom_info[1]
            self.selected_atom_Y = selected_atom_info[2]
            self.selected_atom_Z = selected_atom_info[3]
            self.selected_atom_properties = selected_atom_info[4]
        self.quality = quality

        self.QuadObjS = []
        self.object = None
        self.NLists = 10
        self.history_of_atom_selection = []
        self.CanSearch = False
        self.xsOld = 0
        self.ysOld = 0

        self.x0 = 0
        self.y0 = 0
        self.z0 = 0

        self.init_params()

        self.openGLWidget.initializeGL()
        self.openGLWidget.paintGL = self.paintGL
        self.openGLWidget.initializeGL = self.initializeGL
        self.openGLWidget.setMouseTracking(True)
        self.filter = mouse_events_filter(self)
        self.openGLWidget.installEventFilter(self.filter)

    def init_params(self, TheObject=None):
        if TheObject == None:
            self.ViewOrtho = True
            self.ViewAtoms = True
            self.ViewBox = False
            self.ViewBonds = True
            self.ViewSurface = False
            self.ViewContour = False
            self.ViewContourFill = False
            self.ViewVoronoi = False
            self.ViewBCP = False
            self.ViewBondpath = False
            self.active = False
            self.Scale = 1
            self.bondWidth = 20
            self.xScene = 0
            self.yScene = 0
            self.x = 0
            self.y = 0
            self.z = -20
            self.rotX = 0
            self.rotY = 0
            self.rotZ = 0
            self.selected_atom = -1
            self.selected_cp = -1
            self.prop = "charge"
            self.SelectedFragmentMode = False
            self.SelectedFragmentAtomsListView = None
            self.SelectedFragmentAtomsTransp = 1.0
            self.color_of_bonds = [0, 0, 0]
        else:
            self.ViewOrtho = TheObject.ViewOrtho
            self.ViewAtoms = TheObject.ViewAtoms
            self.ViewBox = TheObject.ViewBox
            self.ViewBonds = TheObject.ViewBonds
            self.ViewSurface = TheObject.ViewSurface
            self.ViewContour = TheObject.ViewContour
            self.ViewContourFill = TheObject.ViewContourFill
            self.ViewVoronoi = TheObject.ViewVoronoi
            self.ViewBCP = TheObject.ViewBCP
            self.ViewBondpath = TheObject.ViewBondpath
            self.active = TheObject.active
            self.Scale = TheObject.Scale
            self.bondWidth = TheObject.bondWidth
            self.xsOld = TheObject.xsOld
            self.ysOld = TheObject.ysOld
            self.xScene = TheObject.xScene
            self.yScene = TheObject.yScene
            self.x = TheObject.x
            self.y = TheObject.y
            self.z = TheObject.z
            self.rotX = TheObject.rotX
            self.rotY = TheObject.rotY
            self.rotZ = TheObject.rotZ
            self.selected_atom = TheObject.selected_atom
            self.selected_cp = TheObject.selected_cp
            self.prop = TheObject.prop
            self.SelectedFragmentMode = TheObject.SelectedFragmentMode
            self.SelectedFragmentAtomsListView = TheObject.SelectedFragmentAtomsListView
            self.SelectedFragmentAtomsTransp = TheObject.SelectedFragmentAtomsTransp
            self.MainModel = TheObject.MainModel
            self.color_of_atoms = TheObject.color_of_atoms
            self.color_of_bonds = TheObject.color_of_bonds
            self.color_of_bonds_by_atoms = TheObject.color_of_bonds_by_atoms
            self.color_of_box = TheObject.color_of_box
            self.ViewAxes = TheObject.ViewAxes

    def update(self):
        self.openGLWidget.update()

    def setSelectedFragmentMode(self, SelectedFragmentAtomsListView, SelectedFragmentAtomsTransp):
        if SelectedFragmentAtomsListView == None:
            if self.SelectedFragmentMode == True:
                self.SelectedFragmentAtomsListView.clear()
            self.SelectedFragmentAtomsListView = None
            self.SelectedFragmentMode = False
        else:
            self.SelectedFragmentMode = True
            self.SelectedFragmentAtomsListView = SelectedFragmentAtomsListView
            self.SelectedFragmentAtomsTransp = SelectedFragmentAtomsTransp
            self.atoms_of_selected_fragment_to_form()

    def atoms_of_selected_fragment_to_form(self):
        self.SelectedFragmentAtomsListView.clear()
        self.SelectedFragmentAtomsListView.addItems(['Atoms'])
        for i in range(0, len(self.MainModel.atoms)):
            if (self.MainModel.atoms[i]).fragment1:
                self.SelectedFragmentAtomsListView.addItems([str(i)])

    def color_atoms_with_property(self, prop):
        self.clean()
        self.prop = prop
        self.add_atoms()
        self.add_bonds()
        self.add_box()

    def color_atoms_with_charge(self):
        self.clean()
        self.prop = "charge"
        self.add_atoms()
        self.add_bonds()
        self.add_box()

    def selected_atom_changed(self):
        if self.selected_atom >= 0:
            x = self.MainModel[self.selected_atom].x - self.x0
            y = self.MainModel[self.selected_atom].y - self.y0
            z = self.MainModel[self.selected_atom].z - self.z0
            self.selected_atom_data_to_form(self.MainModel[self.selected_atom].charge, x, y, z)
            if self.SelectedFragmentMode:
                self.MainModel[self.selected_atom].fragment1 = not self.MainModel[self.selected_atom].fragment1
                self.atoms_of_selected_fragment_to_form()
        else:
            self.selected_atom_data_to_form(0, 0, 0, 0)
        self.selected_atom_properties_to_form()

    def selected_atom_data_to_form(self, a, b, c, d):
        self.selected_atom_type.setCurrentIndex(a)
        self.selected_atom_X.setValue(b)
        self.selected_atom_X.update()
        self.selected_atom_Y.setValue(c)
        self.selected_atom_Y.update()
        self.selected_atom_Z.setValue(d)
        self.selected_atom_Z.update()

    def selected_atom_properties_to_form(self):
        text = ""
        if self.selected_atom >= 0:
            text += "Selected atom: " + str(self.selected_atom + 1) + "\n"
            atom = self.MainModel.atoms[self.selected_atom]
            text += "Element: " + atom.let + "\n"
            for key in atom.properties:
                text += str(key) + ": " + str(atom.properties[key]) + "\n"

            if len(self.history_of_atom_selection) > 1:
                text += "\n\nHistory of atoms selection: "+str(self.history_of_atom_selection)+"\n"
                text += "Distance from atom " + str(self.history_of_atom_selection[-1] + 1) + " to atom " + str(self.history_of_atom_selection[-2] + 1) + " : "
                dist = self.MainModel.atom_atom_distance(self.history_of_atom_selection[-1], self.history_of_atom_selection[-2])
                text += str(round(dist/10, 6)) + " nm\n"

                if (len(self.history_of_atom_selection) > 2) and (self.history_of_atom_selection[-1] != self.history_of_atom_selection[-2]) and (self.history_of_atom_selection[-3] != self.history_of_atom_selection[-2]):
                    x1 = self.MainModel.atoms[self.history_of_atom_selection[-1]].x
                    y1 = self.MainModel.atoms[self.history_of_atom_selection[-1]].y
                    z1 = self.MainModel.atoms[self.history_of_atom_selection[-1]].z

                    x2 = self.MainModel.atoms[self.history_of_atom_selection[-2]].x
                    y2 = self.MainModel.atoms[self.history_of_atom_selection[-2]].y
                    z2 = self.MainModel.atoms[self.history_of_atom_selection[-2]].z

                    x3 = self.MainModel.atoms[self.history_of_atom_selection[-3]].x
                    y3 = self.MainModel.atoms[self.history_of_atom_selection[-3]].y
                    z3 = self.MainModel.atoms[self.history_of_atom_selection[-3]].z

                    vx1 = x1 - x2
                    vy1 = y1 - y2
                    vz1 = z1 - z2

                    vx2 = x3 - x2
                    vy2 = y3 - y2
                    vz2 = z3 - z2

                    a = vx1*vx2 + vy1*vy2 + vz1*vz2
                    b = math.sqrt(vx1*vx1 + vy1*vy1 + vz1*vz1)
                    c = math.sqrt(vx2 * vx2 + vy2 * vy2 + vz2 * vz2)

                    arg = a/(b*c)
                    if math.fabs(arg) > 1:
                        arg = 1

                    angle = math.acos(arg)

                    text += "Angle " + str(self.history_of_atom_selection[-1] + 1) + " - " + str(
                        self.history_of_atom_selection[-2] + 1) + " - " + str(
                        self.history_of_atom_selection[-3] + 1) + " : " + str(round(math.degrees(angle), 3)) + " degrees\n"

        if self.selected_cp >= 0:
            SysCoord = np.array([self.MainModel.LatVect1, self.MainModel.LatVect2, self.MainModel.LatVect3])
            obr = np.linalg.inv(SysCoord).transpose()
            text += "\nSelected critical point: " + str(self.selected_cp) + " "
            cp = self.MainModel.bcp[self.selected_cp]
            atoms = self.MainModel.atoms

            bond1 = cp.getProperty("bond1")
            bond2 = cp.getProperty("bond2")

            ind1, ind2 = self.MainModel.atoms_of_bond_path(self.selected_cp)

            text += atoms[ind1].let + str(ind1) + "-" + atoms[ind2].let + str(ind2)

            text += "\nCartesian: [" + str(cp.x) + "; " + str(cp.y) + "; " + str(cp.z) + "]\n"

            Coord = np.array([cp.x, cp.y, cp.z])
            res = obr.dot(Coord)
            x = res[0]
            y = res[1]
            z = res[2]
            text += "Fractional: [" + str(x) + "; " + str(y) + "; " + str(z) + "]\n"

            text += "Bond critical path: " + str(len(bond1)+len(bond2)) + " points (fractional):\n"
            for i in range(0, len(bond1)):
                Coord = np.array([bond1[len(bond1) - i - 1].x, bond1[len(bond1) - i - 1].y, bond1[len(bond1) - i - 1].z])
                res = obr.dot(Coord)
                x = res[0]
                y = res[1]
                z = res[2]
                text += str(x) + " " + str(y) + " " + str(z) + "\n"
            for i in range(0, len(bond2)):
                Coord = np.array([bond2[i].x, bond2[i].y, bond2[i].z])
                res = obr.dot(Coord)
                x = res[0]
                y = res[1]
                z = res[2]
                text += str(x) + " " + str(y) + " " + str(z) + "\n"

        if (self.selected_atom < 0) and (self.selected_cp < 0):
            text += "Select any atom or critical point"

        self.selected_atom_properties.setText(text)

    def isActive(self):
        return self.active

    def isAtomSelected(self):
        return self.selected_atom >= 0

    def copy_state(self, GUI):
        self.init_params(GUI)
        self.add_atoms()
        self.add_bonds()
        self.add_box()
        if self.ViewVoronoi:
            self.color_of_voronoi = GUI.color_of_voronoi
            self.add_voronoi(self.color_of_voronoi)
        if self.ViewContour:
            self.add_contour(GUI.data_contour)
        if self.ViewContourFill:
            self.add_colored_plane(GUI.data_contour_fill)
        if self.ViewSurface:
            self.add_surface(GUI.data_surface)
        self.openGLWidget.update()
        
    def screen2space(self, x, y, width, height):
        radius = min(width, height)*float(self.Scale)
        return (2.*x-width)/radius, -(2.*y-height)/radius

    def set_atomic_structure(self, structure, atomscolors, ViewAtoms, ViewBox, boxcolor, ViewBonds, bondscolor, bondWidth, Bonds_by_atoms, ViewAxes, axescolor, contour_width):
        self.clean()
        self.prop = "charge"
        self.MainModel = deepcopy(structure)
        cm = self.MainModel.centr_mass()
        self.x0 = -cm[0]
        self.y0 = -cm[1]
        self.z0 = -cm[2]
        self.MainModel.move(self.x0, self.y0, self.z0)
        self.ViewBox = ViewBox
        self.ViewAtoms = ViewAtoms
        self.ViewBonds = ViewBonds
        self.color_of_bonds_by_atoms = Bonds_by_atoms
        self.bondWidth = bondWidth
        self.ViewAxes = ViewAxes
        self.color_of_axes = axescolor
        self.ViewSurface = False
        self.ViewContour = False
        self.ViewContourFill = False
        self.active = False
        self.color_of_atoms = atomscolors
        self.add_atoms()
        self.color_of_bonds = bondscolor
        self.color_of_box = boxcolor
        self.MainModel.find_bonds_fast()
        self.contour_width = contour_width
        self.add_bonds()
        self.add_box()
        self.add_axes()
        self.add_bcp()
        self.add_bondpath()
        self.openGLWidget.update()

    def get_model(self):
        newModel = deepcopy(self.MainModel)
        newModel.move(-self.x0, -self.y0, -self.z0)
        return newModel

    def image3D_to_file(self, fname):
        self.openGLWidget.grabFramebuffer().save(fname)

    def atomic_structure_to_file(self, fname):
        newModel = self.get_model()
        if fname.find("POSCAR") >= 0:
            fname = fname.split(".")[0]
            newModel.toVASPposcar(fname)
        if fname.endswith(".inp"):
            newModel.toFireflyINP(fname)
        if fname.endswith(".fdf"):
            newModel.toSIESTAfdf(fname)
        if fname.endswith(".xyz"):
            newModel.toSIESTAxyz(fname)

    def volumeric_data_to_file(self, fname, volumeric_data):
        newModel = self.get_model()
        if fname.find("XSF") >= 0:
            fname = fname.split(".")[0]
            newModel.toXSFfile(fname, volumeric_data)
        if fname.find("cube") >= 0:
            fname = fname.split(".")[0]
            newModel.toCUBEfile(fname, volumeric_data)

    def delete_selected_atom(self):
        if self.selected_atom >= 0:
            self.MainModel.delete_atom(self.selected_atom)
            self.selected_atom = -1
            self.history_of_atom_selection = []
            self.ViewContour = False
            self.ViewContourFill = False
            self.ViewSurface = False
            self.MainModel.find_bonds_fast()
            self.add_atoms()
            self.add_bonds()
            self.openGLWidget.update()

    def add_new_atom(self):
        charge = self.selected_atom_type.currentIndex()
        if charge > 0:
            let = self.selected_atom_type.currentText()
            x = self.selected_atom_X.value() + self.x0
            y = self.selected_atom_Y.value() + self.y0
            z = self.selected_atom_Z.value() + self.z0
            newAtom = TAtom([x, y, z, let, charge])
            self.MainModel.add_atom(newAtom)
            self.ViewContour = False
            self.ViewContourFill = False
            self.ViewSurface = False
            self.add_atoms()
            self.add_bonds()
            self.openGLWidget.update()

    def modify_selected_atom(self):
        if self.selected_atom >= 0:
            charge = self.selected_atom_type.currentIndex()
            if charge > 0:
                let = self.selected_atom_type.currentText()
                x = self.selected_atom_X.value() + self.x0
                y = self.selected_atom_Y.value() + self.y0
                z = self.selected_atom_Z.value() + self.z0
                newAtom = TAtom([x, y, z, let, charge])
                self.MainModel.edit_atom(self.selected_atom, newAtom)
                self.ViewContour = False
                self.ViewContourFill = False
                self.ViewSurface = False
                self.add_atoms()
                self.add_bonds()
                self.openGLWidget.update()

    def set_color_of_atoms(self, colors):
        self.color_of_atoms = colors
        self.add_atoms()
        self.add_bonds()

    def set_color_of_bonds(self, color):
        self.color_of_bonds = color
        self.add_bonds()

    def set_color_of_voronoi(self, voronoicolor):
        self.add_voronoi(voronoicolor)

    def set_color_of_box(self, color):
        self.color_of_box = color
        self.add_box()
        self.openGLWidget.update()

    def set_color_of_axes(self, color):
        self.color_of_axes = color
        self.add_axes()
        self.openGLWidget.update()

    def set_bond_width(self, width):
        self.bondWidth = width
        self.add_bonds()
        self.openGLWidget.update()

    def set_bond_color(self, type):
        self.color_of_bonds_by_atoms = type
        self.add_bonds()
        self.openGLWidget.update()

    def set_contour_width(self, width):
        self.contour_width = width
        self.openGLWidget.update()

    def set_atoms_visible(self, state):
        self.ViewAtoms= state
        self.openGLWidget.update()

    def set_box_visible(self, state):
        self.ViewBox = state
        self.openGLWidget.update()

    def set_bonds_visible(self, state):
        self.ViewBonds = state
        self.openGLWidget.update()

    def set_axes_visible(self, state):
        self.ViewAxes = state
        self.openGLWidget.update()
    
    def scale(self, wheel):
        if self.active:
            self.Scale += 0.05*(wheel/120)
            self.openGLWidget.update()
            return True
    
    def rotat(self, x, y, width, height):
        if self.active:
            xs, ys = self.screen2space(x, y, width, height)
            self.rotY += 10*(xs-self.xsOld)
            self.rotX -= 10*(ys-self.ysOld)
            return True
    
    def move(self, x, y, width, height):
        if self.active:
            xs, ys = self.screen2space(x, y, width, height)
            self.x += xs - self.xsOld
            self.y += ys - self.ysOld
            self.xsOld = xs
            self.ysOld = ys
            return True
   
    def setXY(self, x, y, width, height):
        if self.active:
            self.xsOld, self.ysOld = self.screen2space(x, y, width, height)
            self.xScene, self.yScene = x, y
            self.openGLWidget.update()
            return True

    def move_atom(self, x, y, width, height):
        if self.active:
                dx = x - self.xScene
                dy = y - self.yScene
                mult = 0.01*self.Scale
                vect = mult*np.array([-dx, dy, 0])
                al = -math.pi * self.rotX / 180
                bet = -math.pi * self.rotY / 180
                gam = -math.pi * self.rotZ / 180
                vect = self.rotate_vector(vect, al, bet, gam)
                self.xScene, self.yScene = x, y
                self.MainModel.atoms[self.selected_atom].x -= vect[0]
                self.MainModel.atoms[self.selected_atom].y -= vect[1]
                self.MainModel.atoms[self.selected_atom].z -= vect[2]
                self.selected_atom_changed()

                self.add_atoms()
                self.add_bonds()
                self.ViewVoronoi = False
                self.ViewSurface = False
                self.ViewContourFill = False
                self.ViewContour = False
                return True

    def rotate_vector(self, vect, al, bet, gam):
        cos = math.cos(al)
        sin = math.sin(al)
        Mx = np.array([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
        cos = math.cos(bet)
        sin = math.sin(bet)
        My = np.array([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
        cos = math.cos(gam)
        sin = math.sin(gam)
        Mz = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        vect = Mx.dot(vect)
        vect = My.dot(vect)
        vect = Mz.dot(vect)
        return vect

    def rotate_un_vector(self, vect, al, bet, gam):
        cos = math.cos(al)
        sin = math.sin(al)
        Mx = np.array([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
        cos = math.cos(bet)
        sin = math.sin(bet)
        My = np.array([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
        cos = math.cos(gam)
        sin = math.sin(gam)
        Mz = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

        vect = Mz.dot(vect)
        vect = My.dot(vect)
        vect = Mx.dot(vect)
        return vect

    def add_bond(self, Atom1Pos, Atom2Pos, Radius=0.1, type = 'cylinder'):
        Radius2 = Radius
        if type == 'conus':
            Radius2 = 0
        Rel = [Atom2Pos[0]-Atom1Pos[0], Atom2Pos[1]-Atom1Pos[1], Atom2Pos[2]-Atom1Pos[2]]
        BindingLen = math.sqrt(math.pow(Rel[0], 2) + math.pow(Rel[1], 2) + math.pow(Rel[2], 2)) # высота цилиндра
        if (BindingLen != 0):
            Fall = 180.0/math.pi*math.acos(Rel[2] / BindingLen)
            Yaw = 180.0/math.pi*math.atan2(Rel[1], Rel[0])
       
            gl.glPushMatrix()
            gl.glTranslated(Atom1Pos[0], Atom1Pos[1], Atom1Pos[2])
            gl.glRotated(Yaw, 0, 0, 1)
            gl.glRotated(Fall, 0, 1, 0)
            glu.gluCylinder(glu.gluNewQuadric(),
                Radius, # /*baseRadius:*/
                Radius2, # /*topRadius:*/
                BindingLen, # /*height:*/
                self.quality*15, # /*slices:*/
                1) #/*stacks:*/
            gl.glPopMatrix()

    def clean(self):
        if self.active == True:
            gl.glDeleteLists(self.object, self.NLists)
        self.object = gl.glGenLists(self.NLists)

    def add_selected_atom(self):
        gl.glNewList(self.object+7, gl.GL_COMPILE)
        for at in self.MainModel.atoms:
            if at.isSelected():
                gl.glPushMatrix()
                gl.glTranslatef(at.x, at.y, at.z)
                self.QuadObjS.append(glu.gluNewQuadric())
                gl.glColor3f(1, 0, 0)
                glu.gluSphere(self.QuadObjS[-1], 0.35, 70, 70)
                gl.glPopMatrix()
        gl.glEndList()

    def update_view(self):
        self.clean()
        self.add_atoms()
        self.add_bonds()
        self.add_box()
        self.add_axes()
        self.update()
        
    def add_atoms(self):
        prop = self.prop
        mendeley = TPeriodTable()
        gl.glNewList(self.object, gl.GL_COMPILE)

        min_val = 0
        max_val = 0
        mean_val = 0

        if (len(prop) > 0) and (prop != "charge"):
            min_val = self.MainModel.atoms[0].properties[prop]
            max_val = self.MainModel.atoms[0].properties[prop]
            mean_val = self.MainModel.atoms[0].properties[prop]
            for at in self.MainModel.atoms:
                val = at.properties[prop]
                if min_val > val: min_val = val
                if max_val < val: max_val = val
                mean_val += val
            mean_val /= self.MainModel.nAtoms()

        for at in self.MainModel.atoms:
            gl.glPushMatrix()
            gl.glTranslatef(at.x, at.y, at.z)
            self.QuadObjS.append(glu.gluNewQuadric())
            rad = mendeley.Atoms[at.charge].radius/mendeley.Atoms[6].radius

            if not at.isSelected():
                if (len(prop) > 0) and (prop != "charge"):
                    val = at.properties[prop]
                    if val > mean_val:
                        gl.glColor3f(0, math.fabs((val-mean_val)/(max_val-mean_val)), 0)
                    else:
                        gl.glColor3f(0, 0, math.fabs((val-mean_val)/(min_val-mean_val)))
                else:
                    color = self.color_of_atoms[at.charge]
                    if self.SelectedFragmentMode and at.fragment1:
                        gl.glColor4f(color[0], color[1], color[2], self.SelectedFragmentAtomsTransp)
                    else:
                        gl.glColor3f(color[0], color[1], color[2])
                glu.gluSphere(self.QuadObjS[-1], 0.3*rad, self.quality*70, self.quality*70)
            else:
                gl.glColor3f(1, 0, 0)
                glu.gluSphere(self.QuadObjS[-1], 0.35*rad, self.quality*70, self.quality*70)
            gl.glPopMatrix()
        gl.glEndList()
        self.active = True

    def add_bonds(self):
        gl.glNewList(self.object + 2, gl.GL_COMPILE)
        gl.glColor3f(self.color_of_bonds[0], self.color_of_bonds[1], self.color_of_bonds[2])
        for bond in self.MainModel.bonds:
            x1 = self.MainModel.atoms[bond[0]].x
            y1 = self.MainModel.atoms[bond[0]].y
            z1 = self.MainModel.atoms[bond[0]].z
            x2 = self.MainModel.atoms[bond[1]].x
            y2 = self.MainModel.atoms[bond[1]].y
            z2 = self.MainModel.atoms[bond[1]].z

            if not self.color_of_bonds_by_atoms:
                x3 = (self.MainModel.atoms[bond[1]].x + self.MainModel.atoms[bond[0]].x) / 2
                y3 = (self.MainModel.atoms[bond[1]].y + self.MainModel.atoms[bond[0]].y) / 2
                z3 = (self.MainModel.atoms[bond[1]].z + self.MainModel.atoms[bond[0]].z) / 2
                coords = []
                coords.append([[x1, y1, z1], [x3, y3, z3], self.color_of_atoms[self.MainModel.atoms[bond[0]].charge]])
                coords.append([[x3, y3, z3], [x2, y2, z2], self.color_of_atoms[self.MainModel.atoms[bond[1]].charge]])
            else:
                coords = [[[x1, y1, z1], [x2, y2, z2], self.color_of_bonds]]

            for coord in coords:
                if self.SelectedFragmentMode and (self.MainModel.atoms[bond[0]].fragment1 or self.MainModel.atoms[bond[1]].fragment1):
                    gl.glColor4f(coord[2][0], coord[2][1], coord[2][2], self.SelectedFragmentAtomsTransp)
                else:
                    gl.glColor3f(coord[2][0], coord[2][1], coord[2][2])
                self.add_bond(coord[0], coord[1], self.bondWidth)
        gl.glEndList()

    def add_box(self):
        gl.glNewList(self.object + 3, gl.GL_COMPILE)
        gl.glColor3f(self.color_of_box[0], self.color_of_box[1], self.color_of_box[2])

        v1 = self.MainModel.LatVect1
        v2 = self.MainModel.LatVect2
        v3 = self.MainModel.LatVect3

        origin = - (v1 + v2 + v3) / 2

        p1 = origin
        p2 = origin + v1
        p3 = origin + v2
        p4 = p2 + v2
        p5 = origin + v3
        p6 = p2 + v3
        p7 = p3 + v3
        p8 = p4 + v3
        width = 0.03
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
        gl.glColor3f(self.color_of_axes[0], self.color_of_axes[1], self.color_of_axes[2])
        size = 2
        sizeCone = 0.2
        letter_height = sizeCone
        letter_width = 0.6*sizeCone
        width = 0.06
        self.QuadObjS.append(glu.gluNewQuadric())
        glu.gluSphere(self.QuadObjS[-1], 2*width, 70, 70)
        p0 = np.array([0, 0, 0])
        p1 = np.array([size, 0, 0])
        p1cone = np.array([size+sizeCone, 0, 0])
        p2 = np.array([0, size, 0])
        p2cone = np.array([0, size+sizeCone, 0])
        p3 = np.array([0, 0, size])
        p3cone = np.array([0, 0, size+sizeCone])
        self.add_bond(p0, p1, width)
        self.add_bond(p1, p1cone, 2*width, 'conus')
        self.add_bond(p0, p2, width)
        self.add_bond(p2, p2cone, 2 * width, 'conus')
        self.add_bond(p0, p3, width)
        self.add_bond(p3, p3cone, 2 * width, 'conus')
        # lets drow "X"
        pX = p1cone + np.array([0, 1.5 * sizeCone, 0])
        pX1 = pX + np.array([-0.5 * letter_width, -0.5 * letter_height, 0])
        pX2 = pX + np.array([+0.5 * letter_width, +0.5 * letter_height, 0])
        pX3 = pX + np.array([-0.5 * letter_width, +0.5 * letter_height, 0])
        pX4 = pX + np.array([+0.5 * letter_width, -0.5 * letter_height, 0])
        self.add_bond(pX1, pX2, 0.5 * width)
        self.add_bond(pX3, pX4, 0.5 * width)
        # lets drow "Y"
        pY = p2cone + np.array([0, 1.5 * sizeCone,  0])
        pY1 = pY
        pY2 = pY + np.array([0, +0.5 * letter_height, +0.5 * letter_width])
        pY3 = pY + np.array([0, -0.5 * letter_height, +0.5 * letter_width])
        pY4 = pY + np.array([0, +0.5 * letter_height, -0.5 * letter_width])
        self.add_bond(pY1, pY2, 0.5 * width)
        self.add_bond(pY3, pY4, 0.5 * width)
        # lets drow "Z"
        pZ = p3cone + np.array([1.5 * sizeCone, 0, 0])
        pZ1 = pZ + np.array([-0.5 * letter_height, 0, -0.5 * letter_width])
        pZ2 = pZ + np.array([+0.5 * letter_height, 0, +0.5 * letter_width])
        pZ3 = pZ + np.array([-0.5 * letter_height, 0,  +0.5 * letter_width])
        pZ4 = pZ + np.array([+0.5 * letter_height, 0,  -0.5 * letter_width])
        self.add_bond(pZ1, pZ3, 0.5 * width)
        self.add_bond(pZ1, pZ2, 0.5 * width)
        self.add_bond(pZ2, pZ4, 0.5 * width)
        gl.glEndList()

    def add_surface(self, data):
        self.data_surface = data
        gl.glNewList(self.object + 4, gl.GL_COMPILE)
        for surf in data:
            verts = surf[0]
            faces = surf[1]
            color = surf[2]
            gl.glColor4f(color[0], color[1], color[2], color[3])
            for face in faces:
                gl.glBegin(gl.GL_TRIANGLES)
                for point in face:
                    gl.glVertex3f(verts[point][0], verts[point][1], verts[point][2])
                gl.glEnd()
        gl.glEndList()
        self.ViewSurface = True
        self.openGLWidget.update()

    def add_bcp(self):
        gl.glNewList(self.object + 8, gl.GL_COMPILE)
        for at in self.MainModel.bcp:
            gl.glPushMatrix()
            gl.glTranslatef(at.x, at.y, at.z)
            self.QuadObjS.append(glu.gluNewQuadric())
            gl.glColor3f(1, 0, 0)
            mult = 1
            if at.isSelected():
                gl.glColor3f(0, 0, 1)
                mult = 1.3
            glu.gluSphere(self.QuadObjS[-1], 0.15*mult, self.quality*70, self.quality*70)
            gl.glPopMatrix()

        gl.glEndList()
        self.ViewBCP = True
        self.openGLWidget.update()

    def add_bondpath(self):
        gl.glNewList(self.object + 9, gl.GL_COMPILE)

        for cp in self.MainModel.bcp:
            self.add_critical_path(cp.getProperty("bond1opt"))
            self.add_critical_path(cp.getProperty("bond2opt"))

        gl.glEndList()
        self.ViewBondpath = True
        self.openGLWidget.update()

    def add_critical_path(self, bond):
        if not bond:
            return
        for i in range(1, len(bond)):
            x1 = bond[i - 1].x
            y1 = bond[i - 1].y
            z1 = bond[i - 1].z
            x2 = bond[i].x
            y2 = bond[i].y
            z2 = bond[i].z

            gl.glColor3f(0, 1, 0)
            self.add_bond([x1, y1, z1], [x2, y2, z2], 0.03)

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
        self.ViewContour = True
        self.openGLWidget.update()

    def add_colored_plane(self, data):
        self.data_contour_fill = data
        gl.glDeleteLists(self.object + 6, 1)
        gl.glNewList(self.object + 6, gl.GL_COMPILE)
        for plane in data:
            points = plane[0]
            colors = plane[1]
            Nx = len(points)
            Ny = len(points[0])
            gl.glBegin(gl.GL_TRIANGLES)
            for i in range(0, Nx-1):
                for j in range(0, Ny-1):
                    gl.glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
                    gl.glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
                    gl.glColor3f(colors[i+1][j][0], colors[i+1][j][1], colors[i+1][j][2])
                    gl.glVertex3f(points[i+1][j][0], points[i+1][j][1], points[i+1][j][2])
                    gl.glColor3f(colors[i][j+1][0], colors[i][j+1][1], colors[i][j+1][2])
                    gl.glVertex3f(points[i][j+1][0], points[i][j+1][1], points[i][j+1][2])
                    gl.glColor3f(colors[i][j+1][0], colors[i][j+1][1], colors[i][j+1][2])
                    gl.glVertex3f(points[i][j+1][0], points[i][j+1][1], points[i][j+1][2])
                    gl.glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
                    gl.glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])
                    gl.glColor3f(colors[i + 1][j+1][0], colors[i + 1][j+1][1], colors[i + 1][j+1][2])
                    gl.glVertex3f(points[i + 1][j+1][0], points[i + 1][j+1][1], points[i + 1][j+1][2])
            gl.glEnd()
        gl.glEndList()
        self.ViewContourFill = True
        self.openGLWidget.update()

    def add_voronoi(self, color, maxDist):
        self.color_of_voronoi = color
        volume = np.inf
        if self.selected_atom >= 0:
            ListOfPoligons, volume = TCalculators.VoronoiAnalisis(self.MainModel, self.selected_atom, maxDist)
            gl.glNewList(self.object+1, gl.GL_COMPILE)
            gl.glColor4f(color[0], color[1], color[2], 0.7)
            for poligon in ListOfPoligons:
                gl.glBegin(gl.GL_POLYGON)
                for point in poligon:
                    gl.glVertex3f(point[0], point[1], point[2])
                gl.glEnd()
            gl.glEndList()
            self.ViewVoronoi = True
            self.openGLWidget.update()
        return self.selected_atom, volume

    def paintGL(self):
        QOpenGLWidget.makeCurrent(self.openGLWidget)
        try:
            self.light_prepare()
            self.prepere_scene()
            if self.active:
                    self.prepare_orientation()
                    if self.ViewAtoms:
                        gl.glCallList(self.object)  # atoms

                    if self.ViewBCP:
                        gl.glCallList(self.object + 8)  # BCP

                    if self.CanSearch:
                        self.get_atom_on_screen()

                    if self.ViewBonds and (len(self.MainModel.bonds) > 0):
                        gl.glCallList(self.object + 2)  # find_bonds_exact

                    if self.ViewVoronoi:
                        gl.glCallList(self.object + 1)  # Voronoi

                    if self.ViewBox:
                        gl.glCallList(self.object + 3)  # lattice_parameters_abc_angles

                    if self.ViewSurface:
                        gl.glCallList(self.object + 4)  # Surface

                    if self.ViewContour:
                        gl.glCallList(self.object + 5)  # Contour

                    if self.ViewContourFill:
                        gl.glCallList(self.object + 6)  # ContourFill

                    if self.ViewAxes:
                        gl.glCallList(self.object + 7)  # Axes

                    if self.ViewBondpath:
                        gl.glCallList(self.object + 9)  # Bondpath

                    #self.renderText(900, 500, "GUI4dft");

        except Exception as exc:
            print(exc)
            pass

    def renderText(self, x, y, str_text, font=QFont()):
        # Identify x and y locations to render text within widget
        height = self.openGLWidget.height()
        point = self.get_point_in_3D(x, y)
        textPosX, textPosY, textPosZ = point[0], point[1], point[2]
        textPosY = height - textPosY # y is inverted

        fontColor = QColor.fromRgbF(0.0, 0.0, 0.0, 1)

        # Render text
        painter = QPainter(self.openGLWidget)
        painter.setPen(fontColor)
        painter.setFont(font)
        painter.drawText(textPosX, textPosY, str_text)
        painter.end()



    def light_prepare(self):
        # очищаем буфер кадра и глубины
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # свойства материала
        material_diffuse = [1.0, 1.0, 1.0, 1.0]
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, material_diffuse)

        light_sample = 0

        # установка источников света
        if light_sample == 1:
            """ направленный источник света """
            light0_diffuse = [0.4, 0.7, 0.2]
            light0_direction = [0.0, 0.0, 1.0, 0.0]

            gl.glEnable(gl.GL_LIGHT0)
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, light0_diffuse)
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light0_direction)

        #  --------------------------------------
        if light_sample == 2:
            """ точечный источник света убывание интенсивности с расстоянием отключено (по умолчанию) """
            light1_diffuse = [0.4, 0.7, 0.2]
            light1_position = [0.0, 0.0, 1.0, 1.0]

            gl.glEnable(gl.GL_LIGHT1)
            gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, light1_diffuse)
            gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, light1_position)

        if light_sample == 0:
            ambient = [0.5, 0.5, 0.5, 1]
            #ambient = [0.2 * self.Scale, 0.2 * self.Scale, 0.2 * self.Scale, 1]
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
            gl.glLightModelf(gl.GL_LIGHT_MODEL_TWO_SIDE, gl.GL_TRUE) # двухсторонний расчет освещения
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_LIGHT0)
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glEnable(gl.GL_COLOR_MATERIAL)

            lightpos = [5.0, 5.0, 100.0]

            if self.quality == 1:
                lightpos = self.lightpos_rotate(lightpos)

            gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightpos)  # Определяем положение источника света

    def lightpos_rotate(self, lightpos):
        # self.x0, self.y0, self.z0
        lightpos = [lightpos[0] - self.x0, lightpos[1] - self.y0, lightpos[2] - self.z0]

        alpha = - self.rotX * math.pi / 180
        # ox
        xnn = float(lightpos[1]) * math.cos(alpha) - float(lightpos[2]) * math.sin(alpha)
        ynn = float(lightpos[1]) * math.sin(alpha) + float(lightpos[2]) * math.cos(alpha)
        lightpos[1] = xnn
        lightpos[2] = ynn
        alpha = - self.rotY * math.pi / 180
        # oy
        xnn = float(lightpos[0]) * math.cos(alpha) + float(lightpos[2]) * math.sin(alpha)
        ynn = -float(lightpos[0]) * math.sin(alpha) + float(lightpos[2]) * math.cos(alpha)
        lightpos[0] = xnn
        lightpos[2] = ynn
        alpha = - self.rotZ * math.pi / 180
        # oz
        xnn = float(lightpos[0]) * math.cos(alpha) - float(lightpos[1]) * math.sin(alpha)
        ynn = float(lightpos[0]) * math.sin(alpha) + float(lightpos[1]) * math.cos(alpha)
        lightpos[0] = xnn
        lightpos[1] = ynn

        return [lightpos[0] + self.x0, lightpos[1] + self.y0, lightpos[2] + self.z0]

    def prepare_orientation(self):
        gl.glTranslated(self.x, self.y, self.z)
        gl.glRotate(self.rotX, 1, 0, 0)
        gl.glRotate(self.rotY, 0, 1, 0)
        gl.glRotate(self.rotZ, 0, 0, 1)
        gl.glScale(self.Scale, self.Scale, self.Scale)

    def prepere_scene(self):
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        x, y, width, height = gl.glGetDoublev(gl.GL_VIEWPORT)
        if self.ViewOrtho == False:
            glu.gluPerspective(
                45,  # field of view in degrees
                width / float(height or 1),  # aspect ratio
                .25,  # near clipping plane
                200)  # far clipping plane
        else:
            radius = .5 * min(width, height)
            w, h = width / radius, height / radius

            gl.glOrtho(-2 * w,  # GLdouble left
                       2 * w,  # GLdouble right
                       -2 * h,  # GLdouble bottom
                       2 * h,  # GLdouble top
                       -0.25,  # GLdouble near
                       200.0)  # GLdouble far
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def get_atom_on_screen(self):
        point = self.get_point_in_3D(self.xScene, self.yScene)

        oldSelected = self.selected_atom
        need_for_update = False

        ind, minr = self.nearest_point(self.MainModel.atoms, point)
        cp_ind, cp_minr = self.nearest_point(self.MainModel.bcp, point)

        if cp_minr < 1.4:
            if self.selected_cp == cp_ind:
                self.MainModel.bcp[self.selected_cp].setSelected(False)
                self.selected_cp = -1
            else:
                self.MainModel.bcp[self.selected_cp].setSelected(False)
                self.selected_cp = cp_ind
                self.MainModel.bcp[self.selected_cp].setSelected(True)
            need_for_update = True
            self.add_bcp()

        if minr < 1.4:
            if self.selected_atom >= 0:
                self.ViewVoronoi = False
            if self.selected_atom != ind:
                if self.selected_atom >= 0:
                    self.MainModel.atoms[self.selected_atom].setSelected(False)
                self.selected_atom = ind
                self.MainModel.atoms[self.selected_atom].setSelected(True)
            else:
                if self.selected_atom >= 0:
                    self.MainModel.atoms[self.selected_atom].setSelected(False)
                self.selected_atom = -1
            self.add_atoms()
            self.add_bonds()

        self.CanSearch = False
        if oldSelected != self.selected_atom:
            if self.selected_atom == -1:
                self.history_of_atom_selection = []
            else:
                self.history_of_atom_selection.append(self.selected_atom)
            need_for_update = True

        if need_for_update:
            self.selected_atom_changed()
            self.openGLWidget.update()

    def nearest_point(self, ats, point):
        minr1 = 10000
        ind1 = -1
        for at in range(0, len(ats)):
            rx2 = (point[0] - ats[at].x) ** 2
            ry2 = (-point[1] - ats[at].y) ** 2
            rz2 = (point[2] - ats[at].z) ** 2
            r = math.sqrt(rx2 + ry2 + rz2)
            if r < minr1:
                minr1 = r
                ind1 = at
        return ind1, minr1

    def get_point_in_3D(self, x, y):
        model = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
        proj = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
        view = gl.glGetIntegerv(gl.GL_VIEWPORT)
        winY = int(float(view[3]) - float(y))
        z = gl.glReadPixels(x, winY, 1, 1, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT)
        point = glu.gluUnProject(x, y, z, model, proj, view)
        al = math.pi * self.rotX / 180
        bet = 0 # math.pi * self.rotY / 180
        gam = math.pi * self.rotZ / 180
        point = self.rotate_un_vector(np.array(point), al, bet, gam)
        point = self.rotate_vector(np.array(point), al, bet, gam)
        return point

    def initializeGL(self):
        QOpenGLWidget.makeCurrent(self.openGLWidget)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(1)
        gl.glDepthFunc(gl.GL_LEQUAL)
        self.object = gl.glGenLists(self.NLists)
        gl.glNewList(self.object, gl.GL_COMPILE)
        gl.glEndList()
