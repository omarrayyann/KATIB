import pygame
import Cell
import math
import copy


# The Maze class handles creating and solving the maze
class Maze:

    # Constructor
    def __init__(self, w, draw_width, draw_height):
        self.w = w
        self.draw_width = draw_width
        self.draw_height = draw_height
        self.cols = math.floor(draw_width / w)
        self.rows = math.floor(draw_height / w)
        self.grid = []
        self.stack = []
        self.solution = []
        self.create_cells()
        self.current = self.grid[0]
        self.stack.append(self.current)
        self.current.visited = True
        self.drawn = False

    # Returns the 1-D index from the column and row indeces
    def index(self, i, j):
        return j + self.cols * i

    # Creating the cells of the maze
    def create_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.append(Cell.Cell(i, j, self))

    # Draws out all the cells in the grid list starting from a defined position
    def draw_maze(self, screen, line_color, x_start, y_start):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[self.index(i, j)].draw_cell(screen, line_color, x_start, y_start, self.w)
        self.highlight_current(screen, x_start, y_start)
        #if len(self.solution) != 0 and len(self.stack) == 0:
            #self.highlight_solution(screen, x_start, y_start)

    def highlight_current(self, screen, x_start, y_start):
        pygame.draw.rect(screen, (0, 0, 100), pygame.Rect(self.current.j * self.w + x_start + 2, self.current.i * self.w + y_start + 2, self.w - 4, self.w - 4))

    def highlight_solution(self, screen, x_start, y_start):
        for cell in self.solution:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(cell.j * self.w + x_start + 2, cell.i * self.w + y_start + 2, self.w - 4, self.w - 4))

    def find_solution(self):
        self.solution = copy.copy(self.stack)
        # self.solution = list(dict.fromkeys(self.solution))

    def move(self):
        next_cell = self.current.check_neighbors()
        if next_cell:
            self.current.remove_wall(next_cell)
            self.current = next_cell
            self.current.visited = True
            self.stack.append(self.current)
            if self.current == self.grid[len(self.grid) - 1]:
                self.find_solution()
                self.current = self.stack[len(self.stack) - 2]
                self.stack.pop()
        elif len(self.stack) != 0:
            self.current = self.stack[len(self.stack) - 2]
            self.stack.pop()
        elif len(self.stack) == 0:
            self.drawn = True
