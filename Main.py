import pygame
import Button
import serial
import time
import GameParameters
import os

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Setting up screen
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
(width, height) = pygame.display.get_surface().get_size()
pygame.display.set_caption('Serious Games')

# Setting up game variables:
volume = GameParameters.GameParameters.volume
opacity = 255 - GameParameters.GameParameters.brightness
current_menu = 0
prev_menu_stack = []
calibrated = False
on_katib = False

# Design Variables:
padding = 20

gSer = ''

# Setting up the serial connection
if on_katib:
    gSer = serial.Serial('/dev/ttyACM0', '115200')
    time.sleep(3)
    gSer.flush()
    gSer.flush()
    print(gSer.readline())
    print(gSer.readline())
    time.sleep(1)
    gSer.write(str.encode('$X\n'))
    gSer.write(str.encode('M3 S100\n'))
    gSer.write(str.encode('M3 S500\n'))
    gSer.write(str.encode('$H\n'))
    time.sleep(5)

# Setting up images:
# Grass Background
bg = pygame.image.load("bbg.jpg")

# Creating menu-less buttons:
# Quit Button
quit_btn = Button.Button('img', ['exit.png'], 50, 'Exit', False, 50, [(0, 0, 0)], (width * (14 / 15), height * (1 / 9)))
# Return Button
prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], 50, 'Prev', False, 50, [(0, 0, 0)],
                              (width / 15, height / 9))

# Start Menu:
start_menu = []
# Start Button
start_btn = Button.Button('img', ['play.png'], 150, 'PLAY', True, 20, [(255, 255, 255)], (width / 2, height / 2))
start_menu.append(start_btn)
# Settings Button
settings_btn = Button.Button('img', ['settings.png'], 50, 'Settings', False, 50, [(0, 0, 0)],
                             (width / 15, height * (8 / 9)))
start_menu.append(settings_btn)

# Settings Menu:
settings_menu = []

# Games Menu:
games_menu = []
# Round-the-Sheep Button
rnd_shp_btn = Button.Button('rect', [(0, 0, 0), (50, 50, 50)], (200, 100), 'Round the Sheep', True, 20,
                            [(255, 255, 255), (200, 200, 50)], (0, 0))
# Maze Button
maze_btn = Button.Button('rect', [(0, 0, 0), (50, 50, 50)], (200, 100), 'Maze', True, 20,
                         [(255, 255, 255), (200, 200, 50)], (0, 0))
# Hand-writing Button
hnd_wrtng_btn = Button.Button('rect', [(0, 0, 0), (50, 50, 50)], (200, 100), 'Hand-Writing', True, 20,
                              [(255, 255, 255), (200, 200, 50)], (0, 0))
games_menu.append(rnd_shp_btn)
games_menu.append(maze_btn)
games_menu.append(hnd_wrtng_btn)

for i in range(len(games_menu)):
    games_menu[i].move((width / 2, height / len(games_menu) + i * (games_menu[i].size[1] + padding)))

# Grouping all menus
menus = [start_menu, games_menu, settings_menu]


def apply_brightness(surf):
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    surf.blit(s, (0, 0))


# Function for switching between menus
def switch_to_menu(new_menu):
    global current_menu
    prev_menu_stack.append(current_menu)
    current_menu = new_menu


# Function for calibrating the Katib device
def calibrate():
    # S 600 with the Gerbel protocol.
    # Calibrate
    gSer.write(str.encode('$X\n'))
    gSer.write(str.encode('M3 S500\n'))
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
    time.sleep(2)
    global calibrated
    calibrated = True
    # Confirmation
    print('Calibrated Katib device... Ready for commands')
    pygame.mixer.init()  # Initialize the mixer module.
    sound1 = pygame.mixer.Sound('success.mp3')  # Load a sound.


try:
    while True:
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        for button in menus[current_menu]:
            button.draw_button(screen)
        quit_btn.draw_button(screen)
        # Only draws the previous menu button if there is a previous menu to go back to
        if len(prev_menu_stack) != 0:
            prev_menu_btn.draw_button(screen)
        apply_brightness(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                if current_menu != 0 and prev_menu_btn.rect.collidepoint(e.pos):
                    current_menu = prev_menu_stack.pop()
                elif quit_btn.rect.collidepoint(e.pos):
                    raise StopIteration
                if current_menu == 0:
                    if start_menu[0].rect.collidepoint(e.pos):
                        if not calibrated and on_katib:
                            calibrate()
                        switch_to_menu(1)
                    elif start_menu[1].rect.collidepoint(e.pos):
                        switch_to_menu(2)
                elif current_menu == 1:
                    if games_menu[0].rect.collidepoint(e.pos):
                        exec(open('Collecting_Task.py').read())
                    elif games_menu[1].rect.collidepoint(e.pos):
                        exec(open('PreMaze.py').read())
except StopIteration:
    pass
if on_katib:
    string2send = str(0.0) + '\n'
    gSer.write(str.encode('M3 S100\n'))
    gSer.write(str.encode('M3 S800\n'))
pygame.quit()
