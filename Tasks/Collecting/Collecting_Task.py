import numpy
import pygame
import random
import time
import GameParameters


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Camel:
    def __init__(self, point):
        self.point = point
        self.collected = False
        self.path = generate_path(point, 2)
        self.drawn_point = point
        self.started = False


nested = False
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1600, 900))
draw_on = False
drowOn = False
radius = 10
flag = 1
boundaries_x = 150
boundaries_y = 150
collected = 0
sheep_size = 100
goal_point = Point(1230, 357)
screen_width, screen_height = pygame.display.get_surface().get_size()
x_length = screen_width-(boundaries_x*2)
x_size = boundaries_x
y_length = screen_height-(boundaries_y*2)
y_size = boundaries_y
new_points = []
points = []
camels = []
goal = 100
firstOpen = True
x = []
y = []
pygame.mixer.init()  # Initialize the mixer module
sound1 = pygame.mixer.Sound('Media/SFX/success.mp3')  # Load a sound.
working = True
rect = pygame.draw.rect(screen, (255, 255, 255),
                        (x_size, y_size, x_length, y_length), 5)


def draw_path(points):
    for v in range(len(points)-1):
        pygame.draw.line(screen, (199, 199, 199, 0.5),
                         (points[v].x, points[v].y),  (points[v+1].x, points[v+1].y), 6)


def generate_path(from_point, degree):

    # Straight Line
    if degree == 1:
        to_point = Point(screen_width/2, screen_height/2)
        a = (((screen_height/4)**2 - (randomX-screen_width/2)**2))**0.5
        m = (to_point.y-from_point.y)/(to_point.x-from_point.x)
        c = from_point.y - m*from_point.x
        domain = to_point.x - from_point.x
        distance = ((((to_point.x - from_point.x)**2) +
                    ((to_point.y-from_point.y)**2))**0.5)
        n = int(distance/6)
        x_step_size = domain/n
        points = []
        for i in range(n):
            points.append(Point(from_point.x+x_step_size*i,
                                m*(from_point.x+x_step_size*i)+c))
        print(len(points))
        return points

    # Quadratic Graph
    elif degree == 2:
        to_point = Point(screen_width/2, screen_height/2)
        vertical_parabola = 1
        # bool(random.getrandbits(1))

        if vertical_parabola:
            done = True
            while done:
                done = False
                randomX = random.uniform(from_point.x, to_point.x)
                randomY = random.uniform(
                    boundaries_y, screen_height - boundaries_y)

                between_point = Point(randomX, randomY)
                print("Between points: ", randomX, " , ", randomY)
                x1, x2, x3 = from_point.x, between_point.x, to_point.x
                y1, y2, y3 = from_point.y, between_point.y, to_point.y

                A = (y1-y3)/(x1**2-2*x2*x1-x3**2+2*x2*x3)
                B = -2*A*x2
                C = y1 - A*(x1**2) - B*x1

                points = []

                domain = to_point.x - from_point.x
                # distance = ((((to_point.x - from_point.x)**2) +
                #             ((to_point.y-from_point.y)**2))**0.5)
                x1_intergral = (1/(4*A))*((2*A*x1+B)*(1+(2*A*x1+B))
                                          ** 0.5+numpy.log(2*A*x1+B+(1+(2*A*x1+B)**2)*0.5))
                x3_intergral = (1/(4*A))*((2*A*x3+B)*(1+(2*A*x3+B))
                                          ** 0.5+numpy.log(2*A*x3+B+(1+(2*A*x3+B)**2)*0.5))
                distance = abs(x3_intergral - x1_intergral)
                n = int(distance/2.5)
                # n = 75
                x_step_size = domain/n

                for i in range(n):
                    x = from_point.x+x_step_size*i
                    y = A*(x**2)+B*(x)+C
                    points.append(Point(x, y))
                    if x < boundaries_x or x > screen_width-boundaries_x or y < boundaries_y or y > screen_height-boundaries_y:
                        done = True
        else:
            randomX = random.uniform(
                boundaries_x, screen_width/2 - boundaries_x*2)
            randomY = random.uniform(from_point.y, to_point.y)

            between_point = Point(randomX, randomY)

            x1, x2, x3 = from_point.y, between_point.y, to_point.y
            y1, y2, y3 = from_point.x, between_point.x, to_point.x

            A = (x1-x3)/(y1**2-2*y2*y1-y3**2+2*y2*y3)
            B = -2*A*y2
            C = x1 - A*(y1**2) - B*y1

            points = []

            domain = to_point.y - from_point.y
            distance = ((((to_point.x - from_point.x)**2) +
                        ((to_point.y-from_point.y)**2))**0.5)
            n = int(distance/6)
            y_step_size = domain/n

            for i in range(n):
                y = from_point.y+y_step_size*i
                x = A*(y**2)+B*(y)+C
                points.append(Point(x, y))
        return points


