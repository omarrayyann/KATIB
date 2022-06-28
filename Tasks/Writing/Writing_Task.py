import pygame
import GameParameters
from Tasks.Shared import DrawArea
from Input import Button
import csv
import os
import string
import serial
import time

# Setting up game variables:
nested = False
volume = GameParameters.GameParameters.volume
opacity = 255 - GameParameters.GameParameters.brightness
mode = 'letter'
padding = 50
current_task = 0
current_point = 0
show = True
haptic_on = True
on_katib = False

if not nested:
    os.chdir('../../')
    # Initializing pygame
    pygame.init()
    # fpsClock = pygame.time.Clock()
    # FPS = 100
    # Electromagnet Setup
    force_pin = 18
    magnet1Pin = 23
    magnet2Pin = 24
    if on_katib:
        global gSer
        gSer = serial.Serial('/dev/ttyACM0', '115200')
        time.sleep(3)
        gSer.flush()
        gSer.flush()
        print(gSer.readline())
        print(gSer.readline())
        time.sleep(1)
        gSer.write(str.encode('$X\n'))
        gSer.write(str.encode('M3 S100\n'))
        gSer.write(str.encode('M3 S600\n'))
        gSer.write(str.encode('$H\n'))

        time.sleep(5)

        gSer.write(str.encode('$X\n'))
        gSer.write(str.encode('M3 S600\n'))
        time.sleep(1)
        gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
        print(gSer.readline())
        time.sleep(0.1)
        gSer.write(str.encode('G21 X25  Y-10 F4000\n'))
        print(gSer.readline())
        time.sleep(0.1)
        gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
        print(gSer.readline())
        time.sleep(2)
        gSer.write(str.encode('$X\n'))
        print(gSer.readline())
        gSer.write(str.encode('M3 S1000\n'))
        print(gSer.readline())
        gSer.write(str.encode(' G21 X0 Y-154 F4000\n'))
        print(gSer.readline())
        gSer.write(str.encode('$X\n'))
        gSer.write(str.encode(' G21 X250 Y-154 F4000\n'))
        print(gSer.readline())
        gSer.write(str.encode('$X\n'))
        gSer.write(str.encode(' G21 X0 Y0 F4000\n'))
        print(gSer.readline())
        gSer.write(str.encode('$X\n'))
        gSer.write(str.encode('M3 S1000\n'))

    # Screen Setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    (screen_width, screen_height) = pygame.display.get_surface().get_size()
    boundaries_x = 150
    boundaries_y = 150
    y_length = screen_height - (boundaries_y * 2)
    x_length = y_length
    x_size = (screen_width - x_length) / 2
    y_size = boundaries_y

magnet_point = pygame.draw.circle(screen, (100, 0, 0), (0, 0), 30)
pygame.display.set_caption('Writing Serious Game')
bg_color = (0, 0, 0)
start_pos = (x_size, y_size)
canvas_color = (255, 255, 255)
draw_area = DrawArea.DrawArea(x_length, y_length, start_pos, canvas_color)

delim = ' '
imageDir = 'Letters_Data/Arabic/Image'
letterDir = 'Letters_Data/Arabic/Data/'

d = dict.fromkeys(string.ascii_lowercase, [])
letterImg = []
lettersX = []
lettersY = []

cwd = os.getcwd()
Data_path = cwd+"/Letters_Data/Arabic/Data_KMCP_Equidistant"
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
                x.append(int(x_size+50+(0.7*x_length)*(float(row[0]))))
                y.append(int(y_size+50+(0.8*y_length)*(float(row[1]))))
    lettersX.append(x)
    lettersY.append(y)

Data_path = cwd+"/Letters_Data/Arabic/Image"
letter_paths = os.listdir(Data_path)
for file_name in letter_paths:
    img = pygame.image.load(Data_path + '/' + file_name).convert_alpha(screen)
    img = pygame.transform.scale(img, (50, 50))
    rect = img.get_rect()
    rect.center = (screen_width/2, padding + 25)
    letterImg.append([img, rect])

# Grass Background
bg = pygame.image.load("Media/Backgrounds/bbg.jpg")

