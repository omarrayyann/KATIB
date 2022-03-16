from asyncio import current_task
from cmath import sqrt
import pygame
import random
import time
import string
import os
import csv
import copy
import serial
import math
# from scipy import interpolate
# import numpy as np


# Functions


def generate_path_coordinates(from_point, n):
    randomX = random.uniform(
        screen_width/2 - screen_height/4.5, screen_width/2 + screen_height/4)

    a = (((screen_height/4)**2 - (randomX-screen_width/2)**2))**0.5

    randomY = random.uniform(-a, a)+screen_height/2

    to_point = point(randomX, randomY)

    m = (to_point.y-from_point.y)/(to_point.x-from_point.x)
    c = from_point.y - m*from_point.x
    domain = to_point.x - from_point.x
    x_step_size = domain/n
    points = []
    for i in range(n):
        points.append(point(from_point.x+x_step_size*i,
                            m*(from_point.x+x_step_size*i)+c))
    return points


def generate_path_coordinates_parabola(from_point, n):
    randomX = random.uniform(
        screen_width/2 - screen_height/4.5, screen_width/2 + screen_height/4)

    a = (((screen_height/4)**2 - (randomX-screen_width/2)**2))**0.5

    randomY = random.uniform(-a, a)+screen_height/2

    to_point = point(randomX, randomY)

    between_point = point(500, 400)

    x1 = from_point.x
    x2 = between_point.x
    x3 = to_point.x

    y1 = from_point.y
    y2 = between_point.y
    y3 = to_point.y

    C = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / C
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / C
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 *
         (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / C

    points = []
    domain = to_point.x - from_point.x
    x_step_size = domain/n

    for i in range(n):
        x = from_point.x+x_step_size*i
        y = A*(x**2)+B*(x)+C
        points.append(point(x, y))
    return points


def invKin(x_in, y_in):
    # x_in = 0.024+0.052*(1-(xs+xl-x_in)/xl)
    # y_in = 0.1171+0.047*((ys+yl-y_in)/yl)
    R = math.sqrt(x_in**2+y_in**2)
    k = math.atan(y_in/x_in)
    phi = math.acos(R/0.2)

    thetaL = math.degrees(k+phi)

    x_in = x_in-0.1

    R = math.sqrt(x_in**2+y_in**2)
    k = math.atan(y_in/x_in)
    phi = math.acos(R/0.2)

    thetaR = math.degrees((k-phi))

    return 90.0+thetaR, -90.0+thetaL


def getCoords(xn, yn):
    if xn < xs+xl and xn >= xs:
        xn = (xn-xs)/xl
    else:
        return
    if yn < ys+yl and yn >= ys:
        yn = (yn-ys)/yl
    else:
        return
    fx = 143*xn
    # fy= 0.00017125*yn+0.09431875
    fy = -95*yn
    return fx, fy


def roundline(srf, color, start, end, radius=10):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0]+float(i)/distance*dx)
        y = int(start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)


def magnet_visualizer():
    pygame.draw.circle(screen, (255, 215, 0), (x_magnet, y_magnet), 10)
    pygame.display.flip()

# Classes


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class camel:
    def __init__(self, point):
        self.point = point
        self.collected = False
        self.path_coordinates = generate_path_coordinates(point, 100)


# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Screen Setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Colors Setup
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Remote Work Magnet Visualization
startMagnetVisualization = False

x_magnet = 0
y_magnet = 0


# Other Configurtions Setup
draw_on = False
drowOn = False
radius = 10
boundaries = 60
screen_width, screen_height = pygame.display.get_surface().get_size()
xl = screen_width-(boundaries*2)
xs = boundaries
yl = screen_height-(boundaries*2)-40
ys = boundaries
flag = 1
new_points = []
points = []
camels = [camel(point(200, 200)), camel(point(1000, 700))]
collected = 0

# Serial Setup

# gSer=serial.Serial('/dev/ttyACM0','115200')
# time.sleep(3)
# gSer.flush()
# serL.write("r\n")
# serR.write("r\n")
# time.sleep(6.1)


# Setting Up Images
clear = pygame.image.load('clear.png').convert()
clear = pygame.transform.scale(clear, (50, 50))
clear = pygame.transform.rotate(clear, 180)
rectClear = clear.get_rect()
rectClear.center = (screen_width/2 + 75, screen_height-52)

load = pygame.image.load('load.png').convert()
load = pygame.transform.scale(load, (50, 50))
load = pygame.transform.rotate(load, 180)
rectLoad = load.get_rect()
rectLoad.center = (screen_width/2, screen_height-52)