def getCoords(xn, yn):
    print(" xN: ", xn, " yN: ", yn)
    if xn < x_size+x_length and xn >= x_size:
        xn = (xn-x_size)/x_length
    else:
        return
    if yn < y_size+y_length and yn >= y_size:
        yn = (yn-y_size)/y_length
    else:
        return
    fx = 305*xn
    fy = -140*yn
    return fx, fy

# Serial Setup
# gSer = serial.Serial('/dev/ttyACM0', '115200')

# time.sleep(3)
# gSer.flush()


startL = pygame.image.load('Media/Images/start_game.png').convert_alpha()
startL = pygame.transform.scale(startL, (207, 64))
rectStart = startL.get_rect()
rectStart.center = (130, screen_height-52)

background_image = pygame.image.load("Media/Backgrounds/grass2.jpg")

sheep_image = pygame.image.load("Media/Images/sheep.png")
sheep_image = pygame.transform.flip(sheep_image, True, False)
sheep_image = pygame.transform.scale(sheep_image, (sheep_size, sheep_size))

fence_image = pygame.image.load("Media/Images/fence2.png")
fence_image = pygame.transform.flip(fence_image, True, False)
fence_image = pygame.transform.scale(fence_image, (469, 345))


def setup_screen():
    apply_brightness()
    # Default Screen Setup
    screen.blit(background_image, (0, 0))
    screen.blit(fence_image, (screen_width/2 - 469/2, screen_height/2 - 345/2))
    screen.blit(startL, rectStart)
    # Updated sheep on the screen
    for camel in camels:
        if camel.started:
            draw_path(camel.path)
            pygame.draw.circle(screen, (199, 199, 199, 0.5),
                               (camel.path[len(camel.path)-1].x, camel.path[len(camel.path)-1].y), 10)
            camel.drawn_point = camel.point
        # screen.blit(sheep_image, (camel.point.x - 50,
        #                           camel.point.y - 50))
        pygame.draw.circle(screen, (0, 0, 199, 0.5), (camel.point.x, camel.point.y), 20)               
            



def genreating_sheep():
    global camels
    outside_radius = 292

    while camels == []:

        x_random = random.uniform(boundaries_x, screen_width-boundaries_x)
        y_random = random.uniform(boundaries_y, screen_height-boundaries_y)

        if (x_random-screen_width/2)**2 + (y_random-screen_height/2)**2 > outside_radius**2:
            camels = [Camel(Point(x_random, y_random))]
