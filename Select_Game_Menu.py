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

# Buttons
prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], (50, 50), 'Prev', False, 50, [(0, 0, 0)],
                              (screen_width / 15, screen_height / 9))
collect_btn = Button.Button('img', ['catch_sheep.png'], (456, 225), '', False, 50, [(255, 255, 255)], (324 + (456/2), 303 + 225/2))
maze_btn = Button.Button('img', ['Maze_button.png'], (456, 225), '', False, 50, [(255, 255, 255)], (820 + (456/2), 303 + 225/2))
handwriting_btn = Button.Button('img', ['Writing_button.png'], (952, 225), '', False, 50, [(255, 255, 255)], (324 + (952/2), 568 + 225/2))
game_btns = [collect_btn, maze_btn, handwriting_btn]

def setup_screen():
    global screen, game_btns
    screen.blit(background, (0, 0))
    for button in game_btns:
        button.draw_button(screen)
    prev_menu_btn.draw_button(screen)

while run:
    setup_screen()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if prev_menu_btn.rect.collidepoint(e.pos):
                raise StopIteration
            if collect_btn.rect.collidepoint(e.pos):
                exec(open('PreMaze.py').read())
            elif collect_btn.rect.collidepoint(e.pos):
                exec(open('Collecting_Task.py').read())
            elif handwriting_btn.rect.collidepoint(e.pos):
                exec(open('Writing_Task.py').read())

    pygame.display.flip()
if not nested:
    pygame.quit()
