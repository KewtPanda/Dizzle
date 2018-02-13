"""
Block class definition.

This module defines the block class. 
It's used to display and animate the block that moves around on the screen.
"""

import pygame
from data.utils.colors import *


class Square(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50, position=[], color=COLORS[RED]):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.position = list(position) or [0, 0]
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position