import pygame
from sympy import true

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()

background = pygame.image.load("Background_Home_Page.png")

run = True


def setup_screen():
    screen.blit(background, (0, 0))


while run:
    setup_screen()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                run = False
    pygame.display.flip()
pygame.quit()
