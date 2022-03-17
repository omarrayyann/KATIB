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

# Screen Setup
# width = 1600
# height = 900
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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

new = pygame.image.load('start.png').convert()
new = pygame.transform.scale(new, (50, 50))
new = pygame.transform.rotate(new, 180)
new_btn = Button.Button(new, 'Next Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 200))
buttons.append(new_btn)

prev = pygame.image.load('start.png').convert()
prev = pygame.transform.scale(prev, (50, 50))
prev_btn = Button.Button(prev, 'Prev Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 330))
buttons.append(prev_btn)

show_sol = pygame.image.load('eye.png').convert()
show_sol = pygame.transform.scale(show_sol, (50, 50))
show_sol_btn = Button.Button(show_sol, 'Prev Maze', 50, (width * area_ratio + (1/2) * (1-area_ratio) * width, 460))
buttons.append(show_sol_btn)

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
            buttons[1].text = 'New Maze'
        else:
            buttons[1].text = 'Next Maze'
        if show:
            buttons[3].text = 'Hide Solution'
        else:
            buttons[3].text = 'Show Solution'
        if current != -1:
            if not mazes[current].drawn:
                mazes[current].move(start_pos[0], start_pos[1])
            mazes[current].draw_maze(screen, (255, 255, 255), start_pos[0], start_pos[1], show)
            draw_areas[current].draw_canvas(screen, (255, 255, 255), 10)
        for button in buttons:
            button.draw_button(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if current != -1:
                if e.type == pygame.MOUSEBUTTONDOWN and draw_areas[current].canvas.collidepoint(e.pos) and mazes[current].drawn:
                    draw_areas[current].drawing = True
                if (e.type == pygame.MOUSEBUTTONUP and draw_areas[current].drawing) or (draw_areas[current].drawing and not draw_areas[current].canvas.collidepoint(e.pos)):
                    draw_areas[current].drawing = False
                    if len(draw_areas[current].points) - 1 != -1:
                        draw_areas[current].breaks.append(len(draw_areas[current].points) - 1)
                draw_areas[current].interact(e)
                if e.type == pygame.MOUSEBUTTONDOWN and buttons[0].rect.collidepoint(e.pos):
                    draw_areas[current].clear_area()
                if e.type == pygame.MOUSEBUTTONDOWN and buttons[2].rect.collidepoint(e.pos):
                    current -= 1
                if e.type == pygame.MOUSEBUTTONDOWN and buttons[3].rect.collidepoint(e.pos):
                    show = not show
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
