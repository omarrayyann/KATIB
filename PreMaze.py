import pygame
import time
import Button
import DrawArea
import Maze
import Cell
import math
import Maze
import serial

# Initializing pygame
import PreMaze

pygame.init()
fpsClock = pygame.time.Clock()
FPS = 100
show = False
skip = False

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Screen Setup
# width = 1600
# height = 900
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
(width, height) = pygame.display.get_window_size()
boundaries_x = 150
boundaries_y = 150
xl = width - (boundaries_x * 2)
xs = boundaries_x
yl = height - (boundaries_y * 2)
ys = boundaries_y

pygame.display.set_caption('Maze Serious Game')
bg_color = (0, 0, 0)
area_ratio = (4 / 5)
start_pos = (10, 10)

# Serial Setup
# gSer = serial.Serial('/dev/ttyACM0', '115200')
# time.sleep(3)
# gSer.flush()

# gSer.flush()
# print(gSer.readline())
# print(gSer.readline())
# time.sleep(1)
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode('M3 S100\n'))
# gSer.write(str.encode('M3 S500\n'))
# gSer.write(str.encode('$H\n'))

# time.sleep(5)

# Calibrate
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode('M3 S500\n'))
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

# Maze & Draw Area lists + current parameter
mazes = []
draw_areas = []
current = -1
current_point = 0
magnet_point = pygame.draw.circle(screen, (0, 0, 0), (0, 0), 10)

# Creating buttons
buttons = []
# Clear Button
clear = pygame.image.load('clear.png').convert()
clear = pygame.transform.scale(clear, (50, 50))
clear = pygame.transform.rotate(clear, 180)
clear_btn = Button.Button(clear, 'clear', 50, (width * area_ratio + (1 / 2) * (1 - area_ratio) * width, 70))
buttons.append(clear_btn)

# New/Next Maze Button
add = pygame.image.load('addedit.png').convert()
add = pygame.transform.scale(add, (50, 50))
new = pygame.image.load('start.png').convert()
new = pygame.transform.scale(new, (50, 50))
new = pygame.transform.rotate(new, 180)
new_btn = Button.Button(add, 'Next Maze', 50, (width * area_ratio + (1 / 2) * (1 - area_ratio) * width, 200))
buttons.append(new_btn)

# Previous maze button
prev = pygame.image.load('start.png').convert()
prev = pygame.transform.scale(prev, (50, 50))
prev_btn = Button.Button(prev, 'Prev Maze', 50, (width * area_ratio + (1 / 2) * (1 - area_ratio) * width, 330))
buttons.append(prev_btn)

# Show/Hide Solution Button
open_eye = pygame.image.load('openeye.png').convert()
open_eye = pygame.transform.scale(open_eye, (50, 50))
closed_eye = pygame.image.load('closedeye.png').convert()
closed_eye = pygame.transform.scale(closed_eye, (50, 50))
sol_btn = Button.Button(open_eye, 'Prev Maze', 50, (width * area_ratio + (1 / 2) * (1 - area_ratio) * width, 460))
buttons.append(sol_btn)

# Save Button
save = pygame.image.load('save.png').convert()
save = pygame.transform.scale(save, (50, 50))
save_btn = Button.Button(save, 'Save', 50, (width * area_ratio + (1 / 2) * (1 - area_ratio) * width, 590))
buttons.append(save_btn)

exit_game = pygame.image.load('exit.png')
close = pygame.image.load('close.png')


def inv_kin(x_in, y_in):
    # x_in = 0.024+0.052*(1-(xs+xl-x_in)/xl)
    # y_in = 0.1171+0.047*((ys+yl-y_in)/yl)
    R = math.sqrt(x_in ** 2 + y_in ** 2)
    k = math.atan(y_in / x_in)
    phi = math.acos(R / 0.2)

    thetaL = math.degrees(k + phi)

    x_in = x_in - 0.1

    R = math.sqrt(x_in ** 2 + y_in ** 2)
    k = math.atan(y_in / x_in)
    phi = math.acos(R / 0.2)

    thetaR = math.degrees((k - phi))

    return 90.0 + thetaR, -90.0 + thetaL


def get_coords(xn, yn):
    if xn < xs + xl and xn >= xs:
        xn = (xn - xs) / xl
    else:
        return
    if yn < ys + yl and yn >= ys:
        yn = (yn - ys) / yl
    else:
        return
    fx = 143 * xn
    # fy= 0.00017125*yn+0.09431875
    fy = -95 * yn
    return fx, fy


