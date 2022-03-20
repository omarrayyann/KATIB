import pygame

import Button
import DrawArea
import Maze
import Cell
import math
import Maze


# Initializing pygame
pygame.init()
fpsClock = pygame.time.Clock()
FPS = 100
show = False
skip = False

# Screen Setup
# width = 1600
# height = 900
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
# screen = pygame.display.set_mode((900, 500))
(width, height) = pygame.display.get_window_size()
pygame.display.set_caption('Maze Serious Game')
bg_color = (0, 0, 0)
area_ratio = (4 / 5)
start_pos = (10, 10)

# Maze & Draw Area lists + current parameter
mazes = []
draw_areas = []
current = -1

# Creating buttons
buttons = []
# Clear Button
clear = pygame.image.load('clear.png').convert()
clear = pygame.transform.scale(clear, (50, 50))
clear = pygame.transform.rotate(clear, 180)
clear_btn = Button.Button(clear, 'clear', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 70))
buttons.append(clear_btn)

add = pygame.image.load('addedit.png').convert()
add = pygame.transform.scale(add, (50, 50))
new = pygame.image.load('start.png').convert()
new = pygame.transform.scale(new, (50, 50))
new = pygame.transform.rotate(new, 180)
new_btn = Button.Button(add, 'Next Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 200))
buttons.append(new_btn)

prev = pygame.image.load('start.png').convert()
prev = pygame.transform.scale(prev, (50, 50))
prev_btn = Button.Button(prev, 'Prev Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 330))
buttons.append(prev_btn)

open_eye = pygame.image.load('openeye.png').convert()
open_eye = pygame.transform.scale(open_eye, (50, 50))
closed_eye = pygame.image.load('closedeye.png').convert()
closed_eye = pygame.transform.scale(closed_eye, (50, 50))
sol_btn = Button.Button(open_eye, 'Prev Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 460))
buttons.append(sol_btn)

save = pygame.image.load('save.png').convert()
save = pygame.transform.scale(save, (50, 50))
save_btn = Button.Button(save, 'Save', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 590))
buttons.append(save_btn)

exit_game = pygame.image.load('exit.png')
close = pygame.image.load('close.png')


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

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if current != -1:
                if e.type == pygame.MOUSEBUTTONDOWN and draw_areas[current].canvas.collidepoint(e.pos) and not mazes[current].drawn:
                    skip = True
                elif e.type == pygame.MOUSEBUTTONDOWN and draw_areas[current].canvas.collidepoint(e.pos) and mazes[current].drawn:
                    draw_areas[current].drawing = True
                elif (e.type == pygame.MOUSEBUTTONUP and draw_areas[current].drawing) or (draw_areas[current].drawing and not draw_areas[current].canvas.collidepoint(e.pos)):
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
                draw_areas[current].interact(e)
            if e.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(e.pos):
                current += 1
                if buttons[1].text == 'New Maze':
                    maze = create_maze(15)
                    mazes.append(maze)
                    draw_areas.append(create_draw_area(mazes[current].draw_width, maze.draw_height))

        # fpsClock.tick(FPS)
except StopIteration:
    pass
pygame.quit()
