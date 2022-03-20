import pygame
import Cell
import math
import copy


def dist(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


def find_midpoint(point1, point2):
    mid_x = (point1[0] + point2[0]) / 2
    mid_y = (point1[1] + point2[1]) / 2
    return (mid_x, mid_y)


# The Maze class handles creating and solving the maze
class Maze:
    min_distance = 10
    resolution = 10

    # Constructor
    def __init__(self, w, draw_width, draw_height):
        self.w = w
        self.draw_width = draw_width
        self.draw_height = draw_height
        self.cols = math.floor(draw_width / w)
        self.rows = math.floor(draw_height / w)
        self.grid = []
        self.stack = []
        self.solution_cells = []
        self.solution_points = []
        self.create_cells()
        self.current = self.grid[0]
        self.stack.append(self.current)
        self.current.visited = True
        self.drawn = False
        self.saved = False
        self.maze_image = ''

    # Returns the 1-D index from the column and row indeces
    def index(self, i, j):
        return j + self.cols * i

    # Creating the cells of the maze
    def create_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.append(Cell.Cell(i, j, self))

    # Draws out all the cells in the grid list starting from a defined position
    def draw_maze(self, screen, line_color, x_start, y_start, show):
        if self.maze_image != '':
            screen.blit(self.maze_image, (x_start, y_start))
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.grid[self.index(i, j)].draw_cell(screen, line_color, x_start, y_start, self.w)
            if not self.drawn:
                self.highlight_current(screen, x_start, y_start)
        if show:
            self.highlight_solution(screen)

    def highlight_current(self, screen, x_start, y_start):
        highlight = pygame.draw.rect(screen, (0, 0, 100), pygame.Rect(self.current.j * self.w + x_start + 2,
                                                                      self.current.i * self.w + y_start + 2, self.w - 4,
                                                                      self.w - 4))
        pygame.display.update(highlight)

    def highlight_solution(self, screen):
        for i in range(0, len(self.solution_points), Maze.resolution):
            circle = pygame.draw.circle(screen, (100, 100, 100), self.solution_points[i], 10)
            pygame.display.update(circle)

    def find_solution(self, x_start, y_start):
        self.solution_cells = copy.copy(self.stack)
        self.solution_cells = list(dict.fromkeys(self.solution_cells))
        for cell in self.solution_cells:
            self.solution_points.append(((cell.j + (1 / 2)) * self.w + x_start, (cell.i + (1 / 2)) * self.w + y_start))
        while dist(self.solution_points[len(self.solution_points) - 1],
                   self.solution_points[len(self.solution_points) - 2]) > Maze.min_distance:
            for i in range(1, 2 * len(self.solution_points) - 1, 2):
                point = find_midpoint(self.solution_points[i], self.solution_points[i - 1])
                self.solution_points.insert(i, point)

    def move(self, x_start, y_start):
        next_cell = self.current.check_neighbors()
        if next_cell:
            self.current.remove_wall(next_cell)
            self.current = next_cell
            self.current.visited = True
            self.stack.append(self.current)
            if self.current == self.grid[len(self.grid) - 1]:
                self.find_solution(x_start, y_start)
                self.current = self.stack[len(self.stack) - 2]
                self.stack.pop()
        elif len(self.stack) != 0:
            self.current = self.stack[len(self.stack) - 2]
            self.stack.pop()
        elif len(self.stack) == 0:
            self.drawn = True
