"""
Button class definition.

This module defines the button class. 
It's used to display the button.
"""

import pygame
from data.utils.colors import *
from data.utils.constants import BG_COLOR, CONTROLS


class Button(pygame.sprite.Sprite):
    def __init__(self, width=150, height=40, position=[], box_color=COLORS[BG_COLOR], color=COLORS[WHITE], text=""):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('Arial', 30)  # setup font
        self.width = width
        self.height = height
        self.position = list(position) or [0, 0]
        self.color = color
        self.box_color = box_color
        self.txt = text
        self.clicked = False
        self.text = self.font.render(self.txt, True, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.box_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def show_text(self, SCREEN):
        SCREEN.blit(self.text, self.position)

    def update(self, menu_pos):
        self.clicked = False
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) or self.rect.collidepoint(menu_pos):
            self.color = COLORS[GREEN]
            if CONTROLS['accept']:
                self.clicked = True
        else:
            self.color = COLORS[WHITE]
        self.text = self.font.render(self.txt, True, self.color)


