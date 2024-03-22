# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy
from core_atomistic.atomic_model import AtomicModel


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
