import pygame
import Maze
import Cell
import math
import Maze

# Initializing pygame
pygame.init()
fpsClock = pygame.time.Clock()
FPS = 500

# Screen Setup
width = 1600
height = 900
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Maze Serious Game')
bg_color = (10, 10, 10)

# Maze Creation
w = 30
draw_width = 1400
draw_height = 700
maze = Maze.Maze(w, draw_width, draw_height)

try:
    while True:
        pygame.display.flip()
        screen.fill(bg_color)
        maze.move()
        maze.draw_maze(screen, (255, 255, 255), 100, 100)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
        fpsClock.tick(FPS)
except StopIteration:
    pass
pygame.quit()
