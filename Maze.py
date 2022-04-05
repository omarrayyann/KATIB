import pygame
import Cell
import math
import copy
import datetime
import csv
import os


# Return the euclidean distance between 2 points
def dist(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


# Return the midpoint of 2 points
def find_midpoint(point1, point2):
    mid_x = (point1[0] + point2[0]) / 2
    mid_y = (point1[1] + point2[1]) / 2
    return (mid_x, mid_y)


# Return the relative orientation (vertical/horizontal) of 2 points
def relative_orientation(point1, point2):
    if point1[0] == point2[0]:
        return 'v'
    else:
        return 'h'


# The Maze class handles creating and solving the maze
class Maze:
    # The minimum distance between any two points in the set of points Katib needs to follow
    min_distance = 10

    # fence_piece_top_full_res = pygame.image.load('fence_piece.jpg')
    # fence_piece_bottom_full_res = pygame.transform.rotate(fence_piece_top_full_res, 180)
    # fence_piece_left_full_res = pygame.transform.rotate(fence_piece_top_full_res, -90)
    # fence_piece_right_full_res = pygame.transform.rotate(fence_piece_top_full_res, 90)
    # fence_pieces_full_res = [fence_piece_top_full_res, fence_piece_right_full_res, fence_piece_bottom_full_res, fence_piece_left_full_res]

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
        self.katib_points = []
        self.current_point = 0
        self.drawn_solution = []
        self.create_cells()

        # self.fence_pieces = []
        # factor = Maze.fence_pieces_full_res[0].get_size()[0] / self.w
        # for i in range(len(Maze.fence_pieces_full_res)):
        #     dim = Maze.fence_pieces_full_res[i].get_size()
        #     new_size = (dim[0] / factor, dim[1] / factor)
        #     self.fence_pieces.append(pygame.transform.scale(Maze.fence_pieces_full_res[i], new_size))

        self.current = self.grid[0]
        self.stack.append(self.current)
        self.current.visited = True
        self.drawn = False
        self.saved = False
        self.maze_image = ''
        self.time_of_creation = datetime.datetime.now()
        self.version = 0

    # Returns the 1-D index from the column and row indices
    def index(self, i, j):
        return j + self.cols * i

    # Creating the cells of the maze
    def create_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.append(Cell.Cell(i, j, self))

    # Draws out all the cells in the grid list starting from a defined position
    def draw_maze(self, screen, line_color, x_start, y_start, skip, show):
        while skip and not self.drawn:
            self.move(x_start, y_start)
        if self.maze_image != '':  # If we have saved the maze, there's no need for recomputation
            screen.blit(self.maze_image, (x_start, y_start))
        else:
            # Draw every cell in the maze
            for i in range(self.rows):
                for j in range(self.cols):
                    self.grid[self.index(i, j)].draw_cell(screen, line_color, x_start, y_start, self.w)
            # If we still haven't finished drawing the maze, highlight the current for visual purposes
            if not self.drawn:
                self.highlight_current(screen, x_start, y_start)
        # If the maze has been fully drawn and saved, and the user asked for the solution to be shown, draw the solution
        if show and self.saved:
            self.highlight_solution(screen)

    # Hightlights the current cell with a certain color
    def highlight_current(self, screen, x_start, y_start):
        highlight = pygame.draw.rect(screen, (0, 0, 100), pygame.Rect(self.current.j * self.w + x_start + 2,
                                                                      self.current.i * self.w + y_start + 2, self.w - 4,
                                                                      self.w - 4))
        pygame.display.update(highlight)

    # Draws out the solution
    def highlight_solution(self, screen):
        for i in range(len(self.drawn_solution) - 1):
            lin = pygame.draw.line(screen, (100, 100, 100), self.drawn_solution[i], self.drawn_solution[i + 1], 20)

    # This function is called when the stack holds cells from the start to the end points with some needless detours
    # in between
    def find_solution(self, x_start, y_start):
        self.solution_cells = copy.copy(self.stack)  # Produce a copy of the current state of the stack
        self.solution_cells = list(dict.fromkeys(self.solution_cells))  # Remove all redundancies

        # Create the set of points to be drawn and points to be followed by Katib
        for cell in self.solution_cells:
            self.drawn_solution.append(((cell.j + (1 / 2)) * self.w + x_start, (cell.i + (1 / 2)) * self.w + y_start))
            self.katib_points.append(((cell.j + (1 / 2)) * self.w + x_start, (cell.i + (1 / 2)) * self.w + y_start))

        # Remove all redundant points in the drawn solution
        prev_orientation = ''
        for i in range(len(self.drawn_solution) - 1, 0, -1):
            if relative_orientation(self.drawn_solution[i], self.drawn_solution[i - 1]) == prev_orientation:
                self.drawn_solution.pop(i)
            prev_orientation = relative_orientation(self.drawn_solution[i], self.drawn_solution[i - 1])

        # Add points in the katib_points set until no two points are further than min_distance away from each other
        while dist(self.katib_points[len(self.katib_points) - 1],
                   self.katib_points[len(self.katib_points) - 2]) > Maze.min_distance:
            for i in range(1, 2 * len(self.katib_points) - 1, 2):
                point = find_midpoint(self.katib_points[i], self.katib_points[i - 1])
                self.katib_points.insert(i, point)

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

    def save_maze(self, screen, start_x, start_y):
        path = 'save_data'
        if not os.path.exists(path):
            os.mkdir(path)
        path += '\\' + self.time_of_creation.strftime("%d-%m-%Y")
        if not os.path.exists(path):
            os.mkdir(path)
        path += '\\' + self.time_of_creation.strftime("%H-%M-%S")
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = path + '\\Maze_' + self.time_of_creation.strftime("%d-%m-%Y_%H-%M-%S") + '_v.' + str(self.version)
        rect = pygame.Rect(start_x, start_y, self.draw_width, self.draw_height)
        maze_area = screen.subsurface(rect)
        pygame.image.save(maze_area, file_name + '.png')
        f = open(file_name + '.csv', 'w')
        writer = csv.writer(f)
        f.close()
        self.version += 1
