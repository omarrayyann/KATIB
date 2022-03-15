from asyncio import current_task
import pygame
import random
import time
import string
import os
import csv
import copy
import serial
import math

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

width = 1600
height = 900
# Screen Setup
# screen = pygame.display.set_mode((width,height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
draw_on = False
drowOn = False
last_pos = (0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
radius = 10

boundaries = 60
screen_width, screen_height = pygame.display.get_surface().get_size()
xl = screen_width-(boundaries*2)
xs = boundaries
yl = screen_height-(boundaries*2)-40
ys = boundaries
imgIndex = 0
delim = ' '
imageDir = 'Arabic/Image'
letterDir = 'Arabic/Data/'
lengthOfarr = 0
flag = 1
# Serial Setup

# gSer=serial.Serial('/dev/ttyACM0','115200')
# time.sleep(3)
# gSer.flush()
# serL.write("r\n")
# serR.write("r\n")
# time.sleep(6.1)


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


d = dict.fromkeys(string.ascii_lowercase, [])
letterImg = []
lettersX = []
lettersY = []

cwd = os.getcwd()
Data_path = cwd+"/Arabic/Data_converted"
letter_paths = os.listdir(Data_path)
print(letter_paths)

x_coordinates = []
y_coordinates = []
x_coordinates_list = []
y_coordinates_list = []


for file_name in letter_paths:

    with open(Data_path+'/'+file_name, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=delim)
        # print(coords)    		#header = next(plots)
        x = []
        y = []
        l = []
        for row in coords:
            if len(row) > 1:
                print(row, row[0], row[1])
                x.append(int(xs+50+(0.7*xl)*(float(row[0]))))
                y.append(int(ys+50+(0.8*yl)*(float(row[1]))))
    lettersX.append(x)
    lettersY.append(y)

    #
# for key in d:
#	img = pygame.image.load(imageDir+'/'+key+'.png').convert()
#	img = pygame.transform.rotozoom(img,0,4)
#	rectImg = img.get_rect()
#	rectImg.center = (1450, 400)
#	letterImg.append(img)
#	with open(letterDir+key+'.csv','r') as csvfile:
#		coords = csv.reader(csvfile, delimiter=delim)
#		#header = next(plots)
#		x=[]
#		y=[]
#		for row in coords:
#			x.append(int(xs+60+(xl-80)*(1-float(row[0]))))
#			y.append(int(ys+60+(yl-80)*(1-float(row[1]))))
#		lettersX.append(x)
#		lettersY.append(y)


# Remote Work Magnet Visualization
magnet = pygame.image.load('clear.png').convert()
magnet = pygame.transform.scale(magnet, (30, 30))

startMagnetVisualization = False


def magnet_visualizer(x, y):
    pygame.draw.circle(screen, (255, 215, 0), (x, y), 10)


def moveCamel(x, y):
    screen.blit(camel, (x, y))
    pygame.display.update()


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

camel = pygame.image.load('camel.png')
camel = pygame.transform.scale(camel, (100, 100))

closeL = pygame.image.load('exit.png').convert()
closeL = pygame.transform.scale(closeL, (50, 50))
# closeL=pygame.transform.rotate(closeL,180)
rectClose = closeL.get_rect()
rectClose.center = (width-50, 100)

ResetMs = pygame.image.load('exit.png').convert()
ResetMs = pygame.transform.scale(ResetMs, (50, 50))
# closeL=pygame.transform.rotate(closeL,180)
rectResetMs = ResetMs.get_rect()
rectResetMs.center = (width-50, 200)

screen.blit(clear, rectClear)
screen.blit(load, rectLoad)
screen.blit(startL, rectStart)
screen.blit(closeL, rectClose)
screen.blit(ResetMs, rectResetMs)

pygame.draw.circle(screen, green, (int(xs), int(ys)), radius)
pygame.draw.circle(screen, blue, (int(xs+xl), int(ys+yl)), radius)

x = []
y = []

goal_box_x_center = screen_width/2
goal_box_y_center = screen_height/2
goal_box_width = 500
goal_box_height = 300
goal_box_start_x = goal_box_x_center-(goal_box_width/2)
goal_box_start_y = goal_box_y_center-(goal_box_height/2)


class point:
    def __init__(p, x, y):
        p.x = x
        p.y = y

    def set_x(p, x):
        p.x = x

    def set_y(p, x):
        p.y = y


def generate_straight_line_coordinates(from_point, to_point, n):
    global x_coordinates, y_coordinates
    m = (to_point.y-from_point.y)/(to_point.x-from_point.x)
    c = from_point.y - m*from_point.x
    domain = from_point.x - to_point.x
    x_step_size = abs(domain/n)
    x_cord_new = []
    y_cord_new = []
    for i in range(n):
        x_cord_new.append(from_point.x+x_step_size*i)
        y_cord_new.append(m*(from_point.x+x_step_size*i)+c)
    x_coordinates = x_cord_new
    y_coordinates = y_cord_new
    return x_cord_new, y_cord_new


number_tasks = 4

new_points = []

xp = []
yp = []

generate_straight_line_coordinates(
    point(500, 500), point(screen_width/2, screen_height/2), 50)

startingPositions = [point(200, 200), point(
    300, 300), point(200, 600)]

number_tasks = len(startingPositions)
current_task = 0
for starter in startingPositions:
    x_coordinates, y_coordinates = generate_straight_line_coordinates(
        starter, point(screen_width/2, screen_height/2), 50)
    x_coordinates_list.append(x_coordinates)
    y_coordinates_list.append(y_coordinates)


try:
    while True:
        rect = pygame.draw.rect(screen, (102, 255, 51), (xs, ys, xl, yl), 7)
        goal = pygame.draw.rect(screen, (102, 51, 10), (goal_box_start_x,
                                                        goal_box_start_y, goal_box_width, goal_box_height), 7)
        screen.blit(clear, rectClear)
        screen.blit(load, rectLoad)
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
                # screen.fill(black)
# Clear check
            if e.type == pygame.MOUSEBUTTONDOWN and rectClear.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectClear, 5)
                pygame.display.flip()
                pygame.draw.rect(screen, black, rectClear, 5)
                time.sleep(0.05)
                drowOn = False
                screen.fill(black)
