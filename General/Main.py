import pygame
from Input import Button
import serial
from Sign_In import Config
import time
import GameParameters

# Electromagnet Setupq
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24

# Setting up screen
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1600, 900))

(screen_width, screen_height) = pygame.display.get_surface().get_size()
boundaries_x = 150
boundaries_y = 150
xl = screen_width - (boundaries_x * 2)
xs = boundaries_x
yl = screen_height - (boundaries_y * 2)
ys = boundaries_y
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

# Setting up images:
# Grass Background
bg = pygame.image.load("../Media/Backgrounds/bbg.jpg")
loading = pygame.image.load("../Media/Backgrounds/loading.png")
pick_game = pygame.image.load("../Media/Backgrounds/pickgame.png")

# Creating menu-less buttons:
# Quit Button
quit_btn = Button.Button('img', ['exit.png'], (50, 50), 'Exit', False, 50, [
    (0, 0, 0)], (screen_width * (14 / 15), screen_height * (1 / 9)))
# Return Button
prev_menu_btn = Button.Button('img', ['go-back-arrow.png'], (50, 50), 'Prev', False, 50, [(0, 0, 0)],
                              (screen_width / 15, screen_height / 9))

# Settings Button
settings_btn = Button.Button('img', ['settings.png'], (50, 50), 'Settings', False, 50, [(0, 0, 0)],
                             (screen_width / 15, screen_height * (8 / 9)))
# start_menu.append(settings_btn)

# Settings Menu:
sign_out_button = Button.Button('rect', [(100, 200, 100), (50, 100, 50)], (100, 50), 'Sign Out', True, 10, [(255, 255, 255), (200, 200, 50)], (2 * screen_width / 15, 2 * screen_height / 9))
settings_menu = [sign_out_button]

collect_btn = Button.Button('img', ['catch_sheep.png'], (456, 225), '', False, 50, [(255, 255, 255)],
                            (324 + (456 / 2), 303 + 225 / 2))
maze_btn = Button.Button('img', ['Maze_button.png'], (456, 225), '', False, 50, [(255, 255, 255)],
                         (820 + (456 / 2), 303 + 225 / 2))
handwriting_btn = Button.Button('img', ['Writing_button.png'], (952, 225), '', False, 50, [(255, 255, 255)],
                                (324 + (952 / 2), 568 + 225 / 2))
game_btns = [collect_btn, maze_btn, handwriting_btn]

# Grouping all menus
menus = [game_btns, settings_menu]


def apply_brightness():
    global screen, screen_height, screen_width, opacity
    s = pygame.Surface((1600, 900), pygame.SRCALPHA)
    s.fill((0, 0, 0, opacity))
    screen.blit(s, (0, 0))


# Function for switching between menus
def switch_to_menu(new_menu):
    global current_menu, prev_menu_stack
    prev_menu_stack.append(current_menu)
    current_menu = new_menu


# Function for calibrating the Katib device
def calibrate():
    # S 600 with the Gerbel protocol.
    # Calibrate
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
    time.sleep(2)
    global calibrated
    calibrated = True
    # Confirmation
    print('Calibrated Katib device... Ready for commands')


try:
    while True:
        if not Config.signed_in:
            pygame.display.set_caption('Sign in screen')
            exec(open('../Sign_In/Sign_In_Page.py').read())
            if not calibrated:
                screen.blit(loading, (0, 0))
                pygame.display.flip()
                calibrate()
        else:
            pygame.display.flip()
            if current_menu == 0:
                screen.blit(pick_game, (0, 0))
            else:
                screen.blit(bg, (0, 0))
            for button in menus[current_menu]:
                button.draw_button(screen)
            quit_btn.draw_button(screen)
            settings_btn.draw_button(screen)
            # Only draws the previous menu button if there is a previous menu to go back to
            if len(prev_menu_stack) != 0:
                prev_menu_btn.draw_button(screen)
            apply_brightness()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise StopIteration
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        raise StopIteration
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if current_menu != 0 and prev_menu_btn.rect.collidepoint(e.pos):
                        current_menu = prev_menu_stack.pop()
                    elif settings_btn.rect.collidepoint(e.pos):
                        switch_to_menu(1)
                    elif quit_btn.rect.collidepoint(e.pos):
                        raise StopIteration
                    if current_menu == 0:
                        if maze_btn.rect.collidepoint(e.pos):
                            exec(open('../Tasks/Maze/Maze_Task.py').read())
                        elif collect_btn.rect.collidepoint(e.pos):
                            exec(open('../Tasks/Collecting/Collecting_Task.py').read())
                        elif handwriting_btn.rect.collidepoint(e.pos):
                            exec(open('../Tasks/Writing/Writing_Task.py').read())
                    elif current_menu == 1:
                        if sign_out_button.rect.collidepoint(e.pos):
                            current_menu = prev_menu_stack.pop()
                            Config.log_out()

except StopIteration:
    pass
if on_katib:
    string2send = str(0.0) + '\n'
    gSer.write(str.encode('M3 S100\n'))
    gSer.write(str.encode('M3 S800\n'))
pygame.quit()
