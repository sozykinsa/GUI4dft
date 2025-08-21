# -*- coding: utf-8 -*-
import numpy as np


dat_file = "SURFRHOO.DAT"
out_file = "rho.dat"
mult = 0.529177249

f = open(dat_file)
row = f.readline()
row = f.readline()
nm = row.split()
n, m = int(nm[0]), int(nm[1])

row = f.readline()
x = row.split()
x_min, x_max, x_step = float(x[0]), float(x[1]), float(x[2])
x = np.linspace(x_min, x_max, n)

row = f.readline()
y = row.split()
y_min, y_max, y_step = float(y[0]), float(y[1]), float(y[2])
y = np.linspace(y_min, y_max, m)

data = []
row = f.readline()

while row:
    row = f.readline()
    data.extend(row.split())

print(n * m, len(data))
f.close()

f = open(out_file, "w")

count = 0
for coor_y in y:
    for coor_x in x:
        f.write(str(coor_x) + "   " + str(coor_y) + "   " + data[count] + "\n")
        count += 1
f.close()
