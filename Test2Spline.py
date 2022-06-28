# imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, interp1d
import os
import csv

plt.rcParams['figure.figsize'] = (12, 8)

delim = ' '
raw_points = []
points = []
x = []
y = []
cwd = os.getcwd()
Data_path = cwd + "/Letters_Data/Arabic/Data_converted/Ayn.csv"
with open(Data_path, 'r') as csvfile:
    coords = csv.reader(csvfile, delimiter=delim)
    for row in coords:
        if len(row) > 1:
            raw_points.append((float(row[0]), float(row[1])))
for i in range(0, len(raw_points), 5):
    x.append(raw_points[i][0])
    y.append(raw_points[i][1])

for i in range(len(x)):
    print(x[i], ", ", y[i])

# apply cubic spline interpolation
cs = CubicSpline(x, y)
# Apply Linear interpolation
linear_int = interp1d(x, y)

xs = np.arange(-10, 10)
ys = linear_int(xs)

# plot linear interpolation
plt.plot(x, y, 'o', label='data')
plt.plot(xs, ys, label="S", color='green')
plt.legend(loc='upper right', ncol=2)
plt.title('Linear Interpolation')
plt.show()

# plot cubic spline interpolation
plt.plot(x, y, 'o', label='data')
plt.plot(xs, 1 / (1 + (xs ** 2)), label='true')
plt.plot(xs, cs(xs), label="S")
plt.plot(xs, cs(xs, 1), label="S'")
plt.plot(xs, cs(xs, 2), label="S''")
plt.plot(xs, cs(xs, 3), label="S'''")
plt.ylim(-1.5, 1.5)
plt.legend(loc='upper right', ncol=2)
plt.title('Cubic Spline Interpolation')
plt.show()