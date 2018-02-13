"""
Block class definition.

This module defines the block class. 
It's used to display and animate the block that moves around on the screen.
"""

import pygame
from data.utils.colors import *
from data.utils.asset import load_image
from data.utils.constants import MOD_IMAGES


class Mod(pygame.sprite.Sprite):
    def __init__(self, SCREEN, position=[], block="", text="", text_color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.position = list(position) or [0, 0]
        self.image, self.rect = load_image(MOD_IMAGES[block])
        self.rect.topleft = self.position

        self.font = pygame.font.SysFont('Arial', 24)  # setup font
        self.text = self.font.render(text, True, COLORS[text_color])
        SCREEN.blit(self.text, (self.position[0]+50, self.position[1]))
