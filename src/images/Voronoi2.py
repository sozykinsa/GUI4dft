import scipy as sp
import scipy.spatial as sptl

base_pts = sp.rand(10, 3)*1000
vor = sptl.Voronoi(points=base_pts)

edges = [[], []]
for facet in vor.ridge_vertices:
    # Create a closed cycle of vertices that define the facet
    edges[0].extend(facet[:-1]+[facet[-1]])
    edges[1].extend(facet[1:]+[facet[0]])
edges = sp.vstack(edges).T  # Convert to scipy-friendly format
mask = sp.any(edges == -1, axis=1)  # Identify edges at infinity
edges = edges[~mask]  # Remove edges at infinity
edges = sp.sort(edges, axis=1)  # Move all points to upper triangle
# Remove duplicate pairs
edges = edges[:, 0] + 1j*edges[:, 1]  # Convert to imaginary
edges = sp.unique(edges)  # Remove duplicates
edges = sp.vstack((sp.real(edges), sp.imag(edges))).T  # Back to real
edges = sp.array(edges, dtype=int)
print(edges)