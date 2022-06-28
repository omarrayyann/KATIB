import math
import os
import pygame
from scipy import interpolate
import numpy as np
import csv
import os
import string

pygame.init()
screen = pygame.display.set_mode((800, 800))
(width, height) = screen.get_size()
minDist = 15
screen.fill((255, 255, 255))
cwd = os.getcwd()
Data_path = "../Letters_Data/Arabic/Data_Equidistant/"
new_data_path = "../Letters_Data/Arabic/Data_Equidistant_KMCP/"
running = True
fetched = False
smoothened = False
padding = 50
pygame.display.flip()
points = []
raw_points = []
smooth_points = []
new_smooth_points = []
angles = []
KMCP = []
letter_paths = os.listdir(Data_path)
lettersX = []
lettersY = []

for file_name in letter_paths:

    with open(Data_path + '' + file_name, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=' ')
        POINTS = []
        x = []
        y = []
        for row in coords:
            if len(row) > 1:
                x.append((int(0 + 50 + (0.8 * 800) * (float(row[0])))))
                y.append((int(0 + 50 + (0.8 * 800) * (float(row[1])))))
                POINTS.append((x[len(x) - 1], y[len(y) - 1]))
    lettersX.append(x)
    lettersY.append(y)
    points.append(POINTS)

def fetch_points():
    global fetched, width, height, raw_points
    delim = ' '
    raw_points = []
    points = []
    cwd = os.getcwd()
    Data_path = cwd + "/Letters_Data/Arabic/Data_converted/Waw.csv"
    with open(Data_path, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=delim)
        for row in coords:
            if len(row) > 1:
                raw_points.append(((float(row[0]) * (width - 2 * padding) + padding), (float(row[1]) * (height - 2 * padding) + padding)))
    for i in range(0, len(raw_points), 2):
        points.append(raw_points[i])
    fetched = True
    return raw_points, points


def draw_points(points, color, size):
    global screen
    for point in points:
        pygame.draw.circle(screen, color, point, size)

def distance(point1, point2):
    return math.sqrt(math.pow(point1[0]-point2[0], 2) + math.pow(point1[1] - point2[1], 2))

def remove_duplicates(points):
    global minDist
    clean = points
    for i in range(len(points) - 2, 0, -1):
        if (distance(points[i], points[i+1]) < minDist):
            # print("removed something haha")
            clean.remove(points[i])
            # print(len(clean))
    return clean

def calculate_angles(points):
    angles = []
    for i in range(len(points) - 1):
        delta_x = points[i+1][0] - points[i][0]
        # print(delta_x)
        delta_y = points[i+1][1] - points[i][1]
        # print(delta_y)
        theta = math.atan2(delta_y, delta_x)
        angles.append(theta)
        # print(theta)
    return angles

def fill_V(points):
    angles = calculate_angles(points)
    T = 0*math.pi / 180
    DELTAS = []
    V = []
    V.append(points[0])
    DELTAS.append(angles[1] - angles[0])
    DELTAS.append(angles[2] - angles[1])
    for i in range(2, len(angles) - 1):
        delta_angles = angles[i+1] - angles[i]
        # print(delta_angles)
        DELTAS.append(delta_angles)
        # if (delta_angles == 0):
        #     continue
        # product_angles = DELTAS[i] * DELTAS[i - 1]
        # if (product_angles <= 0) and (DELTAS[i - 1] != 0):
        # if math.fabs(delta_angles) > T:
        #     # print(product_angles)
        #     V.append(points[i - 1])
        if (DELTAS[i] < DELTAS[i - 1] < DELTAS[i - 2]) and math.fabs(DELTAS[i - 1]) > T and points[i - 1] not in V:
            V.append(points[i - 1])
        elif (DELTAS[i] > DELTAS[i - 1] > DELTAS[i - 2]) and math.fabs(DELTAS[i - 1]) > T and points[i - 1] not in V:
            V.append(points[i - 1])
        elif (math.fabs(DELTAS[i-1]) > math.pi / 2) and points[i - 1] not in V:
            V.append(points[i - 1])
    V.append(points[len(points) - 1])
    return V

def B_spline(waypoints):
    x = []
    y = []
    for point in waypoints:
        x.append(point[0])
        y.append(point[1])
    print(len(waypoints))
    tck, *rest = interpolate.splprep([x, y])
    u = np.linspace(0, 1, num=75)
    smooth = interpolate.splev(u, tck)
    x_smooth, y_smooth = smooth
    strings = []
    for (x, y) in zip(x_smooth, y_smooth):
        strings.append(
            str(x / int(0 + 50 + (0.8 * 800))) + " " + str(y / int(0 + 50 + (0.8 * 800))))
    return strings
    #         for (x, y) in zip(x_smooth, y_smooth):
    #             smooth.append((x, y))


#
# while (running):
#     pygame.display.flip()
#     screen.fill((255, 255, 255))
#     if not fetched:
#         raw_points, points = fetch_points()
#         raw_points = remove_duplicates(raw_points)
#         # print(len(raw_points))
#         KMCP = fill_V(raw_points)
#         # angles = calculate_angles(points)
#     elif not smoothened:
#         # smooth_points = B_spline(points)
#         # x_smooth, y_smooth = smooth_points
#         # smooth = []
#         # for (x, y) in zip(x_smooth, y_smooth):
#         #     smooth.append((x, y))
#         # smooth_points = smooth
#
#         new_smooth_points = B_spline(KMCP)
#         x_smooth, y_smooth = new_smooth_points
#         smooth = []
#         for (x, y) in zip(x_smooth, y_smooth):
#             smooth.append((x, y))
#         new_smooth_points = smooth
#
#         smoothened = True
#     else:
#         draw_points(raw_points, (0, 0, 0), 10)
#         # draw_points(smooth_points, (200, 100, 50), 5)
#         draw_points(new_smooth_points, (50, 100, 255), 5)
#         draw_points(KMCP, (0, 255, 0), 2)
#         pygame.draw.circle(screen, (100, 100, 100), raw_points[0], 5)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if not smoothened:
        i = 0
        for file_name in letter_paths:
            KMCP = fill_V(points[i])
            newPoints = B_spline(KMCP)
            with open(new_data_path + '' + file_name, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([c.strip() for c in r.strip(', ').split(',')] for r in newPoints)
            print('step')
            i += 1
        smoothened = True
        print('done')

    # for i in range(len(newPoints)):
    #     pygame.draw.circle(screen, (0, 0, 255), newPoints[i], 10)

    pygame.display.flip()


pygame.quit()
