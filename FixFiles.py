import os
import csv

delim = ' ';
x = []
y = []
raw_points = []
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