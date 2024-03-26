# -*- coding: utf-8 -*-

from typing import Tuple

import math
import random
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from numpy import polyfit
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi

from core_atomistic import helpers


def gaps(bands, emaxf, eminf, homo, lumo) -> Tuple[float, float]:
    gap = emaxf - eminf
    for band in bands:
        for i in range(0, len(band) - 1):
            if band[i] * band[i + 1] <= 0:
                gap = 0
    if gap > 0:
        for i in range(0, len(bands[0])):
            if lumo[i] - homo[i] < gap:
                gap = lumo[i] - homo[i]
    homo_max = homo[0]
    lumo_min = lumo[0]
    for i in range(0, len(bands[0])):
        if homo[i] > homo_max:
            homo_max = homo[i]
        if lumo[i] < lumo_min:
            lumo_min = lumo[i]
    gap_ind = lumo_min - homo_max
    return gap, gap_ind


def VoronoiAnalisis(model, selected_atom, max_dist):
    new_model = model.grow()
    new_model.move_atoms_to_cell()
    atoms_to_analise = new_model.indexes_of_atoms_in_sphere(range(0, len(new_model.atoms)), selected_atom, max_dist)
    points = np.empty((len(atoms_to_analise), 3))
    k = 0
    for i in atoms_to_analise:
        points[k][0] = new_model[i].x
        points[k][1] = new_model[i].y
        points[k][2] = new_model[i].z
        k += 1

    vor = Voronoi(points)

    indices = vor.regions[vor.point_region[0]]
    if -1 in indices:  # some regions can be opened
        vol = np.inf
    else:
        vol = ConvexHull(vor.vertices[indices]).volume

    regions = []
    for i in range(0, len(vor.point_region)):
        regions.append(vor.regions[vor.point_region[i]])

    point_ridges = []
    for ridge in vor.ridge_vertices:
        if (len(list(set(ridge) - set(regions[0]))) == 0) and (len(ridge) > 0):
            point_ridges.append(ridge)

    list_of_poligons = []

    if point_ridges.count(-1) == 0:
        for rid in point_ridges:
            poligon = []
            for ind1 in rid:
                x = vor.vertices[ind1][0]
                y = vor.vertices[ind1][1]
                z = vor.vertices[ind1][2]
                poligon.append([x, y, z])
                list_of_poligons.append(poligon)
    return list_of_poligons, vol


class Calculators:
    @staticmethod
    def fParabola(x, b0, b1, b2):
        return b0 + b1 * x + b2 * x**2

    @staticmethod
    def approx_parabola(data):
        xdata, ydata = helpers.list_n2_split(data)
        # y = ax^2 + bx + c
        a, b, c = polyfit(xdata, ydata, 2)

        xmin = xdata.min()
        xmax = xdata.max()

        x = np.linspace(xmin, xmax, 200)
        y = Calculators.fParabola(x, c, b, a)

        return [c, b, a], x.tolist(), y.tolist()

    @staticmethod
    def fMurnaghan(parameters, vol):
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]
        return E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1.)

    @staticmethod
    def fBirchMurnaghan(parameters, vol):
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]
        alpha = pow(V0/vol, 2.0/3.0)
        return E0 + 9*V0*B0/16*(((alpha-1)**3)*BP + (alpha-1)**2*(6-4*alpha))

    def objectiveMurnaghan(pars, y, x):
        err = y - Calculators.fMurnaghan(pars, x)
        return err

    def objectiveBirchMurnaghan(pars, y, x):
        err = y - Calculators.fBirchMurnaghan(pars, x)
        return err

    @staticmethod
    def approx_murnaghan(DATA):
        v, e = helpers.list_n2_split(DATA)
        vfit = np.linspace(min(v), max(v), 100)
        # y = ax^2 + bx + c
        a, b, c = polyfit(v, e, 2)

        # initial guesses
        v0 = -b/(2*a)
        e0 = a*v0**2 + b*v0 + c
        b0 = 2*a*v0
        bP = 4

        x0 = [e0, b0, bP, v0]
        murnpars, ier = leastsq(Calculators.objectiveMurnaghan, x0, args=(e, v))
        return murnpars, vfit.tolist(), Calculators.fMurnaghan(murnpars, vfit).tolist()

    @staticmethod
    def approx_birch_murnaghan(data):
        v, e = helpers.list_n2_split(data)
        vfit = np.linspace(min(v), max(v), 100)

        # fit a parabola to the data
        # y = ax^2 + bx + c
        a, b, c = polyfit(v, e, 2)

        # initial guesses
        v0 = -b/(2*a)
        e0 = a*v0**2 + b*v0 + c
        b0 = 2*a*v0
        bP = 4

        x0 = np.array([e0, b0, bP, v0])
        murnpars, ier = leastsq(Calculators.objectiveBirchMurnaghan, x0, args=(e, v))
        return murnpars, vfit.tolist(), Calculators.fMurnaghan(murnpars, vfit).tolist()
