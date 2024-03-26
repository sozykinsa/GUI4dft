# -*- coding: utf-8 -*-

import math
from copy import deepcopy
import numpy as np
from numpy.linalg import norm
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel
import random
from concurrent.futures import ThreadPoolExecutor


class CarbonStructure(AtomicModel):
    def __init__(self, atoms):
        if type(atoms) == list:
            AtomicModel.__init__(self, atoms)
        else:
            self.atoms = deepcopy(atoms.atoms)
            self.lat_vectors = deepcopy(atoms.lat_vectors)

    def nearest_hexagon_of_swnt(self, n_atom, hexagons):
        """The nearest Hexagon Of SWNT if all hexagons know."""
        hexagon = []
        if len(hexagons) != 0:
            radius = 500

            for nlist in hexagons:
                n = len(nlist)
                rad = 0
                for j in range(0, n):
                    rad += self.atom_atom_distance(nlist[j], n_atom)
                rad /= n

                if rad < radius:
                    radius = rad
                    hexagon = deepcopy(nlist)
        return hexagon

    def search_ring(self, atlist, i, n, neighbors, ring_size=6):
        """This function does not work correctly for very short models"""
        neighb = []
        nb = [[i]]
        for j in range(0, ring_size):
            nb1 = []
            while len(nb) > 0:
                nbr = nb.pop()
                for k in range(0, n):
                    if k not in set(nbr):
                        if neighbors[nbr[-1]][k] < 1.7:
                            nbr2 = deepcopy(nbr)
                            nbr2.append(k)
                            nb1.append(nbr2)
                        elif neighbors[nbr[0]][k] < 1.7:
                            nbr2 = deepcopy(nbr)
                            nbr2.insert(0, k)
                            nb1.append(nbr2)
            nb = deepcopy(nb1)
        for it in nb:
            if neighbors[it[0]][it[ring_size-1]] < 1.7:
                ats = []
                for i in range(0, ring_size):
                    ats.append(atlist[it[i]])
                neighb.append(ats)
        return neighb

    @staticmethod
    def remove_the_same(neighb):
        neig = []
        for it in neighb:
            set1 = set(it)

            fl = 1
            for it1 in neig:
                if set1 == set(it1):
                    fl = 0
            if fl == 1:
                neig.append(it)
        return deepcopy(neig)

    def hexagons_of_swnt(self):
        atlist = self.indexes_of_atoms_with_charge(6)
        neighbors = self.distances(atlist)
        n = len(atlist)

        neighb = []

        for i in range(0, n):
            nb = self.search_ring(atlist, i, n, neighbors)
            nb = self.remove_the_same(nb)
            for ring in nb:
                neighb.append(deepcopy(ring))
        neighb = self.remove_the_same(neighb)
        return neighb

    def distances(self, atlist):
        n = len(atlist)
        neighbors = np.zeros((n, n))
        for i in range(0, n):
            for j in range(0, n):
                neighbors[i][j] = self.atom_atom_distance(atlist[i], atlist[j])
        return neighbors


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
