import pygame
from Input import Button
from Tasks.Shared import DrawArea
import math
from Tasks.Maze.Supporting_Classes import Maze
from General import GameParameters

# import serial

# Initializing pygame

fpsClock = pygame.time.Clock()
FPS = 100

# Setting up game variables:
nested = False
volume = GameParameters.GameParameters.volume
opacity = 255 - GameParameters.GameParameters.brightness
show = False
skip = False
haptic_on = False

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Screen Setup
if not nested:
    on_katib = False
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    (screen_width, screen_height) = pygame.display.get_surface().get_size()
    boundaries_x = 150
    boundaries_y = 150
    x_length = screen_width - (boundaries_x * 2)
    x_size = boundaries_x
    y_length = screen_height - (boundaries_y * 2)
    y_size = boundaries_y

pygame.display.set_caption('Maze Serious Game')
bg_color = (0, 0, 0)
start_pos = (boundaries_x, boundaries_y)

# Maze & Draw Area lists + current parameter
mazes = []
draw_areas = []
current = -1
sheep = pygame.image.load('../../Media/Images/sheep.png').convert_alpha()
sheep = pygame.transform.scale(sheep, (50,50))
magnet_point = sheep.get_rect()

# Grass Background
bg = pygame.image.load("../../Media/Backgrounds/bbg.jpg")

# Creating buttons
buttons = []
# Clear Button
clear_btn = Button.Button('img', ['clear.png'], (50, 50), 'Clear', True, 20, [(255, 255, 255)],
                          (screen_width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * screen_width, 70))
buttons.append(clear_btn)

# New/Next Maze Button
new_btn = Button.Button('img', ['addedit.png', 'play.png'], (50, 50), 'New Maze', True, 20, [(255, 255, 255)],
                        (screen_width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * screen_width, 200))
buttons.append(new_btn)

# Previous maze button
prev_btn = Button.Button('img', ['start.png'], (50, 50), 'Prev Maze', True, 20, [(255, 255, 255)],
                         (screen_width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * screen_width, 330))
buttons.append(prev_btn)

# Show/Hide Solution Button
sol_btn = Button.Button('img', ['openeye.png', 'closedeye.png'], (50, 50), 'Show Solution', True, 20, [(255, 255, 255)],
                        (screen_width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * screen_width, 460))
buttons.append(sol_btn)

# Save Button
save_btn = Button.Button('img', ['save.png'], (50, 50), 'Show Solution', True, 20, [(255, 255, 255)],
                         (screen_width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * screen_width, 590))
buttons.append(save_btn)

# Haptic on_off
haptic_toggle = Button.Button('img', ['openeye.png', 'closedeye.png'], (50, 50), 'Toggle Haptic', True, 20, [(255, 255, 255)],
                              (screen_width * (5 / 6) + (1 / 2) * (1 - (5 / 6)) * screen_width, 720))
buttons.append(haptic_toggle)

prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], (50, 50), 'Prev', False, 50, [(0, 0, 0)],
                              (screen_width / 15, screen_height / 9))

exit_game = pygame.image.load('../../Media/Images/exit.png')
close = pygame.image.load('../../Media/Images/close.png')


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


def getCoords(xn, yn):
    print(" xN: ", xn, " yN: ", yn)
    if xn < x_size +x_length and xn >= x_size:
        xn = (xn-x_size)/x_length
    else:
        return
    if yn < y_size +y_length and yn >= y_size:
        yn = (yn-y_size)/y_length
    else:
        return
    fx = 305*xn
    fy = -140*yn
    return fx, fy


def create_maze(maze_w):
    global x_length, y_length
    draw_width = int(x_length / maze_w) * maze_w
    draw_height = int(y_length / maze_w) * maze_w
    w = maze_w
    maze = Maze.Maze(w, draw_width, draw_height)
    return maze


# Canvas Creation
def create_draw_area(draw_width, draw_height):
    global start_pos
    draw_area = DrawArea.DrawArea(draw_width, draw_height, start_pos, (0, 0, 0))
    return draw_area