# Load check

            if e.type == pygame.MOUSEBUTTONDOWN and rectLoad.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectLoad, 5)
                pygame.display.flip()
                time.sleep(0.05)
                pygame.draw.rect(screen, black, rectStart, 5)

                pygame.draw.rect(screen, black, rectLoad, 5)
                pygame.display.flip()
                pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(
                    screen, (102, 255, 51), (xs, ys, xl, yl), 7)
                goal = pygame.draw.rect(screen, (102, 51, 10), (goal_box_start_x,
                                                                goal_box_start_y, goal_box_width, goal_box_height), 7)
                xp = copy.copy(x_coordinates_list[current_task])
                yp = copy.copy(y_coordinates_list[current_task])
                lengthOfarr = len(xp)
                newPoint = pygame.draw.circle(
                    screen, white, (xp.pop(0), yp.pop(0)), 20)
                flag = 1
                drowOn = False
                drow_on = False

                # pygame.display.flip()
# Start check

            if e.type == pygame.MOUSEBUTTONDOWN and rectStart.collidepoint(e.pos):
                pygame.display.flip()
                time.sleep(0.05)
                pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 5)
                for current in range(number_tasks):
                    print("hulu", current)
                    xp.append(copy.copy(x_coordinates_list[current]))
                    yp.append(copy.copy(y_coordinates_list[current]))
                    new_points.append(pygame.draw.circle(
                        screen, (200, 0, 0), (xp[current].pop(0), yp[current].pop(0)), 10))

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

            if draw_on and e.type == pygame.MOUSEMOTION and rect.collidepoint(e.pos) and newPoint.collidepoint(e.pos) and anyPoint:
                # if draw_on and :
                # pygame.draw.circle(screen, color, e.pos, radius)
                # roundline(screen, color, e.pos, last_pos,  radius)
                # last_pos = e.pos
                if len(xp[current])-1 > 0:
                    flag = 1
                    xp0, yp0 = (xp[current].pop(0), yp[current].pop(0))
                    magnet_visualizer(xp0, yp0)
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
                        screen, blue, (xp0, yp0), 20)

                    lengthOfarr -= 1
                    pygame.display.flip()
                    time.sleep(0.002)
                    # TURN ON MAGNET
                    # GPIO.output(magnet2Pin,GPIO.HIGH)
                    # print("ON")
                    # serR.flushInput()
                    # serL.flushInput()
                    # time.sleep(0.02)

                else:
                    if number_tasks > (current_task+1):
                        current_task += 1
                        pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                        rect = pygame.draw.rect(
                            screen, white, (xs, ys, xl, yl), 5)
                        xp = copy.copy(x_coordinates_list[current_task])
                        yp = copy.copy(y_coordinates_list[current_task])
                        lengthOfarr = len(xp)
                        newPoint = pygame.draw.circle(
                            screen, (200, 0, 0), (xp.pop(0), yp.pop(0)), 10)
                        pygame.display.flip()
                        drowOn = True
                    # (thL,thR) = invKin(xin,yin)
                    # print thL,thR
                    # thL = -90+thL
                    # thR = 90+thR
                    gcodeString = "G21 X" + \
                        "0".format(xc)+" Y"+"0".format(yc)+" F4000\n"
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
