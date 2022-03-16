import pygame
import Maze
import math
import random
import seed
import time

random.seed(time.time())


# The Cell class handles cell creation
class Cell:

    # Constructor
    def __init__(self, i, j, parent_maze):
        self.i = i  # Row Index
        self.j = j  # Column index
        # Whether walls should be drawn. Order: [Top Right Bottom Left]
        self.walls = [True, True, True, True]
        self.visited = False
        self.parent_maze = parent_maze

    # Draws the cell on the screen
    def draw_cell(self, screen, line_color, x_start, y_start, w):
        x = x_start + self.j * w
        y = y_start + self.i * w
        # Coloring in visited cells
        #if self.visited:
            # pygame.draw.rect(screen, (100, 0, 100), pygame.Rect(x, y, w, w))

        # Drawing the active walls
        # for k in range(4):
        #    if self.walls[k]:
        #        pygame.draw.line(screen, line_color, (x + math.ceil(k/2) * w, y + math.floor(k/2) * w), (x + math.ceil(k/2 + 0.5) * w, y + math.floor(k/2 + 0.5) * w))
        if self.walls[0]:
            pygame.draw.line(screen, line_color, (x, y), (x + w, y))
        if self.walls[1]:
            pygame.draw.line(screen, line_color, (x + w, y), (x + w, y + w))
        if self.walls[2]:
            pygame.draw.line(screen, line_color, (x + w, y + w), (x, y + w))
        if self.walls[3]:
            pygame.draw.line(screen, line_color, (x, y + w), (x, y))

    def check_neighbors(self):
        neighbors = []

        if self.i != 0:
            top = self.parent_maze.grid[self.parent_maze.index(self.i - 1, self.j)]
            if not top.visited:
                neighbors.append(top)
        if self.j != self.parent_maze.cols - 1:
            right = self.parent_maze.grid[self.parent_maze.index(self.i, self.j + 1)]
            if not right.visited:
                neighbors.append(right)
        if self.i != self.parent_maze.rows - 1:
            bottom = self.parent_maze.grid[self.parent_maze.index(self.i + 1, self.j)]
            if not bottom.visited:
                neighbors.append(bottom)
        if self.j != 0:
            left = self.parent_maze.grid[self.parent_maze.index(self.i, self.j - 1)]
            if not left.visited:
                neighbors.append(left)

        if len(neighbors) == 0:
            return None
        return neighbors[random.randint(0, len(neighbors) - 1)]

    def remove_wall(self, other):
        x = self.j - other.j
        if x == 1:
            self.walls[3] = False
            other.walls[1] = False
        elif x == -1:
            self.walls[1] = False
            other.walls[3] = False
        y = self.i - other.i
        if y == 1:
            self.walls[0] = False
            other.walls[2] = False
        elif y == -1:
            self.walls[2] = False
            other.walls[0] = False
