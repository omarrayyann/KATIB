import math

import pygame

import DrawArea
import Maze


class Button:

    def __init__(self, image, text, size, center):
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = center
        self.size = size
        self.text = text

    #Drawing all the buttons
    def draw_button(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        text_rect.top = self.rect.top + self.size + 5
        screen.blit(text, text_rect)

    # Button responses
    # def interact(self, needed_info):
    #     if self.interaction == 'clear':
    #         # needed_info = [draw_areas current]
    #         needed_info[0][needed_info[1]].clear_area()
    #     if self.interaction == 'start':
    #         # needed_info = [mazes draw_areas current difficulty width height area_ratio]
    #         maze = PreMaze.create_maze(needed_info[3], needed_info[4], needed_info[5], needed_info[6])
    #         needed_info[0].append(maze)
    #         needed_info[1].append(self.create_draw_area(maze.draw_width, maze.draw_height, needed_info[7]))
    #         needed_info[2] += 1
    #     return needed_info

