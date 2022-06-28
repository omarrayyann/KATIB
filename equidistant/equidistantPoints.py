import math
import pygame
import os
import csv

cwd = os.getcwd()
Data_path = cwd+"/letters/"
letter_paths = os.listdir(Data_path)
points = []

# Enter letter name
letter = "Ayn"

with open(Data_path+'' + letter + ".csv", 'r') as csvfile:
    coords = csv.reader(csvfile, delimiter=' ')
    x = []
    y = []
    for row in coords:
        if len(row) > 1:
            x = (int(0+50+(0.7*1000)*(float(row[0]))))
            y = (int(0+50+(0.8*800)*(float(row[1]))))
            points.append((x, y))


def distance(point1, point2):
    dx = point2[0]-point1[0]
    dy = point2[1]-point1[1]
    return (abs(dy**2 + dx**2))**0.5


def averagePoint(point1, point2):
    x = (point2[0]+point1[0])/2
    y = (point2[1]+point1[1])/2
    return [x, y]


def equalDisatantPoints(points, d):
    newPoints = [[points[0][0], points[0][1]]]
    lastPoint = points[0]
    for i in range(len(points)):
        if (distance(newPoints[len(newPoints)-1], points[i]) > d):
            newPoints.append(points[i])
    return newPoints


def resample(points, howMany):
    # v dumb way, there might be a library that does this better
    newPoints = points
    for m in range(howMany):
        tempPoints = newPoints
        newPoints = []
        for i in range(len(tempPoints)):
            if len(newPoints) > 0:
                newPoints.append(averagePoint(
                    tempPoints[i], newPoints[len(newPoints)-1]))
                newPoints.append(tempPoints[i])
            else:
                newPoints.append(tempPoints[i])
    return newPoints


def equidistant(points):
    resampledData = resample(points, 4)
    newPoints = equalDisatantPoints(resampledData, 30)
    return newPoints


pygame.init()
screen = pygame.display.set_mode((1000, 800))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    newPoints = equidistant(points)

    for i in range(len(newPoints)):
        pygame.draw.circle(screen, (0, 0, 255), newPoints[i], 10)

    pygame.display.flip()

pygame.quit()
