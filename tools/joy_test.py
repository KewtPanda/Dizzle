#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, sys, time, os
from pygame.locals import *

pygame.init()  # init pygame
pygame.joystick.init()  # Initialize the joysticks

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.JOYBUTTONDOWN:
            # print("Joystick button pressed.")
            pass

        if event.type == pygame.JOYBUTTONUP:
            # print("Joystick button released.")
            pass
    os.system('clear')
    joystick_count = pygame.joystick.get_count()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()
    button = []
    for i in range(buttons):
        button.append(joystick.get_button(i))
    print(button)
    time.sleep(1 / 30)
pygame.quit()

