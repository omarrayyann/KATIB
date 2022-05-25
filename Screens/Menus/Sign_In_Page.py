import pygame

import Data
import InputBox
import Button
import User
import Config

nested = True
if not nested:
    pygame.init()
screen = pygame.display.set_mode((1600, 900))
# screen = pygame.display.set_mode((1600, 900))
(screen_width, screen_height) = pygame.display.get_surface().get_size()
background = pygame.image.load("background2.png")

run = True

start_rect = pygame.Rect(504, 661, 592, 76)
font = pygame.font.Font('Futura-Bold.otf', 36)
start_btn = Button.Button('rect', [(255, 195, 0), (0, 0, 0)], (592, 76), 'START', True, 36,
                          [(0, 0, 0), (255, 195, 0)], (504 + 592/2, 661 + 76/2))
start_btn.set_corner_radius(int(start_btn.size[1]/2))
start_btn.set_font(font)

# Username Field
username_field_width = 592
username_field_height = 76
username_field_x = 500
username_field_y = 389
username_field = InputBox.InputBox(
    username_field_x, username_field_y, username_field_width, username_field_height, "Username")
username_field_rect = pygame.Rect(
    username_field_x, username_field_y, username_field_width, username_field_height)

password_field_width = 592
password_field_height = 76
password_field_x = 500
password_field_y = 491
password_field = InputBox.InputBox(
    password_field_x, password_field_y, password_field_width, password_field_height, "Password")
password_field_rect = pygame.Rect(
    password_field_x, password_field_y, password_field_width, password_field_height)
password_field.secure = True


fields = [username_field, password_field]

error_text = ""
error = False


def setup_screen():
    global screen, start_btn
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), username_field_rect, 0, int(
        username_field_rect.height/3), int(
        username_field_rect.height/3))
    pygame.draw.rect(screen, (255, 255, 255), password_field_rect, 0, int(
        password_field_rect.height/3), int(
        password_field_rect.height/3))
    start_btn.draw_button(screen)
    username_field.draw(screen)
    password_field.draw(screen)
    pygame.draw.rect(screen, (0, 0, 0), start_rect, 2, 38)
    if error:
        font = pygame.font.Font('Futura-Medium.otf', 20)
        error_label = font.render(error_text, True, (150, 0, 0))
        error_label_rect = pygame.Rect(screen_width/2 - error_label.get_width(
        )/2, password_field_y + error_label.get_height()/2 + 85, 0, 0)
        screen.blit(error_label, error_label_rect)


def clicked_start():
    global error, run, error_text
    if Config.log_in(username_field.text, password_field.text):
        print("success logging in")
        run = False

    else:
        print("failed signing in")
        error_text = "Wrong Username or Password, please try again!"
        error = True


while run:
    setup_screen()
    for e in pygame.event.get():
        username_field.handle_event(e)
        password_field.handle_event(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                active = False
                for field in fields:
                    if field.active:
                        active = True
                run = active
                if not run:
                    raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN and (username_field.rect.collidepoint(e.pos) or password_field.rect.collidepoint(e.pos)):
            error = False
        if e.type == pygame.MOUSEBUTTONDOWN and start_btn.rect.collidepoint(e.pos):
            clicked_start()

    pygame.display.flip()
if not nested:
    pygame.quit()
