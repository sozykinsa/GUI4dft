# -*- coding: utf-8 -*-

from typing import Tuple

import math
import random
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from numpy import polyfit
from numpy.linalg import norm
from scipy.optimize import leastsq
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi

from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
from core_atomistic import helpers
from models.carbon_structure import CarbonStructure


def nearest_hexagon_run(ar):
    return ar[0].nearest_hexagon_of_swnt(ar[1], ar[2])


def hops(models):
    models[0].move_atoms_to_cell()
    new_model = CarbonStructure(models[0])
    atlist = models[0].indexes_of_atoms_with_charge(3)

    hexagons = new_model.hexagons_of_swnt()

    for atom in atlist:
        arg = [[CarbonStructure(model), atom, hexagons] for model in models]
        with ThreadPoolExecutor(max_workers=4) as pool:
            neighbors = list(pool.map(nearest_hexagon_run, arg))
        times = []
        kol = 0

        neighbor = neighbors[0]
        for mol in range(0, len(neighbors)):
            neighbor1 = neighbors[mol]
            if neighbor == neighbor1:
                kol += 1
            else:
                times.append([kol, neighbor])
                kol = 0
                neighbor = neighbor1

        if kol > 0:
            times.append([kol, neighbor])

        print("final:")
        for j in range(0, len(times)):
            field = str(j) + "   " + str(times[j][0]) + "   " + str(times[j][1])
            print(field)


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


def fill_tube(rad_tube, length: float, n_atoms: int, rad_atom, delta, n_prompts: int, let, charge: int):
    """Getting a list of configurations from nAtoms with a radius of radAtom in a cylinder with a radius of radTube
    length. The maximum displacement of atoms in each of the models is not less than delta."""
    models = []
    random.seed(a=None, version=2)

    for i in range(0, n_prompts):
        molecule = AtomicModel()
        j = 0

        while (j < 1000) and (len(molecule.atoms) < n_atoms):
            x = random.uniform(-rad_tube, rad_tube)
            a = math.sqrt(rad_tube * rad_tube - x * x)
            y = random.uniform(-a, a)
            z = random.uniform(0, length)
            molecule.add_atom(Atom([x, y, z, let, charge]), 2 * rad_atom)
            j += 1

        if len(molecule.atoms) < n_atoms:
            rad_atom *= 0.95
            print("Radius of atom was dicreased. New value: " + str(rad_atom))

        if len(molecule.atoms) == n_atoms:
            my_delta = 4 * rad_tube + length
            for newMolecula in models:
                myDelta2 = molecule.delta(newMolecula)
                if myDelta2 < my_delta:
                    my_delta = myDelta2
            if my_delta > delta:
                models.append(molecule)
                print("Iter " + str(i) + "/" + str(n_prompts) + "| we found " + str(len(models)) + " structures")
            if len(models) == 0:
                models.append(molecule)
    return models


def add_adatom(model, n):
    model_hexa = CarbonStructure(model)
    hexagons = model_hexa.hexagons_of_swnt()
    n_hexa = len(hexagons)
    print(n_hexa)
    centers = hexagon_centers(model_hexa, hexagons)
    n = n_hexa - 2
    if n > n_hexa:
        print("Not enough positions")
    else:
        #for i in combinations([str(k) for k in range(n_hexa)], n):
        #    print(i, ' - '.join(i))
        pass
    return []


def hexagon_centers(model, hexagons, normal=0):
    pos = model.get_positions()
    for hexagon in hexagons:
        inds = np.array(hexagon, dtype=int)
        vertices =pos[inds]
        total = np.sum(vertices, axis=0) / 6
        print(total)

        # Example usage
        point_on_perpendicular = find_perpendicular_point(vertices)
        print("Coordinates of the point on the perpendicular from the center:", point_on_perpendicular)
    pass


# Function to find the center of the hexagon
def find_center(vertices):
    center = np.mean(vertices, axis=0)
    return center


def find_normal_vector(vertices):
    v1 = vertices[1] - vertices[0]
    v2 = vertices[2] - vertices[0]
    normal_vector = np.cross(v1, v2)
    return normal_vector / norm(normal_vector)


# Function to find the coordinates of a point on the perpendicular
def find_perpendicular_point(vertices):
    center = find_center(vertices)
    # Assume the perpendicular distance to be 1 unit, you can change as needed
    perpendicular_distance = 1
    # Direction vector along the perpendicular
    direction_vector = find_normal_vector(vertices)
    perpendicular_point = center + perpendicular_distance * direction_vector
    return perpendicular_point


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