if not nested:
    print(" ")
    # gSer.flush()
    # print(gSer.readline())
    # print(gSer.readline())
    # time.sleep(1)
    # gSer.write(str.encode('$X\n'))
    # gSer.write(str.encode('M3 S100\n'))
    # gSer.write(str.encode('M3 S600\n'))
    # gSer.write(str.encode('$H\n'))

    # time.sleep(5)

    # gSer.write(str.encode('$X\n'))
    # gSer.write(str.encode('M3 S600\n'))
    # time.sleep(1)
    # gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
    # print(gSer.readline())
    # time.sleep(0.1)
    # gSer.write(str.encode('G21 X25  Y-10 F4000\n'))
    # print(gSer.readline())
    # time.sleep(0.1)
    # gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
    # print(gSer.readline())
    # time.sleep(2)
    # gSer.write(str.encode('$X\n'))
    # print(gSer.readline())
    # gSer.write(str.encode('M3 S1000\n'))
    # print(gSer.readline())
    # gSer.write(str.encode(' G21 X0 Y-154 F4000\n'))
    # print(gSer.readline())
    # gSer.write(str.encode('$X\n'))
    # gSer.write(str.encode(' G21 X250 Y-154 F4000\n'))
    # print(gSer.readline())
    # gSer.write(str.encode('$X\n'))
    # gSer.write(str.encode(' G21 X0 Y0 F4000\n'))
    # print(gSer.readline())
    # gSer.write(str.encode('$X\n'))
    # gSer.write(str.encode('M3 S1000\n'))
    # time.sleep(2)


opacity = 255 - GameParameters.GameParameters.brightness


def apply_brightness():
    global screen
    s = pygame.Surface((screen_height, screen_height), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    screen.blit(s, (0, 0))


while working:
    # INSIDE OF THE GAME LOOP
    if firstOpen:
        firstOpen = False
        collected = 0
        camels = []
        genreating_sheep()
        drowOn = True
        for camel in camels:
            new_points.append(
                pygame.Rect(camel.path[0].x-30, camel.path[0].y-30, 60, 60))
               
    setup_screen()

    screen.blit(startL, rectStart)

    for e in pygame.event.get():

        anyPoint = False
        current = 0

        if e.type == pygame.QUIT:
            working = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                working = False
        # Drawing check
        if e.type == pygame.MOUSEBUTTONDOWN and drowOn and rect.collidepoint(e.pos):
            draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False

        if e.type == pygame.MOUSEMOTION:
            for new_point in new_points:
                if new_point.collidepoint(e.pos):
                    newPoint = new_point
                    anyPoint = True
                    break
                current += 1

        if draw_on and e.type == pygame.MOUSEMOTION and rect.collidepoint(e.pos) and anyPoint and newPoint.collidepoint(e.pos):

            if len(camels[current].path)-1 > 0:
                flag = 1
                xp0, yp0 = (camels[current].path[0].x,
                            camels[current].path[0].y)
                camels[current].path.pop(0)
                camels[current].started = True
                camels[current].point = camels[current].path[0]
                x_magnet = xp0
                y_magnet = yp0
                xc, yc = getCoords(xp0, yp0)
                print("pixels x %f , y %f", (xp0, yp0))
                print(xc, yc)
                gcodeString = "G21 X" + \
                    "{:.3f}".format(xc)+" Y"+"{:.3f}".format(yc)+" F4000\n"
                print(gcodeString)
                # gSer.write(str.encode(gcodeString))
             

                #################SEND GCODE COMMANDS###################################

                time.sleep(0.002)

                new_points[current] =  pygame.Rect(xp0-30, yp0-30, 60, 60)
                pygame.display.flip()
                time.sleep(0.002)

            else:
                collected += 1
                camels = []
                sound1.play()

                if collected == goal:

                    gcodeString = "G21 X" + \
                        "0".format(xc)+" Y"+"0".format(yc)+" F4000\n"
                    x_magnet = xc
                    y_magnet = yc
                    if(flag == 1):
                        #################SEND GCODE END COMMAND######################
                        # gSer.write(str.encode(gcodeString))
                        draw_on = False
                        drawOn = False
                        # REVERSE MAGNET POLARIT
                        flag = 0
                        time.sleep(0.02)
                else:
                    genreating_sheep()

        pygame.display.flip()
if not nested:
    pygame.quit()
