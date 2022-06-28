import math
import pygame
import os
import csv

cwd = os.getcwd()
Data_path = "../Letters_Data/Arabic/Data_KMCP/"
new_data_path = "../Letters_Data/Arabic/Data_KMCP_Equidistant/"
points = []
newPoints = []
cleaned = False
lettersX = []
lettersY = []

# Enter letter name
letter = "Ayn"

letter_paths = os.listdir(Data_path)
# print(letter_paths)
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

# with open(Data_path+'' + letter + ".csv", 'r') as csvfile:
#     coords = csv.reader(csvfile, delimiter=' ')
#     x = []
#     y = []
#     for row in coords:
#         if len(row) > 1:
#             x = (int(0+50+(0.7*1000)*(float(row[0]))))
#             y = (int(0+50+(0.8*800)*(float(row[1]))))
#             points.append((x, y))


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
    strings = []
    for i in range(len(newPoints)):
        strings.append(str(newPoints[i][0] / int(0 + 50 + (0.8 * 800))) + " " + str(newPoints[i][1] / int(0 + 50 + (0.8 * 800))))
    return strings


pygame.init()
screen = pygame.display.set_mode((800, 800))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    if not cleaned:
        i = 0
        for file_name in letter_paths:
            newPoints = equidistant(points[i])
            with open(new_data_path + '' + file_name, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([c.strip() for c in r.strip(', ').split(',')] for r in newPoints)
            i += 1
        cleaned = True
        print('done')

    # for i in range(len(newPoints)):
    #     pygame.draw.circle(screen, (0, 0, 255), newPoints[i], 10)

    pygame.display.flip()



pygame.quit()
