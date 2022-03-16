import pygame


class DrawArea:

    def __init__(self, width, height, top_left, color):
        self.width = width
        self.height = height
        self.color = color
        self.canvas = pygame.Rect(0, 0, width, height)
        self.canvas.topleft = top_left
        self.drawing = False
        self.points = []

    def draw_canvas(self, screen, pen_color, pen_size):
        pygame.draw.rect(screen, self.color, self.canvas)
        for point in self.points:
            pygame.draw.circle(screen, pen_color, point, pen_size)

    def interact(self, event):
        if self.drawing:
            self.points.append(event.pos)

