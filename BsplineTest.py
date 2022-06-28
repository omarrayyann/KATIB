import pygame
from scipy import interpolate
import numpy as np
import csv
import os
import string

pygame.init()
screen = pygame.display.set_mode((800, 512))
(width, height) = screen.get_size()
screen.fill((255, 255, 255))
running = True
fetched = False
smoothened = False
padding = 50
pygame.display.flip()
points = []
raw_points = []
smooth_points = []


def fetch_points():
    global fetched, width, height
    delim = ' '
    raw_points = []
    points = []
    cwd = os.getcwd()
    Data_path = cwd + "/Letters_Data/Arabic/Data_converted/Ayn.csv"
    with open(Data_path, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=delim)
        for row in coords:
            if len(row) > 1:
                raw_points.append(
                    (float(row[0]) * (width - 2 * padding) + padding, float(row[1]) * (height - 2 * padding) + padding))
    for i in range(0, len(raw_points), 9):
        points.append(raw_points[i])
    fetched = True
    return raw_points, points


def draw_points(points, color, size):
    global screen
    for point in points:
        pygame.draw.circle(screen, color, point, size)


def B_spline(waypoints):
    x = []
    y = []
    for point in waypoints:
        x.append(point[0])
        y.append(point[1])
    tck, *rest = interpolate.splprep([x, y])
    u = np.linspace(0, 1, num=100)
    smooth = interpolate.splev(u, tck)
    return smooth


while (running):
    pygame.display.flip()
    screen.fill((255, 255, 255))
    if not fetched:
        raw_points, points = fetch_points()
    elif not smoothened:
        smooth_points = B_spline(points)
        smoothened = True
        x_smooth, y_smooth = smooth_points
        smooth = []
        for (x, y) in zip(x_smooth, y_smooth):
            smooth.append((x, y))
        smooth_points = smooth
    else:
        draw_points(raw_points, (0, 0, 0), 10)
        draw_points(smooth_points, (200, 100, 50), 5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