startL = pygame.image.load('start.png').convert()
startL = pygame.transform.scale(startL, (50, 50))
startL = pygame.transform.rotate(startL, 180)
rectStart = startL.get_rect()
rectStart.center = (screen_width/2 - 75, screen_height-52)

closeL = pygame.image.load('exit.png').convert()
closeL = pygame.transform.scale(closeL, (50, 50))
rectClose = closeL.get_rect()
rectClose.center = (50, 100)

ResetMs = pygame.image.load('exit.png').convert()
ResetMs = pygame.transform.scale(ResetMs, (50, 50))
rectResetMs = ResetMs.get_rect()
rectResetMs.center = (50, 200)

pygame.draw.circle(screen, green, (int(xs), int(ys)), radius)
pygame.draw.circle(screen, blue, (int(xs+xl), int(ys+yl)), radius)

goal_box_x_center = screen_width/2
goal_box_y_center = screen_height/2
goal_box_width = 500
goal_box_height = 300
goal_box_start_x = goal_box_x_center-(goal_box_width/2)
goal_box_start_y = goal_box_y_center-(goal_box_height/2)

bg = pygame.image.load("bgg.jpg")
# screen.blit(bg, (0, 0))

camel_image = pygame.image.load("sheep.png")
camel_image = pygame.transform.flip(camel_image, True, False)
camel_image = pygame.transform.scale(camel_image, (100, 100))


def update_camels():
    screen.fill((106, 164, 82))
    # screen.blit(bg, (0, 0))
    # screen.blit(clear, rectClear)
    # screen.blit(load, rectLoad)
    screen.blit(startL, rectStart)
    rect = pygame.draw.rect(screen, (220, 182, 122), (xs, ys, xl, yl), 7)
    goal = pygame.draw.circle(screen, (204, 102, 20),
                              [screen_width/2, screen_height/2 - 20], screen_height/4, 7)
    for camel in points:
        pygame.draw.line(screen, (49, 74, 54), (camel[0].x,
                                                camel[0].y), (camel[len(camel)-1].x, camel[len(camel)-1].y), 15)
        pygame.draw.circle(screen, (49, 74, 54),
                           (camel[len(camel)-1].x, camel[len(camel)-1].y), 15)
        screen.blit(camel_image, (camel[0].x - 50, camel[0].y - 50))

    pygame.display.flip()


firstOpen = False

try:
    while True:
        # INSIDE OF THE GAME LOOP
        magnet_visualizer()
        if not firstOpen:
            firstOpen = True
            screen.fill((106, 164, 82))
            rect = pygame.draw.rect(
                screen, (220, 182, 122), (xs, ys, xl, yl), 7)
            goal = pygame.draw.circle(screen, (204, 102, 20),
                                      [screen_width/2, screen_height/2 - 20], screen_height/4, 7)

        # screen.blit(clear, rectClear)
        # screen.blit(load, rectLoad)
        screen.blit(startL, rectStart)

        for e in pygame.event.get():

            # e = pygame.event.wait()
            # keys=pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                raise StopIteration
            if (e.type == pygame.KEYDOWN):
                if e.key == pygame.K_q:
                    raise StopIteration
                if e.key == pygame.K_c:
                    screen.fill(black)
            if e.type == pygame.MOUSEBUTTONDOWN and rectClose.collidepoint(e.pos):
                raise StopIteration
# Reset Motors
            if e.type == pygame.MOUSEBUTTONDOWN and rectResetMs.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectResetMs, 5)
                pygame.display.flip()
                time.sleep(0.05)
                pygame.draw.rect(screen, black, rectResetMs, 5)
                pygame.display.flip()
                # serL.write("r\n")
                time.sleep(3)
                # serR.write("r\n")
# Clear check
            if e.type == pygame.MOUSEBUTTONDOWN and rectClear.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectClear, 5)
                pygame.display.flip()
                pygame.draw.rect(screen, black, rectClear, 5)
                time.sleep(0.05)
                drowOn = False
                screen.fill(black)
# Load check

    # no load for now

# Start check

            if e.type == pygame.MOUSEBUTTONDOWN and rectStart.collidepoint(e.pos):
                pygame.display.flip()
                time.sleep(0.05)
                # pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 5)
                collected = 0
                for camel in camels:
                    print("hulu", current)

                    points.append(camel.path_coordinates)

                    new_points.append(pygame.draw.circle(
                        screen, (200, 0, 0), (points[len(points)-1][0].x, points[len(points)-1][0].y), 20))
                    update_camels()

                    points[len(points)-1].pop(0)

                    pygame.display.flip()

                drowOn = True
                #
                # screen.fill(black)


