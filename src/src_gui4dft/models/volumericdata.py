# -*- coding: utf-8 -*-

from copy import deepcopy
from core_gui_atomistic import helpers
import numpy as np
import skimage
if skimage.__version__ >= '0.17.2':
    from skimage.measure import marching_cubes
else:
    from skimage.measure import marching_cubes_lewiner
from skimage.measure import find_contours


class VolumericData:
    def __init__(self):
        self.filename = ""
        self.Nx = None
        self.Ny = None
        self.Nz = None
        self.blocks = []
        self.atoms = []
        self.data3D = np.zeros((1, 1))
        self.spacing = (0, 0, 0)
        self.origin = np.zeros(3)
        self.origin_to_export = np.zeros(3)
        self.type = "TVolumericData"

    def volumeric_data_read(self, f, orderData):
        ind = 0
        while ind < self.Nx * self.Ny * self.Nz:
            row = f.readline().split()
            for data in row:
                self.data3D[0, ind] = float(data)
                ind += 1
        f.readline()
        helpers.spacedel(f.readline())

        self.min = np.min(self.data3D)
        self.max = np.max(self.data3D)
        self.data3D = self.data3D.reshape((self.Nx, self.Ny, self.Nz), order=orderData)

    def difference(self, secondData, mult=1):
        if (self.Nx == secondData.Nx) and (self.Ny == secondData.Ny) and (self.Nz == secondData.Nz):
            for i in range(0, self.Nx):
                for j in range(0, self.Ny):
                    for k in range(0, self.Nz):
                        self.data3D[i][j][k] -= mult * secondData.data3D[i][j][k]
        self.min = np.min(self.data3D)
        self.max = np.max(self.data3D)

    def isosurface(self, value):
        if skimage.__version__ < '0.17.2':
            verts, faces, normals, values = marching_cubes_lewiner(self.data3D, level=value, spacing=self.spacing,
                                                                   gradient_direction='descent', step_size=1,
                                                                   allow_degenerate=True, use_classic=False)
        else:
            verts, faces, normals, values = marching_cubes(self.data3D, level=value, spacing=self.spacing,
                                                           gradient_direction='descent', step_size=1,
                                                           allow_degenerate=True, method='lewiner')

        for i in range(0, len(verts)):
            verts[i] += self.origin
        return verts, faces, normals

    def contours(self, values, type_of_plane="xy", _slice=5):
        conts = []
        spacing = self.spacing
        origin = self.origin
        r = []
        if type_of_plane == "xy":
            r = self.data3D[:, :, _slice]
        if type_of_plane == "xz":
            r = self.data3D[:, _slice, :]
        if type_of_plane == "yz":
            r = self.data3D[_slice, :, :]
        for value in values:
            cont = find_contours(r, value)
            contours = []
            for i in range(0, len(cont)):
                contour = []
                for j in range(0, len(cont[i])):
                    if type_of_plane == "xy":
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + cont[i][j][1] * spacing[1],
                                        origin[2] + _slice * spacing[2]])
                    if type_of_plane == "xz":
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + _slice * spacing[1],
                                        origin[2] + cont[i][j][1] * spacing[2]])
                    if type_of_plane == "yz":
                        contour.append([origin[0] + _slice * spacing[0], origin[1] + cont[i][j][0] * spacing[1],
                                        origin[2] + cont[i][j][1] * spacing[2]])
                contours.append(contour)
            conts.append(contours)
        return conts

    def plane(self, type_of_plane="xy", _slice=5):
        origin = deepcopy(self.origin)
        r = []
        spacing = [0, 0]
        if type_of_plane == "xy":
            r = self.data3D[:, :, _slice]
            origin[2] = self.origin[2] + _slice * self.spacing[2]
            spacing = [self.spacing[0], self.spacing[1]]

        if type_of_plane == "xz":
            r = self.data3D[:, _slice, :]
            origin[1] = self.origin[1] + _slice * self.spacing[1]
            spacing = [self.spacing[0], self.spacing[2]]

        if type_of_plane == "yz":
            r = self.data3D[_slice, :, :]
            origin[0] = self.origin[0] + _slice * self.spacing[0]
            spacing = [self.spacing[0], self.spacing[2]]

        Nx = len(r)
        Ny = len(r[0])
        points = []
        for i in range(0, Nx):
            row = []
            for j in range(0, Ny):
                x = i * spacing[0]
                y = j * spacing[1]
                z = 0
                if type_of_plane == "xz":
                    x, y, z = x, z, y
                if type_of_plane == "yz":
                    x, y, z = z, x, y
                x += origin[0]
                y += origin[1]
                z += origin[2]
                row.append([x, y, z, r[i][j]])
            points.append(row)
        return points

    def to_cube_text(self, model, x1, x2, y1, y2, z1, z2):
        text = "DATA.cube\n"
        text += "DATA.cube\n"
        mult = 0.52917720859

        n_x = x2 - x1
        n_y = y2 - y1
        n_z = z2 - z1

        multx = mult * self.Nx
        multy = mult * self.Ny
        multz = mult * self.Nz

        origin = self.origin_to_export + x1 * model.lat_vector1 / multx + y1 * model.lat_vector2 / multy + \
            z1 * model.lat_vector3 / multz

        text += str(model.n_atoms()) + "     " + str(origin[0]) + "    " + str(origin[1]) + "    " + str(origin[2])
        text += "\n " + str(n_x) + " "
        text += " " + str(model.lat_vector1[0] / multx) + "   " + str(model.lat_vector1[1] / multx) + "   " + \
                str(model.lat_vector1[2] / multx) + "\n"
        text += " " + str(n_y) + " "
        text += " " + str(model.lat_vector2[0] / multy) + "   " + str(model.lat_vector2[1] / multy) + "   " + \
                str(model.lat_vector2[2] / multy) + "\n"
        text += " " + str(n_z) + " "
        text += " " + str(model.lat_vector3[0] / multz) + "   " + str(model.lat_vector3[1] / multz) + "   " + \
                str(model.lat_vector3[2] / multz) + "\n"

        for atom in model.atoms:
            text += " " + str(atom.charge) + "     0.000000     " + str(atom.x / mult) + "    " + str(
                atom.y / mult) + "    " + str(atom.z / mult) + "\n"
        print("data start")

        new_data = self.data3D[x1:x2, y1:y2, z1:z2]
        new_n = new_data.size
        data_3d = np.reshape(new_data, new_n, 'C')
        print("text start: ", data_3d.size)

        text_ar = np.array2string(data_3d, threshold=data_3d.size)[1:-1]
        print(len(text_ar))

        #for i in range(0, data_3d.size):
        #    if i % 1000 == 0:
        #        print(i, "/", data_3d.size)
        #    text += str(data_3d[i]) + "   "
        text += text_ar
        print("stop")

        return text

    def to_xsf_text(self, model, x1, x2, y1, y2, z1, z2):
        text = "ATOMS\n"
        for atom in model.atoms:
            text += " " + str(atom.charge) + "    " + str(atom.x) + "    " + str(atom.y) + "    " + str(atom.z) + "\n"

        text += "BEGIN_BLOCK_DATAGRID_3D\n "
        text += "  DATA_from:GUI4DFT_diff\n"
        text += "  BEGIN_DATAGRID_3D_RHO:spin_1\n"
        text += " " + str(x2 - x1) + " " + str(y2 - y1) + " " + str(z2 - z1) + "\n"
        origin = self.origin_to_export
        text += " " + str(origin[0]) + " " + str(origin[1]) + " " + str(origin[2]) + "\n"

        vector1 = model.lat_vector1 * (x2 - x1) / self.Nx
        vector2 = model.lat_vector2 * (y2 - y1) / self.Ny
        vector3 = model.lat_vector3 * (z2 - z1) / self.Nz

        text += " " + str(vector1[0]) + "   " + str(vector1[1]) + "   " + str(vector1[2]) + "\n"
        text += " " + str(vector2[0]) + "   " + str(vector2[1]) + "   " + str(vector2[2]) + "\n"
        text += " " + str(vector3[0]) + "   " + str(vector3[1]) + "   " + str(vector3[2]) + "\n"

        new_data = self.data3D[x1:x2, y1:y2, z1:z2]
        new_n = new_data.size
        data_3d = np.reshape(new_data, new_n, 'F')

        for i in range(0, data_3d.size):
            text += str(data_3d[i]) + "   "

        text += "\n"

        text += " END_DATAGRID_3D\n"
        text += "END_BLOCK_DATAGRID_3D\n"

        return text
