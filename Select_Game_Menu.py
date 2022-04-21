import pygame
import InputBox
import Button
import User

nested = True
if not nested:
    pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1600, 900))
(screen_width, screen_height) = pygame.display.get_surface().get_size()
background = pygame.image.load("pickgame.png")

run = True


# Rects
collect_btn = Button.Button('img', ['catch_sheep.png'], (456, 225), '', False, 50, [(255, 255, 255)], (820, 303))
# maze_rect = pygame.Rect(820, 303, 456, 225)
collect_rect = pygame.Rect(324, 303, 456, 225)
handwriting_rect = pygame.Rect(324, 568, 952, 225)


def setup_screen():
    global screen, start_btn
    screen.blit(background, (0, 0))
    collect_btn.draw_button()


while run:
    setup_screen()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if collect_btn.rect.collidepoint(e.pos):
                exec(open('PreMaze.py').read())
            elif collect_rect.collidepoint(e.pos):
                exec(open('Collecting_Task.py').read())
            elif handwriting_rect.collidepoint(e.pos):
                exec(open('Writing_Task.py').read())

    pygame.display.flip()
if not nested:
    pygame.quit()