# Drawing check

            if e.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(e.pos) and drowOn:

                draw_on = True
                if e.type == pygame.MOUSEBUTTONUP:
                    draw_on = False
            anyPoint = False
            current = 0
            for new_point in new_points:
                if new_point.collidepoint(e.pos):
                    newPoint = new_point
                    anyPoint = True
                    break
                current += 1

            if draw_on and e.type == pygame.MOUSEMOTION and rect.collidepoint(e.pos) and anyPoint and newPoint.collidepoint(e.pos):

                if len(points[current])-1 > 0:
                    flag = 1
                    xp0, yp0 = (points[current][0].x, points[current][0].y)
                    points[current].pop(0)
                    x_magnet = xp0
                    y_magnet = yp0
                    pygame.display.update()
                    xc, yc = getCoords(xp0, yp0)
                    print("pixels x %f , y %f", (xp0, yp0))
                    print(xc, yc)
                    # (thL,thR)=invKin(xc,yc)
                    gcodeString = "G21 X" + \
                        "{:.3f}".format(xc)+" Y"+"{:.3f}".format(yc)+" F4000\n"
                    print(gcodeString)
                    # gSer.write(str.encode(gcodeString))
                    # print 'xp: '+str(xp0)+'yp: '+str(yp0)+'xc: '+str(xc)+'yc: '+str(yc)
                    # thL=-90+thL
                    # thR=90+thR
                    # print str(thL)+' '+str(thR)

                    #################SEND GCODE COMMANDS###################################
                   # sting2send=str(thR)+'\n'
                    # serR.write(sting2send)

                    # readlinR = serR.readline()
                    # time.sleep(0.002)

                    # sting2send = str(thL)+'\n'
                    # serL.write(sting2send)

                    time.sleep(0.002)
                    # readlinL = serL.readline()

                    # print readlinL,readlinR

                    new_points[current] = pygame.draw.circle(
                        screen, blue, (xp0, yp0), 10)
                    update_camels()
                    pygame.display.flip()
                    time.sleep(0.002)
                    # TURN ON MAGNET
                    # GPIO.output(magnet2Pin,GPIO.HIGH)
                    # print("ON")
                    # serR.flushInput()
                    # serL.flushInput()
                    # time.sleep(0.02)

                else:
                    collected += 1
                    # if len(camels) > (current_task+1):
                    #     current_task += 1
                    #     pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                    #     rect = pygame.draw.rect(
                    #         screen, white, (xs, ys, xl, yl), 5)
                    #     xp = copy.copy(x_coordinates_list[current_task])
                    #     yp = copy.copy(y_coordinates_list[current_task])
                    #     lengthOfarr = len(xp)
                    #     newPoint = pygame.draw.circle(
                    #         screen, (200, 0, 0), (xp.pop(0), yp.pop(0)), 10)
                    #     pygame.display.flip()
                    #     drowOn = True
                    # # (thL,thR) = invKin(xin,yin)
                    # # print thL,thR
                    # # thL = -90+thL
                    # # thR = 90+thR
                    gcodeString = "G21 X" + \
                        "0".format(xc)+" Y"+"0".format(yc)+" F4000\n"
                    x_magnet = xc
                    y_magnet = yc
                    if(flag == 1):
                        #################SEND GCODE END COMMAND######################
                        # gSer.write(str.encode(gcodeString))
                        # sting2send=str(thR)+'\n'
                        # serR.write(sting2send)
                        # readlinR = serR.readline()
                        # sting2send = str(thL)+'\n'
                        # serL.write(sting2send)
                        # readlinL = serL.readline()

                        # print readlinL,readlinR
                        draw_on = False
                        drawOn = False
                        # REVERSE MAGNET POLARIT

                        flag = 0
                        time.sleep(0.02)
            pygame.display.flip()
except StopIteration:
    pass
string2send = str(0.0)+'\n'
# gSer.write(str.encode('M3 S100\n'))
# gSer.write(str.encode('M3 S800\n'))
# serL.write(string2send)
# serR.write(string2send)
# time.sleep(0.1)
# serL.close()
# gSer.close()
# serR.close()
# Electromagnet cleanup
# GPIO.output(magnet1Pin,GPIO.LOW)
# GPIO.output(magnet2Pin,GPIO.LOW)
# GPIO.output(force_pin,GPIO.LOW)
# GPIO.cleanup()

pygame.quit()
