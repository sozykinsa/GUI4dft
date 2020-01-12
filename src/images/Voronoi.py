import numpy as np

import matplotlib.pyplot as plt
points = np.random.rand(10,3) #random
print(points)
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
print("res---------------------------")
print(vor.vertices)
print("res---------------------------")
print(vor.ridge_vertices)
print("res---------------------------")
print(vor.regions)

#fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
#plt.add_atoms()