def create_maze(difficulty):
    draw_width = math.floor(width * area_ratio - 20)
    draw_height = math.floor(height - 20)
    w = math.gcd(draw_height, draw_width) * difficulty
    maze = Maze.Maze(w, draw_width, draw_height)
    return maze


# Canvas Creation
def create_draw_area(draw_width, draw_height):
    draw_area = DrawArea.DrawArea(draw_width, draw_height, start_pos, (0, 0, 0))
    return draw_area

def draw_magnet():
    return pygame.draw.circle(screen, (255, 0, 0), mazes[current].katib_points[current_point], 10)


try:
    while True:
        pygame.display.flip()
        screen.fill(bg_color)
        if current + 1 == len(mazes):
            buttons[1].image = add
            buttons[1].text = 'New Maze'
        else:
            buttons[1].image = new
            buttons[1].text = 'Next Maze'
        if show:
            buttons[3].image = open_eye
            buttons[3].text = 'Hide Solution'
        else:
            buttons[3].image = closed_eye
            buttons[3].text = 'Show Solution'
        if current != -1:
            mazes[current].draw_maze(screen, (255, 255, 255), start_pos[0], start_pos[1], skip, show)
            if not mazes[current].drawn:
                mazes[current].move(start_pos[0], start_pos[1])
            elif skip:
                skip = False
            elif not mazes[current].saved:
                mazes[current].saved = True
                maze_area = screen.subsurface(draw_areas[current].canvas)
                maze_area = maze_area.copy()
                maze_area.unlock()
                mazes[current].maze_image = maze_area
            draw_areas[current].draw_canvas(screen, (200, 0, 200), 10)
        for button in buttons:
            button.draw_button(screen)
        if current != -1 and mazes[current].drawn:
            magnet_point = draw_magnet()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if current != -1:
                if e.type == pygame.MOUSEBUTTONDOWN and draw_areas[current].canvas.collidepoint(e.pos) and not mazes[
                    current].drawn:
                    skip = True
                elif e.type == pygame.MOUSEBUTTONDOWN and draw_areas[current].canvas.collidepoint(e.pos) and mazes[
                    current].drawn:
                    draw_areas[current].drawing = True
                elif (e.type == pygame.MOUSEBUTTONUP and draw_areas[current].drawing) or (
                        draw_areas[current].drawing and not draw_areas[current].canvas.collidepoint(e.pos)):
                    draw_areas[current].drawing = False
                    if len(draw_areas[current].points) - 1 != -1:
                        draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                elif e.type == pygame.MOUSEBUTTONDOWN and buttons[0].rect.collidepoint(e.pos):
                    draw_areas[current].clear_area()
                elif e.type == pygame.MOUSEBUTTONDOWN and buttons[2].rect.collidepoint(e.pos):
                    current -= 1
                elif e.type == pygame.MOUSEBUTTONDOWN and buttons[3].rect.collidepoint(e.pos):
                    show = not show
                elif e.type == pygame.MOUSEBUTTONDOWN and buttons[4].rect.collidepoint(e.pos) and mazes[current].saved:
                    mazes[current].save_maze(screen, start_pos[0], start_pos[1])
                if draw_areas[current].drawing:
                    # Move to next point
                    if magnet_point.collidepoint(e.pos) and current_point != len(mazes[current].katib_points) - 1:
                        current_point += 1
                    (j, i) = (int((e.pos[0] - start_pos[0]) / mazes[current].w),
                              int((e.pos[1] - start_pos[1]) / mazes[current].w))
                    if draw_areas[current].canvas.collidepoint(e.pos):
                        for line in mazes[current].grid[mazes[current].index(i, j)].lines:
                            if line.collidepoint(e.pos):
                                draw_areas[current].drawing = False
                                if len(draw_areas[current].points) - 1 != -1:
                                    draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                draw_areas[current].interact(e)
            if e.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(e.pos):
                current += 1
                if buttons[1].text == 'New Maze':
                    maze = create_maze(50)
                    mazes.append(maze)
                    draw_areas.append(create_draw_area(mazes[current].draw_width, maze.draw_height))

        # fpsClock.tick(FPS)
except StopIteration:
    pass
# string2send = str(0.0) + '\n'
# gSer.write(str.encode('M3 S100\n'))
# gSer.write(str.encode('M3 S800\n'))

pygame.quit()