# Draws the point at which the magnet is present
def draw_magnet():
    global screen, sheep, magnet_point
    magnet_point.center = mazes[current].katib_points[mazes[current].current_point]
    screen.blit(sheep, magnet_point)


def apply_brightness():
    global screen
    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    screen.blit(s, (0, 0))


try:
    while True:
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        if current + 1 == len(mazes):
            buttons[1].switch_img(0)
            buttons[1].txt = 'New Maze'
        else:
            buttons[1].switch_img(1)
            buttons[1].txt = 'Next Maze'
        if show:
            buttons[3].switch_img(0)
            buttons[3].txt = 'Hide Solution'
        else:
            buttons[3].switch_img(1)
            buttons[3].txt = 'Show Solution'
        if haptic_on:
            buttons[5].switch_img(0)
            buttons[5].txt = 'Haptic On'
        else:
            buttons[5].switch_img(1)
            buttons[5].txt = 'Haptic Off'
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
            draw_areas[current].draw_data(screen,  (0, 0, 0), 20)
        for button in buttons:
            button.draw_button(screen)
        prev_menu_btn.draw_button(screen)
        if current != -1 and mazes[current].drawn:
            draw_magnet()
        apply_brightness()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN and prev_menu_btn.rect.collidepoint(e.pos):
                raise StopIteration
            if current != -1:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if draw_areas[current].canvas.collidepoint(e.pos) and not mazes[current].drawn:
                        skip = True
                    # elif draw_areas[current].canvas.collidepoint(e.pos) and mazes[
                    #     current].drawn:
                    #     draw_areas[current].drawing = True
                    elif buttons[0].rect.collidepoint(e.pos):
                        draw_areas[current].clear_area()
                        mazes[current].current_point = 0
                    elif buttons[2].rect.collidepoint(e.pos):
                        current -= 1
                    elif buttons[3].rect.collidepoint(e.pos):
                        show = not show
                    elif buttons[4].rect.collidepoint(e.pos) and mazes[current].saved:
                        mazes[current].save_maze(screen, start_pos[0], start_pos[1])
                    elif buttons[5].rect.collidepoint(e.pos):
                        haptic_on = not haptic_on
                        mazes[current].save_maze(screen, start_pos[0], start_pos[1])
                elif not pygame.mouse.get_pressed()[0]:
                    draw_areas[current].toggle_interaction(True)
                if draw_areas[current].drawing:
                    # Move to next point
                    if magnet_point.collidepoint(pygame.mouse.get_pos()) and mazes[current].current_point != len(mazes[current].katib_points) - 1:
                        mazes[current].current_point += 1
                        xp0, yp0 = mazes[current].katib_points[mazes[current].current_point]
                        x_magnet = xp0
                        y_magnet = yp0
                        xc, yc = getCoords(xp0, yp0)
                        print("pixels x %f , y %f", (xp0, yp0))
                        print(xc, yc)
                        gcodeString = "G21 X" + \
                                      "{:.3f}".format(xc) + " Y" + "{:.3f}".format(yc) + " F4000\n"
                        print(gcodeString)
                        if nested and haptic_on and on_katib:
                            gSer.write(str.encode(gcodeString))
                    (j, i) = (int((pygame.mouse.get_pos()[0] - start_pos[0]) / mazes[current].w),
                              int((pygame.mouse.get_pos()[1] - start_pos[1]) / mazes[current].w))
                    if draw_areas[current].canvas.collidepoint(pygame.mouse.get_pos()):
                        for line in mazes[current].grid[mazes[current].index(i, j)].lines:
                            if line.collidepoint(pygame.mouse.get_pos()):
                                draw_areas[current].drawing = False
                                draw_areas[current].toggle_interaction(False)
                                if len(draw_areas[current].points) - 1 != -1:
                                    draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                draw_areas[current].interact(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
            if e.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(e.pos):
                current += 1
                if buttons[1].txt == 'New Maze':
                    maze = create_maze(150)
                    mazes.append(maze)
                    # Cell.adjust_fence_size(maze.w)
                    draw_areas.append(create_draw_area(mazes[current].draw_width, maze.draw_height))

        # fpsClock.tick(FPS)
except StopIteration:
    pass

if not nested:
    pygame.quit()