# Creating Buttons
# Previous menu/exit button
prev_menu_btn = Button.Button('img', ['Media/Images/go-back-arrow.png'], (50, 50), 'Prev', False, 50, [(0, 0, 0)], (screen_width / 15, screen_height / 9))

buttons = []
# Clear Button
clear_btn = Button.Button('img', ['Media/Images/clear.png'], (50, 50), 'Clear', False, 20, [(255, 255, 255)],
                          (0, 0))
buttons.append(clear_btn)

# Previous maze button
prev_btn = Button.Button('img', ['Media/Images/start.png'], (50, 50), 'Prev', False, 20, [(255, 255, 255)],
                         (0, 0))
buttons.append(prev_btn)

# New/Next Maze Button
new_btn = Button.Button('img', ['Media/Images/play.png'], (50, 50), 'Next', False, 20, [(255, 255, 255)],
                        (0, 0))
buttons.append(new_btn)

# Show/Hide Solution Button
sol_btn = Button.Button('img', ['Media/Images/openeye.png', 'Media/Images/closedeye.png'], (50, 50), 'Show Solution', False, 20, [(255, 255, 255)],
                        (0, 0))
buttons.append(sol_btn)

for i in range(len(buttons)):
    buttons[i].move((x_size + padding + ((x_length - 2 * padding) / (len(buttons) - 1)) * i, draw_area.canvas.bottom + padding))

# Draws the point at which the magnet is present
def draw_magnet():
    global screen, magnet_point, current_point, current_task
    magnet_point = pygame.draw.circle(screen, (100, 0, 0), (lettersX[current_task][current_point], lettersY[current_task][current_point]), 10)


def getCoords(xn, yn):
    global x_length, x_size, y_size, y_length
    print(" xN: ", xn, " yN: ", yn)
    if xn < x_size +x_length and xn >= x_size:
        xn = (xn-x_size)/x_length
    else:
        return
    if yn < y_size +y_length and yn >= y_size:
        yn = (yn-y_size)/y_length
    else:
        return
    fx = 305*xn
    fy = -140*yn
    return fx, fy

def draw_solution(current_task):
    global lettersY, lettersX
    for i in range(len(lettersX[current_task])):
        pygame.draw.circle(screen, (100, 100, 100), (lettersX[current_task][i], lettersY[current_task][i]), 10)


def apply_brightness():
    global screen
    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    screen.blit(s, (0, 0))


try:
    while True:
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), letterImg[current_task][1])
        screen.blit(letterImg[current_task][0], letterImg[current_task][1])
        if show:
            buttons[3].switch_img(0)
            buttons[3].txt = 'Hide Solution'
        else:
            buttons[3].switch_img(1)
            buttons[3].txt = 'Show Solution'
        prev_menu_btn.draw_button(screen)
        draw_area.draw_canvas(screen)
        if show:
            draw_solution(current_task)
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
            if magnet_point.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and current_point < len(lettersX[current_task]) - 1:
                current_point += 1
                xp0, yp0 = (lettersX[current_task][current_point], lettersY[current_task][current_point])
                x_magnet = xp0
                y_magnet = yp0
                xc, yc = getCoords(xp0, yp0)
                print("pixels x %f , y %f", (xp0, yp0))
                print(xc, yc)
                gcodeString = "G21 X" + \
                              "{:.3f}".format(xc) + " Y" + "{:.3f}".format(yc) + " F4000\n"
                print(gcodeString)
                if nested and haptic_on and on_katib:
                    gSer.write(str.encode(gcodeString))
            if e.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(e.pos):
                    draw_area.clear_area()
                    current_point = 0
                elif buttons[1].rect.collidepoint(e.pos) and current_task > 0:
                    draw_area.clear_area()
                    current_task -= 1
                    current_point = 0
                elif buttons[2].rect.collidepoint(e.pos) and current_task < len(lettersX) - 1:
                    draw_area.clear_area()
                    current_task += 1
                    current_point = 0
                elif buttons[3].rect.collidepoint(e.pos):
                    show = not show
        # draw_magnet()

except StopIteration:
    pass
if on_katib:
    string2send = str(0.0) + '\n'
    gSer.write(str.encode('M3 S100\n'))
    gSer.write(str.encode('M3 S800\n'))
if not nested:
    pygame.quit()