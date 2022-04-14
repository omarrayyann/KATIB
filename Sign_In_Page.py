import pygame
import InputBox

pygame.init()
screen = pygame.display.set_mode(1600, 900)
screen_width, screen_height = pygame.display.get_surface().get_size()

background = pygame.image.load("Background_Home_Page.png")

run = True

# Start Button
start_button_width = 592
start_button_height = 76
start_button_x = 503
start_button_y = 679
font = pygame.font.Font('Futura-Bold.otf', 36)
text = font.render("START", True, (0, 0, 0))
text_rect = pygame.Rect(screen_width/2 - text.get_width()/2,
                        start_button_y+text.get_height()/2, 0, 0)
screen.blit(text, text_rect)
rect = pygame.Rect(start_button_x, start_button_y,
                   start_button_width, start_button_height)

# Username Field
username_field_width = 592
username_field_height = 76
username_field_x = 503
username_field_y = 424
username_field = InputBox.InputBox(
    username_field_x, username_field_y, username_field_width, username_field_height)

password_field_width = 592
password_field_height = 76
password_field_x = 503
password_field_y = 526
password_field = InputBox.InputBox(
    password_field_x, password_field_y, password_field_width, password_field_height)


def setup_screen():
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (255, 195, 0), rect,
                     0, int(start_button_height/2))
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, int(start_button_height/2))
    username_field.draw(screen)
    password_field.draw(screen)
    screen.blit(text, text_rect)


print(screen_height, screen_width)

while run:
    setup_screen()
    for e in pygame.event.get():
        username_field.handle_event(e)
        password_field.handle_event(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                run = False
    pygame.display.flip()
pygame.quit()
