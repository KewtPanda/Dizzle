"""
Constants Module

This module defines game constants in a central location
so that they can be easily accessed in other modules and
easily modified if need be.
"""

import configparser

# General
GAME_NAME = 'Dizzle'
FPS = 60
RESOLUTION = (1280, 720)
DT = 1./FPS
BG_COLOR = 'black'

# read volume from config file
config = configparser.ConfigParser()
config.read("data/assets/config.ini")
MUSIC_VOLUME = config.getfloat("volume", "music_volume")
EFFECT_VOLUME = config.getfloat("volume", "effect_volume")

# Block
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 12
MODS = ['life', 'death', 'big', 'small', 'multiply', 'snap', 'expand', 'retract', 'explosion', 'laser']
MOD_CHANCE = 10  # % chance to get mod after block is hit

""" Controls for the game """
# Keyboard keys used and for what
KB_KEYS = {
    8: 'erase',  # backspace
    13: 'accept',  # return
    19: 'pause',  # pause/break
    27: 'back',  # escape
    98: 'next_song',  # b
    99: 'close',  # c
    101: 'explosion_ball',  # e
    108: 'laser_ball',  # l
    109: 'mute',  # m
    110: 'normal_ball',  # n
    112: 'plasma_ball',  # p
    113: 'close',  # q
    115: 'snap_ball',  # s
    118: 'prev_song',  # v
    120: 'next_level',  # x
    122: 'prev_level',  # z
    273: 'up',  # up_arrow
    274: 'down',  # down_arrow
    275: 'right',  # right_arrow
    276: 'left'  # left_arrow
}
# Joystick keys used and for what
JS_KEYS = {
    0: 'erase',
    1: 'prev_song',
    2: 'next_song',
    3: 'back',
    4: 'accept',
    5: 'misc',
    6: 'mute',
    7: 'pause'
}
# Values for controls in-game
CONTROLS = {
    'close': False,
    'accept': False,
    'back': False,
    'erase': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'misc': False,
    'pause': False,
    'mouse': (0, 0),
    'pad_0_x': 0,
    'pad_0_y': 0,
    'pad_1_x': 0,
    'pad_1_y': 0,
    'next_level': False,
    'prev_level': False,
    'next_song': False,
    'prev_song': False,
    'mute': False,
    'snap_ball': False,
    'normal_ball': False,
    'explosion_ball': False,
    'laser_ball': False,
    'plasma_ball': False,
    'increase_ball_size': False,
    'decrease_ball_size': False,
    'expand_paddle': False,
    'retract_paddle': False
}
# Standard values for controls in-game (Used to reset values)
STD_CONTROLS = {
    'close': False,
    'accept': False,
    'back': False,
    'erase': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'misc': False,
    'pause': False,
    'mouse': (0, 0),
    'pad_0_x': 0,
    'pad_0_y': 0,
    'pad_1_x': 0,
    'pad_1_y': 0,
    'next_level': False,
    'prev_level': False,
    'next_song': False,
    'prev_song': False,
    'mute': False,
    'snap_ball': False,
    'normal_ball': False,
    'explosion_ball': False,
    'laser_ball': False,
    'plasma_ball': False,
    'increase_ball_size': False,
    'decrease_ball_size': False,
    'expand_paddle': False,
    'retract_paddle': False
}

# Images
IMAGE_PATH = 'data/assets/images/'
BRICK_IMAGES = {
    'red': 'brick_red.gif',
    'orange': 'brick_orange.gif',
    'yellow': 'brick_yellow.gif',
    'green': 'brick_green.gif',
    'blue': 'brick_blue.gif',
    'purple': 'brick_purple.gif',
    'tan': 'brick_tan.gif',
    'white': 'brick_white.gif',
    'grey': 'brick_gray.gif',
    'black': 'brick_black.gif',
    'none': 'brick_cell.gif'
}
MOD_IMAGES = {
    'life': 'mod_life.png',
    'death': 'mod_death.png',
    'big': 'mod_big.png',
    'small': 'mod_small.png',
    'multiply': 'mod_multiply.png',
    'snap': 'mod_snap.png',
    'expand': 'mod_expand.png',
    'retract': 'mod_retract.png',
    'explosion': 'mod_explosion.png',
    'laser': 'mod_laser.png'
}
BALL_IMAGES = {
    'white': 'ball-white.png',
    'red': 'ball-red.png',
    'blue': 'ball-blue.png',
    'purple': 'ball-purple.png'
}

# Sounds
MUSIC_PATH = 'data/assets/music/'
SOUND_PATH = 'data/assets/sounds/'
BALL_SOUNDS = {
    'normal': 'blip.ogg',
    'explosion': 'explosion.ogg',
    'laser': 'laser.ogg',
    'plasma': 'laser.ogg',
    'bounce': 'boing.ogg'
}
GAME_SOUNDS = {
    'victory': 'victory.ogg',
    'lose': 'lose.ogg',
    'final': 'final.ogg'
}

# Levels
LEVEL_PATH = 'data/assets/levels/'
START_LEVEL = 'level_0.json'

# Highscore
HIGHSCORE_FILE = 'data/assets/highscore/highscore.txt'
