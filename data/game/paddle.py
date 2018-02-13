"""
Paddle class definition.

This module defines the paddle class. 
It's used to display and animate the paddle that moves around on the screen.
"""

import pygame
from data.utils.colors import *
from data.utils.constants import RESOLUTION, BLOCK_WIDTH, BLOCK_HEIGHT


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width=BLOCK_WIDTH * 100 / 30, height=BLOCK_HEIGHT * 10 / 12, position=[], color=COLORS[TEAL],
                 level=1, score=0, lives=3):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.original_width = self.width
        self.height = height
        self.position = list(position) or [0, 0]
        self.color = color
        self.level = level
        self.score = score
        self.lives = lives
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.paddle_x, self.paddle_y = self.position
        self.rect.center = (self.paddle_x, self.paddle_y)

    def change_size(self, size):
        if size == 'expand' and self.width < self.original_width * 2:
            self.width *= 2
        elif size == 'retract' and self.width > self.original_width / 2:
            self.width /= 2
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self):
        # get mouse position
        self.paddle_x, mouse_y = pygame.mouse.get_pos()

        # check if mouse is to far to the sides
        if self.paddle_x < self.width / 2:
            self.paddle_x = self.width / 2
        elif self.paddle_x > RESOLUTION[0] - self.width / 2:
            self.paddle_x = RESOLUTION[0] - self.width / 2

        # update position
        self.rect.center = (self.paddle_x, self.paddle_y)
