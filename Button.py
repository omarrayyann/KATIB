import math

import pygame

import DrawArea
import Maze


class Button:

    def __init__(self, btn_type, imgs_or_colors, size, txt, show_txt, font_size, font_clrs, center):
        self.btn_type = btn_type
        self.size = size
        self.center = center
        self.font_size = font_size
        self.txt = txt
        self.font_clrs = font_clrs
        self.mode_index = 0
        self.show_txt = show_txt
        if self.btn_type == 'img':
            self.imgs = imgs_or_colors
            self.img = pygame.image.load(self.imgs[0]).convert_alpha()
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            self.rect = self.img.get_rect()
        elif self.btn_type == 'rect':
            self.rect_clrs = imgs_or_colors
            self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = center

    # Resizing the image and/or text
    def resize(self, new_img_size, new_font_size):
        self.size = new_img_size
        self.img = self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.rect = self.img.get_rect()
        self.rect.center = self.center
        self.font_size = new_font_size

    def move(self, new_center):
        self.center = new_center
        self.rect.center = self.center

    def toggle_show(self):
        self.show_txt = not self.show_txt

    # Drawing a button
    def draw_button(self, screen):
        if self.btn_type == 'rect':
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.hover_mode()
            else:
                self.dormant_mode()
        if self.btn_type == 'img':
            screen.blit(self.img, self.rect)
        elif self.btn_type == 'rect':
            pygame.draw.rect(screen, self.rect_clrs[self.mode_index], self.rect, 0, 3)
        if self.show_txt:
            font = pygame.font.Font('freesansbold.ttf', self.font_size)
            text = font.render(self.txt, True, self.font_clrs[self.mode_index])
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            if self.btn_type == 'img':
                text_rect.top = self.rect.top + self.size + 5
            screen.blit(text, text_rect)

    def hover_mode(self):
        self.switch_mode(1)

    def dormant_mode(self):
        self.switch_mode(0)

    def switch_img(self, index, size):
        self.img = pygame.image.load(self.imgs[index]).convert_alpha()
        self.size = size
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        prev_center = self.rect.center
        self.rect = self.img.get_rect()
        self.rect.center = prev_center

    def switch_mode(self, index):
        self.mode_index = index
