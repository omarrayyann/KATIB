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
FPS = 500

# Screen Setup
# width = 1600
# height = 900
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((900, 500))

(width, height) = pygame.display.get_window_size()
pygame.display.set_caption('Maze Serious Game')
bg_color = (0, 0, 0)

# Maze Creation
draw_width = math.floor(width * (4/5) - 20)
draw_height = math.floor(height - 20)
w = math.gcd(draw_height, draw_width) * 15
maze = Maze.Maze(w, draw_width, draw_height)

# Canvas Creation
draw_area = DrawArea.DrawArea(draw_width, draw_height, (10, 10), (0, 0, 0))

# Creating buttons
buttons = []
# Clear Button
clear = pygame.image.load('clear.png').convert()
clear = pygame.transform.scale(clear, (50, 50))
clear = pygame.transform.rotate(clear, 180)
clear_btn = Button.Button(clear, 'clear', 50, (width * (4/5) + 35, 70), 'clear')
buttons.append(clear_btn)

exit_game = pygame.image.load('exit.png')
close = pygame.image.load('close.png')
play = pygame.image.load('play.png')

try:
    while True:
        pygame.display.flip()
        screen.fill(bg_color)
        draw_area.draw_canvas(screen, (255, 255, 255), 10)
        maze.move()
        maze.draw_maze(screen, (255, 255, 255), 10, 10)
        buttons[0].draw_button(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN and draw_area.canvas.collidepoint(e.pos) and maze.drawn:
                draw_area.drawing = True
            if e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEMOTION and not draw_area.canvas.collidepoint(e.pos):
                draw_area.drawing = False
            draw_area.interact(e)

        #fpsClock.tick(FPS)
except StopIteration:
    pass
pygame.quit()
