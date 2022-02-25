# -*- coding: utf-8 -*-

from copy import deepcopy
from utils import helpers
import numpy as np
from skimage.measure import marching_cubes
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
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + cont[i][j][1] * spacing[1], origin[2] + _slice * spacing[2]])
                    if type_of_plane == "xz":
                        contour.append([origin[0] + cont[i][j][0] * spacing[0], origin[1] + _slice * spacing[1], origin[2] + cont[i][j][1] * spacing[2]])
                    if type_of_plane == "yz":
                        contour.append([origin[0] + _slice * spacing[0], origin[1] + cont[i][j][0] * spacing[1], origin[2] + cont[i][j][1] * spacing[2]])
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
