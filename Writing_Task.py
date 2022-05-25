import pygame
import GameParameters
import DrawArea
import Button
import csv
import os
import string
# import serial

# Setting up game variables:
nested = False
volume = GameParameters.GameParameters.volume
opacity = 255 - GameParameters.GameParameters.brightness
mode = 'letter'
padding = 50
current = 0
show = True

# yl = ys = xl = xs = 0

if not nested:
    # Initializing pygame
    pygame.init()
    # fpsClock = pygame.time.Clock()
    # FPS = 100
    # Electromagnet Setup
    force_pin = 18
    magnet1Pin = 23
    magnet2Pin = 24

    # Screen Setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    (screen_width, screen_height) = pygame.display.get_surface().get_size()
    boundaries_x = 150
    boundaries_y = 150
    xl = screen_width - (boundaries_x * 2)
    xs = boundaries_x
    yl = screen_height - (boundaries_y * 2)
    ys = boundaries_y

pygame.display.set_caption('Writing Serious Game')
bg_color = (0, 0, 0)
start_pos = (xs, ys)
canvas_color = (255, 255, 255)
draw_area = DrawArea.DrawArea(xl, yl, start_pos, canvas_color)

delim = ' '
imageDir = 'Arabic/Image'
letterDir = 'Arabic/Data/'

d = dict.fromkeys(string.ascii_lowercase, [])
letterImg = []
lettersX = []
lettersY = []

cwd = os.getcwd()
Data_path = cwd+"/Arabic/Data_converted"
letter_paths = os.listdir(Data_path)
# print(letter_paths)
for file_name in letter_paths:

    with open(Data_path+'/'+file_name, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=delim)
        x = []
        y = []
        # l = []
        for row in coords:
            if len(row) > 1:
                # print(row, row[0], row[1])
                x.append(int(xs+50+(0.7*xl)*(float(row[0]))))
                y.append(int(ys+50+(0.8*yl)*(float(row[1]))))
    lettersX.append(x)
    lettersY.append(y)

Data_path = cwd+"/Arabic/Image"
letter_paths = os.listdir(Data_path)
for file_name in letter_paths:
    img = pygame.image.load(Data_path + '/' + file_name).convert_alpha(screen)
    img = pygame.transform.scale(img, (50, 50))
    rect = img.get_rect()
    rect.center = (screen_width/2, padding + 25)
    letterImg.append([img, rect])

# Grass Background
bg = pygame.image.load("bbg.jpg")

# Creating Buttons
# Previous menu/exit button
prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], (50, 50), 'Prev', False, 50, [(0, 0, 0)], (screen_width / 15, screen_height / 9))

buttons = []
# Clear Button
clear_btn = Button.Button('img', ['clear.png'], (50, 50), 'Clear', False, 20, [(255, 255, 255)],
                          (0, 0))
buttons.append(clear_btn)

# Previous maze button
prev_btn = Button.Button('img', ['start.png'], (50, 50), 'Prev', False, 20, [(255, 255, 255)],
                         (0, 0))
buttons.append(prev_btn)

# New/Next Maze Button
new_btn = Button.Button('img', ['play.png'], (50, 50), 'Next', False, 20, [(255, 255, 255)],
                        (0, 0))
buttons.append(new_btn)

# Show/Hide Solution Button
sol_btn = Button.Button('img', ['openeye.png', 'closedeye.png'], (50, 50), 'Show Solution', False, 20, [(255, 255, 255)],
                        (0, 0))
buttons.append(sol_btn)

for i in range(len(buttons)):
    buttons[i].move((xs + padding + ((xl - 2 * padding) / (len(buttons) - 1)) * i, draw_area.canvas.bottom + padding))


def draw_solution(current):
    global lettersY, lettersX
    for i in range(len(lettersX[current])):
        pygame.draw.circle(screen, (100, 100, 100), (lettersX[current][i], lettersY[current][i]), 10)


def apply_brightness():
    global screen
    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    screen.blit(s, (0, 0))


try:
    while True:
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), letterImg[current][1])
        screen.blit(letterImg[current][0], letterImg[current][1])
        if show:
            buttons[3].switch_img(0)
            buttons[3].txt = 'Hide Solution'
        else:
            buttons[3].switch_img(1)
            buttons[3].txt = 'Show Solution'
        prev_menu_btn.draw_button(screen)
        draw_area.draw_canvas(screen)
        if show:
            draw_solution(current)
        draw_area.draw_data(screen, (200, 0, 0), 10, )
        apply_brightness()
        for button in buttons:
            button.draw_button(screen)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN and prev_menu_btn.rect.collidepoint(e.pos):
                raise StopIteration
            draw_area.interact(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
            if e.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(e.pos):
                    draw_area.clear_area()
                elif buttons[1].rect.collidepoint(e.pos) and current > 0:
                    draw_area.clear_area()
                    current -= 1
                elif buttons[2].rect.collidepoint(e.pos) and current < len(lettersX) - 1:
                    draw_area.clear_area()
                    current += 1
                elif buttons[3].rect.collidepoint(e.pos):
                    show = not show

except StopIteration:
    pass

if not nested:
    pygame.quit()