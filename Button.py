import pygame


class Button:

    def __init__(self, image, text, size, center, interaction):
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = center
        self.size = size
        self.text = text
        self.interaction = interaction

    def draw_button(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        text_rect.top = self.rect.top + self.size + 5
        screen.blit(text, text_rect)
