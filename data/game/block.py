"""
Block class definition.

This module defines the block class. 
It's used to display and animate the block that moves around on the screen.
"""

import pygame
from data.utils.colors import *
from data.utils.constants import BLOCK_WIDTH, BLOCK_HEIGHT, MOD_IMAGES
from data.utils.asset import load_image
from data.game.ball import *


class Block(pygame.sprite.Sprite):
    def __init__(self, width=BLOCK_WIDTH, height=BLOCK_HEIGHT, position=[], color=COLORS[RED], mod=None):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.position = list(position) or [0, 0]
        self.color = color
        self.status = 0
        self.mod = mod
        if self.mod is None:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
        else:
            self.image, self.rect = load_image(MOD_IMAGES[self.mod])
        self.rect.topleft = self.position

    def update(self, mods_group, paddle, ball_group, walls):
        # update position
        self.position[1] += 3
        self.rect.topleft = self.position

        if self.rect.colliderect(paddle.rect):
            if self.mod == 'expand':
                paddle.score += 1
                paddle.change_size('expand')
            elif self.mod == 'retract':
                paddle.score += 5
                paddle.change_size('retract')
            elif self.mod == 'life':
                if paddle.lives < 20:
                    paddle.lives += 1
                else:
                    paddle.score += 5
            elif self.mod == 'death':
                paddle.score += 20
                paddle.lives -= 1
            elif self.mod == 'big':
                paddle.score += 1
                for ball in ball_group:
                    ball.change_size('big')
            elif self.mod == 'small':
                paddle.score += 5
                for ball in ball_group:
                    ball.change_size('small')
            elif self.mod == 'multiply':
                paddle.score += 1
                for ball in ball_group:
                    ball_group.add(Ball(position=ball.position, velocity=(50, ball.velocity[1]),
                                        color=ball.color, state=ball.state, size=ball.size,  volume=ball.volume))
            elif self.mod == 'snap':
                paddle.score += 1
                for ball in ball_group:
                    ball.state = SNAP
            elif self.mod == 'explosion':
                paddle.score += 1
                for ball in ball_group:
                    ball.color = 'red'
                    ball.change_effect()
            elif self.mod == 'laser':
                paddle.score += 1
                for ball in ball_group:
                    ball.color = 'blue'
                    ball.change_effect()
            mods_group.remove(self)

        elif self.rect.colliderect(walls.rect):  # if it hits the end of map
            mods_group.remove(self)

