# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi


def VoronoiAnalisis(Molecula, selectedAtom, maxDist):
        new_model = Molecula.grow()
        new_model.move_atoms_to_cell()
        atoms_to_analise = new_model.indexes_of_atoms_in_sphere(range(0, len(new_model.atoms)), selectedAtom, maxDist)
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
