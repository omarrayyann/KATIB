import pygame
import Button
import DrawArea
import math
import Maze
import Cell
import GameParameters
# import serial

# Initializing pygame
pygame.init()
fpsClock = pygame.time.Clock()
FPS = 100

# Setting up game variables:
nested = True
broken = False
volume = GameParameters.GameParameters.volume
opacity = 255 - GameParameters.GameParameters.brightness
show = False
skip = False

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Screen Setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
(width, height) = pygame.display.get_surface().get_size()
boundaries_x = 150
boundaries_y = 150
xl = width - (boundaries_x * 2)
xs = boundaries_x
yl = height - (boundaries_y * 2)
ys = boundaries_y

pygame.display.set_caption('Maze Serious Game')
bg_color = (0, 0, 0)
start_pos = (boundaries_x, boundaries_y)

# Maze & Draw Area lists + current parameter
mazes = []
draw_areas = []
current = -1
sheep = pygame.image.load('sheep.png').convert_alpha()
sheep = pygame.transform.scale(sheep, (50,50))
magnet_point = sheep.get_rect()

# Grass Background
bg = pygame.image.load("bbg.jpg")

# Creating buttons
buttons = []
# Clear Button
clear_btn = Button.Button('img', ['clear.png'], 50, 'Clear', True, 20, [(255, 255, 255)],
                          (width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * width, 70))
buttons.append(clear_btn)

# New/Next Maze Button
new_btn = Button.Button('img', ['addedit.png', 'play.png'], 50, 'New Maze', True, 20, [(255, 255, 255)],
                        (width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * width, 200))
buttons.append(new_btn)

# Previous maze button
prev_btn = Button.Button('img', ['start.png'], 50, 'Prev Maze', True, 20, [(255, 255, 255)],
                         (width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * width, 330))
buttons.append(prev_btn)

# Show/Hide Solution Button
sol_btn = Button.Button('img', ['openeye.png', 'closedeye.png'], 50, 'Show Solution', True, 20, [(255, 255, 255)],
                        (width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * width, 460))
buttons.append(sol_btn)

# Save Button
save_btn = Button.Button('img', ['save.png'], 50, 'Show Solution', True, 20, [(255, 255, 255)],
                         (width * (4 / 5) + (1 / 2) * (1 - (4 / 5)) * width, 590))
buttons.append(save_btn)

prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], 50, 'Prev', False, 50, [(0, 0, 0)],
                              (width / 15, height / 9))

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


def create_maze(maze_w):
    global xl, yl
    draw_width = int(xl / maze_w) * maze_w
    draw_height = int(yl / maze_w) * maze_w
    w = maze_w
    maze = Maze.Maze(w, draw_width, draw_height)
    return maze


# Canvas Creation
def create_draw_area(draw_width, draw_height):
    draw_area = DrawArea.DrawArea(draw_width, draw_height, start_pos, (0, 0, 0))
    return draw_area


# Draws the point at which the magnet is present
def draw_magnet():
    global screen, sheep, magnet_point
    magnet_point.center = mazes[current].katib_points[mazes[current].current_point]
    screen.blit(sheep, magnet_point)


def apply_brightness():
    global screen
    s = pygame.Surface((width, height), pygame.SRCALPHA)
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
            draw_areas[current].draw_canvas(screen, (0, 0, 0), 20)
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
                broken = True
                break
            if current != -1:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if draw_areas[current].canvas.collidepoint(e.pos) and not mazes[
                        current].drawn:
                        skip = True
                    elif draw_areas[current].canvas.collidepoint(e.pos) and mazes[
                        current].drawn:
                        draw_areas[current].drawing = True
                    elif buttons[0].rect.collidepoint(e.pos):
                        draw_areas[current].clear_area()
                        mazes[current].current_point = 0
                    elif buttons[2].rect.collidepoint(e.pos):
                        current -= 1
                    elif buttons[3].rect.collidepoint(e.pos):
                        show = not show
                    elif buttons[4].rect.collidepoint(e.pos) and mazes[
                        current].saved:
                        mazes[current].save_maze(screen, start_pos[0], start_pos[1])
                elif (e.type == pygame.MOUSEBUTTONUP and draw_areas[current].drawing) or (
                        draw_areas[current].drawing and not draw_areas[current].canvas.collidepoint(pygame.mouse.get_pos())):
                    draw_areas[current].drawing = False
                    if len(draw_areas[current].points) - 1 != -1:
                        draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                if draw_areas[current].drawing:
                    # Move to next point
                    if magnet_point.collidepoint(pygame.mouse.get_pos()) and mazes[current].current_point != len(mazes[current].katib_points) - 1:
                        mazes[current].current_point += 1
                    (j, i) = (int((pygame.mouse.get_pos()[0] - start_pos[0]) / mazes[current].w),
                              int((pygame.mouse.get_pos()[1] - start_pos[1]) / mazes[current].w))
                    if draw_areas[current].canvas.collidepoint(pygame.mouse.get_pos()):
                        for line in mazes[current].grid[mazes[current].index(i, j)].lines:
                            if line.collidepoint(pygame.mouse.get_pos()):
                                draw_areas[current].drawing = False
                                if len(draw_areas[current].points) - 1 != -1:
                                    draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                draw_areas[current].interact(pygame.mouse.get_pos())
            if e.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(e.pos):
                current += 1
                if buttons[1].txt == 'New Maze':
                    maze = create_maze(150)
                    mazes.append(maze)
                    # Cell.adjust_fence_size(maze.w)
                    draw_areas.append(create_draw_area(mazes[current].draw_width, maze.draw_height))
        if broken:
            break


        # fpsClock.tick(FPS)
except StopIteration:
    pass

if not nested:
    pygame.quit()
