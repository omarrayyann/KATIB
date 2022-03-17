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
        self.breaks = []

    def draw_canvas(self, screen, pen_color, pen_size):
        # pygame.draw.rect(screen, self.color, self.canvas)
        # print('Ye I''m here')
        for i in range(1, len(self.points)):
            is_a_break = False
            for b in self.breaks:
                if b == i - 1:
                    is_a_break = True
            if not is_a_break:
                pygame.draw.line(screen, pen_color, self.points[i-1], self.points[i], pen_size)
            else:
                pygame.draw.circle(screen, pen_color, self.points[i], pen_size/2)

    def interact(self, event):
        if self.drawing:
            self.points.append(event.pos)

    def clear_area(self):
        self.points = []
        self.breaks = []

