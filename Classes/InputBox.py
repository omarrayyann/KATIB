
import pygame


pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = (200, 200, 200)
COLOR_ACTIVE = pygame.Color('black')
FONT = pygame.font.Font('Futura-Medium.otf', 35)


class InputBox:

    def __init__(self, x, y, w, h, place_holder_text, text=''):
        self.h = h
        self.x = x
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.secure = False
        self.cursor_show = False
        self.place_holder_text = place_holder_text
        self.box_list = []

    def get_text(self):
        return self.text

    def get_text_secure(self):
        return "*"*(len(self.text))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.cursor_show = True
                self.active = True
            else:
                self.cursor_show = False
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.move_to_next_box()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.cursor_show = True
                elif self.txt_surface.get_size()[0] >= (self.rect.size[0] - 40):
                    self.cursor_show = False
                else:
                    self.text += event.unicode
                    # print(self.text)
                # Re-render the text.
        # Change the current color of the input box.
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if self.secure:
            self.txt_surface = FONT.render("*" * (len(self.text)), True, self.color)
        else:
            self.txt_surface = FONT.render(self.text, True, self.color)


    def move_to_next_box(self):
        index = self.box_list.index(self)
        if index < len(self.box_list) - 1:
            self.cursor_show = False
            self.active = False
            self.box_list[index + 1].active = True
            self.box_list[index + 1].cursor_show = True


    def draw(self, screen):
        # Blit the text.
        if self.secure:
            screen.blit(self.txt_surface, (self.rect.x + 20, self.rect.y+ self.h/6 + 10))
        else:
            screen.blit(self.txt_surface, (self.rect.x + 20, self.rect.y + self.h/6 + 3))
        if self.cursor_show:
            screen.blit(FONT.render('|', True, self.color), (self.rect.x + 20 + self.txt_surface.get_size()[0], self.rect.y + self.h/6 + 3))
        # Blit the rect.
        if self.get_text() == "":
            font = pygame.font.Font('Futura-Medium.otf', 30)
            placeholder_text = FONT.render(self.place_holder_text, True, (150, 150, 150))
            placeholder_text_rect = placeholder_text.get_rect()
            placeholder_text_rect.center = self.rect.center
            screen.blit(placeholder_text, placeholder_text_rect)
        pygame.draw.rect(screen, self.color, self.rect, 3, int(self.rect.height/3), int(self.rect.height/3))
