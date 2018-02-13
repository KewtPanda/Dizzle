"""
Ball class definition.

This module defines the ball class. 
It's used to display and animate balls that bounce around the screen.
"""

import pygame
import math
import random
from data.utils.constants import RESOLUTION, DT, BALL_SOUNDS, BALL_IMAGES, BLOCK_HEIGHT, MOD_IMAGES, MOD_CHANCE, \
    SOUND_PATH
from data.utils.asset import load_image, load_sound
from data.utils.colors import *
from data.utils.state import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, position=[], velocity=[], color=WHITE, state=STOP, size=int(BLOCK_HEIGHT * 10 / 6), volume=0.50):
        pygame.sprite.Sprite.__init__(self)
        self.position = list(position) or [0, 0]
        self.velocity = list(velocity) or [0, 0]
        self.color = color
        self.state = state
        self.snap_once = False
        self.snap_x_pos = 0
        self.size = size
        self.original_size = self.size
        self.effect = BALL_EFFECTS[self.color]
        self.angle = 0
        self.volume = volume
        self.snap_sound = True
        self.sound = load_sound(BALL_SOUNDS[self.effect])
        self.sound.set_volume(self.volume)
        self.sound_bounce = load_sound(BALL_SOUNDS['bounce'])
        self.sound_bounce.set_volume(self.volume)
        self.sound_laser_now = pygame.time.get_ticks()
        self.sound_laser_last = 0

        self.original_image, self.original_rect = load_image(BALL_IMAGES[self.color])
        # self.image = pygame.image.load('images/ball_football.png').convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image,
                                                   (self.size, self.size))  # scale image to default size
        self.scaled_rect = self.scaled_image.get_rect()
        self.rotation_rect = self.scaled_rect.copy()
        self.image = self.scaled_image
        self.rect = self.image.get_rect()

        self.radius = self.rect.size[0] / 2
        self.rect.center = self.position
        self.bounds = (RESOLUTION[0] - self.radius, RESOLUTION[1] - self.radius)

    def change_effect(self, volume=0.50):
        self.effect = BALL_EFFECTS[self.color]
        self.volume = volume
        self.sound = load_sound(BALL_SOUNDS[self.effect])
        self.sound.set_volume(self.volume)
        self.original_image, self.original_rect = load_image(BALL_IMAGES[self.color])
        self.scaled_image = pygame.transform.scale(self.original_image,
                                                   (self.size, self.size))  # scale image to default size
        self.scaled_rect = self.scaled_image.get_rect()
        self.image = self.scaled_image
        self.rect = self.image.get_rect()

        self.radius = self.rect.size[0] / 2
        self.rect.center = self.position
        self.bounds = (RESOLUTION[0] - self.radius, RESOLUTION[1] - self.radius)

    def change_size(self, size):
        if size == 'big' and self.size <= self.original_size:
            self.size = int(self.size * 2)
            self.scaled_image = pygame.transform.scale(self.original_image,
                                                       (self.size, self.size))  # scale image to default size
            self.scaled_rect = self.scaled_image.get_rect()
            self.image = self.scaled_image
            self.rect = self.image.get_rect()

            self.radius = self.rect.size[0] / 2
            self.rect.center = self.position
            self.bounds = (RESOLUTION[0] - self.radius, RESOLUTION[1] - self.radius)
        elif size == 'small' and self.size >= self.original_size:
            self.size = int(self.size / 2)
            self.scaled_image = pygame.transform.scale(self.original_image,
                                                       (self.size, self.size))  # scale image to default size
            self.scaled_rect = self.scaled_image.get_rect()
            self.image = self.scaled_image
            self.rect = self.image.get_rect()

            self.radius = self.rect.size[0] / 2
            self.rect.center = self.position
            self.bounds = (RESOLUTION[0] - self.radius, RESOLUTION[1] - self.radius)

    # rotate the ball
    def rotate(self, paddle):
        if self.state == STOP:
            self.angle = 0
        elif self.state == SNAP and self.rect.colliderect(paddle.rect):
            pass
        elif self.velocity[0] < 0:
            self.angle += math.fabs(self.velocity[0] * 0.025)
            self.angle %= 360
        elif self.velocity[0] > 0:
            self.angle -= math.fabs(self.velocity[0] * 0.025)
            self.angle %= 360

        # self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = pygame.transform.rotozoom(self.scaled_image, self.angle, 1.0)
        self.rotation_rect = self.scaled_rect.copy()
        self.rotation_rect.center = self.image.get_rect().center
        self.image = self.image.subsurface(self.rotation_rect).copy()
        self.rect.center = self.position

    # move the ball
    def move(self, paddle, joy_start):
        if self.state == STOP:
            self.position[0] = paddle.paddle_x
            self.position[1] = paddle.paddle_y - paddle.height / 2 - self.radius
            if pygame.mouse.get_pressed()[0] or joy_start:
                self.state = RUN
        elif self.state == SNAP:
            if self.snap_once:
                self.position[0] = paddle.paddle_x + self.snap_x_pos
                self.position[1] = paddle.paddle_y - paddle.height / 2 - self.radius + 1
                if pygame.mouse.get_pressed()[0] or joy_start:
                    self.snap_sound = True
                    self.snap_once = False
                    if self.velocity[1] > 0:
                        self.velocity[1] *= -1
                    self.position[0] += self.velocity[0] * DT
                    self.position[1] += self.velocity[1] * DT
            elif not self.snap_once:
                if self.rect.colliderect(paddle.rect):
                    self.snap_once = True
                    self.snap_x_pos = self.position[0] - paddle.paddle_x
                else:
                    self.position[0] += self.velocity[0] * DT
                    self.position[1] += self.velocity[1] * DT
        elif self.state == RUN:
            self.position[0] += self.velocity[0] * DT
            self.position[1] += self.velocity[1] * DT

        self.rect.center = self.position

    # check ball collision
    def check_collision(self, paddle, level_group, balls):
        # check if ball hits left side
        if self.position[0] < self.radius:
            self.position[0] = self.radius
            self.velocity[0] *= -1
            self.sound_bounce.play()

        # check if ball hits right side
        elif self.position[0] > self.bounds[0]:
            self.position[0] = self.bounds[0]
            self.velocity[0] *= -1
            self.sound_bounce.play()

            # check if ball hits top side
        elif self.position[1] < self.radius:
            self.position[1] = self.radius
            self.velocity[1] *= -1
            self.sound_bounce.play()

            # check if ball hits the paddle
        if self.rect.colliderect(paddle.rect):
            self.velocity[1] *= -1
            self.velocity[0] = (self.position[0] - paddle.paddle_x) * 10
            if self.state == SNAP:
                if self.snap_sound:
                    self.sound_bounce.play()
                    self.snap_sound = False
            else:
                self.sound_bounce.play()

        # check if ball collide with a block
        for element in level_group:
            if self.rect.colliderect(element.rect):
                paddle.score += 1
                # position to ball in contrast to block
                diff_x = self.position[0] - (element.position[0] + element.width / 2)
                diff_y = self.position[1] - (element.position[1] + element.height / 2)
                pheta = math.degrees(math.atan((self.radius + element.height / 2) / (self.radius + element.width / 2)))  # angle to decides what direction to reverse)

                # do something with the different ball effects
                if self.effect == NORMAL:
                    self.sound.play()
                    if diff_x == 0:  # if tan is in "deadzone"
                        self.velocity[1] *= -1
                    else:
                        alpha = math.degrees(math.atan(diff_y / diff_x))  # angle of ball in relation to block
                        if alpha <= (-pheta) or alpha >= pheta:
                            self.velocity[1] *= -1
                        else:
                            self.velocity[0] *= -1

                elif self.effect == EXPLOSION:
                    self.sound.play()
                    if diff_x == 0:  # if tan is in "deadzone"
                        self.velocity[1] *= -1
                    else:
                        alpha = math.degrees(math.atan(diff_y / diff_x))  # angle of ball in relation to block
                        if alpha <= (-pheta) or alpha >= pheta:
                            self.velocity[1] *= -1
                        else:
                            self.velocity[0] *= -1
                    explosion_points = [(element.position[0] - element.width, element.position[1]),
                                        (element.position[0] - element.width, element.position[1] - element.height),
                                        (element.position[0], element.position[1] - element.height),
                                        (element.position[0] + element.width * 2, element.position[1] - element.height),
                                        (element.position[0] + element.width * 2, element.position[1]),
                                        (element.position[0] + element.width * 2,
                                         element.position[1] + element.height * 2),
                                        (element.position[0], element.position[1] + element.height * 2),
                                        (element.position[0] - element.width, element.position[1] + element.height * 2)]
                    for exp_ele in level_group:
                        for pos in explosion_points:
                            if exp_ele.rect.collidepoint(pos):
                                level_group.remove(exp_ele)

                elif self.effect == LASER:
                    self.sound_laser_now = pygame.time.get_ticks()
                    if self.sound_laser_now > self.sound_laser_last + 100:
                        self.sound.play()
                    self.sound_laser_last = pygame.time.get_ticks()

                elif self.effect == PLASMA:
                    self.sound.play()
                    explosion_points = [(element.position[0] - element.width, element.position[1]),
                                        (element.position[0] + element.width * 2, element.position[1])]
                    for exp_ele in level_group:
                        for pos in explosion_points:
                            if exp_ele.rect.collidepoint(pos):
                                level_group.remove(exp_ele)

                if random.randint(1, int(100/MOD_CHANCE)) == 1:
                    pos = element.position
                    level_group.remove(element)
                    return pos
                level_group.remove(element)
                return None

    # update function for the ball
    def update(self, paddle, level_group, ball, joy_start):
        self.rotate(paddle)
        pos = self.check_collision(paddle, level_group, ball)
        self.move(paddle, joy_start)
        return pos

